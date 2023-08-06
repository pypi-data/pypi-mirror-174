import json
import urllib.request

import requests
from . import Showdown


def convert_team(team):
    if "\r" not in team:
        team = team.split('\n')
        team = [line + '  ' for line in team]
        team = '\r\n'.join(team)
        team = team.replace("  \r", "\r")
    return team

cookies = {
    'light': 'false',
    'vgc': 'true',
    'eviv': 'true',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:105.0) Gecko/20100101 Firefox/105.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Origin': 'https://pokepast.es',
    'Connection': 'keep-alive',
    'Referer': 'https://pokepast.es/',
    # Requests sorts cookies= alphabetically
    # 'Cookie': 'light=false; vgc=true; eviv=true',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
}

def createPokePaste(team, author="", title="", notes="", format=""):
    notes = f'Format: {format}\n{notes}'
    team = convert_team(team)
    # replace \r\n at the end with ""
    team = team[:-6]

    data = {
        'paste': team, 
        'title': title,
        'author': author,
        'notes': notes,
    }
    response = requests.post('https://pokepast.es/create', cookies=cookies, headers=headers, data=data)
    return response.url

def retrieve_pokepaste(url):
    with urllib.request.urlopen(url+"/json") as response:
        html = response.read()
        html = html.decode('utf-8')
        jsonn = json.loads(html)
        jsonn['paste'] = jsonn['paste'].replace("  ", " ")
        toReturn = pokemon_from_paste(jsonn['paste'])
        return toReturn

def pokemon_from_paste(paste):
    if "\r\n\r\n" in paste:
        pokemon = paste.split("\r\n\r\n")
    else:
        pokemon = paste.split("\r\n")
    for poke in pokemon:
        poke.replace("\r\n", "\n")
        pokemon[pokemon.index(poke)] = Showdown.parse_pokemon(poke)
    pokemon = [poke for poke in pokemon if poke['species']]
    return pokemon
