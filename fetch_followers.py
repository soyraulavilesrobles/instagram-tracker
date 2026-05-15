import requests
import csv
import os
import time
from datetime import datetime

SESSION_ID = os.environ.get('INSTAGRAM_SESSION_ID', '')
USERNAMES_FILE = 'usernames.txt'
DATA_FILE = 'data.csv'


def get_followers(username):
    url = 'https://www.instagram.com/api/v1/users/web_profile_info/?username=' + username
    headers = {
        'x-ig-app-id': '936619743392459',
        'Cookie': 'sessionid=' + SESSION_ID,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'Accept': '*/*',
        'Referer': 'https://www.instagram.com/',
    }
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code != 200:
            return 'ERROR_' + str(resp.status_code)
        data = resp.json()
        return data['data']['user']['edge_followed_by']['count']
    except Exception as e:
        return 'ERROR'


def main():
    with open(USERNAMES_FILE, 'r') as f:
        usernames = [line.strip() for line in f if line.strip()]

    today = datetime.utcnow().strftime('%Y-%m-%d')

    # crear CSV con headers si no existe
    file_exists = os.path.isfile(DATA_FILE)
    if not file_exists:
        with open(DATA_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['fecha'] + usernames)

    row = [today]
    for username in usernames:
        count = get_followers(username)
        print(f'@{username}: {count}')
        row.append(count)
        time.sleep(2)

    with open(DATA_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(row)

    print('Listo. Fila guardada:', row)


if __name__ == '__main__':
    main()
