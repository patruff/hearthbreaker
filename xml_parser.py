from lxml import etree
data_file = "blah"
root = etree.parse(data_file).getroot()

# for each game, get the players
# one is me, the other is my opponent
for game in root.findall('Game'):
    for entity in game.findall('Player'):
        print(entity.get("name"))
        print(entity.get("playerID"))

opponent_cards = []
# below gets a list of card IDs for the opponent (30 cards)
for game in root.findall('Game'):
    for entity in game.findall('Block'):
        for subentity in entity.findall('ShowEntity'):
            if not subentity.get('cardID').startswith('VAN'):
                continue
            else:
                print(subentity.get('cardID') + ' and count is ' + count)
            

            

# so need to find out which playerID is which
# in the example game the playerID is 2
# <ShowEntity entity="96" cardID="VAN_EX1_571">
# <Tag tag="50" value="2"/>

# so tag 50 is the controller, in this case the player
# so player 1 is represented by 1, player 2
playerID="2" is the value to get

deck = root.find('Deck')
instrument = instruments.findall('Instrument')
for grandchild in instrument:
    code, source = grandchild.find('Code'), grandchild.find('Source')
    print (code.text), (source.text)