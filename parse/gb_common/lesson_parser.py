import json

from bs4 import BeautifulSoup


class LessonParser():
    """."""

    def __init__(self, soup):
        self.soup = soup

        self.lesson = dict()

    def get_lesson_name(self):
        """Get lesson name from lesson's html soup."""
        self.lesson['lesson_name'] = self.soup.find("h3", {"class": "title"}).text

    def get_material(self):
        # добавить отдельно сохранения видео
        # div id vjs_video_3
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
