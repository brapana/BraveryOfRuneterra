# Bravery Of Runeterra

Riot Games-approved website built in Python3, Flask, Bootstrap4, and JavaScript that generates valid decks for use in their collectible card game Legends of Runeterra. Also utilizes the [LoR Deck Codes Python library](https://github.com/Rafalonso/LoRDeckCodesPython) to convert the generated deck into a code readable by the Legends of Runeterra game client. Allows users to filter cards by type and view deck contents as they appear in-game. This code is hosted at https://braveryofruneterra.com/ via AWS EC2, Elastic Beanstalk, and RDS.

# Features
![Bravery of Runeterra Home Page](https://i.imgur.com/TOTi6yK.png "Bravery of Runeterra Home Page")

Visitors are initially shown a deck created using two randomly-selected regions, and may click the "shuffle" button to generate a new deck. Users may also click on the region icons in order to highlight up to two regions from which newly generated decks will be comprised of. Each generated deck allows users to easily click to copy the deck code and displays each card in the deck using assets from the set bundles used here: https://developer.riotgames.com/docs/lor. Hovering the main deck cover block also displays the number of different card archetypes contained within the deck.  

# How it Works

The randomization aspect of the calculation is done by first either randomly picking a subset of two regions, or utilizing the region(s) as chosen by the user. Once the region subset chosen, Bravery of Runeterra uses the data present in the set bundle json files (eg. set3-en_us.json) to generate 40 random card codes (unique IDs that identify a card) adhering to the requirements of a valid deck (max of 6 champions, 3 copies of each card, two regions). Each card code is then encoded into a singular deck code by the LoR Deck Codes Python library and made available to the user. Each individual card code is also saved into lists sorted upon their type and mana cost, which are displayed to the user with their respective card images. A history of each deck code generated is also saved to a PostgreSQL database (the current size of the database is shown as the current deck number). 

# Usage

Create a file named secrets.py at the root of the project folder (alongside app.py) containing the following lines:

```
DATABASE_URL="postgresql://db_username:db_password@ip_address/db_name"
APP_SETTINGS="config.{TestingConfig|DevelopmentConfig|StagingConfig|ProductionConfig}"
SECRET_KEY="Your Secret Key Here" (set a key unique to you)
```

Install Dependencies:

```
pip3 install -r requirements.txt
```

Run Server:

```
python3 app.py
```

# Note

Deck counting/database functionality is temporarily disabled in order to save on AWS fees, code is still present in comments.

Files such as card images and set bundles are not included in this distribution as they contain property owned by Riot Games.

Bravery of Runeterra isn't endorsed by Riot Games and doesn't reflect the views or opinions of Riot Games or anyone officially involved in producing or managing Riot Games properties. Riot Games, and all associated properties are trademarks or registered trademarks of Riot Games, Inc. Bravery of Runeterra is also not associated with Ultimate Bravery or any other "bravery"-type website or application.
