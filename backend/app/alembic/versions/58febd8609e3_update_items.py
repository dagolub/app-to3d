"""update items

Revision ID: 58febd8609e3
Revises: d4867f3a4c0a
Create Date: 2021-09-10 19:56:40.603335

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '58febd8609e3'
down_revision = 'd4867f3a4c0a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('item', sa.Column('name', sa.String(), nullable=True))
    op.add_column('item', sa.Column('source', sa.String(), nullable=True))
    op.add_column('item', sa.Column('reference', sa.String(), nullable=True))
    op.add_column('item', sa.Column('description_html', sa.String(), nullable=True))
    op.add_column('item', sa.Column('original_link_to_item', sa.String(), nullable=True))
    op.add_column('item', sa.Column('tags', sa.JSON(), nullable=True))
    op.add_column('item', sa.Column('categories', sa.JSON(), nullable=True))
    op.add_column('item', sa.Column('images', sa.JSON(), nullable=True))
    op.add_column('item', sa.Column('files', sa.JSON(), nullable=True))
    op.add_column('item', sa.Column('comments', sa.JSON(), nullable=True))
    op.drop_index('ix_item_description', table_name='item')
    op.drop_index('ix_item_title', table_name='item')
    op.drop_constraint('item_owner_id_fkey', 'item', type_='foreignkey')
    op.drop_column('item', 'title')
    op.drop_column('item', 'owner_id')
    op.alter_column('user', 'email',
                    existing_type=sa.VARCHAR(),
                    nullable=False)
    op.alter_column('user', 'hashed_password',
                    existing_type=sa.VARCHAR(),
                    nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'hashed_password',
                    existing_type=sa.VARCHAR(),
                    nullable=True)
    op.alter_column('user', 'email',
                    existing_type=sa.VARCHAR(),
                    nullable=True)
    op.add_column('item', sa.Column('owner_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('item', sa.Column('title', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.create_foreign_key('item_owner_id_fkey', 'item', 'user', ['owner_id'], ['id'])
    op.create_index('ix_item_title', 'item', ['title'], unique=False)
    op.create_index('ix_item_description', 'item', ['description'], unique=False)
    op.drop_column('item', 'comments')
    op.drop_column('item', 'files')
    op.drop_column('item', 'images')
    op.drop_column('item', 'categories')
    op.drop_column('item', 'tags')
    op.drop_column('item', 'original_link_to_item')
    op.drop_column('item', 'description_html')
    op.drop_column('item', 'reference')
    op.drop_column('item', 'source')
    op.drop_column('item', 'name')