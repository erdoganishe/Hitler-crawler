import time
import requests
from bs4 import BeautifulSoup
from collections import deque


#use Beatiful soup library for better parse performace
def get_links(page):

    r = requests.get(page)
    soup = BeautifulSoup(r.content, 'html.parser')
    base_url = page[:page.find('/wiki/')]
    links = list({base_url + a['href'] for a in soup.select('p a[href]') if a['href'].startswith('/wiki/')})
    return links

def find_shortest_path(start, end):

    # use double-edged query against list, also getting path in process, not after
    path = {}
    path[start] = [start]
    Q = deque([start])

    while len(Q) != 0:

        page = Q.popleft()
        links = get_links(page)


        for link in links:


            if link in end:
                return path[page] + [link]


            if (link not in path) and (link != page):
                path[link] = path[page] + [link]
                Q.append(link)


    return None

# formating resulting path
def result(start, end, path):

    if path:
        result = path
    else:
        result = "Hitler not found"
    d = {"start": start, "end": end, "path": result}
    return d

# test for redirects: for Hitler wiki page is not just 'https://en.wikipedia.org/wiki/Adolf_Hitler',
# but also 'https://en.wikipedia.org/wiki/Hitler', https://en.wikipedia.org/wiki/The_F%C3%BChrer, etc

def redirected(end):

    end_soup = BeautifulSoup(requests.get(end).content, 'html.parser')
    title = end_soup.find('h1').text
    title = title.replace(' ', '_', len(title))
    base_url = end[:end.find('/wiki/') + len('/wiki/')]
    return set([end, base_url + title])


def main():
    start = "https://en.wikipedia.org/wiki/Oreo"
    end = "https://en.wikipedia.org/wiki/Adolf_Hitler"

    print("started")
    starttime = time.time()

    path = find_shortest_path(start, redirected(end))
    print(path)

    endtime = time.time()
    print(endtime - starttime)


main()