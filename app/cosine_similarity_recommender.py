import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler

# Load Data
data = pd.read_csv("https://raw.githubusercontent.com/Lambda-Spotify-Song-Suggester-3/datascience/master/kaggle_data/encoded.csv")
df = data.copy()

dictionary = df[["artist_name", "track_name", "track_key", "track_id"]]

# Drop
df = df.drop(columns=['artist_name','track_id', 'track_name','track_key', 'duration_ms', 'loudness', 'time_signature'])

scaler = MinMaxScaler()
df_s = scaler.fit_transform(df)

def epic_predictor(input_track_key):
  '''
  This function takes in a 'track_key' which is a number from 0 to 130,000 something.
  The function returns a list of ten numbers that are the "track_id"s of the
  dataframe imported above.
  -------
  For example, your function will look like this for Britney Spears' "Toxic":
  > input:
  toxic_track_key = 119347
  epic_predictor(toxic_track_key)
  
  >output:
  >>> ['7dbDPHivUEXRlrrSmw2L6E',
  >>> '4ZurPit9M0ISoEaDjIeR17',
  >>> '3EmVLU2EHNEJf646hdsu7s',
  >>> '6FoAzNJTueEuCw1J68VeVk',
  >>> '4YK3zrLBWbsb8lVHVFy0sX',
  >>> '1y0Kx4EftBK6vfLWSaAxOh',
  >>> '7ynOkljlhjeldKu1fTy3vh',
  >>> '4Qgj02O7e0eakpPH9qMCEC',
  >>> '0o7TZ372wdFUM2IH2cRope',
  >>> '49xmhJzBfsIHKGIETsfnEY']
  '''

  # Cosign Similarity
  matrix = cosine_similarity(df_s, df_s[input_track_key:(input_track_key + 1)])
  matrix = pd.DataFrame(matrix)
  top = matrix[0].sort_values(ascending=False)[:10]

  # Print Playlist
  z = top.reset_index()
  ten_similar_tracks = []

  for col in z["index"]:
    track = (dictionary['track_id'].iloc[col])
    ten_similar_tracks.append(track)

  return ten_similar_tracks

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