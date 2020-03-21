import json
import os

from bs4 import BeautifulSoup

from common.config import STATES_NOT_COMPLETED_COURSES, WEBINAR_TYPE_PREFIX, \
    VIDEO_TYPE_PREFIX, VIDEOS_TYPE, WEBINARS_TYPE, INTERACTIVE_TYPE,  \
    VIDEO_TYPE, WEBINAR_TYPE, GB_VIDEO_TYPE, GB_WEBINAR_TYPE, GB_INTERACTIVE_TYPE
from exceptions.exceptions import SoupDataError


class GetCourseInfo:
    """Parse json from main GeekBrains to database format."""

    def __init__(self, gb_lesson):
        # extract lesson data from GB tuple with id and lesson data
        self.gb_lesson = gb_lesson[1]
        self.lesson = dict()

    def get_common_info(self):
        completed_on_gb = False

        if self.gb_lesson['state'] not in STATES_NOT_COMPLETED_COURSES:
            completed_on_gb = True

        link = self.gb_lesson['link']

        if self.gb_lesson.get('courseUrl'):
            link = self.gb_lesson.get('courseUrl')

        self.lesson['course_name'] = self.gb_lesson['title']
        self.lesson['completed_on_gb'] = completed_on_gb
        self.lesson['course_link'] = link

    def get_video(self):
        self.lesson['type'] = VIDEO_TYPE
        self.lesson['link_id'] = self.gb_lesson['progressItems'][VIDEOS_TYPE]

    def get_webinar(self):
        self.lesson['type'] = WEBINAR_TYPE
        self.lesson['link_id'] = self.gb_lesson['progressItems'][WEBINARS_TYPE]

    def get_interactive(self):
        self.lesson['type'] = INTERACTIVE_TYPE
        self.lesson['link_id'] = self.gb_lesson['progressItems'][WEBINARS_TYPE]


class ParseCourseInfo(GetCourseInfo):
    """docstring for ParseCourseInfos."""
    def __init__(self, gb_lesson):
        super().__init__(gb_lesson)
        # self.get_course()

    def __getitem__(self, key):
        return self.lesson.get(key)

    def get_course(self) -> dict:
        is_webinar, is_interactive, is_video, is_link = False, False, False, True

        if self.gb_lesson.get('link') is None:
            is_link = False
        elif GB_INTERACTIVE_TYPE in self.gb_lesson['courseType']:
            is_interactive = True
        elif GB_VIDEO_TYPE in self.gb_lesson['courseType']:
            is_video = True
        elif GB_WEBINAR_TYPE in self.gb_lesson['courseType']:
            is_webinar = True

        if is_link:
            self.get_common_info()

            if is_webinar:
                self.get_webinar()
            elif is_video:
                self.get_video()
            elif is_interactive:
                self.get_interactive()

            return self.lesson


class ParseCourses():
    """Parse all bought courses information from GeekBrains."""
    def __init__(self, soup: BeautifulSoup) -> list:
        self.soup = soup
        # self.get_courses()

    def get_courses(self) -> list:
        all_lessons = list()
        parse_courses = self.parse_courses()

        for lesson in parse_courses.items():
            course_info = ParseCourseInfo(lesson).get_course()

            if course_info:
                all_lessons.append(course_info)

        return all_lessons

    def parse_courses(self) -> dict:
        """Parse json with info from main page with bought courses"""
        courses = self.soup.find('script', {"data-component-name": "EducationPage"})

        if courses is None:
            raise SoupDataError()

        courses = courses.text
        loads = json.loads(courses)

        return loads['data']['attendees']
