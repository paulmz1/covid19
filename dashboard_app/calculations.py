import pandas as pd




class Calc:
    def __init__(self, data: {}):
        self.data = data

    def filter_countries(country_ids: str) -> pd.DataFrame:
        ids = to_list(country_ids)
        return


def to_list(string):
    if string in ['','[]']:
        return []
    return [int(x) for x in string[1:-1].split(',')]

if __name__ == '__main__':
    pass

