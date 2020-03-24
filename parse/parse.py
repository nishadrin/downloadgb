import os
import json

from parse.gb_common.course_parser import ParseCourses
from parse.gb_common.lesson_parser import ParseWebinar, ParseInteractive, ParseVideo
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

    def save_lesson(self, lesson):
        link_handler = LinkHandler()
        link_id = (lesson.link, lesson.link_id)

        if lesson.type == VIDEO_TYPE:
            link = link_handler.video_or_webinar_link(*link_id)
            parse_lesson = ParseVideo(self.get_soup(link)).parse_video()

        elif lesson.type == WEBINAR_TYPE:
            link = link_handler.video_or_webinar_link(*link_id)
            link_hw = link_handler.webinar_link_hw(*link_id)
            parse_lesson = ParseWebinar(self.get_soup(link), self.get_soup(link_hw)).parse_webinar()

        elif lesson.type == INTERACTIVE_TYPE:
            link = link_handler.interactive_link(*link_id)
            link_hw = link_handler.interactive_link_hw(*link_id)
            parse_lesson = ParseInteractive(self.get_soup(link), self.get_soup(link_hw)).parse_interactive()

        data = dict()
        data['link_id'] = lesson.link_id
        data['lesson_name'] = parse_lesson['lesson_name']

        if lesson.completed_on_gb:
            data['is_parse'] = True
        if parse_lesson.get('announcement'):
            data['announcement'] = parse_lesson['announcement']
        if parse_lesson.get('homework'):
            data['homework'] = parse_lesson['homework']

        self.database.update_lesson(**data)
        self.save_materials(lesson.link_id, parse_lesson.get('materials'))

    def save_lessons(self):
        for lesson in self.database.get_lessons(is_parse=False):
            self.save_lesson(lesson)

    def save_materials(self, link_id, materials):
        if materials:
            for link_name, link in materials.items():
                self.database.add_material(link_id, link_name, link)

    def parse_materials(self):
        """Parse all information."""
        user = self.database.get_user(self.email)

        courses = ParseCourses(self.get_soup(MAIN_LINK + COURSES_LINK_PREFIX)).get_courses()
        self.save_main_info(courses)

        self.save_lessons()
