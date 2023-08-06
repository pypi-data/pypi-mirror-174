def parse_pokemon(pokemon):
    pokemon = pokemon.replace("\r", "")
    returnDictionary = {
        "species": "",
        "gender": "",
        "item": "",
        "ability": "",
        "nature": "",
        "evs": {
            "HP": 0,
            "Atk": 0,
            "Def": 0,
            "SpA": 0,
            "SpD": 0,
            "Spe": 0
        },
        "ivs": {
            "HP": 31,
            "Atk": 31,
            "Def": 31,
            "SpA": 31,
            "SpD": 31,
            "Spe": 31
        },
        "moves": [],
        "Gigantamax": False,
        "Happiness": 255,
        "Hidden Power Type": "",
        "Level": 100,
        "Shiny": False,
    }
    firstLine = firstLineFromSet(pokemon)
    returnDictionary["species"] = firstLine[0]
    returnDictionary["nickname"] = firstLine[1]
    returnDictionary["gender"] = firstLine[2]
    returnDictionary["item"] = firstLine[3]
    for line in pokemon.split("\n"):
        if "Ability:" in line:
            returnDictionary["ability"] = line.split("Ability: ")[1]
        elif "EVs:" in line:
            evs = line.split("EVs: ")[1].split(" / ")
            for ev in evs:
                ev = ev.split(" ")
                returnDictionary["evs"][ev[1]] = int(ev[0])
        elif " Nature" in line:
            returnDictionary["nature"] = line.split(" Nature")[0]
        elif "IVs:" in line:
            ivs = line.split("IVs: ")[1].split(" / ")
            for iv in ivs:
                iv = iv.split(" ")
                returnDictionary["ivs"][iv[1]] = int(iv[0])
        elif "Gigantamax" in line:
            returnDictionary["Gigantamax"] = True
        elif "Happiness:" in line:
            returnDictionary["Happiness"] = int(line.split("Happiness: ")[1])
        elif "Hidden Power:" in line:
            returnDictionary["Hidden Power Type"] = line.split("Hidden Power: ")[1]
        elif "Level:" in line:
            returnDictionary["Level"] = int(line.split("Level: ")[1])
        elif "Shiny" in line:
            returnDictionary["Shiny"] = True
        elif "- " in line:
            returnDictionary["moves"].append(line.split("- ")[1])
    return returnDictionary

def get_pokemon_gender(pokemon):
    if "(M)" in pokemon:
        return "M"
    elif "(F)" in pokemon:
        return "F"
    else:
        return ""

def firstLineFromSet(pset):
    line = pset.split("\n")[0]
    name = ""
    nickname = ""
    item = ""
    gender = get_pokemon_gender(line)
    if gender != "":
        line = line.replace(f" ({gender}) ", "")
    if "@" in line:
        if ")" in line:
            name = line.split("(")[1].split(")")[0]
            nickname = line.split(" (")[0]
        else:
            name = line.split("@")[0]
            nickname = name
        item = line.split("@")[1].strip()
    else:
        if ")" in line:
            name = line.split("(")[1].split(")")[0]
            nickname = line.split(" (")[0]
        else:
            name = line
            nickname = name
    return name, nickname, gender, item

def jsonToShowdown(json):
    returnString = ""
    for pokemon in json:
        firstLine = ""
        if pokemon["nickname"] != pokemon["species"]:
            firstLine += f'{pokemon["nickname"]} ({pokemon["species"]})'
        else:
            firstLine += pokemon["species"][:-1]
        if pokemon["item"]:
            firstLine += f' @ {pokemon["item"]}'

        returnString += firstLine

        returnString += f'\nAbility: {pokemon["ability"]}'

        evString = "\nEVs: "
        ivString = "\nIVs: "
        for stat in pokemon["evs"]:
            if pokemon["evs"][stat] != 0:
                evString += f'{pokemon["evs"][stat]} {stat} / '
        for stat in pokemon["ivs"]:
            if pokemon["ivs"][stat] != 31:
                ivString += f'{pokemon["ivs"][stat]} {stat} / '
        if evString != "\nEVs: ":
            returnString += evString[:-3]
        if ivString != "\nIVs: ":
            returnString += ivString[:-3]

        returnString = returnString[:-3]
        returnString += f'\n{pokemon["nature"]} Nature'
        if pokemon["Gigantamax"]:
            returnString += '\nGigantamax: Yes'
        if pokemon["Happiness"] != 255:
            returnString += f'\nHappiness: {pokemon["Happiness"]}'
        if pokemon["Hidden Power Type"]:
            returnString += f'\nHidden Power: {pokemon["Hidden Power Type"]}'
        if pokemon["Level"] != 100:
            returnString += f'\nLevel: {pokemon["Level"]}'
        if pokemon["Shiny"]:
            returnString += f'\nShiny: Yes'
        for move in pokemon["moves"]:
            returnString += f'\n- {move}'
        returnString += '\n\n'
    return returnString[:-2]

