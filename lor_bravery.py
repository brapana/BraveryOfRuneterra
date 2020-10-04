# Legends of Runeterra Bravery
from lor_deckcodes import LoRDeck, CardCodeAndCount
import json
import random
from string import capwords
from collections import defaultdict


set01_file = open('set_bundles/en_us/data/set1-en_us.json', 'r', encoding='utf-8')
set02_file = open('set_bundles/en_us/data/set2-en_us.json', 'r', encoding='utf-8')
set03_file = open('set_bundles/en_us/data/set3-en_us.json', 'r', encoding='utf-8')
globals_file = open('core_bundle/en_us/data/globals-en_us.json', 'r', encoding='utf-8')

set01_bundle = json.load(set01_file)
set02_bundle = json.load(set02_file)
set03_bundle = json.load(set03_file)

globals_dict = json.load(globals_file)

all_bundles = set01_bundle + set02_bundle + set03_bundle

MAX_DECK_SIZE = 40
MAX_CHAMPIONS = 6
MAX_CARD_COPIES = 3

# extract all available regions from globals_dict
ALL_REGIONS = [x['nameRef'] for x in globals_dict['regions']]


def find_card_info(card_code: str) -> dict:
    """Return card info from Riot's set bundle given the card code"""
    set_dict = {'01': set01_bundle, '02': set02_bundle, '03': set03_bundle}

    for card in set_dict[card_code[:2]]:
        if card['cardCode'] == card_code:
            return card


def trim_card_info(card_info: dict):
    """Trim card info dictionary to only what is neccessary"""

    # TODO: Remove unneeded attributes
    trimmed_card_info = {'name': card_info['name'], 'cost': card_info['cost'], 'type': card_info['type'], 'region': card_info['region'],
    'full_img': card_info['assets'][0]['fullAbsolutePath'], 'card_img': card_info['assets'][0]['gameAbsolutePath'], 'copies': card_info['copies'],
    'description': card_info['descriptionRaw'], 'level_description': card_info['levelupDescriptionRaw'], 'keywords': card_info['keywords'],
    'subtypes': card_info['subtypes'], 'supertype': card_info['supertype'], 'card_code': card_info['cardCode']}

    return trimmed_card_info


def find_deck_info(deck: [str]) -> dict:
    """Lookup data for each card in deck and return a list of dicts containing json data from Riot's set bundles."""
    champions = []
    followers = []
    spells = []

    for card in deck:
        card_code = card[2:]
        card_info = find_card_info(card_code)
        card_info['copies'] = int(card[0])

        if card_info['supertype'] == 'Champion':
            champions.append(trim_card_info(card_info))
        elif card_info['type'] == 'Unit':
            followers.append(trim_card_info(card_info))
        else:
            spells.append(trim_card_info(card_info))

    # sort deck information by cost, number of copies, then type
    champions.sort(key=lambda x: (x['cost'], x['copies']), reverse=True)
    followers.sort(key=lambda x: (x['cost'], x['copies']), reverse=True)
    spells.sort(key=lambda x: (x['cost'], x['copies']), reverse=True)

    return {'champions': champions, 'followers': followers, 'spells': spells}


def generate_frequency_list(freq_dict: dict) -> [ () ]:
    """Given a dictionary of type key : int return an output of tuple pairs
        in the format [(key, freq), ...] sorted by highest to lowest freq"""
    freq_output = []

    key_list = list(freq_dict.keys())

    key_list.sort(key=lambda x: freq_dict[x], reverse=True)

    for key in key_list:
        freq_output.append((key, freq_dict[key]))

    return freq_output


