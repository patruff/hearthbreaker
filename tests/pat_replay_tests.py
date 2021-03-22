import json
import unittest
from io import StringIO
from os import listdir
from os.path import isdir
import re
import random

# trying to insert path
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

#import mymodule

from hearthbreaker.cards.heroes import Malfurion, Jaina
from hearthbreaker.engine import Game, Deck

from hearthbreaker.replay import Replay, record, playback
from hearthbreaker.agents.basic_agents import PredictableAgent, RandomAgent
from hearthbreaker.constants import CHARACTER_CLASS
from hearthbreaker.cards import *
import hearthbreaker.game_objects
from tests.agents.testing_agents import PlayAndAttackAgent, OneCardPlayingAgent
from tests.testing_utils import StackedDeck

# added this too
from hearthbreaker.engine import Game, Deck, card_lookup
from hearthbreaker.cards.heroes import hero_for_class

import ast

# trying TradeAgent
from hearthbreaker.agents.trade_agent import TradeAgent

class TestReplay(unittest.TestCase):

    def __compare_json(self, json1, json2):
        return json.loads(json1) == json.loads(json2)

    def test_reading_and_writing_compact(self):
        file_match = re.compile(r'.*\.rep')
        files = []

        def process_line(line):
            line = re.sub(r'\s*,\s*', ',', line)
            line = re.sub(r'\s*\(\s*', '(', line)
            line = re.sub(r'\s+\)', ')', line)
            return re.sub(r'(^\s+)|(\s*(;.*)?$)', '', line)

        def get_files_from(folder_name):
            for file in listdir(folder_name):
                if file_match.match(file):
                    files.append(folder_name + "/" + file)
                elif isdir(folder_name + "/" + file):
                    get_files_from(folder_name + "/" + file)

        get_files_from("tests/replays/compact")

        for rfile in files:
            replay = Replay()
            replay.read(rfile)
            output = StringIO()
            replay.write(output)
            f = open(rfile, 'r')
            file_string = f.read()
            f.close()
            file_string = "\n".join(map(process_line, file_string.split("\n")))

            self.assertEqual(output.getvalue(), file_string, "File '" + rfile + "' did not match")

    def test_compact_to_json_conversion(self):
        file_match = re.compile(r'.*\.rep')
        files = []

        def process_line(line):
            line = re.sub(r'\s*,\s*', ',', line)
            line = re.sub(r'\s*\(\s*', '(', line)
            line = re.sub(r'\s+\)', ')', line)
            return re.sub(r'(^\s+)|(\s*(;.*)?$)', '', line)

        def get_files_from(folder_name):
            for file in listdir(folder_name):
                if file_match.match(file):
                    files.append(folder_name + "/" + file)
                elif isdir(folder_name + "/" + file):
                    get_files_from(folder_name + "/" + file)

        get_files_from("tests/replays/compact")

        for rfile in files:
            replay = Replay()
            replay.read(rfile)
            json_output = StringIO()
            replay.write_json(json_output)
            json_replay = Replay()
            json_input = StringIO(json_output.getvalue())
            json_replay.read_json(json_input)
            output = StringIO()
            json_replay.write(output)
            f = open(rfile, 'r')
            file_string = f.read()
            f.close()
            file_string = "\n".join(map(process_line, file_string.split("\n")))

            self.assertEqual(output.getvalue(), file_string, "File '" + rfile + "' did not match")

    def load_deck(self, filename):
        cards = []
        character_class = CHARACTER_CLASS.MAGE

        with open(filename, "r") as deck_file:
            contents = deck_file.read()
            items = contents.splitlines()
            for line in items[0:]:
                parts = line.split(" ", 1)
                count = int(parts[0])
                for i in range(0, count):
                    card = card_lookup(parts[1])
                    if card.character_class != CHARACTER_CLASS.ALL:
                        character_class = card.character_class
                    cards.append(card)

        if len(cards) > 30:
            pass

        return Deck(cards, hero_for_class(character_class))

    def test_loading_game(self):
        game = playback(Replay("tests/replays/example.hsreplay"))

        game.start()

        self.assertEqual(game.current_player.deck.hero.name, "Malfurion Stormrage")
        self.assertEqual(game.other_player.deck.hero.name, "Jaina Proudmoore")

        self.assertEqual(game.current_player.hero.health, 29)
        self.assertTrue(game.current_player.hero.dead)

    def test_recording_game(self):
        self.maxDiff = None
        random.seed(9876)

        deck1name = "pat_freeze_mage.hsdeck"
        deck2name = "pat_midrange_druid.hsdeck"
        # testing custom decks
        # need to convert card names to the actual functions
        deck1 = self.load_deck(deck1name)
        deck2 = self.load_deck(deck2name)

        # below are what works
        #deck1 = hearthbreaker.engine.Deck([StonetuskBoar() for i in range(0, 30)], Jaina())
        #deck2 = hearthbreaker.engine.Deck([Naturalize() for i in range(0, 30)], Malfurion())

        # PredictableAgent() works, let's try TradeAgent()
        agent1 = TradeAgent()
        agent2 = TradeAgent()

        # agent1 = PredictableAgent()
        # agent2 = PredictableAgent()

        game = Game([deck1, deck2], [agent1, agent2])
        replay = record(game)
        game.start()
        output = StringIO()
        replay.write_json(output)


        with open('pat_replay_2.hsreplay', mode='w') as f:
            print(output.getvalue(), file=f)


        # testing something 2021_3_15

        # ast.literal_eval("{'muffin' : 'lolz', 'foo' : 'kitty'}")
        replay_json = ast.literal_eval(output.getvalue())

          # {
      #"character": {
       #  "minion": 2,
     #   "player": "p1"
      # },
      # "name": "attack",
     # "target": {
     #   "player": "p2"
     #  }
     #},
    # {
      # "name": "end"
    # }
   #]
   #}

        # last move is always "name": "end" since that's last action taken
        # so get the move before
        last_move = replay_json['moves'][-2]

        # it depends on the last move, we need to check for different situations
        # if last_move['character']:


        # END OF 2021_3_15 new stuff

        #with open('pat_replay.hsreplay', 'w') as f:
        #    json.dump(output, f)

        #obj = open('pat_replay.hsreplay', 'w')
        #obj.write(output)
        #obj.close

        #f = open("pat_stonetusk_innervate.hsreplay", 'r')
        #dif = self.__compare_json(output.getvalue(), f.read())
        #self.assertTrue(dif)
        #f.close()

    def test_option_replay(self):
        game = playback(Replay("tests/replays/stonetusk_power.hsreplay"))
        game.start()
        self.assertEqual(1, len(game.other_player.minions))
        panther = game.other_player.minions[0]
        self.assertEqual(panther.card.name, "Panther")
        self.assertEqual(panther.health, 3)
        self.assertEqual(panther.calculate_attack(), 4)
        self.assertEqual(panther.index, 0)

    def test_random_character_saving(self):
        deck1 = hearthbreaker.engine.Deck([RagnarosTheFirelord() for i in range(0, 30)], Jaina())
        deck2 = hearthbreaker.engine.Deck([StonetuskBoar() for i in range(0, 30)], Malfurion())
        agent1 = PlayAndAttackAgent()
        agent2 = OneCardPlayingAgent()
        random.seed(4879)
        game = Game([deck1, deck2], [agent1, agent2])
        replay = record(game)
        game.pre_game()
        for turn in range(0, 17):
            game.play_single_turn()

        output = StringIO()
        replay.write_json(output)
        random.seed(4879)
        new_game = playback(Replay(StringIO(output.getvalue())))
        new_game.pre_game()
        for turn in range(0, 17):
            new_game.play_single_turn()

        self.assertEqual(2, len(new_game.current_player.minions))
        self.assertEqual(30, new_game.other_player.hero.health)
        self.assertEqual(5, len(new_game.other_player.minions))

    def test_json_saving(self):
        self.maxDiff = 6000
        deck1 = hearthbreaker.engine.Deck([RagnarosTheFirelord() for i in range(0, 30)], Jaina())
        deck2 = hearthbreaker.engine.Deck([StonetuskBoar() for i in range(0, 30)], Malfurion())
        agent1 = PlayAndAttackAgent()
        agent2 = OneCardPlayingAgent()
        random.seed(4879)
        game = Game([deck1, deck2], [agent1, agent2])
        replay = record(game)
        game.pre_game()
        for turn in range(0, 17):
            game.play_single_turn()

        output = StringIO()
        replay.write_json(output)
        inp = StringIO(output.getvalue())
        new_replay = Replay()
        new_replay.read_json(inp)
        old_output = output.getvalue()
        other_output = StringIO()
        new_replay.write_json(other_output)
        self.assertEqual(other_output.getvalue(), old_output)

    # Due to bug #55 (thanks to dur3x)
    def test_deck_shortening(self):
        deck1 = Deck([RagnarosTheFirelord(), RagnarosTheFirelord(), RagnarosTheFirelord(), RagnarosTheFirelord(),
                      RagnarosTheFirelord(), RagnarosTheFirelord(), RagnarosTheFirelord(), RagnarosTheFirelord(),
                      RagnarosTheFirelord(), RagnarosTheFirelord(), RagnarosTheFirelord(), RagnarosTheFirelord(),
                      RagnarosTheFirelord(), RagnarosTheFirelord(), RagnarosTheFirelord(), RagnarosTheFirelord(),
                      RagnarosTheFirelord(), RagnarosTheFirelord(), RagnarosTheFirelord(), RagnarosTheFirelord(),
                      RagnarosTheFirelord(), RagnarosTheFirelord(), RagnarosTheFirelord(), RagnarosTheFirelord(),
                      RagnarosTheFirelord(), RagnarosTheFirelord(), RagnarosTheFirelord(), RagnarosTheFirelord(),
                      GoldshireFootman(), GoldshireFootman()], Malfurion())
        deck2 = StackedDeck([StonetuskBoar()], CHARACTER_CLASS.HUNTER)
        game = Game([deck1, deck2], [RandomAgent(), RandomAgent()])
        replay = record(game)
        game.start()
        replay.write(StringIO())

    def test_replay_validation(self):
        from jsonschema import validate
        file_match = re.compile(r'.*\.hsreplay')
        files = []

        def get_files_from(folder_name):
            for file in listdir(folder_name):
                if file_match.match(file):
                    files.append(folder_name + "/" + file)
                elif isdir(folder_name + "/" + file):
                    get_files_from(folder_name + "/" + file)
        with open("replay.schema.json", "r") as schema_file:
            schema = json.load(schema_file)
            get_files_from("tests/replays")
            for rfile in files:
                with open(rfile, "r") as replay_file:
                    replay_json = json.load(replay_file)
                    validate(replay_json, schema)

if __name__ == '__main__':
    TestReplay().test_recording_game()
