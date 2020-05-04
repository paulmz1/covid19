class Countries:

    def __init__(self):
        self.all_days = None
        self.last_date = None
        self.last_day = None
        self.default_countries = None
        self.loaded = False

    def load(self, all_days, last_date, last_day, default_countries):
        self.all_days = all_days
        self.last_date = last_date
        self.last_day = last_day
        self.default_countries = default_countries
        self.loaded = True
