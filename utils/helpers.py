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

############ 2. GET_SYNOPSIS

def getSynopsis(anime,path_synopsis_df):
    synopsis_df=pd.read_csv(path_synopsis_df)
    if isinstance(anime,int):
        return synopsis_df[synopsis_df["MAL_ID"]==anime].sypnopsis.values[0]
    if isinstance(anime,str):
        return synopsis_df[synopsis_df["Name"]==anime].sypnopsis.values[0]
    
########## 3. CONTENT RECOMMENDATION
def find_similar_animes(name, path_anime_weights, path_anime2anime_encoded, path_anime2anime_decoded, path_anime_df, n=10, return_dist=False, neg=False):
    try:
        anime_weights=joblib.load(path_anime_weights)
        anime2anime_encoded=joblib.load(path_anime2anime_encoded)
        anime2anime_decoded=joblib.load(path_anime2anime_decoded)

        # 1. Get the correct index
        anime_info = getAnimeFrame(name, path_anime_df)
        if anime_info.empty:
            return None
            
        index = anime_info.anime_id.values[0]
        encoded_index = anime2anime_encoded.get(index)

        # 2. Ensure weights are 2D (Rows x Features)
        weights = np.squeeze(anime_weights)
        target_vector = weights[encoded_index].reshape(-1) 
        
        # 3. Vectorized Similarity Calculation
        # weights: (17555, 32), weights[encoded_index]: (32,)
        dists = np.dot(weights, target_vector)
        
        # 4. Sorting logic
        sorted_dists = np.argsort(dists)
        n_plus = n + 1 

        if neg:
            closest = sorted_dists[:n_plus]
        else:
            closest = sorted_dists[-n_plus:]

        if return_dist:
            return dists, closest

        # 5. Build Result List
        SimilarityArr = []
        for close in closest:
            decoded_id = anime2anime_decoded.get(close)
            anime_frame = getAnimeFrame(decoded_id, path_anime_df)
            
            if not anime_frame.empty:
                SimilarityArr.append({
                    "anime_id": decoded_id,
                    "name": anime_frame.eng_version.values[0],
                    "similarity": dists[close],
                    "genre": anime_frame.Genres.values[0],
                })

        # 6. Final DataFrame formatting
        Frame = pd.DataFrame(SimilarityArr).sort_values(by="similarity", ascending=False)
        # Remove the input anime from results
        return Frame[Frame.anime_id != index].drop(['anime_id'], axis=1)

    except Exception as e:
        print(f"Error Occurred for {name}: {e}")
        return None

############### 4. FIND_SIMILAR_USERS
def find_similar_users(item_input,path_user_weights,path_user2user_encoded,path_user2user_decoded,n=10,return_dist=False,neg=False):
    try:
        user2user_encoded=joblib.load(path_user2user_encoded)
        user2user_decoded=joblib.load(path_user2user_decoded)
        user_weights=joblib.load(path_user_weights)

        index=item_input
        encoded_index=user2user_encoded.get(index)

        weights=user_weights

        dists=np.dot(weights,weights[encoded_index])
        sorted_dists=np.argsort(dists)

        n=n+1

        if neg:# Fetch dissimilar anime
            closest = sorted_dists[:n]
        else:
            closest = sorted_dists[-n:]


        if return_dist:
            return dists,closest

        SimilarityArr=[]

        for close in closest:
            similarity=dists[close]

            if isinstance(item_input,int):
                decoded_id=user2user_decoded.get(close)
                SimilarityArr.append({
                    "similar_users":decoded_id,
                    "similarity":similarity
                })

        similar_users=pd.DataFrame(SimilarityArr).sort_values(by="similarity",ascending=False)
        similar_users=similar_users[similar_users.similar_users!=item_input]
        return similar_users
    except Exception as e:
        print("Error Occured",e)

######## 5. GET USER PREFERENCES

def get_user_preferences(user_id,path_rating_df,path_anime_df):

    rating_df=pd.read_csv(path_rating_df)
    df=pd.read_csv(path_anime_df)

    animes_watced_by_user=rating_df[rating_df['user_id']==user_id]

    user_rating_percentile=np.percentile(animes_watced_by_user['rating'],75) # only the users top 25 %tile rating is present

    animes_watced_by_user=animes_watced_by_user[animes_watced_by_user['rating']>=user_rating_percentile]

    top_animes_user=(
        animes_watced_by_user.sort_values(by="rating",ascending=False)['anime_id'].values
    )

    anime_df_rows=df[df['anime_id'].isin(top_animes_user)]
    anime_df_rows=anime_df_rows[["eng_version","Genres"]]

    
    return anime_df_rows

####### 6. GET USER RECOMMENDATION
def get_user_recommendation(similar_users,user_pref,path_anime_df,path_synopsis_df,path_rating_df,n=10):

    recommended_anime=[]
    anime_list=[]

    for user_id in similar_users['similar_users'].values:
        pref_list=get_user_preferences(user_id,path_rating_df,path_anime_df)

        pref_list=pref_list[~pref_list['eng_version'].isin(user_pref['eng_version'].values)]

        if not pref_list.empty:
            anime_list.append(pref_list['eng_version'].values)

    if anime_list:
            anime_list=pd.DataFrame(anime_list)

            sorted_list=pd.DataFrame(pd.Series(anime_list.values.ravel()).value_counts().head(n))

            for i,anime_name in enumerate(sorted_list.index):
                n_user_pref=sorted_list[sorted_list.index==anime_name].values[0][0]

                if isinstance(anime_name,str):
                    frame=getAnimeFrame(anime_name,path_anime_df)
                    anime_id=frame['anime_id'].values[0]
                    genre=frame['Genres'].values[0]
                    synopsis=getSynopsis(int(anime_id),path_synopsis_df)

                    recommended_anime.append({
                        "n":n_user_pref,
                        "anime_name":anime_name,
                        "Genres":genre,
                        "Synopsis":synopsis
                    })

    return pd.DataFrame(recommended_anime).head(n)



