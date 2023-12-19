"""Change in product expense table

Revision ID: f7cad2eb5d88
Revises: 27084dec630b
Create Date: 2023-12-19 20:37:31.855628

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f7cad2eb5d88'
down_revision: Union[str, None] = '27084dec630b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('product_expense', 'main_unit',
               existing_type=sa.VARCHAR(),
               type_=sa.UUID(),
               existing_nullable=True, postgresql_using='main_unit::uuid')
    op.create_foreign_key(None, 'product_expense', 'reference_units', ['main_unit'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'product_expense', type_='foreignkey')
    op.alter_column('product_expense', 'main_unit',
               existing_type=sa.UUID(),
               type_=sa.VARCHAR(),
               existing_nullable=True)
    # ### end Alembic commands ###
