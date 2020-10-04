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
from flask_pymongo import PyMongo

from datetime import datetime
from datetime import timedelta
from pytz import utc

# Python file containing credentials
import secrets

# LOR Bravery Backend
import lor_bravery

application = Flask(__name__)
application.config.from_object(secrets.APP_SETTINGS)
mongo = PyMongo(application)


@application.route('/', methods=['GET', 'POST'])
def home_page():
    '''
    Main LOR Bravery Page
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


    deck = lor_bravery.generate_rand_deck(lor_bravery.pick_rand_n_regions(2, lor_bravery.ALL_REGIONS))

    formatted_deck_info = lor_bravery.format_deck_info(deck)


    # store generated deck with timestamp and IP into mongo db
    deck_history = mongo.db['deck_history']
    deck_history.insert_one({'ip_address': client_IP, 'time_stamp': utc_now, 'deck_code': formatted_deck_info['deck_code']})
    deck_count = deck_history.count()


    return render_template('index.html', formatted_deck_info=formatted_deck_info, deck_count=deck_count)


@application.route('/about', methods=['GET'])
def about_page():
    '''
    About LOR Bravery Page
    '''

    return render_template('about.html')


@application.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


if __name__ == '__main__':
    application.run(host='0.0.0.0', port=5000, debug=True)
