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

Spent some more time looking into the XML parsing. There is a concept of turns, the XML basically loads up in chronological
order and so you can know which player is which, which cards were the starting cards, and which cards were mulliganned
(this will be a bit tricky, need to keep track of the original cards and the cards drawn and see the difference).

My rough notes on this are below:

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

