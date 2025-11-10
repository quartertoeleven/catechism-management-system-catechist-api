"""change user accounts table schemas

Revision ID: 301014c552ef
Revises: 6b6f5ae66867
Create Date: 2025-11-10 09:37:14.996741

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '301014c552ef'
down_revision = '6b6f5ae66867'
branch_labels = None
depends_on = None


def upgrade():
    op.execute('create schema if not exists auth;')
    op.execute('alter table public.user_accounts set schema auth;')
    with op.batch_alter_table('user_accounts', schema='auth') as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_accounts_login_id'))
        batch_op.create_index(batch_op.f('ix_auth_user_accounts_login_id'), ['login_id'], unique=True)
    op.execute("COMMIT")

def downgrade():
    with op.batch_alter_table('user_accounts', schema='auth') as batch_op:
        batch_op.drop_index(batch_op.f('ix_auth_user_accounts_login_id'))
        batch_op.create_index(batch_op.f('ix_user_accounts_login_id'), ['login_id'], unique=True)
    op.execute('alter table auth.user_accounts set schema public;')
    op.execute('drop schema if exists auth;')
    op.execute("COMMIT")
