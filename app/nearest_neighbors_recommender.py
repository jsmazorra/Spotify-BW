import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors

# Load Data
data = pd.read_csv("https://raw.githubusercontent.com/Lambda-Spotify-Song-Suggester-3/datascience/master/kaggle_data/encoded.csv")
df = data.copy()

dictionary = df[["artist_name", "track_name", "track_key", "track_id"]]

# Drop
df = df.drop(columns=['artist_name','track_id', 'track_name','track_key', 'duration_ms', 'mode', 'loudness', 'time_signature'])

# Scale the data

scaler = StandardScaler()
df_s = scaler.fit_transform(df)

def epic_predictor(input_track_key):
  '''
  This function takes in a 'track_key' of a song in the dataframe imported
  above, which is a number from 0 to 130,000 something.
  The function returns a list of ten hashes that are the "track_id"s of most
  closely related songs in the dataframe imported above.
  -------
  For example, your function will look like this for Britney Spears' "Toxic":
  > input:
  toxic_track_key = 119347
  epic_predictor(toxic_track_key)
  
  >output:
  >>>['4fbaKWFRghusXd4bSBvvfN',
  >>>'5cesclKWAhsCcZJDBhkWaa',
  >>> '7IE8eERSpTC9Jaw3arl99B',
  >>> '6MLvUL2dYphJTwgiBvuJ1J',
  >>> '4RYtaqxjDJUOY2GrtkLTFf',
  >>> '6gJ1T7THE0Pxk5VpTovwJH',
  >>> '7hiFcSUWRVotWd2pxhRIDJ',
  >>> '6flP4UZGozZGQk8rpE09g4',
  >>> '4uLmKWOb8hl49MYYAc4bnn',
  >>> '39Z6LCw3UEFYjQivDV1UF1']
  '''


  ## Convert "input_track_key" to the index of the song (the song's position
  ## in the dataframe).
  input_dictionary_entry = dictionary[dictionary['track_key']==input_track_key]
  input_index = input_dictionary_entry.index[0]

  ## Nearest Neighbors model
  nn = NearestNeighbors(n_neighbors=10, algorithm='kd_tree')
  nn.fit(df_s)

  neighbor_predictions = nn.kneighbors([df_s[input_index]])

  ## This is a list of the INDEXES of the songs
  list_of_predictions = neighbor_predictions[1][0].tolist()

  ten_similar_tracks = []
  for item in list_of_predictions:
    track_hash = dictionary['track_id'].iloc[item]
    ten_similar_tracks.append(track_hash)

  return ten_similar_tracks

#testing

#toxic_track_key = 119347
#epic_predictor(toxic_track_key)

## You can use this to print out the artist name and track name of the list of hashes generated.
#print(dictionary[dictionary['track_id']=='4fbaKWFRghusXd4bSBvvfN'])
#print(dictionary[dictionary['track_id']=='5cesclKWAhsCcZJDBhkWaa'])

## This function is deprecated. Don't use it.

#from sklearn.metrics.pairwise import cosine_similarity
#from sklearn.preprocessing import MinMaxScaler

#scaler = MinMaxScaler()
#df_s = scaler.fit_transform(df)

# def epic_predictor(input_track_key):
#   '''
#   This function is deprecated. Don't use it.

#   This function takes in a 'track_key' which is a number from 0 to 130,000 something.
#   The function returns a list of ten numbers that are the "track_id"s of the
#   dataframe imported above.
#   -------
#   For example, your function will look like this for Britney Spears' "Toxic":
#   > input:
#   toxic_track_key = 119347
#   epic_predictor(toxic_track_key)
  
#   >output:
#   >>>['4fbaKWFRghusXd4bSBvvfN',
#   >>>'5cesclKWAhsCcZJDBhkWaa',
#   >>>'7IE8eERSpTC9Jaw3arl99B',
#   >>>'5HypDLkUG04hMqepEP3OMM',
#   >>>'7hiFcSUWRVotWd2pxhRIDJ',
#   >>>'6MLvUL2dYphJTwgiBvuJ1J',
#   >>>'12j3KX5TkcAswLUUPMTNqA',
#   >>>'39Z6LCw3UEFYjQivDV1UF1',
#   >>>'2v5JTeM6hSmi5wWy7jiwrI',
#   >>>'6gJ1T7THE0Pxk5VpTovwJH']

#   '''

#   # Cosine Similarity
#   matrix = cosine_similarity(df_s, df_s[input_track_key:(input_track_key + 1)])
#   matrix = pd.DataFrame(matrix)
#   top = matrix[0].sort_values(ascending=False)[:10]

#   # Print Playlist
#   z = top.reset_index()
#   ten_similar_tracks = []

#   for col in z["index"]:
#     track = (dictionary['track_id'].iloc[col])
#     ten_similar_tracks.append(track)

#   return ten_similar_tracks

#testing
#toxic_track_key = 119493
#epic_predictor(toxic_track_key)

def feature_average(input_track_key):
  '''
  This function returns the sum of the features for the ten recommended songs.
  '''
  ten_similar_tracks = epic_predictor(input_track_key)
  # Return a dataframe with only the ten most similar tracks
  ten_similar_tracks = data[data["track_id"].isin(ten_similar_tracks)]
  ten_similar_tracks = ten_similar_tracks[['acousticness', 'danceability', 
                                           'energy', 'instrumentalness', 
                                           'liveness', 'mode', 
                                           'speechiness', 'valence']]
  # Average features of ten tracks                                           
  acousticness = round(ten_similar_tracks['acousticness'].mean(),2)
  danceability = round(ten_similar_tracks['danceability'].mean(),2)
  energy = round(ten_similar_tracks['energy'].mean(),2)
  instrumentalness = round(ten_similar_tracks['instrumentalness'].mean(),2)
  liveness = round(ten_similar_tracks['liveness'].mean(),2)
  mode = round(ten_similar_tracks['mode'].mean(),2)
  speechiness = round(ten_similar_tracks['speechiness'].mean(),2)
  valence = round(ten_similar_tracks['valence'].mean(),2)
  # Store all to "features" variable
  features = []
  attributes = [acousticness, danceability, energy, instrumentalness, liveness, mode, speechiness, valence]
  #features.append(acousticness)
  for attribute in attributes:
    features.append(attribute)
  return features
