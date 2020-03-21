from common.config import MAIN_LINK, VIDEO_TYPE_PREFIX, WEBINAR_TYPE_PREFIX, INTERACTIVE_VIDEOS_PREFIX, WEBINAR_HOMEWORK_PREFIX, INTERACTIVE_TYPE_PREFIX, INTERACTIVE_HOMEWORK_PREFIX



class LinkHandler:
    """Collect links for database"""

    def interactive_link(self, url: str, lesson_id: str) -> str:
        """Compile interactive link."""
        return f"{MAIN_LINK}{url}{INTERACTIVE_VIDEOS_PREFIX}/{lesson_id}"

    def interactive_link_hw(self, url: str, lesson_id: str) -> str:
        """Compile homework interactive link."""
        return f"{MAIN_LINK}{url}{INTERACTIVE_HOMEWORK_PREFIX}/{lesson_id}"

    def video_or_webinar_link(self, url: str, lesson_id: str) -> str:
        """Compile video link or webinar link."""
        lesson_type = WEBINAR_TYPE_PREFIX

        if VIDEO_TYPE_PREFIX in url:
            lesson_type = VIDEO_TYPE_PREFIX

        return f"{MAIN_LINK}{lesson_type}/{lesson_id}"

    def webinar_link_hw(self, url: str, lesson_id: str) -> str:
        """Compile homework video link or homework webinar link."""
        return self.video_or_webinar_link(url, lesson_id) + WEBINAR_HOMEWORK_PREFIX

    def course_url(self, url: str) -> str:
        """Compile url with main link for parsing."""
        return f"{MAIN_LINK}{url}"
