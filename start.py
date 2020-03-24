from common.secrets import email, password
from parse.parse import ParseGeekBrains
from database.storage import DatabaseInteraction


# Будет "Скачать", "Пропарсить" и "Скачать урок", но не забываем
# про "Скачать и пропарсить"

def main():
    database = DatabaseInteraction()
    # email = 'email'
    # password = 'password'
    database.add_user(email, password)
    ParseGeekBrains(email, password).start_parse()


if __name__ == '__main__':
    main()

# что нужно в базе:

# self.email
# self.password

# directory

# course_name
# link
# type
# state_on_gb
#
# lesson_name
# link
# is_download
# announcement
# homework
#
# %Materials
# link_name
# link
