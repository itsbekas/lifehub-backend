import datetime as dt

import argon2
from jose import JWTError

from lifehub.core.common.base_service import BaseService
from lifehub.core.module.models import ModuleResponse, ModuleWithProvidersResponse
from lifehub.core.module.schema import Module
from lifehub.core.provider.models import ProviderResponse, ProviderWithModulesResponse
from lifehub.core.provider.repository.provider_token import ProviderTokenRepository
from lifehub.core.provider.schema import Provider, ProviderToken
from lifehub.core.user.models import UserTokenResponse
from lifehub.core.user.repository.user import UserRepository
from lifehub.core.user.schema import User
from lifehub.core.utils.auth import (
    create_jwt_token,
    decode_jwt_token,
    hash_password,
    verify_password,
)


class UserService(BaseService):
    def __init__(self):
        super().__init__()
        self.user_repository = UserRepository(self.session)
        self.provider_token_repository = ProviderTokenRepository(self.session)
        self.password_hasher = argon2.PasswordHasher()

    def create_user(self, username: str, password: str, name: str) -> User:
        user = self.user_repository.get_by_username(username)

        if user is not None:
            # TODO: Service exception (#27)
            raise Exception("User already exists")

        hashed_password = hash_password(password)

        new_user = User(username=username, password=hashed_password, name=name)
        self.user_repository.add(new_user)
        self.user_repository.commit()
        self.user_repository.refresh(new_user)

        return new_user

    def create_access_token(self, user: User) -> UserTokenResponse:
        expires_at = dt.datetime.now() + dt.timedelta(days=30)

        return UserTokenResponse(
            name=user.name,
            access_token=create_jwt_token(user.username, expires_at),
            expires_at=expires_at,
        )

    def login_user(self, username: str, password: str) -> User:
        user: User | None = self.user_repository.get_by_username(username)

        if user is None or not verify_password(password, user.password):
            # TODO: Service exception (#27)
            raise Exception("Invalid credentials")

        return user

    def authenticate_user(self, token: str) -> User:
        try:
            payload = decode_jwt_token(token)
        except JWTError:
            # TODO: Service exception (#27)
            raise Exception("Invalid token")

        username: str = payload.get("sub")  # type: ignore

        user: User | None = self.user_repository.get_by_username(username)

        if user is None:
            # TODO: Service exception (#27)
            raise Exception("User not found")

        return user

    def delete_user(self, user: User) -> None:
        self.user_repository.delete(user)
        self.user_repository.commit()

    def get_user_providers(self, user: User) -> list[ProviderResponse]:
        return [
            ProviderResponse(id=provider.id, name=provider.name)
            for provider in user.providers
        ]

    def get_user_providers_with_modules(
        self, user: User
    ) -> list[ProviderWithModulesResponse]:
        return [
            ProviderWithModulesResponse(
                id=provider.id,
                name=provider.name,
                type=provider.config.auth_type,
                modules=[
                    ModuleResponse(id=module.id, name=module.name)
                    for module in provider.modules
                ],
            )
            for provider in user.providers
        ]

    def add_provider_to_user(self, user: User, provider: Provider) -> None:
        user.providers.append(provider)
        self.user_repository.commit()

    def remove_provider_from_user(self, user: User, provider: Provider) -> None:
        token = self.provider_token_repository.get(user, provider)
        if token is not None:
            self.provider_token_repository.delete(token)
        self.user_repository.commit()

    def add_provider_token_to_user(
        self,
        user: User,
        provider: Provider,
        token: str,
        refresh_token: str | None,
        created_at: dt.datetime | None,
        expires_at: dt.datetime | None,
    ) -> None:
        provider_token = ProviderToken(
            user_id=user.id,
            provider_id=provider.id,
            token=token,
            refresh_token=refresh_token,
            created_at=created_at,
            expires_at=expires_at,
        )
        self.provider_token_repository.add(provider_token)
        user = self.session.merge(user)
        provider = self.session.merge(provider)
        user.providers.append(provider)
        self.user_repository.add(user)
        self.session.commit()

    def update_provider_token(self, user: User, provider: Provider, token: str) -> None:
        provider_token = self.provider_token_repository.get(user, provider)
        provider_token.token = token
        self.provider_token_repository.commit()

    def get_user_modules(self, user: User) -> list[ModuleResponse]:
        return [
            ModuleResponse(id=module.id, name=module.name) for module in user.modules
        ]

    def get_user_modules_with_providers(
        self, user: User
    ) -> list[ModuleWithProvidersResponse]:
        return [
            ModuleWithProvidersResponse(
                id=module.id,
                name=module.name,
                providers=[
                    ProviderResponse(id=provider.id, name=provider.name)
                    for provider in module.providers
                ],
            )
            for module in user.modules
        ]

    def add_module_to_user(self, user: User, module: Module) -> None:
        if module in user.modules:
            raise Exception(f"User already has module {module.name}")

        missed_providers = []

        module = self.session.merge(module)
        user = self.session.merge(user)

        for provider in module.providers:
            if provider not in user.providers:
                missed_providers.append(provider.name)

        if missed_providers:
            raise Exception(f"User is missing providers: {', '.join(missed_providers)}")

        user.modules.append(module)
        self.user_repository.commit()

    def remove_module_from_user(self, user: User, module: Module) -> None:
        if module not in user.modules:
            raise Exception(f"User does not have module {module.name}")

        user.modules.remove(module)
        self.user_repository.commit()

    def __del__(self):
        self.user_repository.close()
