import os
import json

from parse.gb_common.course_parser import ParseCourses
from parse.gb_common.lesson_parser import ParseLesson
from database.storage import DatabaseInteraction
from parse.parser.parser import Parser
from common.config import MAIN_LINK, COURSES_LINK_PREFIX, VIDEO_TYPE, WEBINAR_TYPE, INTERACTIVE_TYPE
from parse.gb_common.link_handler import LinkHandler


class ParseGeekBrains(Parser):
    """Parse all materials from GeekBrains."""

    def __init__(self, email, password):
        super(Parser, self).__init__(email, password)
        self.database = DatabaseInteraction()

    def start_parse(self):
        """Login, parse and logout."""
        self.login_gb()
        self.parse_materials()
        self.logout_gb()

    def save_main_info(self, courses):
        for course in courses:
            self.database.add_course(self.email, course['course_link'], course['course_name'], course['type'], course['completed_on_gb'])

            for link_id in course['link_id']:
                self.database.add_lesson(course['course_link'], link_id)

    def save_lessons(self):
        link_handler = LinkHandler()

        for lesson in self.database.get_lessons(is_parse=False):
            link_id = (lesson.link, lesson.link_id)

            if lesson.type == VIDEO_TYPE:
                link = link_handler.video_or_webinar_link(*link_id)

                parse_lesson = ParseLesson(self.get_soup(link), is_video=True).start_parse()

            elif lesson.type == WEBINAR_TYPE:
                link = link_handler.video_or_webinar_link(*link_id)
                link_hw = link_handler.webinar_link_hw(*link_id)

                parse_lesson = ParseLesson(self.get_soup(link), self.get_soup(link_hw), is_webinar=True).start_parse()

            elif lesson.type == INTERACTIVE_TYPE:
                link = link_handler.interactive_link(*link_id)
                link_hw = link_handler.interactive_link_hw(*link_id)

                parse_lesson = ParseLesson(self.get_soup(link), self.get_soup(link_hw), is_interactive=True).start_parse()

            data = dict()

            data['course'] = parse_lesson['course_name']
            data['link_id'] = parse_lesson['link_id']
            data['lesson_name'] = parse_lesson['lesson_name']

            if parse_lesson.get(announcement):
                data['announcement'] = parse_lesson['announcement']

            if parse_lesson.get(homework):
                data['homework'] = parse_lesson['homework']

            if lesson.course.completed_on_gb:
                data['is_parse'] = True

            self.database.update_lesson(**data)

    def save_materials(self):
        pass

    def parse_materials(self):
        """Parse all information."""
        user = self.database.get_user(self.email)

        courses = ParseCourses(self.get_soup(MAIN_LINK + COURSES_LINK_PREFIX)).get_courses()

        self.save_main_info(courses)
        # self.save_lessons()

        # file2 = os.getcwd() + '/tests2.json'
        # with open(file2, 'w') as f:
        #     lessons = json.dumps(lesson_list)
        #     f.write(lessons)

        # file2 = os.getcwd() + '/tests2.json'
        # with open(file2, 'r') as f:
        #     lessons = f.read()
        #     lessons = json.loads(lessons)



        # self.database.add_material(link_name, link)

        # is_parse что бы делать ее True когда парсинг прошел этого урока

        # 0 понять с какими данными работать
        # 1 произвести работу над ссылками
        # 2 добавить в базу если таких нет
        # 3 достать данные с фильтром по нескаченным
        # 4 отправить на парсинг
        # 5 собрать материал
        # сохранить по местам в бд

        # lesson_name
        # link
        # is_download
        # announcement
        # homework
        #
        # %Materials
        # link_name
        # link
