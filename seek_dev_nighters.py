import requests
import datetime
import time
from pytz import timezone

API_PAGE_URL = 'https://devman.org/api/challenges/solution_attempts/?page='


def get_time_period():
    sometime = input('До которого часа ночь? -->')
    end_time_st = time.strptime(sometime, "%H:%M")
    return end_time_st


def load_attempts(page_count):
    for page in range(1, page_count, 1):
        response = requests.request('GET', API_PAGE_URL + str(page))
        elem = response.json()
        for record in elem['records']:
            # FIXME подключить загрузку данных из API
            yield {
                'username': record['username'],
                'timestamp': record['timestamp'],
                'timezone': record['timezone'],
            }


def find_midnighter(attempt, night_end_time):
    if attempt['timestamp'] is not None:
        attempt_time = datetime.datetime.fromtimestamp(attempt['timestamp'],
                                                       tz=timezone(attempt['timezone']))
        attempt_time = attempt_time.time()
        night_time = datetime.time(night_end_time.tm_hour, night_end_time.tm_min)
        if datetime.time(0, 0) < attempt_time < night_time:
            midnighter = attempt['username'] + '  ' + str(attempt_time)
        else:
            midnighter = None
    else:
        midnighter = None
    return midnighter


if __name__ == '__main__':
    night_time = get_time_period()
    response = requests.request('GET', API_PAGE_URL + str(2))
    pages = response.json()['number_of_pages']
    attempts = load_attempts(pages)
    midnighters = []
    for rec in attempts:
        man = find_midnighter(rec, night_time)
        if man is not None:
            midnighters.append(man)
    for human in midnighters:
        print(human)
