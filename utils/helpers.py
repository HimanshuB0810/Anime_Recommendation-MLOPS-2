import pandas as pd
import numpy as np
import joblib
from config.path_config import *

########## 1. GET_ANIME_FRAME

def getAnimeFrame(anime,path_df):
    df=pd.read_csv(path_df)
    if isinstance(anime,int):
        return df[df['anime_id']==anime]
    if isinstance(anime,str):
        return df[df['eng_version']==anime] 

