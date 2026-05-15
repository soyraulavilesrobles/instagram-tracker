import requests
import csv
import os
import time
from datetime import datetime
from urllib.parse import unquote

SESSION_ID = unquote(os.environ.get('INSTAGRAM_SESSION_ID', ''))
USERNAMES_FILE = 'usernames.txt'
DATA_FILE = 'data.csv'

# ds_user_id es el numero al inicio del session id
DS_USER_ID = SESSION_ID.split(':')[0] if ':' in SESSION_ID else ''


def get_followers(username):
    url = 'https://www.instagram.com/api/v1/users/web_profile_info/?username=' + username
    cookie = 'sessionid=' + SESSION_ID
    if DS_USER_ID:
        cookie += '; ds_user_id=' + DS_USER_ID
    headers = {
        'x-ig-app-id': '936619743392459',
        'Cookie': cookie,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'Accept': '*/*',
        'Accept-Language': 'es-CL,es;q=0.9,en;q=0.8',
        'Referer': 'https://www.instagram.com/',
        'Origin': 'https://www.instagram.com',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
    }
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        print('  status:', resp.status_code)
        if resp.status_code != 200:
            return 'ERROR_' + str(resp.status_code)
        data = resp.json()
        return data['data']['user']['edge_followed_by']['count']
    except Exception as e:
        print('  excepcion:', e)
        return 'ERROR'


def main():
    print('Session ID (decoded):', SESSION_ID[:20] + '...')
    print('DS User ID:', DS_USER_ID)

    with open(USERNAMES_FILE, 'r') as f:
        usernames = [line.strip() for line in f if line.strip()]

    today = datetime.utcnow().strftime('%Y-%m-%d')

    file_exists = os.path.isfile(DATA_FILE)
    if not file_exists:
        with open(DATA_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['fecha'] + usernames)

    row = [today]
    for username in usernames:
        print('@' + username)
        count = get_followers(username)
        print('  resultado:', count)
        row.append(count)
        time.sleep(3)

    with open(DATA_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(row)

    print('Listo. Fila guardada:', row)


if __name__ == '__main__':
    main()
