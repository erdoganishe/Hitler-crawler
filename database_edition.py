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

                    if len(path[link]) == 4:
                        return None

                    Q.append(link)

    return None


def result(start, end, path):
    if path:
        result = path
    else:
        result = "No path! :( "
    d = {"start": start, "end": end, "path": result}
    return d


def write_to_db(element, file_path):
    with open(file_path, 'r', newline='') as file:
        reader = csv.reader(file)

        if not any(element in row for row in reader):
            with open(file_path, 'a', newline='') as file:
                writer = csv.writer(file)

                writer.writerow([element])


def main():
    start = "https://en.wikipedia.org/wiki/Special:Random"
    end = "https://en.wikipedia.org/wiki/Adolf_Hitler"

    while True:
        print("started")
        path = find_shortest_path(start, end)
        print(path)
        if path:
            write_to_db(path[-2], 'db.csv')


main()
