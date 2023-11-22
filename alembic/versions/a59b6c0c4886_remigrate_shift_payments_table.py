"""Remigrate shift_payments table

Revision ID: a59b6c0c4886
Revises: 66d30f4ab6a6
Create Date: 2023-11-13 21:21:25.289515

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a59b6c0c4886'
down_revision: Union[str, None] = '66d30f4ab6a6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('shift_payments',
    sa.Column('id', sa.BIGINT(), autoincrement=True, nullable=False),
    sa.Column('order_id', sa.UUID(), nullable=True),
    sa.Column('order_num', sa.BIGINT(), nullable=True),
    sa.Column('payment_id', sa.UUID(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('nomenclature_id', sa.UUID(), nullable=True),
    sa.Column('nomenclature_name', sa.String(), nullable=True),
    sa.Column('shift_id', sa.UUID(), nullable=True),
    sa.Column('shift_num', sa.Integer(), nullable=True),
    sa.Column('cashier_id', sa.UUID(), nullable=True),
    sa.Column('soldwithdish_id', sa.UUID(), nullable=True),
    sa.Column('soldwithitem_id', sa.UUID(), nullable=True),
    sa.Column('department_id', sa.UUID(), nullable=True),
    sa.Column('ordertype_id', sa.UUID(), nullable=True),
    sa.Column('ordertype', sa.String(), nullable=True),
    sa.Column('paymenttype_id', sa.UUID(), nullable=True),
    sa.Column('paymenttype', sa.String(), nullable=True),
    sa.Column('paymenttype_group', sa.String(), nullable=True),
    sa.Column('measure_unit', sa.String(), nullable=True),
    sa.Column('nomenclature_amount', sa.DECIMAL(), nullable=True),
    sa.Column('sum', sa.DECIMAL(), nullable=True),
    sa.Column('is_delivery', sa.String(), nullable=True),
    sa.Column('guest_num', sa.Integer(), nullable=True),
    sa.Column('guestcard_num', sa.String(), nullable=True),
    sa.Column('guestcard_owner', sa.String(), nullable=True),
    sa.Column('paymentcard_num', sa.String(), nullable=True),
    sa.Column('bonuscard_num', sa.String(), nullable=True),
    sa.Column('last_update', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['cashier_id'], ['employees.id'], ),
    sa.ForeignKeyConstraint(['department_id'], ['departments.id'], ),
    sa.ForeignKeyConstraint(['nomenclature_id'], ['nomenclatures.id'], ),
    sa.ForeignKeyConstraint(['shift_id'], ['shift_list.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('shift_payments')
    # ### end Alembic commands ###
