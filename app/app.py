from flask import Flask, jsonify, request
import sqlite3
import pandas as pd
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import numpy as np
from sklearn import preprocessing
from sklearn.neighbors import NearestNeighbors
from sklearn.model_selection import train_test_split
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
from typing import List, Tuple
from app.nearest_neighbors_recommender import epic_predictor, feature_average

def create_app():

    app = Flask(__name__)

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

    @app.route('/m', methods=['POST'])
    def post_definer():
        data = request.get_json(force=True)
        input_data = data['track_key']

        return jsonify(epic_predictor(input_data))

    @app.route('/r', methods=['POST'])
    def feature():
        data = request.get_json(force=True)
        input_data = data['track_key']

        return jsonify(feature_average(input_data))

    return app
