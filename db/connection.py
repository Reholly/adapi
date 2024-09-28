from typing import Optional

from sqlalchemy.engine import Engine, create_engine
from sqlalchemy.event import listens_for
from sqlalchemy.exc import ArgumentError, OperationalError
from sqlalchemy.orm import close_all_sessions, sessionmaker

from .config import config

_session_factory: Optional['sessionmaker'] = None
_db_engine: Optional['Engine'] = None


def _make_engine(url: str, echo: bool) -> 'Engine':
    engine = create_engine(url, echo=echo)

    @listens_for(Engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record) -> None:
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    return engine


def start_db_connections(engine_factory=_make_engine) -> None:
    global _db_engine, _session_factory

    if _db_engine:
        raise RuntimeError('DB connection is already initialized')

    if not config.URL.startswith('sqlite'):
        _db_url_error()

    try:
        _db_engine = engine_factory(config.URL, echo=config.ECHO)
        _session_factory = sessionmaker(
            autocommit=False, autoflush=False, expire_on_commit=False, bind=_db_engine
        )
        _check_conn()
    except (OperationalError, ArgumentError) as exc:
        _db_url_error(exc)


def stop_db_connections() -> None:
    global _db_engine, _session_factory
    if not _db_engine:
        return

    close_all_sessions()
    _db_engine.dispose()
    _session_factory = None
    _db_engine = None


def get_engine() -> 'Engine':
    global _db_engine
    if not _db_engine:
        raise RuntimeError('DB connection was not initialized')

    return _db_engine


def get_session_factory():
    global _session_factory
    if _session_factory is None:
        raise RuntimeError('DB connection was not initialized')

    return _session_factory


def _db_url_error(exc=None):
    print(
        f'\n'
        f'DB_URL environment variable seems to be invalid: "{config.URL}" \n'
        f'Please provide a valid SQLite db path. \n'
        f'See https://docs.sqlalchemy.org/en/14/core/engines.html#sqlite for details \n'
    )
    if exc:
        print(f'Error:\n{exc!s}\n')
    exit(1)


def _check_conn():
    global _session_factory

    s = _session_factory()
    try:
        list(s.execute('SELECT 1;'))
    finally:
        s.close()
