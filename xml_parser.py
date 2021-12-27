from lxml import etree
import os
import json
from datetime import datetime
from dateutil import parser

replay_folder = "C:\\Users\\patru\\PycharmProjects\\hearthbreaker\\hsreplays_xml\\"
replay_name = "4EUDoPi8WskTsCDJGiLm6G.xml"
path = replay_folder + replay_name

with open(path) as file:
    header = next(file)

    print('inside ' + replay_name)

    print(os.getcwd())

    print(file)

    root = etree.parse(file).getroot()

    opponent_name = ""
    timestamp_string = ""
    opponent_deck = []
    # for each game, get the players
    # one is me, the other is my opponent
    for game in root.findall('Game'):
        timestamp_string = game.get('ts')

        print('TIMESTAMP IS ' + timestamp_string)
        new_date = parser.parse(timestamp_string)
        new_date_string = new_date.strftime("%Y-%m-%d %H:%M")

        for entity in game.findall('Player'):
            print(entity.get("name"))
            print(entity.get("playerID"))

            if entity.get("name") == "patruff#11779":
                # get my deck
                for deck in entity.findall('Deck'):
                    for card in deck.findall('Card'):
                        print('pat card ' + card.get('id'))
                        opponent_deck.append(card.get('id'))
                continue
            else:
                opponent_name = entity.get("name")
                print(opponent_name)

    pat_cards = []
    pat_card_names = []
    # below gets a list of card IDs for the opponent (30 cards)
    for game in root.findall('Game'):
        for entity in game.findall('Block'):
            for subentity in entity.findall('ShowEntity'):
                if not subentity.get('cardID').startswith('VAN'):
                    print(subentity.get('cardID'))
                    continue
                else:
                    print(subentity.get('cardID'))
                    pat_cards.append(subentity.get('cardID'))

    print('and the opponent card list looks like' + str(pat_cards) + ' and the length is ' + str(len(pat_cards)))
            
    with open ('hearthstone_cards.json', 'r', encoding="utf8") as jfile:
        data = json.load(jfile)

        # json_i_want = {
        #        "opponent_name": opponent_name,
       #         "date_played": new_date_string,
       #         "replay_id": replay_name,
       #         "opponent_mulligan_count": number,
      #          "opponent_opening_cards": [string],
       #         "pat_won": bool,
        #        "highest_matched_archetype": enum,
       #         "match_perc": float precision 2,
       #         "opponent_deck_list": ["Ancient of Lore", "Ancient of Lore", etc],
       #         "pat_mulligan_count": number,
        #        "pat_opening_cards": [string],
        #        "pat_highest_matched_archetype":
        #            "opponent_deck": [string]
        #}

        opponent_deck_translated = []

        for card in data:
            if card['id'] in opponent_deck:
                print('opponent deck has ' + card['name'])
                opponent_deck_translated.append(card['name'])

        for card in data:
            if card['id'] in pat_cards and card['id'] not in opponent_deck:
                print('card ' + card['name'] + ' is in pat deck')

                pat_card_names.append(card['name'])

    #


# so need to find out which playerID is which
# in the example game the playerID is 2
# <ShowEntity entity="96" cardID="VAN_EX1_571">
# <Tag tag="50" value="2"/>

# so tag 50 is the controller, in this case the player
# so player 1 is represented by 1, player 2
# playerID="2" is the value to get
