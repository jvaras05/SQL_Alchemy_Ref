from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, sessionmaker


engine = create_engine('postgresql://ptest:supersecretpassword@localhost/test')
Base = declarative_base()

class User(Base):
    __tablename__='users'

    id = Column (Integer(), primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(50), nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.now())
    courses = relationship('Course', backref='user')

    def __str__(self):
        return self.username

class Course(Base):
    __tablename__ = 'courses'
    id = Column(Integer(), primary_key=True)
    title = Column(String(50), nullable=False)
    user_id = Column(ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.now())

    def __str__(self):
        return self.title

Session = sessionmaker(engine)
session = Session()

if __name__== '__main__':
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    user1 = User(username='User1', email='user1@test.com')
    user2 = User(username='User2', email='user2@test.com')
    user3 = User(username='User3', email='user3@test.com')
    user4 = User(username='User4', email='user4@test.com')

    user1.courses.append(
        Course(title='Curso de base de datos')
    )

    user1.courses.append(
        Course(title='Curso de python')
    )

    user1.courses.append(
        Course(title='Curso de Go')
    )

    session.add(user1)
    session.add(user2)
    session.add(user3)
    session.add(user4)
    session.commit()

    
    """ otra forma
    course1 = Course(title='Curso de base de datos', user_id=user1.id)
    course2 = Course(title='Curso de python', user_id=user1.id)
    course3 = Course(title='Curso de Go', user_id=user1.id)
    session.add(course1)
    session.add(course2)
    session.add(course3)
    session.commit() 

   for course in user1.courses: #(sin el backref) Saber los cursos de un usuarios
       print(course)

    print(course1.user.created_at) #con backref se puede saber lo contrario, cuales usuarios estan en el curso
    """
    

##Joins
    ##inner join
    users = session.query(User).join(
        Course, User.id == Course.user_id #on
    )

    for user in users:
        print(user)
    
    ##left join
    users = session.query(User).outerjoin(
        Course
    ).filter(
        Course.id == None
    ).order_by(
        User.id
    )
    print('___printing left join___')
    for user in users:
        print(user)