def format_deck_info(deck: [str]) -> dict:
    """Format the deck info returned by find_deck_info for the inputted deck list,
    and generate a fitting name for the deck"""

    deck_info = find_deck_info(deck)

    keyword_freqs = defaultdict(int)
    subtype_freqs = defaultdict(int)
    region_freqs = defaultdict(int)

    total_champions = 0
    total_followers = 0
    total_spells = 0

    cards_output = f""

    flattened_deck_info = deck_info['champions'] + deck_info['followers'] + deck_info['spells']

    # TODO: what in this loop can be removed/calculated without this loop?
    # gather data on cards, while building the output string
    for card_info in flattened_deck_info:

        if card_info['type'] == 'Unit':
            if card_info['supertype'] == 'Champion':
                total_champions += card_info['copies']
            else:
                total_followers += card_info['copies']
            if card_info['keywords']:
                for keyword in card_info['keywords']:
                    keyword_freqs[keyword] += 1
            if card_info['subtypes']:
                for subtype in card_info['subtypes']:
                    subtype_freqs[subtype] += 1

        else:
            total_spells += card_info['copies']

        region_freqs[card_info['region']] += card_info['copies']


    keyword_freq_list = generate_frequency_list(keyword_freqs)
    subtype_freq_list = generate_frequency_list(subtype_freqs)
    region_freq_list = generate_frequency_list(region_freqs)

    most_freq_keyword = keyword_freq_list[0] if keyword_freq_list else ('', -1)
    most_freq_subtype = subtype_freq_list[0] if subtype_freq_list else ('', -1)

    keyword_stats = "".join([capwords(x[0]) + ": " + str(x[1]) + "<br>" for x in keyword_freq_list])
    subtype_stats = "".join([capwords(x[0]) + ": " + str(x[1]) + "<br>" for x in subtype_freq_list])
    region_stats = "".join([capwords(x[0]) + ": " + str(x[1]) + "<br>" for x in region_freq_list])

    # construct deck stats html for popover
    deck_stats = f"<div class='row'> \
                        <div class='col-lg-4'><h6>Regions</h6>{region_stats}</div> \
                        <div class='col-lg-4'><h6>Keywords</h6>{keyword_stats}</div> \
                        <div class='col-lg-4'><h6>Subtypes</h6>{subtype_stats}</div> \
                   </div>"

    # TODO: If deck is somehow all spells, this will error
    most_significant_unit = deck_info['champions'][0] if deck_info['champions'] else deck_info['followers'][0]

    # deck name is "[most common keyword/subtype] [most frequent champion or highest cost unit if no champs]"
    deck_name = f"{capwords(most_freq_keyword[0]) if most_freq_keyword[1] > most_freq_subtype[1] else capwords(most_freq_subtype[0])} {most_significant_unit['name']}"


    formatted_deck_info = {'deck_name': deck_name, 'deck_code': deck.encode(), 'champions': deck_info['champions'],
                           'followers': deck_info['followers'], 'spells': deck_info['spells'],
                           'cover_card': most_significant_unit['card_code'], 'deck_stats': deck_stats,
                           'total_champions': total_champions, 'total_followers': total_followers, 'total_spells': total_spells}


    return formatted_deck_info



def pick_rand_n_regions(num_regions: int, regions: [str]) -> [str]:
    """Pick n amount of regions from a list of regions"""
    regions = random.choices(regions, k=num_regions)
    return regions


def generate_rand_deck(selected_regions: [str]) -> [str]:
    """Generates a random and valid Legends of Runeterra deck with the selected regions"""
    num_champions = random.randrange(0, MAX_CHAMPIONS)

    champion_codes = []
    non_champion_codes = []

    # separate cards from selected regions into champions and non_champions (followers/spells), store only card codes
    for card in all_bundles:
        if card['regionRef'] in selected_regions and card['collectible']:
            if card['supertype'] == 'Champion':
                champion_codes.append(card['cardCode'])
            else:
                non_champion_codes.append(card['cardCode'])

    # store the the max amount of copies of each card in each list (3)
    champion_codes = champion_codes * MAX_CARD_COPIES
    non_champion_codes = non_champion_codes * MAX_CARD_COPIES

    # sample champion and non-champion list adhering to the chosen number of champions for this deck
    selected_champion_codes = random.sample(champion_codes, k=num_champions)
    selected_non_champion_codes = random.sample(non_champion_codes, k=MAX_DECK_SIZE-num_champions)

    new_deck_codes = selected_champion_codes + selected_non_champion_codes

    # TODO: better way to pick only unique cards than cast as set?
    new_deck = LoRDeck([CardCodeAndCount(card_code, new_deck_codes.count(card_code)) for card_code in set(new_deck_codes)])

    return new_deck


if __name__ == '__main__':
    deck = generate_rand_deck(pick_rand_n_regions(2, ALL_REGIONS))
