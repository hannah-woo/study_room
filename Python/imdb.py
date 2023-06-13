import requests
from bs4 import BeautifulSoup

url = 'https://www.imdb.com/chart/top/?ref_=nv_mv_250'
res = requests.get(url)

result = {}
if res.status_code == 200:
    soup = BeautifulSoup(res.text, 'html.parser')
    chunk = soup.find('tbody', class_='lister-list')
    parts = chunk.find_all('td', class_='titleColumn')

    for idx, data in enumerate(parts):
        title = data.find('a').string
        year = data.find('span', class_='secondaryInfo').get_text()
        val = f'{title} - {year}년작'
        result[idx+1] = val

print(result)
        