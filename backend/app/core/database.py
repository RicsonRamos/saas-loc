from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import settings

engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
    # O Supabase (porta 6543) usa PgBouncer em modo "transaction": cada statement
    # pode ser roteado para uma conexão física diferente no Postgres, então um
    # prepared statement criado pelo psycopg3 numa conexão pode não existir mais
    # na próxima ("prepared statement ... does not exist"). Desabilita o
    # autoprepare do psycopg3 para funcionar com esse tipo de pooler.
    connect_args={"prepare_threshold": None},
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    pass


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
