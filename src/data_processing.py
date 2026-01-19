import os
import pandas as pd
import numpy as np
import joblib
import tensorflow as tf
from sklearn.model_selection import train_test_split
from src.logger import get_logger
from src.custom_exception import CustomException
from config.path_config import *
import sys

logger=get_logger(__name__)

class DataProcessor:
    def __init__(self,input_file,output_dir):
        self.input_file=input_file
        self.output_dir=output_dir

        self.rating_df=None
        self.anime_df=None

        self.train_ds=None
        self.val_ds=None

        self.user2user_encoded={}
        self.user2user_decoded={}
        self.anime2anime_encoded={}
        self.anime2anime_decoded={}

        os.makedirs(self.output_dir,exist_ok=True)
        logger.info("DataProcessing Initalized")

    def load_data(self,usecols):
        try:
            self.rating_df=pd.read_csv(self.input_file,low_memory=True,usecols=usecols)
            logger.info("Data Loaded sucessfully for Data Processing")
        except Exception as e:
            raise CustomException("Failed to load data",sys)
        

    def filter_users(self,min_rating=400):
        try:
            self.n_rating=self.rating_df['user_id'].value_counts()
            valid_user_indices = self.n_rating[self.n_rating >= 400].index
            self.rating_df = self.rating_df[self.rating_df["user_id"].isin(valid_user_indices)].copy() 
            logger.info("Filtered User successfully ")
        except Exception as e:
            raise CustomException("Failed to filter data",sys)
        
    def scale_rating(self):
        try:
            min_rating=min(self.rating_df["rating"])
            max_rating=max(self.rating_df["rating"])

            self.rating_df["rating"] = self.rating_df["rating"].apply(lambda x: (x-min_rating)/(max_rating-min_rating)).astype(np.float64)
            logger.info("Scaling done for Processing")
        except Exception as e:
            raise CustomException("Failed to scaled data",sys)
        
    def encode_data(self):
        try:
            ### User
            user_ids = self.rating_df["user_id"].unique().tolist()
            self.user2user_encoded = {ids : index for index , ids in enumerate(user_ids)}
            self.user2user_decoded = {index : ids for index,ids in enumerate(user_ids)}
            self.rating_df["user"] = self.rating_df["user_id"].map(self.user2user_encoded)

            ### Anime
            anime_ids=self.rating_df["anime_id"].unique().tolist()
            self.anime2anime_encoded={ids : index for index,ids in enumerate(anime_ids)}
            self.anime2anime_decoded={index : ids for index,ids in enumerate(anime_ids)}
            self.rating_df["anime"]=self.rating_df["anime_id"].map(self.anime2anime_encoded)

            logger.info("Encoding Done for Users and Anime")
        except Exception as e:
            raise CustomException("Failed to Encode data",sys)
        
    def split_data(self,test_size=1000,random_state=43):
        try:
            self.rating_df=self.rating_df.sample(frac=1,random_state=43).reset_index(drop=True)
            X = self.rating_df[["user","anime"]].values
            y = self.rating_df["rating"]

            train_indices=self.rating_df.shape[0]-test_size

            X_train,X_test,y_train,y_test=(
                X[:train_indices],
                X[train_indices :],
                y[:train_indices],
                y[train_indices :]
            )

            batch_size = 10000
            # Convert Train data to Dataset
            train_ds = tf.data.Dataset.from_tensor_slices(
                (
                    {"user": X_train[:, 0], "anime": X_train[:, 1]},
                    y_train
                )
            ).shuffle(10000).batch(batch_size).prefetch(tf.data.AUTOTUNE)

            # Convert Test/Validation data to Dataset
            val_ds = tf.data.Dataset.from_tensor_slices(
                (
                    {"user": X_test[:, 0], "anime": X_test[:, 1]},
                    y_test
                )
            ).batch(batch_size).prefetch(tf.data.AUTOTUNE)

            tf.data.Dataset.save(train_ds, "artifacts/processed/data/train_ds")
            tf.data.Dataset.save(val_ds, "artifacts/processed/data/val_ds")

            logger.info("Data Splitted Successfully")

        except Exception as e:
            raise CustomException("Failed to Split data",sys)
        
    def save_artifacts(self):
        try:
            artifacts={
                "user2user_encoded":self.user2user_encoded,
                "user2user_decoded":self.user2user_decoded,
                "anime2anime_encoded":self.anime2anime_encoded,
                "anime2anime_decoded":self.anime2anime_decoded
            }

            for name,data in artifacts.items():
                joblib.dump(data, os.path.join(self.output_dir,f"{name}.pkl"))
                logger.info(f"{name} saved successfully in processed directory")

            self.rating_df.to_csv(RATING_DF,index=False)

            logger.info("user2user, anime2anime encoded-decoded and rating_df is saved")
        except Exception as e:
            raise CustomException("Failed to save artifacts",sys)
        
    def process_anime_data(self):
        try:
            df=pd.read_csv(ANIME_CSV)

            cols = ["MAL_ID","Name","Genres","sypnopsis"]
            synopsis_df=pd.read_csv(ANIMESYNOPSIS_CSV,usecols=cols)

            df=df.replace("Unknown",np.nan)

            def getAnimeName(anime_id):
                try:
                        name=df[df['anime_id'] == anime_id]['eng_version'].values[0]
                        if name is np.nan:
                            name = df[df['anime_id'] == anime_id]['Name'].values[0]
                except:
                        print("Error")
                return name
            
            df["anime_id"]=df["MAL_ID"]
            df["eng_version"]=df["English name"]
            df["eng_version"]=df['anime_id'].apply(lambda x: getAnimeName(x))

            df.sort_values(by=["Score"],inplace=True,ascending=False,kind="quicksort",na_position="last")

            df=df[["anime_id","eng_version","Score","Genres","Episodes","Type","Premiered","Members"]]

            df.to_csv(DF,index=False)
            synopsis_df.to_csv(SYNOPSIS_DF,index=False)

            logger.info("DF and SYNOPSIS_DF saved Successfully")

        except Exception as e:
            raise CustomException("Failed to save anime and anime_synopsis data",sys)
        
    def run(self):
        try:
            self.load_data(usecols=["user_id","anime_id","rating"])
            self.filter_users()
            self.scale_rating()
            self.encode_data()
            self.split_data()
            self.save_artifacts()
            self.process_anime_data()

            logger.info("Data Processing Pipeline Run Successfully")
        except CustomException as e:
            logger.error(str(e))

if __name__=="__main__":
    data_processor=DataProcessor(ANIMELIST_CSV,PROCESSED_DIR)
    data_processor.run()