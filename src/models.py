class Athlete:
    def __init__(self, id=None):
        self.id = id

    def set_name(self, name):
        self.name = name

    def set_club(self, club):
        self.club = club

    def set_gender(self, gender):
        self.gender = gender

    def set_county(self, county):
        self.county = county

    def set_region(self, region):
        self.region = region

    def set_nation(self, nation):
        self.nation = nation

    def set_coach(self, coach):
        self.coach = coach

    def __repr__(self):
        return u"< Athlete: %s >" % self.name


class Ranking:
    # rank = IntType()
    # time = StringType() # needs to change
    # athlete = ModelType(Athlete)
    # venue = StringType()
    # date = StringType() # Again needs to change
    # event = StringType()
    # year = StringType()
    # age_group = StringType()

    def __repr__(self):
        return "< Ranking: {0} {1} {2} {3} {4}>".format(
            self.rank, self.time, self.athlete.name, self.event, self.year
        )

