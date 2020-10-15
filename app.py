#Flask Project
import os
from collections import defaultdict
from flask import Flask
from flask import render_template
from flask import request
from flask import flash
from flask import redirect
from flask import url_for
from flask import session
from flask import send_from_directory
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc

from datetime import datetime
from datetime import timedelta
from pytz import utc

# Python file containing credentials
import secrets

# LOR Bravery Backend
import lor_bravery

application = Flask(__name__)
application.config.from_object(secrets.APP_SETTINGS)
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(application)

from models import *


@application.route('/', methods=['GET'])
def home_page():
    '''
    Main LOR Bravery Page, generate new deck with selected regions
    (or pick two random regions) and store the results with a timestamp into MongoDB.
    '''
    client_IP = ''
    # retrieve client IP (through SSL proxy if necessary)
    if request.headers.getlist("X-Forwarded-For"):
        client_IP = request.headers.getlist("X-Forwarded-For")[0]
    else:
        client_IP = request.remote_addr

    # create correctly labeled utcnow object (for correct timezone conversion)
    utc_now = datetime.utcnow()
    utc_now = utc_now.replace(tzinfo=utc)

    # if regions are not selected, generate two random regions to use
    selected_regions = []
    random_regions = True
    if 'regions' in request.args:
        selected_regions = request.args.getlist('regions')
        random_regions = False
    else:
        selected_regions = lor_bravery.pick_rand_n_regions(2, lor_bravery.ALL_REGIONS)
        random_regions = True

    # generate random deck with these regions and return formatted deck info
    deck = lor_bravery.generate_rand_deck(selected_regions)
    formatted_deck_info = lor_bravery.format_deck_info(deck)

    try:
        # store generated deck code with timestamp and IP into postgreSQL table
        deck_history_item = DeckHistory(deck_code = formatted_deck_info['deck_code'], ip_address=client_IP, time_stamp=utc_now)
        db.session.add(deck_history_item)
        db.session.commit()
        deck_count = db.session.query(DeckHistory).count()
    except SQLAlchemyError:
        deck_count = "?"

    return render_template('index.html', selected_regions=selected_regions, random_regions=random_regions,
                            formatted_deck_info=formatted_deck_info, deck_count=deck_count, regions=lor_bravery.ALL_REGIONS)


@application.route('/about', methods=['GET'])
def about_page():
    '''
    About LOR Bravery Page
    '''
    return render_template('about.html')


@application.route('/riot.txt')
def riot_txt():
    '''
    Host riot.txt for verification
    '''
    return send_from_directory('static', 'riot.txt')


@application.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


if __name__ == '__main__':
    application.run(host='0.0.0.0', port=5000, debug=True)
