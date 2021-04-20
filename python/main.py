from python.scraper import movie_scraper
from python.db_connector import DBConnector

# Data will be fetched from this URL
total_movies_required = 1000
source_url = 'https://www.imdb.com/search/title/?title_type=feature&release_date=2011-01-01,2021-04-30&genres=horror&count=250'


def main():
    DBConnector.connect_db()
    data = []
    try:
        while len(data) < 1000:
            count = len(data)
            url = source_url + "&start=" + str(count + 1) + "&ref_=adv_nxt"
            soup = movie_scraper.Scraper.get_parsed_soup(url)
            data.extend(movie_scraper.Scraper.get_movies_list(parsed_html=soup))
    except Exception:
        print('Error occurred')
    finally:
        DBConnector.insert_many(data)


if __name__ == "__main__":
    main()
