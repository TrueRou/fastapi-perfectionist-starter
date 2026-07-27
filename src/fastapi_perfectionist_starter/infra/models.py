import re
import uuid
from datetime import UTC, datetime

from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict
from sqlalchemy import ForeignKey, MetaData
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column, relationship

NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class BaseModel(PydanticBaseModel):
    model_config = ConfigDict(use_enum_values=True, from_attributes=True)


class DbBase(DeclarativeBase):
    metadata = MetaData(naming_convention=NAMING_CONVENTION)


class BaseDbModel(DbBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        table_name = re.sub(r"(?<!^)(?=[A-Z])", "_", cls.__name__).lower()
        return f"tbl_{table_name}"


class PkWithTimestampDbModel(BaseDbModel):
    __abstract__ = True

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(UTC))
    updated_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(UTC))


class User(PkWithTimestampDbModel):
    username: Mapped[str] = mapped_column(index=True, unique=True)
    email: Mapped[str] = mapped_column(index=True, unique=True)
    hashed_password: Mapped[str]

    rel_notes: Mapped[list[Note]] = relationship(back_populates="rel_user", lazy="raise")


class Note(PkWithTimestampDbModel):
    title: Mapped[str]
    content: Mapped[str]
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tbl_user.id"), index=True)

    rel_user: Mapped[User] = relationship(back_populates="rel_notes", lazy="raise")
