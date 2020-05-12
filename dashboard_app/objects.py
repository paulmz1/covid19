class Countries:

    def __init__(self):
        self.all_days = None
        self.last_day = None
        self.last_date = None
        self.default_countries = None
        self.commit_date = 'n/a'
        self.population = None
        self.loaded = False

    def load(self, all_days, last_day, last_date, default_countries, population):
        self.all_days = all_days
        self.last_day = last_day
        self.last_date = last_date
        self.default_countries = default_countries
        self.population = population
        self.loaded = True
