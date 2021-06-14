from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine('postgresql://ptest:supersecretpassword@localhost/test')
Base = declarative_base()

class User(Base):
    __tablename__='users'

    id = Column (Integer(), primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(50), nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.now())

    def __str__(self):
        return self.username

Session = sessionmaker(engine)
session = Session()

if __name__== '__main__':
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    user1 = User(username='User1', email='user1@test.com')
    user2 = User(username='User2', email='user2@test.com')
    user3 = User(username='User3', email='user3@test.com')

    session.add(user1)
    session.add(user2)
    session.add(user3)
    session.commit()

    #Select * FROM
    #users = session.query(User).all()

    #Select con where
    users = session.query(User.id, User.username, User.email).filter(
        User.id >=2
    ).filter(
        User.username == 'User3'
    )

    for user in users:
        print(user)

    #first si no existe returna none
    #one si no existe genera excepcion
    user = session.query(User).filter(
        User.id == 1
    ).first()

    if user:
        print(user)
    else:
        print('El usuario no existe en la base de datos!')

    #update 1
    user = session.query(User).filter(User.id==1).first()
    user.username='Nuevo username'
    user.email = 'nuevo@email.com'
    session.add(user)
    session.commit()

    #update 2
    session.query(User).filter(
        User.id == 2
    ).update(
        {
            User.username : 'nuevo valor 2',
            User.email : 'nuevo2@email.com'
        }
    )
    session.commit()


    #delete 1
    session.query(User).filter(
        User.id == 1
    ).delete()

    session.commit()