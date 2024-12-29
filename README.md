# Pokémon TCG Pack Recommender

## Project Description

The **Pokémon TCG Pack Recommender** is a tool designed to help players of the Pokémon Trading Card Game (TCG) make informed decisions about which booster packs to purchase based on various metrics such as card rarity, value, and synergy with specific decks. The project aims to improve the player's pack-opening experience by providing personalized recommendations based on their collection and gameplay preferences.

This project implements algorithms that analyze and recommend booster packs based on predefined criteria, offering insights into the best potential pack for a given budget or strategy.

## How to Run the Code

To run the code and get started with the Pokémon TCG Pack Recommender, follow these steps:

### Prerequisites

Make sure you have the following installed:
- **Python** (preferably version 3.8 or higher)
- **Pip** (Python package manager)

### Installation Steps
1. **Clone the repository:**
   ```bash
   git clone https://github.com/jacobop2/PokemonTCGP-PackRecommender.git
   cd PokemonTCGP-PackRecommender
   ```
2. **Install the required python packages:**
   ```python
   pip install -r requirements.txt
   ```
3. **Fill out the input/search_pokemon.txt file**
Enter the pokemon you wish to find, one per line. Make sure that spelling is correct.
Example:
   ```
   Greninja
   Charizard ex
   Mew ex
   ```
5. **Run the code**
   ```python
   python3 pack_rec.py
   ```
