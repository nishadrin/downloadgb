from common.config import MAIN_LINK
from parse.authorization import AuthorizationGeekBrains
from database.storage import DatabaseInteraction as database


class ParseGeekBrains(AuthorizationGeekBrains):
    """Parse all materials from GeekBrains."""

    def __init__(self):
        super().__init__()

    def start_parse(self):
        """Login, parse and logout."""
        self.login_gb()
        self.parse_materials()
        self.logout_gb()

    def parse_materials(self):
        """Parse all information."""
        ParseCourses()
        ParseVideo()
        ParseWebinar()
        ParseInteractive()


class ParseCourses:
    """Parse all bought course's information from GeekBrains."""

    def __init__(self):
        pass

    def start_parse_links(self):
        pass


class ParseMaterial:
    """Parse material links and names from lesson."""

    def __init__(self):
        pass

    def parse_material(self):
        """Parse material info."""
        pass


class ParseImportantAnnouncement:
    """Parse important announcement from lesson."""

    def __init__(self):
        pass

    def parse_announcement(self):
        """Parse important announcement from lesson."""
        pass


class ParseInteractive(ParseMaterial, ParseImportantAnnouncement):
    """Parse information from interactive lesson."""

    def __init__(self):
        pass

    def start_parse_interactive(self):
        self.parse_interactive()
        self.parse_interactive_homework()

    def parse_interactive(self):
        pass

    def parse_interactive_homework(self):
        pass


class ParseWebinar(ParseMaterial, ParseImportantAnnouncement):
    """Parse information from webinar lesson."""

    def __init__(self):
        pass

    def start_parse_webinar(self):
        self.parse_webinar()

    def parse_webinar(self):
        pass


class ParseVideo(ParseMaterial, ParseImportantAnnouncement):
    """Parse information from video lesson."""

    def __init__(self):
        pass

    def start_parse_video(self):
        self.parse_video()
        self.parse_video_homework()

    def parse_video(self):
        pass

    def parse_video_homework(self):
        pass
