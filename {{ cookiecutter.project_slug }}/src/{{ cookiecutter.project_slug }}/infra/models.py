import re
import uuid
from datetime import datetime, timezone
from typing import Any, Literal

from pydantic import ConfigDict
from sqlalchemy.orm import declared_attr
from sqlmodel import Field, Relationship, SQLModel


def Rel(back_populates: str | None = None, eager: Literal["raise", "joined", "selectin"] = "raise") -> Any:
    return Relationship(back_populates=back_populates, sa_relationship_kwargs={"lazy": eager})


class BaseModel(SQLModel):
    model_config = ConfigDict(use_enum_values=True, from_attributes=True)  # type: ignore


class BaseDbModel(BaseModel):
    @declared_attr  # type: ignore
    def __tablename__(cls) -> str:  # type: ignore
        table_name = re.sub(r"(?<!^)(?=[A-Z])", "_", cls.__name__).lower()
        return f"tbl_{table_name}"


class PkWithTimestampDbModel(BaseDbModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class User(PkWithTimestampDbModel, table=True):
    username: str = Field(index=True, unique=True)
    email: str = Field(index=True, unique=True)
    hashed_password: str

    rel_notes: list["Note"] = Rel(back_populates="rel_user", eager="raise")


class Note(PkWithTimestampDbModel, table=True):
    title: str
    content: str
    user_id: uuid.UUID = Field(foreign_key="tbl_user.id", index=True)

    rel_user: User = Rel(back_populates="rel_notes", eager="raise")
