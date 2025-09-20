from uuid import uuid4

from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from .base import db


class UserAccount(db.Model):
    __tablename__ = "user_accounts"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        server_default=db.func.gen_random_uuid(),
    )
    login_id = Column(String(100), nullable=False, unique=True, index=True)
    password = Column(Text, nullable=False)
    catechist_id = Column(
        UUID(as_uuid=True), ForeignKey("catechists.id", ondelete="set null", onupdate="cascade"), nullable=True
    )
