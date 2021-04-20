import requests
from bs4 import BeautifulSoup


class Scraper:

    @staticmethod
    def get_parsed_soup(url):
        html = requests.get(url)
        return BeautifulSoup(html.content, features="html.parser")

    @staticmethod
    def get_movies_list(parsed_html):
        list_parent_item = parsed_html.find('div', 'lister-list')
        element_list = list_parent_item.find_all('div', 'lister-item mode-advanced')
        result = []
        for element in element_list:
            movie_name = element.select_one('h3.lister-item-header a').contents[0]
            movie_full_link = element.select_one('h3.lister-item-header a')['href']
            runtime = element.select_one('p.text-muted span.runtime')
            if runtime is not None:
                runtime = runtime.contents[0]
            genre = element.select_one('p.text-muted span.genre')
            if genre is not None:
                genre = genre.contents[0]
            cover_art = element.select_one('div.lister-item-image > a > img')
            if cover_art is not None:
                cover_art = cover_art['src']
            release_year = element.select_one('h3.lister-item-header > span.lister-item-year')
            if release_year is not None:
                release_year = release_year.contents[0]
                release_year = release_year.replace('(', '')
                release_year = release_year.replace(')', '')
            crew = element.select('p[class=""] > *')
            directors = []
            all_directors_added = False
            actors = []
            for member in crew:
                if member.contents[0] == '|':
                    all_directors_added = True
                    continue
                if not all_directors_added:
                    directors.append(member.contents[0].strip())
                else:
                    actors.append(member.contents[0].strip())
            result.append({
                "name": (movie_name or 'N/A').strip(),
                "runtime": (runtime or 'N/A').strip(),
                "genre": (genre or 'N/A').strip(),
                "cover_art": cover_art.strip(),
                "directors": directors,
                "actors": actors,
                "release_year": (release_year or "N/A"),
                "movie_full_link": movie_full_link
            })
        return result
