from lxml import etree
import os
import json
from datetime import datetime
from dateutil import parser
from deck_helper import get_basic_decks

known_player = "patruff#11779"
opponent_player = ""
known_player_class = ""
opponent_player_class = ""
coin_holder = ""
winner = ""
opponent_player_cards_played = []
known_player_cards_played = []

known_player_cards_played_names = []
opponent_player_cards_played_names = []

known_player_cards_mulliganned = []
opponent_player_cards_mulliganned = []

known_player_cards_kept = []
opponent_player_cards_kept = []

known_player_cards_mulliganned_names = []
opponent_player_cards_mulliganned_names = []

known_player_cards_kept_names = []
opponent_player_cards_kept_names = []

known_player_pre_mulligan_hand_names = []
opponent_player_pre_mulligan_hand_names = []

replay_folder = "C:\\Users\\patru\\PycharmProjects\\hearthbreaker\\hsreplays_xml\\"
replay_name = "4EUDoPi8WskTsCDJGiLm6G.xml"

replay_name = "GPFAbQzkavyvmYtGJPDrbi.xml"
path = replay_folder + replay_name

def convert_list_to_string(somelist):
    string_separated_list = (',').join(somelist)

    if string_separated_list == "":
        string_separated_list = "none"

    return string_separated_list

