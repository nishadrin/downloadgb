import datetime

from sqlalchemy import create_engine, Column, Table, String, DateTime, \
    ForeignKey, Integer, Text, Boolean
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from common.config import DATABASE_PATH

Base = declarative_base()


class StorageGeekBrainsDownloader:
    """Database for parsed materials and technical info."""

    def __init__(self):
        # Сreate engine for database
        self.engine = create_engine(DATABASE_PATH, echo=True, pool_recycle=7200)

        Base.metadata.create_all(self.engine)
        # Create session
        Session = sessionmaker(bind=self.engine)
        self.session = Session()


    class Users(Base):
        """Create User table for database."""
        __tablename__ = 'users'
        id = Column(Integer, primary_key=True)
        email = Column(String, unique=True)
        password = Column(String)

        def __init__(self, email, password):
            self.email = email
            self.password = password

        def __repr__(self):
            return f"<User({self.email}, {self.password})>"


    class Directories(Base):
        """Create Directory table for database."""
        __tablename__ = 'directories'
        id = Column(Integer, primary_key=True)
        email = Column('email', ForeignKey('users.id'))
        directory = Column(String)

        def __init__(self, directory):
            self.directory = directory

        def __repr__(self):
            return f"<Directory({self.email}, {self.directory})>"


    class Courses(Base):
        """Create Course table for database."""
        __tablename__ = 'courses'
        id = Column(Integer, primary_key=True)
        email = Column('email', ForeignKey('users.id'))
        course_name = Column(String)
        link = Column(String)
        datetime = Column(DateTime)
        state_on_gb = Column(String)

        def __init__(self, course_name, link, state_on_gb):
            self.course_name = course_name
            self.link = link
            self.datetime = datetime.datetime.now()
            self.state_on_gb = state_on_gb # интересует только 2 варианта: continue и begin - значит курс еще не закончился

        def __repr__(self):
            return f"<Course({self.email}, {self.course_name}, {self.link}, " \
                   f"{self.datetime})>"


    class Lessons(Base):
        """Create Lesson table for database."""
        __tablename__ = 'lessons'
        id = Column(Integer, primary_key=True)
        course_name = Column('course_name', ForeignKey('courses.id'))
        lesson_name = Column(String)
        link = Column(String)
        datetime = Column(DateTime)
        type = Column(String)
        is_download = Column(Boolean)
        announcement = Column(Text)
        homework = Column(Text)

        def __init__(self, lesson_name, link, type, announcement, homework, is_download=False):
            self.lesson_name = lesson_name
            self.link = link
            self.datetime = datetime.datetime.now()
            self.type = type
            self.is_download = is_download
            self.announcement = announcement
            self.homework = homework

        def __repr__(self):
            return f"<Lesson({self.course_name}, {self.lesson_name}, " \
                   f"{self.link}, {self.datetime}, {self.announcement}, " \
                   f"{self.homework})>"


    class Materials(Base):
        """Create Material table for database."""
        __tablename__ = 'materials'
        id = Column(Integer, primary_key=True)
        lesson_name = Column('lesson_name', ForeignKey('lessons.id'))
        link_name = Column(String)
        link = Column(String)
        datetime = Column(DateTime)

        def __init__(self, link_name, link):
            self.link_name = link_name
            self.link = link
            self.datetime = datetime.datetime.now()

        def __repr__(self):
            return f"<Lesson({self.lesson_name}, {self.link_name}, " \
                   f"{self.link}, {self.datetime})>"


class DatabaseInteraction(StorageGeekBrainsDownloader):
    """Interaction with database."""

    def __init__(self):
        super().__init__()

    def get_login_data(self) -> dict:
        """Get email and password."""
        pass

    def get_directories(self) -> list:
        """Get directories to save files for user interface."""
        pass

    def get_courses(self):
        """Get all courses."""
        pass

    def get_lessons(self):
        """Get all lessons, materials, announcements, homeworks."""
        pass
