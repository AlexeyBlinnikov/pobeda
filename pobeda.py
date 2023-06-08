from bs4 import BeautifulSoup as BS
import requests

go = []
mac = []
electro = []
tent_beda = []

def pobeda_gopro():

    r = requests.get("https://победа-63.рф/catalog/foto-i-videotehnika/videokamery/?q=20&s=new&c=0&cg=127&a=0&min=15000&max=68900&")
    html = BS(r.content, 'html.parser')

    data = html.find_all('div', class_ = 'card is-lazy')
    for i in data:
        content = i.find("a", class_ = 'card-title')
        name = content['title']
        if name not in go:
            go.append(name)      
    
    return go[-1]

def pobeda_mac():
    r = requests.get("https://победа-63.рф/catalog/search/1/?k=macbook&q=20&s=new&c=0&cg=0&a=0&page=1&min=20000&max=100000&")
    
    html = BS(r.content, 'html.parser')
    data = html.find_all('div', class_ = 'card is-lazy')
    for i in data:
        content = i.find("a", class_ = 'card-title')
        name = content['title']
        if name not in mac:
            mac.append(name)
    return mac[-1]

def pobeda_electro():
    r = requests.get("https://победа-63.рф/catalog/search/1/?k=электросамокат&q=20&s=new&c=0&cg=0&a=0&page=1&")
    html = BS(r.content, 'html.parser')
    data = html.find_all('div', class_ = 'card is-lazy')
    for i in data:
        content = i.find("a", class_ = 'card-title')
        name = content['title']
        if name not in electro:
            electro.append(name)
    return electro[-1]

def pobeda_tent():
    r = requests.get("https://победа-63.рф/catalog/search/1/?k=палатка&q=20&s=new&c=0&cg=0&a=0&page=1&")
    html = BS(r.content, 'html.parser')
    data = html.find_all('div', class_ = 'card is-lazy')
    for i in data:
        content = i.find("a", class_ = 'card-title')
        name = content['title']
        if name not in tent_beda:
            tent_beda.append(name)
    return tent_beda[-1]