#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, jsonify
import sqlite3
import pandas as pd
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import numpy as np
from sklearn import preprocessing
from sklearn.neighbors import NearestNeighbors
from sklearn.model_selection import train_test_split
from typing import List, Tuple

DB = SQLAlchemy()


# Tell SQLAlchemy what the table name is and if there's any table-specific arguments it should know about

class Songs(DB.Model):

    __tablename__ = 'Songs'
    id = DB.Column(DB.BigInteger, primary_key=True)
    artist_name = DB.Column(DB.String(50))
    track_name = DB.Column(DB.String(100))
    track_id = DB.Column(DB.String(50))
    popularity = DB.Column(DB.Integer)
    acousticness = DB.Column(DB.Float)
    danceability = DB.Column(DB.Float)
    duration_ms = DB.Column(DB.Integer)
    energy = DB.Column(DB.Float)
    instrumentalness = DB.Column(DB.Float)
    key = DB.Column(DB.Integer)
    liveness = DB.Column(DB.Float)
    loudness = DB.Column(DB.Float)
    mode = DB.Column(DB.Integer)
    speechiness = DB.Column(DB.Float)
    tempo = DB.Column(DB.Float)
    time_signature = DB.Column(DB.Integer)
    valence = DB.Column(DB.Float)

    def __repr__(self):
        return '<Song {}>'.format(self.track_name)


def create_app():

    app = Flask(__name__)
    engine = create_engine('sqlite:///Spotify_Songs.db')
    Songs.metadata.create_all(engine)
    file_name = 'https://raw.githubusercontent.com/jsmazorra/Spotify-BW/master/app/samplesongs.csv'
    df = pd.read_csv(file_name)
    db = df.to_sql(con=engine, index_label='id',
                   name=Songs.__tablename__, if_exists='replace')

    # accepts the cursor and the row as a tuple and returns a dictionary result and you can object column by name

    def dict_factory(cursor, row):
        d = {}
        for (idx, col) in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    # Landing Page

    @app.route('/')
    def hello_world():

        return 'DeepTunes API is working!'

    return app