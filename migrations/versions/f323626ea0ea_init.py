"""init

Revision ID: f323626ea0ea
Revises:
Create Date: 2026-03-14 22:46:17.733353

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'f323626ea0ea'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'users',
        sa.Column('uid', postgresql.UUID(), nullable=False, default=sa.text('gen_random_uuid()')),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('role', sa.String(), nullable=True),
        sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), nullable=True),
        sa.Column('updated_at', postgresql.TIMESTAMP(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('uid'),
        sa.UniqueConstraint('uid'),
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)

    op.create_table(
        'barbershops',
        sa.Column('uid', postgresql.UUID(), nullable=False, default=sa.text('gen_random_uuid()')),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('address', sa.String(), nullable=False),
        sa.Column('phone', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('owner_id', postgresql.UUID(), nullable=False),
        sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), nullable=True),
        sa.Column('updated_at', postgresql.TIMESTAMP(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['owner_id'], ['users.uid']),
        sa.PrimaryKeyConstraint('uid'),
        sa.UniqueConstraint('uid'),
    )

    op.create_table(
        'services',
        sa.Column('uid', postgresql.UUID(), nullable=False, default=sa.text('gen_random_uuid()')),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('category', sa.String(), nullable=False),
        sa.Column('duration_minutes', sa.Integer(), nullable=True),
        sa.Column('price', sa.Float(), nullable=True),
        sa.Column('barbershop_id', postgresql.UUID(), nullable=False),
        sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), nullable=True),
        sa.Column('updated_at', postgresql.TIMESTAMP(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['barbershop_id'], ['barbershops.uid']),
        sa.PrimaryKeyConstraint('uid'),
        sa.UniqueConstraint('uid'),
    )

    op.create_table(
        'schedules',
        sa.Column('uid', postgresql.UUID(), nullable=False, default=sa.text('gen_random_uuid()')),
        sa.Column('user_id', postgresql.UUID(), nullable=False),
        sa.Column('barbershop_id', postgresql.UUID(), nullable=False),
        sa.Column('day_of_week', sa.Integer(), nullable=False),
        sa.Column('start_time', sa.Time(), nullable=False),
        sa.Column('end_time', sa.Time(), nullable=False),
        sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), nullable=True),
        sa.Column('updated_at', postgresql.TIMESTAMP(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.uid']),
        sa.ForeignKeyConstraint(['barbershop_id'], ['barbershops.uid']),
        sa.PrimaryKeyConstraint('uid'),
        sa.UniqueConstraint('uid'),
    )

    op.create_table(
        'bookings',
        sa.Column('uid', postgresql.UUID(), nullable=False, default=sa.text('gen_random_uuid()')),
        sa.Column('user_id', postgresql.UUID(), nullable=False),
        sa.Column('service_id', postgresql.UUID(), nullable=False),
        sa.Column('schedule_id', postgresql.UUID(), nullable=False),
        sa.Column('status', sa.String(), nullable=True),
        sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), nullable=True),
        sa.Column('updated_at', postgresql.TIMESTAMP(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.uid']),
        sa.ForeignKeyConstraint(['service_id'], ['services.uid']),
        sa.ForeignKeyConstraint(['schedule_id'], ['schedules.uid']),
        sa.PrimaryKeyConstraint('uid'),
        sa.UniqueConstraint('uid'),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('bookings')
    op.drop_table('schedules')
    op.drop_table('services')
    op.drop_table('barbershops')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
