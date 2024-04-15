from lifehub.clients.db.db_service import DatabaseService


db_service = DatabaseService()

def get_session():
    session = db_service.get_session()
    try:
        yield session
    finally:
        session.close()
