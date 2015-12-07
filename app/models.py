from app import db
from flask.ext.login import UserMixin


class User(UserMixin, db.Model, object):
    id = db.Column(db.Integer,
                   primary_key=True)
    social_id = db.Column(db.String(64),
                          nullable=False,
                          unique=True)
    nickname = db.Column(db.String(64),
                         nullable=False)
    email = db.Column(db.String(64),
                      nullable=True)
    settings = db.relationship('Settings',
                               backref='User',
                               lazy='dynamic')

    def __repr__(self):
        return __str__

    def __str__(self):
        return '<User %r>' % self.nickname

class Event(db.Model, object):
    id = db.Column(db.Integer,
                   primary_key=True)
    name = db.Column(db.String(1000),
                     nullable=False,
                     unique=True)
    description = db.Column(db.String(5000),
                            nullable=True)
    start_date = db.Column(db.Date,
                           nullable=False)
    end_date = db.Column(db.Date,
                         nullable=False)
    creation_date = db.Column(db.Date,
                              nullable=False)
    creator_id = db.Column(db.Integer,
                           db.ForeignKey('user.id'),
                           nullable=False)
    creator = db.relationship('User',
                              backref='CreatedEvents',
                              lazy='dynamic')
    status = db.Column(db.String,
                       nullable=False)  # TODO status jako enum

    def set_from_dict(self, dict):
        id = dict["id"]
        name = dict["name"]
        description = dict["description"]
        start_date = dict["start_date"]
        end_date = dict["end_date"]
        creation_date = dict["creation_date"]
        creator_id = dict["creator_id"]
        creator = dict["creator"]
        status = dict["status"]

    def __repr__(self):
        __str__()

    def __str__(self):
        print id
        print name
        print description
        print start_date
        print end_date
        print creation_date
        print creator
        print status


class TicketType(db.Model, object):
    id = db.Column(db.Integer,
                   primary_key=True)
    name = db.Column(db.String(1000),
                     nullable=False)
    description = db.Column(db.String(5000),
                            nullable=True)
    event_id = db.Column(db.Integer,
                         db.ForeignKey('event.id'),
                         nullable=False)
    event = db.relationship('Event',
                            backref='TicketTypes',
                            lazy='dynamic')
    cost = db.Column(db.Float,
                     nullable=False)

    def set_from_dict(self, dict):
        id = dict["id"]
        name = dict["name"]
        description = dict["description"]
        event_id = dict["event_id"]
        event = dict["event"]
        cost = dict["dict"]
        raise NotImplementedError('Not implemented!')


class Ticket(db.Model, object):
    id = db.Column(db.Integer,
                   primary_key=True)
    user = db.Column(db.Integer,
                     db.ForeignKey('user.id'),
                     nullable=False)
    ticket_type_id = db.Column(db.Integer,
                               db.ForeignKey('ticket_type.id'),
                               nullable=False)
    ticket_type = db.relationship('TicketType',
                                  backref='Tickets',
                                  lazy='dynamic')
    special_discount = db.Column(db.Floatm,
                                 nullable=True)
    creation_date = db.Column(db.Date,
                              nullable=False)
    payment_status_id = db.Column(db.Integer,
                                  db.ForeignKey('PaymentStatus.id'),
                                  nullable=False)
    payment_status = db.relationship('PaymentStatus')
    payment_status_change = db.Column(db.Date)

    def set_from_dict(self, dict):
        id = dict["id"]
        user = dict["user"]
        ticket_type_id = dict["ticketTypeId"]
        ticket_type = dict["ticket_type"]
        special_discount = dict["special_discount"]
        creation_date = dict["creation_date"]
        payment_status = dict["payment_status"]
        payment_status_id = dict["payment_status_id"]
        payment_status_change = dict["payment_status_change"]
        raise NotImplementedError('Not implemented!')


class PaymentStatus(db.Model, object):
    id = db.Column(db.Integer,
                   primary_key=True)
    name = db.Column(db.String)


class Settings(db.Model, object):
    id = db.Column(db.Integer,
                   primary_key=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('user.id'))

    def set_from_dict(self, dict):
      self.id = dict
        raise NotImplementedError('Not implemented!')
