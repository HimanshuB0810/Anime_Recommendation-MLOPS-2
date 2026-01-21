from utils.helpers import *
from config.path_config import *
from pipeline.predication_pipeline import hybrid_recommendation

# print(find_similar_animes('Fairy Tail',ANIME_WEIGHTS_PATH,ANIME2ANIME_ENCODED,ANIME2ANIME_DECODED,DF))
# SIMILAR_USER=similar_users=find_similar_users(item_input=11880,path_user_weights=USER_WEIGHTS_PATH,path_user2user_encoded=USER2USER_ENCODED,
#                    path_user2user_decoded=USER2USER_DECODED)
# print(SIMILAR_USER)

# USER_PREF=get_user_preferences(user_id=11880,path_rating_df=RATING_DF,path_df=DF)
# print(USER_PREF)

# print(get_user_recommendation(SIMILAR_USER,USER_PREF,DF,SYNOPSIS_DF,RATING_DF))

print(hybrid_recommendation(11880))