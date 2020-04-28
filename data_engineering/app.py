from flask import Flask
import pandas as pd
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import numpy as np

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
SECRET_KEY = os.getenv('SECRET_KEY', default='super secret')


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = SECRET_KEY

    # Configure the database:

    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # suppress warning messages
    db.init_app(app)
    migrate.init_app(app, db)

    file_name = 'samplesongs.csv'
    df = pd.read_csv(file_name)
    db = df.to_sql(con=engine, index_label='id',
                   name=Songs.__tablename__, if_exists='replace')


    # Landing Page

    @app.route('/')
    def hello_world():
    return 'Welcome to DeepTunes!'

return app

if __name__ == '__main__':
    my_app = create_app()
    my_app.run(debug=True)
