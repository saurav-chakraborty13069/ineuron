import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep
from random import randint
from time import time
from logger import App_Logger
from warnings import warn


def scrape():
    pages = [str(i) for i in range(1,2)]
    years_url = [str(i) for i in range(2017,2018)]
    names = []
    years = []
    ratings = []
    metascores = []
    votes = []
    descriptions = []
    certficates = []
    runtimes = []
    genres = []
    directors = []
    stars = []
    gross_earnings = []

    headers = {"Accept-Language": "en-US, en;q=0.5"}
    start_time = time()
    request = 0

    # url = 'http://www.imdb.com/search/title?release_date=2017&sort=num_votes,desc&page=1'
    # response = requests.get(url)
    # #print(response.text[:500])
    # html_soup = BeautifulSoup(response.text, 'html.parser')
    # movie_containers = html_soup.find_all('div', class_ = 'lister-item mode-advanced')

    for year_url in years_url:
        for page in pages:
            response = requests.get('http://www.imdb.com/search/title?release_date=' + year_url +
            '&sort=num_votes,desc&page=' + page, headers = headers)

            sleep(randint(8, 15))

            request += 1
            elapsed_time = time() - start_time
            print('Request:{}; Frequency: {} requests/s'.format(request, request / elapsed_time))
            # if response.status_code != 200:
            #     warn('Request: {}; Status code: {}'.format(request, response.status_code))
            #
            #     # Break the loop if the number of requests is greater than expected
            # if request > 72:
            #     warn('Number of requests was greater than expected.')
            #     break

            page_html = BeautifulSoup(response.text, 'html.parser')

            mv_containers = page_html.find_all('div', class_='lister-item mode-advanced')

            for container in mv_containers:
            #if container.find('div', class_ = 'ratings-metascore') is not None:
                try:
                    name = container.h3.a.text
                    names.append(name)
                except:
                    name = 'No Name'
                    names.append(name)

                try:
                    year = container.h3.find('span',class_ = 'lister-item-year text-muted unbold').text
                    years.append(year)
                except:

                    year = 'No year'
                    years.append(year)

                try:
                    rating = container.strong.text
                    ratings.append(rating)
                except:
                    rating = 'No Rating'
                    ratings.append(rating)

                try:
                    metascore = container.find('span', class_ = 'metascore favorable').text
                    metascores.append(metascore)
                except:
                    metascore = "No metascore"
                    metascores.append(metascore)

                try:
                    vote = container.find('span', attrs = {'name': "nv"}).text
                    votes.append(vote)
                except:
                    vote = "no vote"
                    votes.append(vote)

                try:
                    desc = container.find_all('p', class_='text-muted')[1].text
                    descriptions.append(desc)
                except:
                    desc = 'No Description'
                    descriptions.append(desc)

                try:
                    cert = container.find('span', class_='certificate').text
                    certficates.append(cert)
                except:
                    cert = 'No cert'
                    certficates.append(cert)

                try:
                    runtime = container.find('span', class_='runtime').text
                    runtimes.append(runtime)
                except:
                    runtime = 'No runtime'
                    runtimes.append(runtime)

                try:
                    genre = container.find('span', class_='genre').text
                    genres.append(genre)
                except:
                    genre = 'No genre'
                    genres.append(genre)

                try:
                    director = container.find_all('p')[2].a.text
                    directors.append(director)
                except:
                    director = 'No director'
                    directors.append(director)

                try:
                    st = container.find_all('p')[2].find_all('a')[1:]
                    star = [s.text for s in st]
                    stars.append(star)
                except:
                    stars.append('No Star')

                try:
                    gross = container.find_all('span', attrs = {'name': "nv"})[1].text
                    gross_earnings.append(gross)
                except:
                    gross_earnings.append('No Earning')


    mydict = {'name': names, 'year': years, 'rating':ratings, 'metascore': metascores, 'vote': votes, 'description':descriptions,
              'certificate':certficates, 'runtime':runtimes, 'genre': genres, 'director':directors, 'stars': stars, 'earning':gross_earnings}
    df = pd.DataFrame(mydict)
    df.to_csv('first50movies.csv')
    #print(df.info())

    return df
