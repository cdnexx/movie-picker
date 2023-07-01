from django.http import HttpResponse
from django.shortcuts import render, redirect
import requests
from bs4 import BeautifulSoup
import random

# Create your views here.
def index_page(request):
    return render(request, 'index.html')

def get_url(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        return redirect(f"/list/{url.split('/')[-1]}")
    return HttpResponse('Invalid Method')

def get_movie_list(list_id):
    url = f"https://www.listchallenges.com/print-list/{list_id}"

    response = requests.get(url)
    html = response.text

    soup = BeautifulSoup(html, 'html.parser')
    list_title = soup.find('h1')
    list_title = list_title.get_text(strip=True)
    movie_container = soup.find('div', id='repeaterItems')

    movie_list = []
    for line in movie_container.text.splitlines():
        movie = ''
        for i in line:
            if i.lower() in "abcdefghijklmnopqrstuvwxyz0123456789().:'- ":
                movie += i
        if movie != '':
            split_index = movie.find('. ')+2
            movie_list.append(movie[split_index:])

    return list_title, movie_list


def list_page(request, list_id = ""):
    if list_id == "":
        return redirect("/")
    
    list_title, movie_list = get_movie_list(list_id)

    return render(request, 'list.html', {
        'list_id': list_id,
        'list_title': list_title,
        'list_length': len(movie_list),
        'movie_list': movie_list
    })


def random_page(request, list_id=""):
    if list_id == "":
        return redirect("/")
    
    list_title, movie_list = get_movie_list(list_id)

    random_index = random.randint(0, len(movie_list)-1)
    pick = movie_list[random_index]
    # Mask (1985)

    pick_title = pick[0:-7]
    pick_year = pick[-6:]
    pick_year = pick_year[1:-1]

    # print(pick)
    # print(pick_title, pick_year)

    url = f"https://api.themoviedb.org/3/search/movie?query={pick_title}&include_adult=true&language=en-US&page=1&year={pick_year}"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJhZTQzNWI0MGU4NjcxMjc5MmJjZTNiZDBhYzQxZDM0MiIsInN1YiI6IjY0OWY5OTI4YzM5MGM1MDE0ZTNiYzYyYSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.Ztab9yOwhYGySinubX0xUNgh_ujqnxLydy-g61ksSq4"
    }

    response = requests.get(url, headers=headers)

    data = response.json()
    data = data['results'][0]

    title = data['title']
    release = data['release_date']
    overview = data['overview']
    image = f"https://www.themoviedb.org/t/p/w600_and_h900_bestv2/{data['poster_path']}"

    return render(request, 'random.html', {
        'list_title': list_title,
        'title': title,
        'release': release,
        'overview': overview,
        'image': image
    })
    

