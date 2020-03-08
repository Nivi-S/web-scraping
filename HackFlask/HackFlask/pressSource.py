from enum import Enum


class pressSource:
    def __init__(self, id, url):
        if id == "WHO":
            self.level = "global"
        elif id == "CDC":
            self.level = "national"
        elif id == "CA":
            self.level = "state"
        elif id == "LA":
            self.level = "county"
        elif id == "UCLA" or id == "USC":
            self.level = "school"

        self.id = id
        self.url = url
        self.confirmed = 0
        self.deaths = 0
        self.date = ""
        self.headline = ""

    def set_deaths(self, count):
        self.deaths = count

    def set_confirmed(self, count):
        self.confirmed = count
