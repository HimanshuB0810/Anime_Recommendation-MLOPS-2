import pandas as pd
import numpy as np
import joblib
from config.path_config import *

########## 1. GET_ANIME_FRAME

# def getAnimeFrame(anime,path_df):
#     df=pd.read_csv(path_df)
#     if isinstance(anime,int):
#         return df[df['anime_id']==anime]
#     if isinstance(anime,str):
#         return df[df['eng_version']==anime] 

def getAnimeFrame(anime, path_df):
    df = pd.read_csv(path_df)
    print(f"Available columns: {df.columns.tolist()}") # Debugging line
    
    if 'anime_id' not in df.columns:
        # Fallback if the column is named MAL_ID in the CSV
        if 'MAL_ID' in df.columns:
            df.rename(columns={'MAL_ID': 'anime_id'}, inplace=True)
        else:
            raise KeyError("The column 'anime_id' was not found in the CSV.")

    if isinstance(anime, int):
        return df[df['anime_id'] == anime]
    if isinstance(anime, str):
        return df[df['eng_version'] == anime]