"""fix relationships

Revision ID: 51cba5e532e1
Revises: 801512ea833b
Create Date: 2020-05-11 13:48:51.915288

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '51cba5e532e1'
down_revision = '801512ea833b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('questions', sa.Column('category_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'questions', 'categories', ['category_id'], ['id'])
    op.drop_column('questions', 'category')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('questions', sa.Column('category', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'questions', type_='foreignkey')
    op.drop_column('questions', 'category_id')
    # ### end Alembic commands ###
