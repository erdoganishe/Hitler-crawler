import time
import requests
from bs4 import BeautifulSoup
from collections import deque
from concurrent.futures import ThreadPoolExecutor

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
                    Q.append(link)

    return None

def result(start, end, path):
    if path:
        result = path
    else:
        result = "No Hitler found"
    d = {"start": start, "end": end, "path": result}
    return d

def get_path(start, use_db = True):
    end = "https://en.wikipedia.org/wiki/Adolf_Hitler"

    start_time = time.time()

    path = find_shortest_path(start, end)
    

    end_time = time.time()
    return {
        "path": path,
        "elapsed_time": end_time - start_time
    }
