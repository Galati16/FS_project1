#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_
import logging
from logging import Formatter, FileHandler
from flask_wtf import FlaskForm
from forms import *
from flask_migrate import Migrate
from models import db, Shows, Venue, Artist
from datetime import datetime

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#
app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db.init_app(app)
migrate=Migrate(app,db)

current_time = datetime.now().strftime('%Y-%m-%d %H:%S:%M')

# TODO: connect to a local postgresql database

''' #----------------------------------------------------------------------------#
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
    seeking_description=db.Column(db.String(1000)) '''
    

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():#DONE
  location=db.session.query(Venue.city,Venue.state).order_by(Venue.city.desc()).distinct().all()
  data=[]
  for i in range(0, len(location)):
  #cyle over locations: 
      venue=db.session.query(Venue.id,Venue.name).filter_by(city=location[i][0]).all()
      venue_lists=[]
      #cyle over venues at location:
      for j in range(0, len(venue)):
          num_upcoming_shows =Shows.query.filter(and_(Shows.venue_id==venue[j][0], Shows.start_time > current_time)).count()  
          venue_dict ={
            "id": venue[j][0],
            "name": venue[j][1],
            "num_upcoming_shows": num_upcoming_shows
          }
          venue_lists.append(venue_dict)
          print(venue_dict)
        
      data_location={
        "city": location[i][0],
        "state": location[i][1],
        "venues": venue_lists
        }                   
      data_copy = data_location.copy()             
      data.append(data_copy)
  return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():#DONE
  venue_list=[]
  search_term = request.form.get('search_term')
  venue = Venue.query.filter(Venue.name.ilike('%' + search_term +'%')).all()
  
  for venues in venue:
        upcoming_shows = Shows.query.filter_by(venue_id=venues.id).filter(Shows.start_time > datetime.utcnow()).count()
        venue_dict={
          "id": venues.id,
          "name":venues.name,
          "num_upcoming_shows": upcoming_shows
          }
        venue_list.append(venue_dict)
        
  response={
    "count": len(venue),
    "data": venue_list
  }

  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):#DONE
  venue_data=Venue.query.get(venue_id)
  
  # current, previous shows
  num_upcoming_shows =Shows.query.filter(and_(Shows.venue_id==venue_id, Shows.start_time > current_time)).count()
  upcoming_shows = Shows.query.filter(and_(Shows.venue_id==venue_id, Shows.start_time > current_time))
  num_past_shows = Shows.query.filter(and_(Shows.venue_id==venue_id, Shows.start_time < current_time)).count()
  past_shows = Shows.query.filter(and_(Shows.venue_id==venue_id, Shows.start_time < current_time))
  
  upcoming=[]
  past=[]
  for show in upcoming_shows:
        artist = Artist.query.filter(Artist.id==show.artist_id).first()
        upcoming_dict={
          "artist_id": show.artist_id,
          "artist_name": artist.name,
          "artist_image_link": artist.image_link,
          "start_time": show.start_time.strftime('%Y-%m-%d %H:%S:%M'),
        }
        upcoming.append(upcoming_dict)
       
  for show in past_shows:
        artist = Artist.query.filter(Artist.id==show.artist_id).first()
        past_dict={
          "artist_id": show.artist_id,
          "artist_name": artist.name,
          "artist_image_link": artist.image_link,
          "start_time": show.start_time.strftime('%Y-%m-%d %H:%S:%M'),
        }
        past.append(past_dict)      
        
  data={
    "id": venue_data.id,
    "name": venue_data.name,
    "genres": venue_data.genres,
    "address": venue_data.address,
    "city": venue_data.city,
    "state": venue_data.state,
    "phone": venue_data.phone,
    "website": venue_data.website_link,
    "facebook_link": venue_data.facebook_link,
    "seeking_talent": venue_data.looking_for_Talent,
    "seeking_description": venue_data.seeking_description,
    "image_link": venue_data.image_link,
    "past_shows": past,
    "upcoming_shows": upcoming,
    "past_shows_count": num_past_shows,
    "upcoming_shows_count": num_upcoming_shows,
  }
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():#DONE
  error = False
  try:
        form = VenueForm(request.form)
        venue = Venue(
        name = request.form['name'],
        city = request.form['city'],
        state = request.form['state'],
        address = request.form['address'],
        phone = request.form['phone'],
        genres = form.genres.data,
        facebook_link = request.form['facebook_link'],
        image_link = request.form['image_link'],
        website_link = request.form['website_link'],
        seeking_description = request.form['seeking_description']
        )
        db.session.add(venue)
        db.session.commit()
        # on successful db insert, flash success
        flash('Venue ' + request.form['name'] + ' was successfully listed!')
  except Exception as e:
        print(e)
        error = True
        db.session.rollback()
        flash('An error occurred. Venue ' + request.form['name']+ ' could not be listed.')
  finally:
        db.session.close()
        
      
  
  # TODO: modify data to be the data object returned from db insertion
  # TODO: on unsuccessful db insert, flash an error instead.
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id): #DONE
      error = False
      try:
        venue = Venue.query.get(venue_id)
        db.session.delete(venue)
        db.session.commit()
      except:
        error = True
        db.session.rollback()
      finally:
        db.session.close()
      if error:
        abort (400)
      return render_template('home.html')
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
 

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists(): #DONE
  artists=db.session.query(Artist.id,Artist.name).order_by(Artist.name.desc()).distinct().all()
  #num_upcoming_shows =db.session.query(shows.venue_id)
  data=[]
  for i in range(0, len(artists)):
  #cyle over artists:  
      artist_dict ={
        "id": artists[i][0],
        "name": artists[i][1]
      }
      data.append(artist_dict)
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists(): #DONE
  artist_list=[]
  search_term = request.form.get('search_term')
  artist = Artist.query.filter(Artist.name.ilike('%' + search_term +'%')).all()
  
  for artists in artist:
        upcoming_shows = Shows.query.filter_by(artist_id=artists.id).filter(Shows.start_time > datetime.utcnow()).count()
        artist_dict={
          "id": artists.id,
          "name":artists.name,
          "num_upcoming_shows": upcoming_shows
          }
        artist_list.append(artist_dict)
        
  response={
    "count": len(artist),
    "data": artist_list
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>') 
def show_artist(artist_id):  #DONE
  artist=Artist.query.get(artist_id)
  
  # current, previous shows
  num_upcoming_shows =Shows.query.filter(and_(Shows.artist_id==artist_id, Shows.start_time > current_time)).count()
  upcoming_shows = Shows.query.filter(and_(Shows.artist_id==artist_id, Shows.start_time > current_time))
  num_past_shows = Shows.query.filter(and_(Shows.artist_id==artist_id, Shows.start_time < current_time)).count()
  past_shows = Shows.query.filter(and_(Shows.artist_id==artist_id, Shows.start_time < current_time))
  
  upcoming=[]
  past=[]
  for show in upcoming_shows: 
        #artist = Artist.query.filter(Artist.id==show.artist_id).first()
        upcoming_dict={
          "artist_id": show.artist_id,
          "artist_name": artist.name,
          "artist_image_link": artist.image_link,
          "start_time": show.start_time.strftime('%Y-%m-%d %H:%S:%M'),
        }
        upcoming.append(upcoming_dict)
       
  for show in past_shows:
        #artist = Artist.query.filter(Artist.id==show.artist_id).first()
        past_dict={
          "artist_id": show.artist_id,
          "artist_name": artist.name,
          "artist_image_link": artist.image_link,
          "start_time": show.start_time.strftime('%Y-%m-%d %H:%S:%M'),
        }
        past.append(past_dict)
  
  data={
    "id": artist.id,
    "name": artist.name,
    "genres": list(artist.genres),
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "website": artist.website_link,
    "facebook_link": artist.facebook_link,
    "seeking_venue": artist.looking_for_venue,
    "seeking_description": artist.seeking_description,
    "image_link":artist.image_link,
    "past_shows":past,
    "upcoming_shows": upcoming,
    "past_shows_count": num_past_shows,
    "upcoming_shows_count": num_upcoming_shows,
  }
  
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist = Artist.query.filter_by(id=artist_id).first()
  
  form.name.data = artist.name
  form.city.data = artist.city
  form.state.data = artist.state
  form.phone.data = artist.phone
  form.genres.data = artist.genres
  form.image_link.data = artist.image_link
  form.facebook_link.data = artist.facebook_link
  form.website_link.data = artist.website_link
  form.seeking_description.data = artist.seeking_description
  form.seeking_venue.data = artist.looking_for_venue
  
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    venue = Venue.query.filter_by(id=venue_id).first()
    
    form.name.data = venue.name
    form.city.data = venue.city
    form.state.data = venue.state
    form.address.data = venue.address
    form.phone.data = venue.phone
    form.genres.data = venue.genres
    form.image_link.data = venue.image_link
    form.facebook_link.data = venue.facebook_link
    form.website_link.data = venue.website_link
    form.seeking_description.data = venue.seeking_description
    form.seeking_talent.data = venue.looking_for_Talent
  
    return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():#DONE
  form = ArtistForm(request.form, meta={'csrf': False})
  error = False
  try:
        if request.form['seeking_venue']== 'y':
              seeking_venue=True
        else:
              seeking_venue=False
        artist = Artist(
        name = request.form['name'],
        city = request.form['city'],
        state = request.form['state'],
        phone = request.form['phone'],
        genres = form.genres.data,
        image_link =request.form['image_link'],
        facebook_link = request.form['facebook_link'],
        website_link = request.form['website_link'],
        looking_for_venue = seeking_venue,
        seeking_description = request.form['seeking_description'],
        )    
        db.session.add(artist)
        db.session.commit()
        flash('Artist ' + request.form['name'] + ' was successfully listed!')
  except Exception as e :
        print(e)
        error = True
        db.session.rollback()
        flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')

  finally:
        db.session.close()
        
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows(): #DONE
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  show = Shows.query.all()
  data = []    
  for shows in show:
        artist = Artist.query.filter(Artist.id==shows.artist_id).first()
        venue = Venue.query.filter(Venue.id==shows.venue_id).first()
        data_dict={
          "venue_id": shows.venue_id,
          "venue_name": venue.name,
          "artist_id": shows.artist_id,
          "artist_name": artist.name,
          "artist_image_link": artist.image_link,
          "start_time": shows.start_time.strftime('%Y-%m-%d %H:%S:%M'),
        }
        data.append(data_dict)
  ''' data2=[{
    "venue_id": 1,
    "venue_name": "The Musical Hop",
    "artist_id": 4,
    "artist_name": "Guns N Petals",
    "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    "start_time": "2019-05-21T21:30:00.000Z"
  }]'''
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission(): #DONE
  error = False
  try:  
        form = ShowForm(request.form)
        print(form)
        show_list = Shows(
            artist_id=form.artist_id.data,
            venue_id=form.venue_id.data,
            start_time=form.start_time.data
        )   
        db.session.add(show_list)
        db.session.commit()
        flash('New show was successfully listed!')
  except Exception as e :
        print(e)
        error = True
        db.session.rollback()
        flash('An error occurred. New show could not be listed.')

  finally:
        db.session.close()
        
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run(debug=True)

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
