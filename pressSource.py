from enum import Enum


class level(Enum):
    WORLD = 'world'
    NATIONAL = 'national'
    STATE = 'state'
    COUNTY = 'county'
    SCHOOL = 'school'


class pressSource:
    def __init__(self, level, url):
        self.level = level
        self.url = url
        self.confirmed = 0
        self.deaths = 0

    def increase_death(self):
        self.deaths += 1

    def increase_confirmed(self):
        self.confirmed += 1
