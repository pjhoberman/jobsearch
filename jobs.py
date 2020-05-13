import multiprocessing as mp
import json
import requests
from bs4 import BeautifulSoup

jobs_json = None
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) ' \
             'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
headers = {'User-Agent': user_agent, "Content-Type": "text/html"}


def get_site_text(url):
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("{}: {}".format(response.status_code, url))
        return response.status_code

    soup = BeautifulSoup(response.text, 'html.parser')
    return list(soup.stripped_strings)


def create_readable_diff(a, b):
    diffs = [{"-": p[0], "+": p[1]} for p in zip(a, b) if p[0] != p[1]]
    if len(a) > len(b):
        diffs += [{"-": x, "+": ""} for x in a[len(b) - len(a):]]
    elif len(b) > len(a):
        diffs += [{"-": x, "+": ""} for x in b[len(a) - len(b):]]
    return diffs


def check_site(url):
    global jobs_json

    text = get_site_text(url)
    diff = {"url": url, "diff": None}
    if jobs_json.get(url) and jobs_json.get(url) != text:
        diff['diff'] = create_readable_diff(jobs_json.get(url), text)
    jobs_json[url] = text

    return diff


def check_sites():
    global jobs_json
    with open("urls.txt", "r") as file, open("jobs.json", "r") as j:
        urls = [line.strip() for line in file]
        jobs_json = json.loads(j.read())

    # Removed for now - need to figure out global vars with multiprocessing, or some other solution
    # pool = mp.Pool(mp.cpu_count())
    # changed = pool.map(check_site, urls)
    # pool.close()
    changed = []
    for url in urls:
        changed.append(check_site(url))

    with open("jobs.json", "w") as file:
        file.write(json.dumps(jobs_json))

    for change in changed:
        print("### ", change['url'], " ###")
        print(change['diff'])


if __name__ == '__main__':
    check_sites()
