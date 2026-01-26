from config.path_config import *
from utils.helpers import *
import pandas as pd


# def hybrid_recommendation(user_id=None,genre_list=None,user_weight=0.5,content_weight=0.5):
#     combined_scores={}
#     anime_df_obj = pd.read_csv(DF)

#     ### USER RECOMMENDATION
#     if user_id is not None:
#         try:
#             similar_users=find_similar_users(user_id,USER_WEIGHTS_PATH,USER2USER_ENCODED,USER2USER_DECODED)
#             user_pref=get_user_preferences(user_id,RATING_DF,DF)
#             user_recommended_animes=get_user_recommendation(similar_users,user_pref,DF,SYNOPSIS_DF,RATING_DF)

#             user_recommended_anime_list=user_recommended_animes["anime_name"].tolist()
#             for anime in user_recommended_anime_list:
#                 combined_scores[anime]=combined_scores.get(anime,0) + user_weight

#         except Exception as e:
#             print(f"User-based filtering failed: {e}")

def hybrid_recommendation(
    # user_id=None,
    genre_list=None,
    # user_weight=0.5,
    content_weight=1
):
    combined_scores = {}
    anime_df_obj = pd.read_csv(DF)

    # ---------- USER PROFILE–BASED (NO rating_df) ----------
    # if user_id is not None:
    #     try:
    #         user_recs = user_profile_recommendation(user_id, anime_df_obj)
    #         for anime in user_recs:
    #             combined_scores[anime] = combined_scores.get(anime, 0) + user_weight
                
    #     except Exception as e:
    #         print(f"[INFO] User-profile CF skipped: {e}")

    ### CONTENT RECOMMENDATION
    content_recommended_animes=[]

    if genre_list:
        matched_animes = anime_df_obj[
            anime_df_obj['Genres'].str.contains('|'.join(genre_list), case=False, na=False)
        ]

        top_genre_animes = matched_animes.sort_values(by='Score',ascending=False)

        top_genre_animes=top_genre_animes["eng_version"].tolist()

        for anime in top_genre_animes:
            combined_scores[anime]=combined_scores.get(anime,0) + content_weight

    sorted_animes=sorted(combined_scores.items(),key=lambda x:x[1],reverse=True)

    return [anime for anime, score in sorted_animes[:10]]