with open(path) as file:
    header = next(file)

    print('inside ' + replay_name)

    print(os.getcwd())

    print(file)

    root = etree.parse(file).getroot()

    opponent_name = ""
    timestamp_string = ""
    known_player_deck = []
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

            if entity.get("name") == known_player:

                print('known player is entity id ' + entity.get("id"))

                if entity.get("id") == "2":
                    print('pat goes first')

                else:
                    print('pat goes second')
                    coin_holder = known_player

                # get my deck
                for deck in entity.findall('Deck'):
                    for card in deck.findall('Card'):
                        print('pat card ' + card.get('id'))
                        known_player_deck.append(card.get('id'))
                continue
            else:
                opponent_player = entity.get("name")
                print(opponent_player)

                if entity.get("id") == "3":
                    print('opponent goes second')
                    coin_holder = opponent_player

    opponent_card_names = []

    final_turn = ""

    # get final turn
    for game in root.findall('Game'):
        for block in game.findall('Block'):
            for tagchange in block.findall('TagChange'):
                if tagchange.get('tag') == '271':
                    if tagchange.get('entity') == '1':
                        print('turn is ' + tagchange.get('value'))
                        final_turn = tagchange.get('value')

    print("FINAL TURN IS " + final_turn)
    #< TagChange
    #entity = "1"
    #tag = "271"
    # = "20" / >

    known_player_total_mulligan_entity_list = []
    opponent_player_total_mulligan_entity_list = []

    known_player_mulligan_entity_list = []
    opponent_player_mulligan_entity_list = []

    known_player_kept_entity_list = []
    opponent_player_kept_entity_list = []

    for game in root.findall('Game'):
        for block in game.findall('Block'):
            for mulligan_choices in block.findall('Choices'):
                print('MULLIGAN CHOICES' + str(mulligan_choices))
                who_is_choosing = mulligan_choices.get('entity')
                for mulligan_choice in mulligan_choices.findall('Choice'):
                    print(mulligan_choice.get('entity'))
                    if who_is_choosing == '3':
                        # if the entity choosing is the 2nd player
                        if coin_holder == known_player:
                            known_player_total_mulligan_entity_list.append(mulligan_choice.get('entity'))
                        else:
                            opponent_player_total_mulligan_entity_list.append(mulligan_choice.get('entity'))
                    elif who_is_choosing == '2':
                        # if the entity choosing is the first player
                        if coin_holder != known_player:
                            known_player_total_mulligan_entity_list.append(mulligan_choice.get('entity'))
                        else:
                            opponent_player_total_mulligan_entity_list.append(mulligan_choice.get('entity'))

    print('original total mulligan list for known player is ' + str(known_player_total_mulligan_entity_list))
    print('original total mulligan list for opponent player is ' + str(opponent_player_total_mulligan_entity_list))

    for game in root.findall('Game'):
        for block in game.findall('Block'):
            for mulligan_choices in block.findall('ChosenEntities'):
                print('MULLIGAN CHOICES' + str(mulligan_choices))
                who_is_choosing = mulligan_choices.get('entity')
                for mulligan_choice in mulligan_choices.findall('Choice'):
                    print(mulligan_choice.get('entity'))
                    if who_is_choosing == '3':
                        # if the entity choosing is the 2nd player
                        if coin_holder == known_player:
                            known_player_kept_entity_list.append(mulligan_choice.get('entity'))
                        else:
                            opponent_player_kept_entity_list.append(mulligan_choice.get('entity'))
                    elif who_is_choosing == '2':
                        # if the entity choosing is the first player
                        if coin_holder != known_player:
                            known_player_kept_entity_list.append(mulligan_choice.get('entity'))
                        else:
                            opponent_player_kept_entity_list.append(mulligan_choice.get('entity'))

    set_difference = set(known_player_total_mulligan_entity_list) - set(known_player_kept_entity_list)
    known_player_mulligan_entity_list = list(set_difference)

    set_difference = set(opponent_player_total_mulligan_entity_list) - set(opponent_player_kept_entity_list)
    opponent_player_mulligan_entity_list = list(set_difference)

    print("print out of the lists")
    print("known_player_mulligan_entity_list is " + str(known_player_mulligan_entity_list))
    print("opponent_player_mulligan_entity_list is " + str(opponent_player_mulligan_entity_list))

    print("known_player_kept_entity_list is " + str(known_player_kept_entity_list))
    print("opponent_player_kept_entity_list is " + str(opponent_player_kept_entity_list))

    # below gets the winner
    for game in root.findall('Game'):
        for tagchange_element in game.findall('TagChange'):
            if tagchange_element.get('entity') == '2':
                if tagchange_element.get('tag') == '17':
                    if tagchange_element.get('value') == '4':
                        print("THE WINNER IS OPPONENT " + opponent_player)
                        if coin_holder == known_player:
                            winner = opponent_player
                        else:
                            winner = known_player

            elif tagchange_element.get('entity') == '3':
                if tagchange_element.get('tag') == '17':
                    if tagchange_element.get('value') == '4':
                        print("THE WINNER IS KNOWN PLAYER " + known_player)
                        winner = coin_holder



    # below gets a list of card IDs for the opponent (30 cards)
    for game in root.findall('Game'):
        for entity in game.findall('Block'):
            tagchange_entity_list = []
            is_entity_2 = True
            entity2_counter = 0
            entity3_counter = 0

            for tagchange_element in entity.findall('TagChange'):
                if tagchange_element.get('entity') == '2':
                    entity2_counter = entity2_counter + 1
                    if tagchange_element.get('tag') == '17':
                        if tagchange_element.get('value') == '4':
                            print("THE WINNER IS KNOWN PLAYER " + opponent_player)
                else:
                    if tagchange_element.get('entity') == '3':
                        entity3_counter = entity3_counter + 1
                        if tagchange_element.get('tag') == '17':
                            if tagchange_element.get('value') == '4':
                                print("THE WINNER IS KNOWN PLAYER " + known_player)
                tagchange_entity_list.append(tagchange_element.get('entity'))

            for subentity in entity.findall('ShowEntity'):
                owner = known_player
                print("inside ShowEntity, before tag ownership, card looks like " + subentity.get('cardID'))
                for Tag in subentity.findall('Tag'):
                    # get the owner of the card
                    if Tag.get('tag') == '50':
                        if Tag.get('value') == '2':
                            if coin_holder == known_player:
                                owner = known_player
                            else:
                                owner = opponent_player
                        if Tag.get('value') == '1':
                            if coin_holder != known_player:
                                owner = known_player
                            else:
                                owner = opponent_player

                if owner == known_player:
                    if subentity.get('cardID').startswith('VAN'):
                        dict_to_append = {'cardID': subentity.get('cardID'), 'entity': subentity.get('entity')}
                        known_player_cards_played.append(dict_to_append)

                else:
                    if subentity.get('cardID').startswith('VAN'):
                        dict_to_append = {'cardID': subentity.get('cardID'), 'entity': subentity.get('entity')}
                        opponent_player_cards_played.append(dict_to_append)

            for innerBlock in entity.findall('Block'):
                for subentity in innerBlock.findall('ShowEntity'):
                    owner = known_player
                    print("inside ShowEntity, before tag ownership, card looks like " + subentity.get('cardID'))
                    for Tag in subentity.findall('Tag'):
                        # get the owner of the card
                        if Tag.get('tag') == '50':
                            if Tag.get('value') == '2':
                                if coin_holder == known_player:
                                    owner = known_player
                                else:
                                    owner = opponent_player
                            if Tag.get('value') == '1':
                                if coin_holder != known_player:
                                    owner = known_player
                                else:
                                    owner = opponent_player

                    if owner == known_player:
                        if subentity.get('cardID').startswith('VAN') and subentity.get('cardID') != "VAN_EX1_145e":
                            # VAN_EX1_145e is preparation as a neutral card, basically for the effect
                            # to avoid duplicates remove this
                            dict_to_append = {'cardID': subentity.get('cardID'), 'entity': subentity.get('entity')}
                            known_player_cards_played.append(dict_to_append)
                    else:
                        if subentity.get('cardID').startswith('VAN') and subentity.get('cardID') != "VAN_EX1_145e":
                            dict_to_append = {'cardID': subentity.get('cardID'), 'entity': subentity.get('entity')}
                            opponent_player_cards_played.append(dict_to_append)


    print('and the opponent card list looks like' + str(opponent_player_cards_played) + ' and the length is ' + str(len(opponent_player_cards_played)))
            
    with open ('hearthstone_cards.json', 'r', encoding="utf8") as jfile:
        data = json.load(jfile)

        known_player_deck_translated = []

        for card in data:
            if card['id'] in known_player_deck:
                print('pat deck has ' + card['name'])
                known_player_deck_translated.append(card['name'])
                if card['cardClass'] != "NEUTRAL":
                    known_player_class = card['cardClass'] # "cardClass": "ROGUE"
                    print(known_player_class)

        entities_used = []
        for index in range(len(known_player_cards_played)):
            # print('KNOWN PLAYER CARDS PLAYED LOOKS LIKE ' + str(known_player_cards_played))
            for card in data:
                if card['id'] == known_player_cards_played[index]['cardID']:

                    if known_player_cards_played[index]['entity'] in entities_used or int(known_player_cards_played[index]['entity']) > 70:
                        continue
                    else:
                        print('INSIDE DICT card ' + card['name'] + ' played by known player and entity is ' + str(
                            known_player_cards_played[index]['entity']))
                        entities_used.append(known_player_cards_played[index]['entity'])

                    known_player_cards_played_names.append(card['name'])

                    if known_player_cards_played[index]['entity'] in known_player_mulligan_entity_list:
                        known_player_cards_mulliganned_names.append(card['name'])
                        # cards are being duplicated so this will handle that


                    if known_player_cards_played[index]['entity'] in known_player_kept_entity_list:
                        known_player_cards_kept_names.append(card['name'])


        for index in range(len(opponent_player_cards_played)):
            for card in data:
                if card['id'] == opponent_player_cards_played[index]['cardID']:

                    if opponent_player_cards_played[index]['entity'] in entities_used or int(opponent_player_cards_played[index]['entity']) > 70:
                        continue
                    else:
                        print('INSIDE DICT card ' + card['name'] + ' played by opponent player and entity is ' + str(
                            opponent_player_cards_played[index]['entity']))
                        opponent_player_cards_played_names.append(card['name'])

                    if card['cardClass'] != "NEUTRAL":
                        opponent_player_class = card['cardClass']  # "cardClass": "ROGUE"
                        print(opponent_player_class)

                    if opponent_player_cards_played[index]['entity'] in opponent_player_mulligan_entity_list:
                        opponent_player_cards_mulliganned_names.append(card['name'])

                    if opponent_player_cards_played[index]['entity'] in opponent_player_kept_entity_list:
                        opponent_player_cards_kept_names.append(card['name'])



        print(get_basic_decks())

        basic_decks = get_basic_decks()

        opponent_max_match_perc = 0
        opponent_max_match_name = ""

        known_player_max_match_perc = 0
        known_player_max_match_name = ""

        for basic_deck in basic_decks:
            opponent_match_perc = len(set(opponent_player_cards_played_names) & set(basic_deck['deck_list'])) / float(len(set(opponent_player_cards_played_names) | set(basic_deck['deck_list']))) * 100
            if opponent_match_perc > opponent_max_match_perc:
                opponent_max_match_perc = opponent_match_perc
                opponent_max_match_name = basic_deck['name']

        for basic_deck in basic_decks:
            pat_match_perc = len(set(known_player_cards_played_names) & set(basic_deck['deck_list'])) / float(len(set(known_player_cards_played_names) | set(basic_deck['deck_list']))) * 100
            if pat_match_perc > known_player_max_match_perc:
                known_player_max_match_perc = pat_match_perc
                known_player_max_match_name = basic_deck['name']

        print('highest match for opponent deck name ' + opponent_max_match_name + ' with a match perc of ' + str(opponent_max_match_perc))
        print('highest match for pat deck name ' + known_player_max_match_name + ' with a match perc of ' + str(known_player_max_match_perc))


        print('known player played these cards ' + str(known_player_cards_played_names))
        print('opponent player played these cards ' + str(opponent_player_cards_played_names))

        print('known player mulliganned these cards ' + str(known_player_cards_mulliganned_names))
        print('opponent player mulliganned these cards ' + str(opponent_player_cards_mulliganned_names))

        print('known player kept these cards ' + str(known_player_cards_kept_names))
        print('opponent player kept these cards ' + str(opponent_player_cards_kept_names))

        known_player_pre_mulligan_hand_names = known_player_cards_mulliganned_names + known_player_cards_kept_names
        opponent_player_pre_mulligan_hand_names = opponent_player_cards_mulliganned_names + opponent_player_cards_kept_names

        # for mongodb, it can't take arrays for values
        # also it can't take nulls so replace "" with "none"

        game_json = {
            "turns_taken": final_turn,
            "known_player": known_player,
            "opponent_player": opponent_player,
            "coin_holder": coin_holder,
            "winner": winner,
            "date_played": new_date_string,
            "_id": replay_name,
            "known_player_class": known_player_class,
            "opponent_player_class": opponent_player_class,
            "known_player_archetype": known_player_max_match_name,
            "opponent_player_archetype": opponent_max_match_name,
            "known_player_archetype_match_perc": str(known_player_max_match_perc),
            "opponent_player_archetype_match_perc": str(opponent_max_match_perc),
            "known_player_cards_mulliganned": convert_list_to_string(known_player_cards_mulliganned_names),
            "opponent_player_cards_mulliganned": convert_list_to_string(opponent_player_cards_mulliganned_names),
            "known_player_cards_kept": convert_list_to_string(known_player_cards_kept_names),
            "opponent_player_cards_kept": convert_list_to_string(opponent_player_cards_kept_names),
            "known_player_premulligan_cards": convert_list_to_string(known_player_pre_mulligan_hand_names),
            "opponent_player_premulligan_cards": convert_list_to_string(opponent_player_pre_mulligan_hand_names),
            "known_player_decklist": convert_list_to_string(known_player_cards_played_names),
            "opponent_player_decklist": convert_list_to_string(opponent_player_cards_played_names),
        }

        print('game JSON below')
        print(game_json)

        with open('test_replay_db_entry.json', 'w', encoding='utf-8') as f:
            json.dump(game_json, f, ensure_ascii=False, indent=4)
