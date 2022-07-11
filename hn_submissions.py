from operator import itemgetter
from plotly import offline

import requests

# Wykonanie wywołania API i zachowanie otrzymanej odpowiedzi.
url = 'https://hacker-news.firebaseio.com/v0/topstories.json'
r = requests.get(url)
print(f"Kod stanu {r.status_code}")

# Przetworzenie informacji o każdym artykule.
submission_ids = r.json()
submission_dicts = []
for submission_id in submission_ids[:30]:
    # Przygotowanie oddzielnego wywołania API dla każdego artykułu.
    url = f"https://hacker-news.firebaseio.com/v0/item/{submission_id}.json"
    r = requests.get(url)
    # print(f"id:{submission_id}\tstatus: {r.status_code}")
    response_dict = r.json()

    # Utworzenie słownika dla każdego artykułu
    submission_dict = {
        'title': response_dict['title'],
        'hn_link':
f"http://news.ycombinator.com/item?id={submission_id}",
        'comments': response_dict['descendants'],
    }
    submission_dicts.append(submission_dict)

submission_dicts = sorted(submission_dicts, key=itemgetter('comments'), reverse=True)

title, links, comm = [], [], []
for submission_dict in submission_dicts:
    print(f"\nTytuł artykułu: {submission_dict['title']}")
    title.append(submission_dict['title'])
    print(f"\nŁącze do dyskusji: {submission_dict['hn_link']}")
    # links.append(submission_dict['hn_link'])
    print(f"\nLiczba komentarzy: {submission_dict['comments']}")
    comm.append(submission_dict['comments'])

    comment_url = submission_dict['hn_link']
    link = f"<a href='{comment_url}'>{submission_dict['title']}</a>"
    links.append(link)


# Utworzenie wizualizacji.
data = [{
    'type': 'bar',
    'x': links,
    'y': comm,
    'hovertext': title,
    'marker': {
        'color': 'rgb(60, 100, 150)',
        'line': {'width': 1.5, 'color': 'rgb(25, 25, 25)'}
    },
    'opacity': 0.6,
}]

my_layout = {
    'title': 'Oznaczone największą liczbą gwiazdek projekty Pythona w serwisie Github',
    ''
    ''
    'titlefont': {'size': 28},
    'xaxis': {
        'title': 'Artykuł',
        'titlefont': {'size': 24},
        'tickfont': {'size': 14}
    },
    'yaxis': {
        'title': 'Komentarze',
        'titlefont': {'size': 24},
        'tickfont': {'size': 14},
    },
}

fig = {'data': data, 'layout': my_layout}
offline.plot(fig, filename='hn_submissions.html')