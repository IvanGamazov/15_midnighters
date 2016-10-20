import requests
import datetime
import time
import argparse
from pytz import timezone

parser = argparse.ArgumentParser()
parser.add_argument("time", nargs='?', help="Время в формате 'hh:mm'")
args = parser.parse_args()

API_PAGE_URL = 'https://devman.org/api/challenges/solution_attempts/?'


def get_time():
    correct_input = False
    while not correct_input:
        sometime = input('До которого часа ночь? -->')
        try:
            end_time_st = time.strptime(sometime, "%H:%M")
            correct_input = True
        except ValueError:
            print('Неверный ввод. Время необходимо вводить в формате "hh:mm".')
    night_time = datetime.time(end_time_st.tm_hour, end_time_st.tm_min)
    return night_time


def load_attempts(page_count):
    for page in range(1, page_count, 1):
        payload = {'page': page}
        response = requests.get(API_PAGE_URL, params=payload)
        elem = response.json()
        for record in elem['records']:
            yield {
                'username': record['username'],
                'timestamp': record['timestamp'],
                'timezone': record['timezone'],
            }


def make_time_from_timestamp(attempt):
    default_time = datetime.time(0, 0)
    if attempt['timestamp'] is not None:
        attempt_time = datetime.datetime.fromtimestamp(attempt['timestamp'],
                                                       tz=timezone(attempt['timezone']))
        attempt_time = attempt_time.time()
        return attempt_time
    else:
        return default_time


def find_midnighters(attempts, night_end_time):
    needed_people = list(filter(lambda attempt: datetime.time(0, 0) <
                                                make_time_from_timestamp(attempt)
                                                < night_end_time, attempts))
    return needed_people


if __name__ == '__main__':
    # print(args)
    if not args.time:
        night_time = get_time()
    else:
        try:
            given_arg = time.strptime(args.time, "%H:%M")
            night_time = datetime.time(given_arg.tm_hour, given_arg.tm_min)
        except ValueError:
            print('Неверный формат параметра, необходимо "hh:mm".')
            night_time = get_time()
    payload = {'page': 2}
    response = requests.get(API_PAGE_URL, params=payload)
    pages = response.json()['number_of_pages']
    attempts = load_attempts(pages)
    midnighters = find_midnighters(attempts, night_time)
    for human in midnighters:
        print(human['username'], make_time_from_timestamp(human), human['timezone'])
