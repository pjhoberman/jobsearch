import multiprocessing as mp
import difflib
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def get_site_text(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    driver = webdriver.Chrome("./chromedriver",
                              options=chrome_options)
    driver.implicitly_wait(5)
    driver.get(url)
    text = driver.find_element_by_tag_name("body").text
    driver.close()
    return text


def create_readable_diff(a, b):
    change = ""
    diff = list(difflib.ndiff(a, b))
    x, y = [l[-1] for l in diff], ["{}{}".format(l[0], l[-1] if l[-1] == "\n" else "") for l in diff]
    xx = "".join(x)
    yy = "".join(y)
    for line1, line2 in zip(xx.split("\n"), yy.split("\n")):
        # Only show lines that are changed. line2 will be a bunch of spaces if no change
        if line2.strip() != "":
            change += line1 + "\n"
            change += line2 + "\n"
    return change


def check_site(url):
    with open("jobs.json", "r") as file:
        j = json.loads(file.read())

    text = get_site_text(url)
    x = {"url": url, "diff": None}
    if j.get(url) and j.get(url) != text:
        x['diff'] = create_readable_diff(j.get(url), text)
    j[url] = text

    with open("jobs.json", "w") as file:
        file.write(json.dumps(j))

    return x


def check_sites():
    with open("urls.txt", "r") as file:
        urls = [line.strip() for line in file]
    pool = mp.Pool(mp.cpu_count())
    changed = pool.map(check_site, urls)
    pool.close()

    for change in changed:
        print("### ", change['url'], " ###")
        print(change['diff'])
    else:
        print("No changes")


if __name__ == '__main__':
    check_sites()
