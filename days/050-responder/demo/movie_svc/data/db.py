import os
import csv
import collections
from typing import List

__movie_data = dict()

Movie = collections.namedtuple(
    'Movie',
    'imdb_code, director, duration, genres, title, lower_title, keywords, rating, year, imdb_score'
)


def movie_to_dict(m: Movie):
    if not m:
        return {}

    d = dict(
        imdb_code=m.imdb_code,
        title=m.title,
        director=m.director,
        keywords=list(m.keywords),
        duration=m.duration,
        genres=list(m.genres),
        rating=m.rating,
        year=m.year,
        imdb_score=m.imdb_score
    )

    return d


def find_by_imdb(imdb_code: str) -> Movie:
    global __movie_data
    movie = __movie_data.get(imdb_code)
    return movie


def search_keyword(keyword: str) -> List[Movie]:
    global __movie_data

    if not keyword:
        return []

    keyword = keyword.lower().strip()

    hits = []
    for m in __movie_data.values():
        if m.lower_title.find(keyword) >= 0:
            hits.append(m)
        elif keyword in m.keywords:
            hits.append(m)

    return hits


def search_title(keyword: str) -> List[Movie]:
    global __movie_data

    if not keyword:
        return []

    keyword = keyword.lower().strip()

    hits = []
    for m in __movie_data.values():
        if m.lower_title.find(keyword) >= 0:
            hits.append(m)

    return hits


def search_director(director: str) -> List[Movie]:
    global __movie_data

    if not director:
        return []

    director = director.lower().strip()

    hits = []
    for m in __movie_data.values():
        if m.director.lower().find(director) >= 0:
            hits.append(m)

    return hits


def global_init():
    global __movie_data
    folder = os.path.dirname(__file__)
    file = os.path.join(folder, 'movies.csv')

    with open(file, mode='r', encoding='utf-8') as fin:
        reader = csv.DictReader(fin)
        rows = list(reader)

    __movie_data = {}
    for row in rows:
        m = Movie(
            imdb_code=__build_imdb_code(row.get('movie_imdb_link', None)),
            director=row.get('director_name', '').strip(),
            rating=row.get('content_rating', '').strip(),
            title=row.get('movie_title', '').replace('\xa0', '').strip(),
            lower_title=row.get('movie_title', '').replace('\xa0', '').strip().lower(),
            duration=__make_numerical(row.get('duration', 0)),
            genres=set(__split_separated_text(row.get('genres', '').lower())),
            keywords=set(__split_separated_text(row.get('plot_keywords', '').lower())),
            imdb_score=float(row.get('imdb_score', 0.0)),
            year=__make_numerical(row.get('title_year', 0))
        )
        __movie_data[m.imdb_code] = m


def __make_numerical(text):
    if not text or not text.strip():
        return 0

    return int(text)


def __build_imdb_code(link):
    # Need to convert this:
    # http://www.imdb.com/title/tt0449088/?ref_=fn_tt_tt_1
    # to this:
    # tt0449088

    parts = link.split('/')
    if len(parts) < 5:
        return None

    return parts[4]


def __split_separated_text(text):
    if not text:
        return text

    text = text.strip()
    parts = [
        p.strip()
        for p in text.split('|')
        if p and p.strip()
    ]

    return parts
