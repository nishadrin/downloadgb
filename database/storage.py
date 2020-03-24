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
        email = Column(String, nullable=False, unique=True)
        password = Column(String, nullable=False)

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
        directory = Column(String, unique=True)

        def __init__(self, email, directory):
            self.email = email
            self.directory = directory

        def __repr__(self):
            return f"<Directory({self.email}, {self.directory})>"


    class Courses(Base):
        """Create Course table for database."""
        __tablename__ = 'courses'
        id = Column(Integer, primary_key=True)
        email = Column('email', ForeignKey('users.id'))
        link = Column(String, unique=True)
        course_name = Column(String, nullable=False)
        type = Column(String, nullable=False)
        datetime = Column(DateTime, nullable=False)
        completed_on_gb = Column(Boolean)

        def __init__(self, email, link, course_name, type, completed_on_gb):
            self.email = email
            self.link = link
            self.course_name = course_name
            self.datetime = datetime.datetime.now()
            self.type = type
            self.completed_on_gb = completed_on_gb

        def __repr__(self):
            return f"<Course({self.email}, {self.course_name}, {self.link}, " \
                   f"{self.type}, {self.datetime}, {self.completed_on_gb})>"


    class Lessons(Base):
        """Create Lesson table for database."""
        __tablename__ = 'lessons'
        id = Column(Integer, primary_key=True)
        course = Column('course_name', ForeignKey('courses.id'))
        lesson_name = Column(String)
        link_id = Column(Integer, nullable=False, unique=True)
        datetime = Column(DateTime, nullable=False)
        is_parse = Column(Boolean, nullable=False)
        is_download = Column(Boolean, nullable=False)
        download_datetime = Column(DateTime)
        announcement = Column(Text)
        homework = Column(Text)

        def __init__(self, course, link_id, lesson_name, announcement, homework, is_download=False, is_parse=False):
            self.course = course
            self.lesson_name = lesson_name
            self.link_id = link_id
            self.datetime = datetime.datetime.now()
            self.is_download = is_download
            self.announcement = announcement
            self.homework = homework
            self.is_parse = is_parse

            if is_download:
                download_datetime = self.datetime

        def __repr__(self):
            return f"<Lesson({self.course}, {self.lesson_name}, " \
                   f"{self.link_id}, {self.datetime}, {self.announcement}, " \
                   f"{self.is_parse}, {self.is_download}, " \
                   f"{self.download_datetime}, {self.announcement}, " \
                   f"{self.homework})>"


    class Materials(Base):
        """Create Material table for database."""
        __tablename__ = 'materials'
        id = Column(Integer, primary_key=True)
        lesson = Column('lesson', ForeignKey('lessons.id'))
        link_name = Column(String)
        link = Column(String, nullable=False, unique=True)
        datetime = Column(DateTime, nullable=False)

        def __init__(self, lesson, link_name, link):
            self.lesson = lesson
            self.link_name = link_name
            self.link = link
            self.datetime = datetime.datetime.now()

        def __repr__(self):
            return f"<Lesson({self.lesson}, {self.link_name}, " \
                   f"{self.link}, {self.datetime})>"


class DatabaseInteraction(StorageGeekBrainsDownloader):
    """Main interactions with database."""

    def add_user(self, email, password):
        """Add user to database."""
        user = self.session.query(self.Users).filter_by(email=email)

        if not user.count():
            user = self.Users(email, password)
            self.session.add(user)
            self.session.commit()

    def add_course(self, email, link, course_name, type, completed_on_gb=False):
        """Add course to database."""
        course = self.session.query(self.Courses).filter_by(link=link)

        if not course.count():
            user = self.session.query(self.Users).filter_by(email=email).first()
            course = self.Courses(user.id, link, course_name, type, completed_on_gb)

            self.session.add(course)
            self.session.commit()

    def add_lesson(self, course_link, link_id, lesson_name=None, announcement=None, homework=None, is_download=False, is_parse=False):
        """Add lesson to database."""
        lesson = self.session.query(self.Lessons).filter_by(link_id=link_id)

        if not lesson.count():
            course = self.session.query(self.Courses).filter_by(link=course_link).first()
            lesson = self.Lessons(course.id, link_id, lesson_name, announcement, homework, is_download, is_parse)

            self.session.add(lesson)
            self.session.commit()

    def add_material(self, link_id, link_name, link):
        """Add material to database."""
        material = self.session.query(self.Materials).filter_by(link=link)

        if not material.count():
            lesson = self.session.query(self.Lessons).filter_by(link_id=link_id).first()
            material = self.Materials(lesson.id, link_name, link)

            self.session.add(material)
        else:
            material = material.first()
            material.link_name = link_name
            material.link = link

        self.session.commit()

    def update_lesson(self, link_id, lesson_name=None, announcement=None, homework=None, is_download=False, is_parse=False):
        lesson = self.session.query(self.Lessons).filter_by(link_id=link_id).first()
        
        if lesson_name:
            lesson.lesson_name = lesson_name
        if announcement:
            lesson.announcement = announcement
        # "<p>Здравствуйте, дорогие ученики! Мы начинаем обучение на первом курсе по языку Python. Расписание занятий вы видите на этой странице - пожалуйста, не опаздывайте на уроки. Если все-таки опоздали - после урока будут доступны видеозаписи.</p><br><p>fdsfefefsdf</p>"
        if homework:
            lesson.homework = homework
        if is_download:
            lesson.is_download = is_download
        if is_parse:
            lesson.is_parse = is_parse

        self.session.commit()

    def get_user(self, email: str):
        """Get user info: email and password."""
        return self.session.query(self.Users).filter_by(email=email).first()

    def get_lessons(self, is_parse=None):
        variables = [
            self.Courses.link, self.Courses.completed_on_gb, self.Courses.type,
            self.Lessons.lesson_name, self.Lessons.link_id,
            self.Lessons.datetime, self.Lessons.is_download,
            self.Lessons.announcement, self.Lessons.homework,
            self.Lessons.is_parse]

        if is_parse is None:
            return self.session.query(*variables).join(self.Lessons).all()

        return self.session.query(*variables).join(self.Lessons).filter_by(is_parse=is_parse).all()

    # def get_directories(self, user):
    #     """Get directories to save files for user interface."""
    #     return self.session.query(self.Directories).filter_by(user=user).all()
