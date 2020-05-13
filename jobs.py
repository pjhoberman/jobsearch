import multiprocessing as mp
import json
import requests
from bs4 import BeautifulSoup

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) ' \
             'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
HEADERS = {'User-Agent': USER_AGENT, "Content-Type": "text/html"}


class Site:
    """
    Object should be instantiated with a url like this:
    s = Site("http://www.randomword.com")
    On init, object checks the site text against the previous text stored in a json file.

    """
    def __init__(self, url):
        self.url = url
        self._new_text = None
        self._old_text = None
        self.diff = None

        if self.old_text and self.old_text != self.new_text:
            self.create_readable_diff()

    @property
    def old_text(self):
        """
        Property declaration to grab old text from json file based on self.url
        :return: list - Beautiful Soup list of strings stored in json file
        """
        if not self._old_text:
            with open("jobs.json", "r") as file:
                self._old_text = json.loads(file.read()).get(self.url, None)
        return self._old_text

    @property
    def new_text(self):
        """
        Property declaration to grab new text from self.url
        :return: list - Beautiful Soup list of strings from site
        """
        if not self._new_text:
            response = requests.get(self.url, headers=HEADERS)
            if response.status_code != 200:
                print("{}: {}".format(response.status_code, self.url))
                self._new_text = response.status_code
            else:
                soup = BeautifulSoup(response.text, 'html.parser')
                self._new_text = list(soup.stripped_strings)
        return self._new_text

    def create_readable_diff(self):
        """
        Creates a low-level diff comparison of self.old_text and self.new_text
        Note: This isn't a super clean diff. One day it will look like a git diff.
            For now, it's more of an attempt to show what lines changed.
        :return: list of dicts showing the + and - comparison
        """
        a = self.old_text
        b = self.new_text
        diffs = [{"-": p[0], "+": p[1]} for p in zip(a, b) if p[0] != p[1]]
        if len(a) > len(b):
            diffs += [{"-": x, "+": ""} for x in a[len(b) - len(a):]]
        elif len(b) > len(a):
            diffs += [{"-": x, "+": ""} for x in b[len(a) - len(b):]]
        self.diff = diffs
        return diffs


def check_sites():
    """
    Function to grab the urls from urls.txt,
    create Site objects with a multiprocessing pool,
    then store some info back into jobs.json and print the results
    :return: None. Prints results
    """
    with open("urls.txt", "r") as file:
        urls = [line.strip() for line in file]

    pool = mp.Pool(mp.cpu_count())
    sites = pool.map(Site, urls)
    pool.close()

    with open("jobs.json", "w") as file:
        file.write(json.dumps({site.url: site.new_text for site in sites}))

    for site in sites:
        print("### ", site.url, " ###")
        print(site.diff)

    print("---")
    print("{} sites loaded.\n{} sites checked.\n{} sites changed".format(
        len(urls),
        len(sites),
        len([site for site in sites if site.diff])
    ))


if __name__ == '__main__':
    check_sites()
