deck_file_list = ['pat_control_warrior.hsdeck', 'pat_face_hunter.hsdeck', 'pat_freeze_mage.hsdeck', 'pat_handlock.hsdeck',
                  'pat_healadin.hsdeck', 'pat_midrange_druid.hsdeck', 'pat_miracle_rogue.hsdeck', 'pat_sunshine_hunter.hsdeck',
                  'pat_zoolock.hsdeck']


def load_deck(filename):
    cards = []

    with open(filename, "r") as deck_file:
        contents = deck_file.read()
        items = contents.splitlines()
        for line in items[0:]:
            parts = line.split(" ", 1)
            count = int(parts[0])
            for i in range(0, count):
                card = parts[1]
                cards.append(card)

    return cards

# decks from this site
# https://www.hearthstonetopdecks.com/the-top-classic-decks-to-try-again-in-classic-mode/


def get_basic_decks():
    basic_deck_list = []

    for deck in deck_file_list:
        # remove "pat_" and ".hsdeck" from the name
        short_deck_name = deck[4:-7]
        new_deck_dict = {'name': short_deck_name, 'deck_list': load_deck(deck)}
        basic_deck_list.append(new_deck_dict)

    return basic_deck_list