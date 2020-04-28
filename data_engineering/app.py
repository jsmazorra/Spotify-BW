from flask import Flask
import pandas as pd
import os
import pickle
import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import numpy as np

CLIENT_ID = 'd5dce052e44443b39bf5452c936f8752'
CLIENT_SECRET = 'd88d2e8d841b46a0b7bd963f34208695'


def create_app():

    app = Flask(__name__)

    # Spotify API authentication details.

    app.config['CLIENT_ID'] = CLIENT_ID
    app.config['SECRET_KEY'] = CLIENT_SECRET

    credentials = \
        spotipy.oauth2.SpotifyClientCredentials(client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET)

    # Backend database location and associated metadata.

    DB = SQLAlchemy(app)
    DB.Model.metadata.reflect(DB.engine)


def to_dict(self):
    return {
        'track_id': self.track_id,
        'track_name': self.track_name,
        'artist_name': self.artist_name,
        'acousticness': self.acousticness,
        'danceability': self.danceability,
        'duration_ms': self.duration_ms,
        'energy': self.energy,
        'instrumentalness': self.instrumentalness,
        'key': self.key,
        'liveness': self.liveness,
        'loudness': self.loudness,
        'mode': self.mode,
        'speechiness': self.speechiness,
        'tempo': self.tempo,
        'time_signature': self.time_signature,
        'valence': self.valence,
        'popularity': self.popularity,
        }

    def __repr__(self):
        return json.dumps(self.to_dict())

    @app.route('/')
    def root():
        return 'DeepTunes API is working!'

    @app.route('/track')
    def track():
        token = credentials.get_access_token()
        spotify = spotipy.Spotify(auth=token)
        track_id = request.args.get('track',
                                    default='1tHDG53xJNGsItRA3vfVgs',
                                    type=str)
        results = spotify.track(track_id)
        return results

    @app.route('/audio_features')
    def audio_features():
        token = credentials.get_access_token()
        spotify = spotipy.Spotify(auth=token)
        track_id = request.args.get('track',
                                    default='1tHDG53xJNGsItRA3vfVgs',
                                    type=str)
        results = spotify.audio_features(track_id)
        return json.dumps(results)

    return app
