import time
import requests
from bs4 import BeautifulSoup
from collections import deque
from concurrent.futures import ThreadPoolExecutor
import csv

def get_links(page):
    r = requests.get(page)
    soup = BeautifulSoup(r.content, 'html.parser')
    base_url = page[:page.find('/wiki/')]
    links = list({base_url + a['href'] for a in soup.select('p a[href]') if a['href'].startswith('/wiki/')})
    return links

def import_db(filename = 'db.csv'):
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        rows = []
        for row in reader:
            rows.append(str(row[0]))

        return rows

def find_shortest_path_with_db(start, end):

    db = import_db()
    path = {}
    path[start] = [start]
    Q = deque([start])

    with ThreadPoolExecutor(max_workers=32) as executor:
        while len(Q) != 0:
            page = Q.popleft()
            links = list(executor.map(get_links, [page]))[0]

            for link in links:
                if link in end:

                    return path[page] + [link]

                if link in db:
                    for check_link in links:
                        if check_link in end:
                            return path[page] + [check_link]

                    return path[page] + [link] + [end]

                if (link not in path) and (link != page):
                    path[link] = path[page] + [link]
                    Q.append(link)

    return None


def find_shortest_path(start, end):
    path = {}
    path[start] = [start]
    Q = deque([start])

    with ThreadPoolExecutor(max_workers=32) as executor:
        while len(Q) != 0:
            page = Q.popleft()
            links = list(executor.map(get_links, [page]))[0]

            for link in links:
                if link in end:
                    return path[page] + [link]

                if (link not in path) and (link != page):
                    path[link] = path[page] + [link]
                    Q.append(link)

    return None


def result(start, end, path):
    if path:
        result = path
    else:
        result = "No path! :( "
    d = {"start": start, "end": end, "path": result}
    return d

def main(use_db):
    start = "https://en.wikipedia.org/wiki/Special:Random"
    end = "https://en.wikipedia.org/wiki/Adolf_Hitler"

    if (use_db):
        path = find_shortest_path_with_db(start, end)
    else:
        path = find_shortest_path(start, end)

    print(path)

main(True)