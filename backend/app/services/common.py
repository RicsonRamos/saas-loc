from sqlalchemy import Select, func, select
from sqlalchemy.orm import Session


def paginar(db: Session, stmt: Select, page: int, limit: int) -> tuple[list, int]:
    count_stmt = select(func.count()).select_from(stmt.subquery())
    total = db.scalar(count_stmt) or 0
    items = db.execute(stmt.offset((page - 1) * limit).limit(limit)).scalars().all()
    return list(items), total
