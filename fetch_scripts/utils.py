import datetime as dt

from sqlmodel import Session, select

from lifehub.lib.models.utils.fetch_update import FetchUpdate


def get_and_update_fetch_timestamp(db_session: Session, table_id: str) -> dt.datetime:
    """
    Get the last time the fetch was updated and update it to the current time
    """
    # Get the last time the fetch was updated
    query = select(FetchUpdate).where(FetchUpdate.id == table_id)
    res = db_session.exec(query).first()
    # TODO: Setup a default value on table creation to avoid this check
    if res is None:
        last_update = dt.datetime.min
        res = FetchUpdate(id=table_id, last_update=last_update)
    else:
        last_update = res.last_update

    # Update last_update to the current time
    # This won't be saved to the database until the session is committed
    res.last_update = dt.datetime.now()
    db_session.add(res)

    # Returns the last time the fetch was updated
    return last_update
