import requests
from bs4 import BeautifulSoup
import random

url = 'https://www.listchallenges.com/print-list/189745'

response = requests.get(url)
html = response.text

soup = BeautifulSoup(html, 'html.parser')
list_title = soup.find('h1')
movie_container = soup.find('div', id='repeaterItems')

movie_list = []
for line in movie_container.text.splitlines():
    movie = ''
    for i in line:
        if i.lower() in "abcdefghijklmnopqrstuvwxyz0123456789(). ":
            movie += i
    if movie != '':
        split_index = movie.find('. ')+2
        movie_list.append(movie[split_index:])

# for movie in movie_list:
#     print(f"{movie}")
print(list_title.get_text(strip=True))
print(f"Movies = {len(movie_list)}")

random_index = random.randint(0, 99)

print(f"Película seleccionada: {movie_list[random_index]}")

