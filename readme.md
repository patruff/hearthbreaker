Hearthbreaker
=============
A Hearthstone Simulator
-----------------------

**Hearthbreaker is no longer under active development.  If you're interested in Hearthstone Simulation, check out the projects
at [https://hearthsim.info/](https://hearthsim.info/)**

Hearthbreaker is an open source Hearthstone simulator for the purposes of machine learning and
data mining of Blizzard's [Hearthstone: Heroes of WarCraft](http://battle.net/hearthstone).  It implements every 
card in the game.  Every attempts has been made to mimic Hearthstone precisely, including edge cases and bugs.
The results of playing simulated games can be used to determine cards which work well together and cards which do not.  
Hearthbreaker is not designed to allow player to play Hearthstone against each other, nor is it designed to play against
human opponents within Hearthstone itself.  It is designed to be used as a library for analysis.

 * Documentation (In Progress) [http://danielyule.github.io/hearthbreaker/](http://danielyule.github.io/hearthbreaker/)
 * Travis CI Build Status: [![Build Status](https://travis-ci.org/danielyule/hearthbreaker.svg?branch=master)](https://travis-ci.org/danielyule/hearthbreaker)
 * Coveralls Code Coverage: [![Coverage Status](https://coveralls.io/repos/danielyule/hearthbreaker/badge.png?branch=master)](https://coveralls.io/r/danielyule/hearthbreaker?branch=master)
 * Developer Mailing List: [Google Group](https://groups.google.com/forum/#!forum/hearthstone-simulator-dev)

Usage
-----

Hearthbreaker is compatible with [Python](https://www.python.org/) 3.2+ and [PyPy3](http://pypy.org/) 2.3+ on any
operating system that supports them.

### Pat edits

So you can grab your replays from HSReplays.net by going to the main page (My Replays) and then right click and "Inspect" the HTML so you're looking at the most recent 100 replays (I think this is all it stores). Grab those xml by first getting the list of XMLs (you can just COPY+PASTE the HTML and then scrape it).
So for example, I'll COPY+PASTE the HTML (you can right click at the highest level and Edit HTML, then just copy all of that) and then copy that HTML with the 100 replays into the main project folder.
From there you just run ```python download_latest_hsnet_replays.py``` to scrape the replay IDs. 
Then with the replay IDs I can use Selenium to grab the XMLs by running ```python download_replay_selenium.py``` which works
off of the file created by the other script. One troubleshooting step is that I was getting an error from my PyCharm IDE
(something like a unicode error, so just go into File->Settings->Editor and make sure the Encodings for the Project 
and globally are just UTF-8).

### Pat edits 2

So after fixing the bug that caused Selenium to crash, the scripts are getting the replays pretty well. The next step
is to take the replays (in XML format) and to scrape the name of the opponent and add them to a database. I'm thinking of
putting the database into a docker container (it might be easier to work with). So you can just create the database in a container
and then from there see the most recent data (it'll just populate whenever the container is spun up).

* need docker
* need to get a simple database (can use MongoDB noSQL DB)
* then need to scrape the XML and convert to JSON
* then need to put the scraped XML into the database

this looks promising https://ishmeet1995.medium.com/how-to-create-restful-crud-api-with-python-flask-mongodb-and-docker-8f6ccb73c5bc

so got their code and also got Docker
the database is working (I downloaded that tool MongoDB Compass and I can use it in read-only mode)
to connect use the address mongodb://localhost:5000

So we have a database!

Next need to scrap the XML and convert to JSON

Something like

Fixed those original Docker files (they had errors), but to get the API working, just run ```docker-compose build```
And then ```docker-compose up``` from the /docker folder

### Pat edits 3

So got the XML parsing working to pick up my cards and the opponent's cards. Right now need to go ahead and get more
replays since I only have 100 (well, should have 400 after this). So got the HTML (manually), ran download_latest_hsnet_replays.net,
then will run download_replay_selenium.py until I have all 400 replays in the folder.

### Pat edits 4

Hearthstone XML notes (how replays work)

Example matchup is me as Miracle Rogue V. Chris6 as a Druid
Replay is: 
https://hsreplay.net/replay/4EUDoPi8WskTsCDJGiLm6G

XML seems to track the game turn by turn

Me: 

First 3 cards (mulligan choice)

Shiv
Backstab
Preparation

	I decided to put mulligan Backstab and Preparation

Next card from the XML is…

Deadly poison (so it’s still counting my deck, I mulliganed 2 cards and this is the first new card)

Shadowstep (2nd new card from mulligan)

Since I’m first, I draw…

Gadgetzan Auctioneer (my first drawn card on turn 1 with 1 mana)


Opponent: now it’s his turn and I see NOTHING in the XML (since has hasn’t played anything yet as a druid with 1 mana)


Me (turn 2): The XML NOW has my first drawn card (when I have 2 mana)

Azure Drake (card 7 in the XML)

CS2_082_H1 is next, basically, the rogue hero power was used (my turn after he passes his 1 mana turn)

Opponent (turn 2): So then he uses his own hero power as Druid, CS2_017o

Me (turn 3): Then shadowstep is drawn
	VAN_EX1_144

I hit with the weapon (it doesn’t show up in the XML again)

Then I see SI:7 agent in the XML

VAN_EX1_134


This is after I had played Shiv from my hand which doesn’t show up in the XML, just the card drawn (this is my turn 3, I have 1 mana after playing Shiv)

Opponent (turn 3): His turn 3 he hero powers again (this shows up) as before CS2_017o


Me (turn 4): I draw Leeroy on my turn 4

VAN_EX1_116

Then I use my hero power again

CS2_082_H1

(that ends my turn 4)

Opponent (turn 4): Now his turn with 4 mana, he plays a Yeti

VAN_CS2_182

Me (turn 5): Now it’s my turn 5, I draw a cold blood

VAN_CS2_073

Then I play a Deadly Poison

CS2_074e

Then I play an SI:7 Agent 

VAN_EX1_134


 At this point I’m wondering if I can determine MY plays by looking to see…

So I can’t see HIS mulligan (without some more digging) but I can infer MY mulligan pretty easily (basically


So for specific cards it will first list which entity is playing them
For example, in this replay, the Game is entity 1, I as a player am entity 2, and my opponent is entity 3

<TagChange entity="2" tag="467" value="1"/>
<ShowEntity entity="19" cardID="VAN_EX1_144">

So you can see TagChange PRIOR to ShowEntity is showing entity 2 (meaning I was the one who drew the card)



Similarly for the opponent when he plays the Yeti

<TagChange entity="3" tag="25" value="4"/>
<TagChange entity="3" tag="418" value="8"/>
<TagChange entity="3" tag="269" value="1"/>
<TagChange entity="3" tag="317" value="1"/>
<TagChange entity="75" tag="263" value="0"/>
<ShowEntity entity="75" cardID="VAN_CS2_182">


You can see entity = 3 but not entity = 2 meaning he played the Yeti



GAME 2 WHERE I GO 2nd

I checked another replay where I go 2nd and sure enough I am entity id=3 in that one and not entity id = 2

https://hsreplay.net/replay/GPFAbQzkavyvmYtGJPDrbi


So can put in if entity id = 2, they are the “first player”

In the other replay when I go 2nd, and show up as entity id=3, you can see after all my mulliganing the coin

<TagChange entity="3" tag="272" value="1"/>
<FullEntity id="68" cardID="GAME_005">


Interestingly in that game my starting hand is

Coldblood, Preparation, Backstab, Preparation

I mulliganed Coldblood and Backstab

So the first card AFTER the coin (which I guess is given AFTER the mulligan) is…

Eviscerate, the first card drawn after mulliganing


This means that IF player id is 3 we can see the original 4 cards AND those that were mulliganed (well, we can see the cards that were drawn anyway AFTER the mulligan)

So we can at least get a count of the cards mulliganed

These new cards must replace old cards too so if you mulligan all 4 cards, you’d know that all 4 were mulliganed

Might need more digging for mulligan choices

OH I KNOW

Could infer the mulliganed card

Keep a list of

	Drawn cards (can know this since each turn you draw a card)

	Then look at “starting cards” (if player is second player, then starting cards are the first 4 cards)


And EVENTUALLY we look at cards drawn V. cards played (

	Entity
	Turn?


So weird thing is once a card is drawn you WILL NOT see it (unless you track it by entity)

So new thing would be to track entities and go from there


For example, in the game I played the warrior above, the last 5 cards played look like whirlwind (he drew it and played it same turn), execute, execute, Sunwalker, Kork’ron Elite

Even though I played Fan of Knives and Azure Drake in-between

I think what I need to do is to assign cardID to an entity in the game, that way I can track things

https://github.com/HearthSim/python-hearthstone/blob/master/hearthstone/enums.py and other things are there

Basically, after the player elements are loaded, the Deck element of the known player (me (Pat)) is then loaded with all of the cardIDs associated with the cards

Then there are 63

Game
Entity 1

Player 1
Entity 2

Player 2
Entity 3

Deck 1 (the 1st player’s deck?)
3-33?

Deck 2 (the 2nd player’s deck?)
33-63?

Life total?
Entity 64

Hero Power Player 1 (confirmed, Warrior hero power)
Entity 65

Hero Power Player 2 (confirmed, Rogue hero power)
Entity 66

Rogue Weapon (separate from hero power)
Entity 67

The coin
Entity 68

Then the game starts

First entity with a cardID is cold blood (entity 59)
This is the first card in my hand (pre-mulligan), I decided to mulligan it



Okay I’m dumb, for mulligans we can see them clearly in this early block (found out that tag 305 is the mulligan state)

<Block entity="1" type="5" effectCardId="System.Collections.Generic.List`1[System.String]" ts="2021-12-30T11:01:48.490023-05:00">
<TagChange entity="2" tag="305" value="1"/>
<Choices entity="2" id="1" taskList="4" type="1" min="0" max="3" source="1" ts="2021-12-30T11:01:48.518025-05:00">
<Choice index="0" entity="30"/>
<Choice index="1" entity="33"/>
<Choice index="2" entity="20"/>
</Choices>
<TagChange entity="3" tag="305" value="1"/>
<Choices entity="3" id="2" taskList="5" type="1" min="0" max="5" source="1" ts="2021-12-30T11:01:48.584023-05:00">
<Choice index="0" entity="59"/>
<Choice index="1" entity="42"/>
<Choice index="2" entity="36"/>
<Choice index="3" entity="60"/>
<Choice index="4" entity="68"/>
</Choices>
<ChosenEntities entity="2" id="1" ts="2021-12-30T11:02:18.362974-05:00"/>
<SendChoices id="2" type="1" ts="2021-12-30T11:02:50.202336-05:00">
<Choice index="0" entity="42"/>
<Choice index="1" entity="60"/>
</SendChoices>
<ChosenEntities entity="3" id="2" ts="2021-12-30T11:02:50.471395-05:00">
<Choice index="0" entity="42"/>
<Choice index="1" entity="60"/>
</ChosenEntities>
</Block>


 dumb, for mulligans we can see them clearly in this early block (found out that tag 305 is the mulligan st
This is the game with me going 2nd as rogue (entity 3), you can see I have 5 choices (bug, probably means 4 cards + the coin that you HAVE to keep)

Whereas the warrior opponent only has the mulligan decision for 3 cards (it also shows that his entities are the 3-33 and my deck falls in the 33-63 range, I’m guessing 68 is the coin)

It also shows that I chose to keep (ChosenEntities) my two preparation cards and discard the coldblood (entity 59) and backstab (entity 36)


I GET IT NOW!!

The decks for each player are just arrays that are filled in later. Basically each card is given an entity at random. So for example, in my Rogue example I have 2 preparations that I keep, but they were given random entity ids at the beginning (regardless of my deck), so they were assigned id 42 and 60 respectively. It works the same for the warrior I played. He decided to keep NOTHING, so for entity 2 you see he doesn’t have any Chosen Entities (meaning that he mulliganned entity 30, entity 33, and entity 20). So duplicate cards still get different entity ids, that’s one thing. Another is that in the game I EVENTUALLY saw him play the 3 cards that he mulliganed. So I could eventually match cardIDs to the cards that he mulliganned.

So for a given game I can see

Opponent cards mulliganned

Entity IDs (can see all of these)
Card IDs (can see a subset of these later, or could be the whole thing)

My cards muligganned

(it shows my cards at the beginning, so I can easily find this out)



For number of turns this is tracked with tag 271, and it increments each turn (so counts each players’ turns). 

<TagChange entity="1" tag="271" value="21"/>
<TagChange entity="2" tag="271" value="21"/>
<TagChange entity="3" tag="271" value="21"/>
<TagChange entity="64" tag="271" value="21"/>
<TagChange entity="65" tag="271" value="21"/>
<TagChange entity="66" tag="271" value="21"/>
<TagChange entity="67" tag="271" value="21"/>
<TagChange entity="144" tag="271" value="3"/>
<TagChange entity="22" tag="271" value="2"/>
<TagChange entity="43" tag="271" value="1"/>


Can also see the final player to act

Like, final card played by will be there (not clear what HP total is though)

Can assume for now final actor is the winner
	So for that game, the final action was playing Kork’ron elite, entity 2 played it, so that player won (if entity 3 had played a card and the game ended you could assume they won)

	This 

Actually can see concede as Game (entity 1), Playstate (tag 17) being set to CONCEDE (value 8) (again this comes from https://github.com/HearthSim/python-hearthstone/blob/master/hearthstone/enums.py)

And in the actual game, where I concede, you can see

<TagChange entity="3" tag="17" value="8"/>


So it looks like certain cards are missing like Azure Drake

Ah, I see, some cards are just buried in another Block inside of the original Block 

<Block entity="36" type="7" effectCardId="System.Collections.Generic.List`1[System.String]" effectIndex="0" target="31" ts="2021-12-30T11:05:12.014448-05:00">
			<TagChange entity="3" tag="269" value="2"/>
			<TagChange entity="3" tag="430" value="1"/>
			<TagChange entity="36" tag="267" value="31"/>
			<TagChange entity="36" tag="261" value="1"/>
			<TagChange entity="36" tag="1068" value="1"/>
			<TagChange entity="36" tag="1068" value="0"/>
			<TagChange entity="58" tag="263" value="7"/>
			<TagChange entity="53" tag="263" value="6"/>
			<TagChange entity="51" tag="263" value="5"/>
			<TagChange entity="36" tag="1037" value="0"/>
			<TagChange entity="36" tag="263" value="0"/>
			<TagChange entity="36" tag="1556" value="1"/>
			<TagChange entity="36" tag="49" value="1"/>
			<MetaData meta="20" data="3000" infoCount="1">
				<Info index="0" entity="36"/>
			</MetaData>
			<Block entity="55" type="5" effectCardId="System.Collections.Generic.List`1[System.String]" effectIndex="0" triggerKeyword="32" ts="2021-12-30T11:05:12.014448-05:00">
				<TagChange entity="3" tag="2166" value="43"/>
				<TagChange entity="3" tag="467" value="1"/>
				<ShowEntity entity="43" cardID="VAN_EX1_284">
					<Tag tag="50" value="2"/>


Number of cards BEFORE checking 1 more level down

inside ShowEntity, before tag ownership, card looks like VAN_CS2_073
inside ShowEntity, before tag ownership, card looks like VAN_EX1_145
inside ShowEntity, before tag ownership, card looks like VAN_CS2_072
inside ShowEntity, before tag ownership, card looks like VAN_EX1_145
inside ShowEntity, before tag ownership, card looks like VAN_EX1_124
inside ShowEntity, before tag ownership, card looks like VAN_EX1_128
inside ShowEntity, before tag ownership, card looks like VAN_EX1_278
inside ShowEntity, before tag ownership, card looks like VAN_CS2_072
inside ShowEntity, before tag ownership, card looks like VAN_CS2_074
inside ShowEntity, before tag ownership, card looks like VAN_EX1_398
inside ShowEntity, before tag ownership, card looks like VAN_EX1_128
inside ShowEntity, before tag ownership, card looks like VAN_EX1_096
inside ShowEntity, before tag ownership, card looks like VAN_EX1_604
inside ShowEntity, before tag ownership, card looks like VAN_CS2_072
inside ShowEntity, before tag ownership, card looks like VAN_EX1_012
inside ShowEntity, before tag ownership, card looks like VAN_EX1_604
inside ShowEntity, before tag ownership, card looks like VAN_EX1_603
inside ShowEntity, before tag ownership, card looks like VAN_CS2_233
inside ShowEntity, before tag ownership, card looks like VAN_EX1_007
inside ShowEntity, before tag ownership, card looks like VAN_EX1_278
inside ShowEntity, before tag ownership, card looks like VAN_EX1_603
inside ShowEntity, before tag ownership, card looks like VAN_EX1_407
inside ShowEntity, before tag ownership, card looks like VAN_EX1_116
inside ShowEntity, before tag ownership, card looks like VAN_EX1_606
inside ShowEntity, before tag ownership, card looks like VAN_EX1_410
inside ShowEntity, before tag ownership, card looks like VAN_EX1_007
inside ShowEntity, before tag ownership, card looks like VAN_EX1_134
inside ShowEntity, before tag ownership, card looks like VAN_EX1_400
inside ShowEntity, before tag ownership, card looks like VAN_EX1_032
inside ShowEntity, before tag ownership, card looks like VAN_CS2_108
inside ShowEntity, before tag ownership, card looks like VAN_CS2_108
inside ShowEntity, before tag ownership, card looks like VAN_NEW1_011


WAY more

inside ShowEntity, before tag ownership, card looks like VAN_CS2_073
inside ShowEntity, before tag ownership, card looks like VAN_EX1_145
inside ShowEntity, before tag ownership, card looks like VAN_CS2_072
inside ShowEntity, before tag ownership, card looks like VAN_EX1_145
inside ShowEntity, before tag ownership, card looks like VAN_EX1_124
inside ShowEntity, before tag ownership, card looks like VAN_EX1_128
inside ShowEntity, before tag ownership, card looks like VAN_EX1_278
inside ShowEntity, before tag ownership, card looks like VAN_CS2_072
inside ShowEntity, before tag ownership, card looks like VAN_EX1_096
inside ShowEntity, before tag ownership, card looks like VAN_CS2_074
inside ShowEntity, before tag ownership, card looks like VAN_EX1_398
inside ShowEntity, before tag ownership, card looks like VAN_EX1_128
inside ShowEntity, before tag ownership, card looks like VAN_EX1_096
inside ShowEntity, before tag ownership, card looks like VAN_EX1_604
inside ShowEntity, before tag ownership, card looks like EX1_604o
inside ShowEntity, before tag ownership, card looks like VAN_CS2_072
inside ShowEntity, before tag ownership, card looks like VAN_EX1_012
inside ShowEntity, before tag ownership, card looks like VAN_EX1_604
inside ShowEntity, before tag ownership, card looks like VAN_EX1_603
inside ShowEntity, before tag ownership, card looks like EX1_603e
inside ShowEntity, before tag ownership, card looks like VAN_EX1_095
inside ShowEntity, before tag ownership, card looks like VAN_CS2_233
inside ShowEntity, before tag ownership, card looks like VAN_EX1_284
inside ShowEntity, before tag ownership, card looks like VAN_EX1_581
inside ShowEntity, before tag ownership, card looks like VAN_EX1_145o
inside ShowEntity, before tag ownership, card looks like VAN_EX1_145e
inside ShowEntity, before tag ownership, card looks like VAN_EX1_145e
inside ShowEntity, before tag ownership, card looks like VAN_EX1_145e
inside ShowEntity, before tag ownership, card looks like VAN_EX1_145e
inside ShowEntity, before tag ownership, card looks like VAN_EX1_145e
inside ShowEntity, before tag ownership, card looks like VAN_EX1_145e
inside ShowEntity, before tag ownership, card looks like VAN_EX1_145e
inside ShowEntity, before tag ownership, card looks like VAN_EX1_129
inside ShowEntity, before tag ownership, card looks like CS2_074e
inside ShowEntity, before tag ownership, card looks like VAN_CS2_073
inside ShowEntity, before tag ownership, card looks like VAN_EX1_145o
inside ShowEntity, before tag ownership, card looks like VAN_EX1_145e
inside ShowEntity, before tag ownership, card looks like VAN_EX1_145e
inside ShowEntity, before tag ownership, card looks like VAN_EX1_145e
inside ShowEntity, before tag ownership, card looks like VAN_EX1_145e
inside ShowEntity, before tag ownership, card looks like VAN_EX1_145e
inside ShowEntity, before tag ownership, card looks like VAN_EX1_145e
inside ShowEntity, before tag ownership, card looks like VAN_EX1_145e
inside ShowEntity, before tag ownership, card looks like VAN_EX1_144
inside ShowEntity, before tag ownership, card looks like VAN_EX1_095
inside ShowEntity, before tag ownership, card looks like VAN_CS2_073
inside ShowEntity, before tag ownership, card looks like CS2_073e2
inside ShowEntity, before tag ownership, card looks like VAN_CS2_117
inside ShowEntity, before tag ownership, card looks like EX1_128e
inside ShowEntity, before tag ownership, card looks like VAN_EX1_007
inside ShowEntity, before tag ownership, card looks like VAN_EX1_278
inside ShowEntity, before tag ownership, card looks like VAN_EX1_613
inside ShowEntity, before tag ownership, card looks like VAN_CS2_074
inside ShowEntity, before tag ownership, card looks like VAN_EX1_124
inside ShowEntity, before tag ownership, card looks like CS2_073e2
inside ShowEntity, before tag ownership, card looks like VAN_EX1_144
inside ShowEntity, before tag ownership, card looks like VAN_EX1_129
inside ShowEntity, before tag ownership, card looks like EX1_128e
inside ShowEntity, before tag ownership, card looks like VAN_EX1_603
inside ShowEntity, before tag ownership, card looks like EX1_603e
inside ShowEntity, before tag ownership, card looks like VAN_EX1_407
inside ShowEntity, before tag ownership, card looks like VAN_EX1_116
inside ShowEntity, before tag ownership, card looks like CS2_074e
inside ShowEntity, before tag ownership, card looks like EX1_613e
inside ShowEntity, before tag ownership, card looks like VAN_EX1_606
inside ShowEntity, before tag ownership, card looks like VAN_EX1_410
inside ShowEntity, before tag ownership, card looks like VAN_EX1_007
inside ShowEntity, before tag ownership, card looks like VAN_EX1_134
inside ShowEntity, before tag ownership, card looks like GBL_002e
inside ShowEntity, before tag ownership, card looks like VAN_EX1_400
inside ShowEntity, before tag ownership, card looks like VAN_EX1_032
inside ShowEntity, before tag ownership, card looks like VAN_CS2_108
inside ShowEntity, before tag ownership, card looks like VAN_CS2_108
inside ShowEntity, before tag ownership, card looks like VAN_NEW1_011

But also some EX1 or GBL…

It seems like the order of play is screwed up, this method gets more cards, but there are things like “cost-2” as a cardID which is dumb/weird. Different effects are being counted here. VanCleef’s Vengeance (the stat bonus VanCleaf has) or “Whipped Into Shape” (the stats you get after playing berserk)

So certain things are not “cards” but effects. Taking out non “VAN” may solve this

Yes, only keep cards that start with “VAN” in their cardID has fixed the problem (no more weird effect “cards”)


### Console Application

![Console Screenshot](http://danielyule.github.io/hearthbreaker/_static/console_screenshot.png)

There is a basic console that you can use for playing against a bot.  There are two bots to choose from: a random bot
that plays completely randomly or a trading bot which tries to trade efficiently with your minions.

Start the console with ``python text_runner.py deck1.hsdeck deck2.hsdeck``.  The two deck files are
in cockatrice format, with a card name in English on each line, preceded by a number to specify how many.  For example:

    2 Goldshire Footman
    2 Murloc Raider
    2 Bloodfen Raptor
    2 Frostwolf Grunt
    2 River Crocolisk
    2 Ironfur Grizzly
    2 Magma Rager
    2 Silverback Patriarch
    2 Chillwind Yeti
    2 Oasis Snapjaw
    2 Sen'jin Shieldmasta
    2 Booty Bay Bodyguard
    2 Fen Creeper
    2 Boulderfist Ogre
    2 War Golem
    
The character class is inferred from the cards present, or defaults to mage.

The console application requires ncurses, which should be included with python on *nix and mac systems, but if you are 
on windows, you must download it from 
[http://www.lfd.uci.edu/~gohlke/pythonlibs/#curses](http://www.lfd.uci.edu/~gohlke/pythonlibs/#curses)

*Note:* Curses is not available for PyPy


### Unit Tests
The tests are located in the [`tests`](tests) package.

All tests can be run with the following command: `python -m unittest discover -s tests -p *_tests.py`

For Python 3.2 and PyPy3, the unit tests are dependent on the [mock package](https://pypi.python.org/pypi/mock).

Progress
--------

All Collectible cards up to The Grand Tournament have been implemented.  There is no plan to expand on the list
of cards beyond that.
The engine is complete, and can be used to simulate games.  The game state can be copied, or serialized to JSON.
Replay functionality is included as well.  Furthermore, minions and weapons can be expressed either in python or
via a JSON declaration.

For an overview of upcoming work, see [the wiki](https://github.com/danielyule/hearthbreaker/wiki/)

Structure
---------
Almost all of the game logic is found in [hearthbreaker.game_objects](hearthbreker/game_objects.py).  The game functions
largely on a tag based system.  See [the wiki](https://github.com/danielyule/hearthbreaker/wiki/Tag-Format) for more
details.

The game is made up of players, each of which has a hand of cards, a hero, secrets and minions.  Decisions are made
by agents, which can either by computer controlled or human controlled.  The system is callback based, in that
when it is time to make a decision, the game will request the decision from the agents, rather than the agents
dictating how the game is run.

The cards themselves are each a class, and can be found in the [hearthbreaker/cards](hearthbreaker/cards) directory, 
organized by type (spell/minion/secret/weapon) and by class.

The project defines a number of interesting formats, which are described 
[on the wiki](https://github.com/danielyule/hearthbreaker/wiki/Formats)

Contributing
------------

To contribute, simply fork the repository, make changes and submit a pull request.

All pull requests which implement new cards must also include a unit test for those cards.  In the case where the card
 has no side effects aside from playing the minion, tests should include another card's effects on it.

All pull requests will be automatically verified through 
[travis-ci.org](https://travis-ci.org/danielyule/hearthbreaker), and a coverage report generated through
 [coveralls.io](https://coveralls.io/r/danielyule/hearthbreaker)

New ideas, and upcoming features are described [on the wiki](https://github.com/danielyule/hearthbreaker/wiki/Roadmap).
Feel free to get involved with any or all of them.

Developers from this and other hearthstone simulation projectors can be found on IRC on freenode.net, channel #hearthsim.

For more specifics about contributing, see the 
[contributing page](http://danielyule.github.io/hearthbreaker/contributing.html), 
or join the [Developer Mailing List](https://groups.google.com/forum/#!forum/hearthstone-simulator-dev)

Related Projects
----------------

A collection of Hearthstone AI related projects can be found at [hs-ai.com](http://hs-ai.com)


### HearthSim
Hiroaki Oyaizu has created [HearthSim](https://github.com/oyachai/HearthSim), another Hearthstone simulator, written in Java
with a stronger focus on efficiency and AI modelling. It currently has fewer cards implemented, but has a much more
sophisticated AI.

### Focus
Raffy is working towards a Domain Specific Language (DSL) for Hearthstone Cards, written in JSON.  The cards are
completely defined, but the engine (called [Focus](http://fluiddruid.net/forum/viewtopic.php?f=24&t=4808)) is still in
progress.  These will allow for anyone to define new cards, by simply writing a JSON object to represent the card.

### Fireplace
Jerome Leclanche is attempting to reverse engineer the xml format for the cards associated with Hearthstone and build
an engine based on that.  It is planned to be a complete simulator, including all collectible and mission cards.
His work can be found on [Fireplace GitHub page](https://github.com/jleclanche/fireplace)

### Soot
[Soot](https://github.com/Mischanix/soot) is a slightly out of date Clojure implementation of all cards in Hearthstone.  It's not clear how well the 
implementations work.  It is interesting for its functional implementation of the cards.

### Hearthstone JSON

[Hearthstone JSON](http://hearthstonejson.com/) is a JSON file containing all cards in Hearthstone, extracted from the executable.  Hearthbreaker
uses this data to verify that its cards are implemented correctly

_Hearthstone: Heroes of WarCraft_ and _Blizzard_ are trademarks of Blizzard Entertainment.

