# from app import db
# from datetime import datetime
#
# class DeckHistory(db.Model):
#     __tablename__ = 'DeckHistory'
#
#     deck_num = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     deck_code = db.Column(db.String())
#     ip_address = db.Column(db.String())
#     time_stamp = db.Column(db.DateTime(timezone=True))
#
#     def __init__(self, deck_code, ip_address, time_stamp):
#         self.deck_code = deck_code
#         self.ip_address = ip_address
#         self.time_stamp = time_stamp
#
#     def __repr__(self):
#         return '<View #{} from {} [{}] at {}>'.format(self.deck_num, self.deck_code,
#                                                 self.ip_address, self.time_stamp)
#
# db.create_all()
