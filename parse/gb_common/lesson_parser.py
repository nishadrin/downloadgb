import abc

from bs4 import BeautifulSoup

from common.config import INTERACTIVE_TYPE, WEBINAR_TYPE, VIDEO_TYPE


class LessonDirector:
    """docstring for LessonDirector."""

    def __init__(self):
        self._lesson = None

    def get_lesson(self, lesson):
        self._lesson = lesson
        self._lesson._get_type()
        self._lesson._get_link_id()
        self._lesson._get_name()
        self._lesson._get_announcement()
        self._lesson._get_materials()
        self._lesson._get_homework()
        self._lesson._get_is_parse()


class Lesson:
    type = ''
    link_id = ''
    name = ''
    announcement = ''
    material = dict()
    homework = ''
    is_parse = False


class AbstractLesson(metaclass=abc.ABCMeta):
    """Abstract lesson."""

    def __init__(self, soup, link_id, is_parse):
        self.lesson = Lesson()
        self.soup = soup
        self.link_id = link_id
        self.is_parse = is_parse

    @abc.abstractmethod
    def _get_name(self):
        pass

    @abc.abstractmethod
    def _get_announcement(self):
        pass

    @abc.abstractmethod
    def _get_materials(self):
        pass

    @abc.abstractmethod
    def _get_homework(self):
        pass

    # Вилео может дублироваться в материалах, а может там не быть
    # можеь быть много видео в интерактиве в одном уроке
    # div id vjs_video_3
    @abc.abstractmethod
    def _get_video(self): # TODO
        pass


class BaseLesson(AbstractLesson):
    """docstring for BaseLesson."""

    def _get_link_id(self):
        """Get link id from lesson."""

        self.lesson.link_id =  self.link_id

    def _get_is_parse(self):
        """Get link id from lesson."""

        self.lesson.is_parse =  self.is_parse


    def _get_name(self):
        """Get lesson name from lesson's html soup."""

        self.lesson.name = self.soup.find("h3", {"class": "title"}).text

    def _get_announcement(self):
        """Get important announcement from lesson's html soup."""

        announcement = self.soup.find("div", {"class": "lesson-content__content"})

        if announcement:
            self.lesson.announcement = announcement.text

    def _get_materials(self):
        """Get material links and names from lesson's html soup."""

        materials = self.soup.findAll("li", {"class": "lesson-contents__list-item"})

        for material in materials:
            self.lesson.material[material.find("a")['href']] = material.find("a").text


class Video(BaseLesson):
    """Parse information from video lesson."""

    def _get_type(self):
        self.lesson.type = VIDEO_TYPE


class Webinar(BaseLesson):
    """Parse information from video lesson."""

    def __init__(self, soup, soup_hw):
        self.soup_hw = soup_hw
        super().__init__(soup)

    def _get_type(self):
        self.lesson.type = WEBINAR_TYPE

    def _get_homework(self):
        """Get homework webinar's from html soup."""

        homework = self.soup_hw.find("div", {"class": "task-block-teacher"})

        if homework:
            self.lesson.homework = homework.text


class Interactive(BaseLesson):
    """Parse information from video lesson."""

    def __init__(self, soup, soup_hw):
        self.soup_hw = soup_hw
        super().__init__(soup)

    def _get_type(self):
        self.lesson.type = INTERACTIVE_TYPE

    def _get_homework(self):
        """Get homework interactive's from html soup."""

        self.lesson.homework = self.soup_hw.find("div", {"class": "homework-description"}).text


class LessonParser():
    """."""

    def __init__(self, soup):
        self.soup = soup

        self.lesson = dict()

    def get_lesson_name(self):
        """Get lesson name from lesson's html soup."""
        self.lesson['lesson_name'] = self.soup.find("h3", {"class": "title"}).text

    def get_material(self):
        """Get material links and names from lesson's html soup."""
        href_name = dict()
        materials = self.soup.findAll("li", {"class": "lesson-contents__list-item"})

        for material in materials:
            href_name[material.find("a")['href']] = material.find("a").text

        self.lesson['materials'] = href_name

    def get_announcement(self):
        """Get important announcement from lesson's html soup."""
        announcement = self.soup.find("div", {"class": "lesson-content__content"})

        if announcement:
            self.lesson['announcement'] = announcement.text




class ParseVideo(LessonParser):
    """Parse information from video lesson."""

    def parse_video(self):
        self.get_lesson_name()
        self.get_material()
        self.get_announcement()


        return self.lesson


class ParseWebinar(LessonParser):
    """Parse information from webinar lesson."""

    def __init__(self, soup, soup_hw):
        self.soup_hw = soup_hw
        super().__init__(soup)

    def parse_webinar(self):
        self.get_lesson_name()
        self.get_material()
        self.get_announcement()
        self.parse_webinar_homework()

        return self.lesson


    def parse_webinar_homework(self) -> str:
        """Get homework webinar's from html soup."""
        homework = self.soup_hw.find("div", {"class": "task-block-teacher"})

        if homework:
            homework = homework.text

        self.lesson['homework'] =  homework


class ParseInteractive(LessonParser):
    """Parse information from interactive lesson."""

    def __init__(self, soup, soup_hw):
        self.soup_hw = soup_hw
        super().__init__(soup)

    def parse_interactive(self):
        self.get_lesson_name()
        self.get_material()
        self.parse_interactive_homework()

        return self.lesson


    def parse_interactive_homework(self) -> str:
        """Get homework interactive's from html soup."""
        self.lesson['homework'] = self.soup_hw.find("div", {"class": "homework-description"}).text
