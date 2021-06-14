from datetime import datetime
from sqlalchemy import create_engine

from sqlalchemy import MetaData

from sqlalchemy import Table, Column, Integer, String, DateTime
from sqlalchemy import select

engine = create_engine('postgresql://ptest:supersecretpassword@localhost/test')
metadata = MetaData()
metadata.bind=engine
# users
users = Table(
    'users',
    metadata,
    Column('id', Integer(), primary_key=True),
    Column('username', String(), index=True, nullable=False),
    Column('email', String(100), nullable=False),
    Column('created_at', DateTime(), default=datetime.now),
)

if __name__ == '__main__':
    metadata.drop_all(engine)
    metadata.create_all(engine)

    with engine.connect() as connection:

        query_insert = users.insert().values(
            username='user1',
            email='user@test.com'
        )

        connection.execute(query_insert)

        #select_query= users.select() #select *
        #select_query= users.select(users.c.username=='user1') #select * where
        select_query= select([
            users.c.username,
            users.c.email
        ]).where(
            users.c.username=='user1'
        )

        result = connection.execute(select_query)

        for user in result.fetchall():
            print(user.username)