import requests
from collections import defaultdict
from bs4 import BeautifulSoup

'''
    Global Variables
'''
# Store the official pack names in a more readable format
ANY_PACK = "Genetic Apex (A1)Any"
MEW = "Mythical Island (A1a)Mew"
MEWTWO = "Genetic Apex (A1)Mewtwo"
CHARIZARD = "Genetic Apex (A1)Charizard"
PIKACHU = "Genetic Apex (A1)Pikachu"
PROMOA = "PromoPromo-A"

VALID_PACKS = [MEW, MEWTWO, CHARIZARD, PIKACHU, PROMOA]

# Used for formatting data
PACK_MARGIN = 60
POKEMON_MARGIN = 20

# Webscrape from the correct columns
TABLE_NUM_COLS = 11
POKEMON_NUM = 1
POKEMON_NAME = 2
RARITY = 3
PACK = 4

DATA_FILE_PATH = "data/pokemon.txt"
INPUT_FILE_PATH = "input/search_pokemon.txt"

# Define color codes for different colors
COLOR_RESET = "\033[0m"
COLOR_RANK = "\033[94m"  
COLOR_POKEMON = "\033[92m" 
COLOR_PACK = "\033[93m" 
COLOR_INVALID = "\033[1;31m"

'''
    1) Webscrape relevant pokemon data from the tcgp archives and write to data file
'''

url = "https://game8.co/games/Pokemon-TCG-Pocket/archives/482685#hl_1"

print( "Beginning data retrieval..." )

response = requests.get( url )
soup = BeautifulSoup( response.text, 'html.parser' )

# pokemon -> [list of packs]
map = defaultdict( list )

# Table is laid out in <tr> rows with <td> columns
'''
Checkbox | Pokemon Number | Pokemon | Rarity | Exclusive Pack | Type | HP | Stage | Pack Points | Retreat Cost/Effect | How To Get | 
'''
pokemons = soup.find_all( 'tr' )

for pokemon in pokemons:
    cols = pokemon.find_all( 'td' )
    
    if len( cols ) >= TABLE_NUM_COLS:
        pokemon_name_tag = cols[POKEMON_NAME].find( 'a', class_='a-link' )
        pokemon_name = pokemon_name_tag.get_text( strip = True ) if pokemon_name_tag else None
        
        pack = cols[PACK].get_text( strip = True )
        
        # Allow multiple versions of the same pokemon to be findable in different packs
        if pokemon_name and pack:
            if pokemon_name in map and pack not in map[pokemon_name]:
                map[pokemon_name].append( pack )
            else:
                map[pokemon_name] = [pack]

# Store the data in the pokemon.txt file
header = "POKEMON".center( POKEMON_MARGIN ) + "|" + "PACK".center( PACK_MARGIN ) + "\n"
with open( DATA_FILE_PATH, 'w' ) as file:
    file.write( header )
    file.write( '-' * len( header ) + "\n" )
    for pokemon in map:
        pack_string = ", ".join( map[pokemon] ) 
        file.write( pokemon.center( POKEMON_MARGIN ) + "|" + pack_string.center( PACK_MARGIN ) + "\n" )

print( f"   SUCCESS: Data retrieval complete, wrote to {DATA_FILE_PATH}" )



'''
    2) Read input list
'''

print( "Reading input list..." )

input_pokemon = []

with open( INPUT_FILE_PATH, 'r') as file:
    input_pokemon = file.readlines() 

input_pokemon = [line.strip() for line in input_pokemon]

if not input_pokemon:
    print( "    ERROR: Input pokemon list is empty" )
else:
    print( f"   SUCCESS: Input pokemon list read" )



'''
    3) Calculate the best pack to open
'''
if input_pokemon:
    invalid_pokemon = []
    pack_count_map = defaultdict( lambda: {"count": 0, "pokemon": []} )

    for pack in VALID_PACKS:
        pack_count_map[pack]["count"] = 0

    for pokemon in input_pokemon:
        if pokemon not in map:
            invalid_pokemon.append( pokemon )
        
        for pack in map[pokemon]:
            if pack not in pack_count_map and pack != ANY_PACK:
                print( f"   ERROR: Encountered invalid pack for pokemon {pokemon}" )

            if pack == ANY_PACK:
                pack_count_map[MEWTWO]["count"] += 1 
                pack_count_map[CHARIZARD]["count"] += 1
                pack_count_map[PIKACHU]["count"] += 1

                pack_count_map[MEWTWO]["pokemon"].append( pokemon )
                pack_count_map[CHARIZARD]["pokemon"].append( pokemon )
                pack_count_map[PIKACHU]["pokemon"].append( pokemon )
            else:
                pack_count_map[pack]["count"] += 1
                pack_count_map[pack]["pokemon"].append( pokemon )

    pack_count = [( count["count"], pack ) for pack, count in pack_count_map.items()]
    pack_count.sort( reverse = True )

    # Loop to print the results with color
    for i, ( count, pack ) in enumerate( pack_count ):
        print( f"{COLOR_RANK}Rank {i + 1}: {COLOR_RESET}{COLOR_PACK}{pack} - {COLOR_RANK}{count} {COLOR_RESET}Pokémon" )
        print( f"  Pokémon in {pack}: {COLOR_POKEMON}{', '.join( pack_count_map[pack]['pokemon'] )}{COLOR_RESET}" )

    if invalid_pokemon:
        print( "\nThe following pokemon were not found:" )
        for pokemon in invalid_pokemon:
            print( f"    {COLOR_INVALID}{pokemon}{COLOR_RESET}" )


