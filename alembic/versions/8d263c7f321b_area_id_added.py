"""area id added

Revision ID: 8d263c7f321b
Revises: e4840a83f517
Create Date: 2024-09-10 23:03:05.232401

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8d263c7f321b'
down_revision: Union[str, None] = 'e4840a83f517'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('meetups', sa.Column('area_id', sa.UUID(), nullable=False))
    op.create_foreign_key(None, 'meetups', 'areas', ['area_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'meetups', type_='foreignkey')
    op.drop_column('meetups', 'area_id')
    # ### end Alembic commands ###
