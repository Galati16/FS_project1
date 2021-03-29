from flask_sqlalchemy import SQLAlchemy

db= SQLAlchemy()
#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#
shows_table = db.Table('shows',
    db.Column('venue_id', db.Integer, db.ForeignKey('Venue.id'),primary_key=True),
    db.Column('artist_id', db.Integer, db.ForeignKey('Artist.id'),primary_key=True)
    )
          
 
class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    looking_for_Talent = db.Column(db.Boolean, nullable=False,default=False)
    seeking_description=db.Column(db.String(1000))
    artists = db.relationship('Artist',secondary=shows_table,backref=db.backref('venues', lazy=True))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    looking_for_venue = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description=db.Column(db.String(1000))