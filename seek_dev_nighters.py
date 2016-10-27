import requests
import datetime
import time
import argparse
import pytz

parser = argparse.ArgumentParser()
parser.add_argument("time", nargs='?', help="Время в формате 'hh:mm'")
args = parser.parse_args()

API_PAGE_URL = 'https://devman.org/api/challenges/solution_attempts/'


def input_night_time():
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


def make_time_from_timestamp(timestamp, timezone):
    if timestamp is not None:
        attempt_time = datetime.datetime.fromtimestamp(timestamp,
                                                       tz=pytz.timezone(timezone))
        attempt_time = attempt_time.time()
        return attempt_time
    else:
        return datetime.time(0, 0)


def find_midnighters(attempts, night_end_time):
    midnighters = list(filter(lambda attempt:
                                datetime.time(0, 0) <
                                make_time_from_timestamp(attempt['timestamp'], attempt['timezone'])
                                < night_end_time, attempts))
    return midnighters


if __name__ == '__main__':
    if not args.time:
        night_time = input_night_time()
    else:
        try:
            given_arg = time.strptime(args.time, "%H:%M")
            night_time = datetime.time(given_arg.tm_hour, given_arg.tm_min)
        except ValueError:
            print('Неверный формат параметра, необходимо "hh:mm".')
            night_time = input_night_time()
    payload = {'page': 2}
    response = requests.get(API_PAGE_URL, params=payload)
    pages = response.json()['number_of_pages']
    attempts = load_attempts(pages)
    midnighters = find_midnighters(attempts, night_time)
    for human in midnighters:
        print(human['username'],
              make_time_from_timestamp(human['timestamp'], human['timezone']),
              human['timezone'])
