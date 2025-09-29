from uuid import uuid4

from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from flask_login import UserMixin

from .base import db


class UserAccount(db.Model, UserMixin):
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

    # pubic functions
    @classmethod
    def find_by_login_id(cls, login_id) -> "UserAccount":
        return cls.query.filter_by(login_id=login_id).first()
    
    @classmethod
    def find_by_id(cls, id) -> "UserAccount":
        return cls.query.filter_by(id=id).first()
