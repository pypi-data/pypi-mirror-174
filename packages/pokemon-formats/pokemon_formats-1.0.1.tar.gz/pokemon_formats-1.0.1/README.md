# Pok&eacute;mon Set Formats

This is a package for interacting with the format used by [Pokémon Showdown](https://pokemonshowdown.com/) and [PokéPaste](https://pokepast.es/). 
It's specific features are:
- Parsing Pokémon Showdown and PokéPaste formats into a dictionary
- Converting a dictionary into a Pokémon Showdown format
- Uploading a text team to PokéPaste and returning the link
- Retrieve a JSON team from PokéPaste

## Installation
```bash
ignore for now
```
# Usage
## Uploading a team to PokéPaste
```python
from pokemon_formats import PokePaste
team = """Axew @ Aguav Berry
Ability: Rivalry
EVs: 248 HP / 252 Atk / 8 SpA
Naughty Nature
- Aqua Tail
- Crunch
- Dragon Claw
- Draco Meteor

Bagon @ Choice Band
Ability: Sheer Force
EVs: 252 Atk / 4 SpD / 252 Spe
Adamant Nature
- Body Slam
- Double-Edge
- Dragon Claw
- Dragon Dance

Bulbasaur @ Eviolite
Ability: Chlorophyll
EVs: 252 Atk / 4 SpA / 252 Spe
Lonely Nature
- Body Slam
- Curse
- Double-Edge
- Energy Ball
"""

url = PokePaste.createPokePaste(team)
print(url)
```







## Retrieving a team from PokéPaste
```python
from pokemon_formats import PokePaste

url = "https://pokepast.es/0840194f9282db1a"
pokepaste_json = PokePaste.retrieve_pokepaste(url)
print(pokepaste_json)
```

## Convert a dictionary to a Pokémon Showdown format
```python
from pokemon_formats import PokePaste
from pokemon_formats import Showdown

team = PokePaste.retrieve_pokepaste("https://pokepast.es/0840194f9282db1a")
showdown_format = Showdown.jsonToShowdown(team)
print(showdown_format)
```

## Convert a Pokémon Showdown format to a dictionary
```python
from pokemon_formats import PokePaste

team = """Axew @ Aguav Berry
Ability: Rivalry
EVs: 248 HP / 252 Atk / 8 SpA
Naughty Nature
- Aqua Tail
- Crunch
- Dragon Claw
- Draco Meteor

Bagon @ Choice Band
Ability: Sheer Force
EVs: 252 Atk / 4 SpD / 252 Spe
Adamant Nature
- Body Slam
- Double-Edge
- Dragon Claw
- Dragon Dance

Bulbasaur @ Eviolite
Ability: Chlorophyll
EVs: 252 Atk / 4 SpA / 252 Spe
Lonely Nature
- Body Slam
- Curse
- Double-Edge
- Energy Ball
"""

json_team = PokePaste.pokemon_from_paste(team)
print(json_team)
```


