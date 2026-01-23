import comet_ml
import joblib
import numpy as np
import os
import sys
import tensorflow as tf
from tensorflow.keras.callbacks import ModelCheckpoint,LearningRateScheduler,TensorBoard,EarlyStopping
from src.logger import get_logger
from src.custom_exception import CustomException
from src.base_model import BaseModel
from config.path_config import *


if os.getenv("CI") == "true":
    print("CI detected → Skipping model training")
    sys.exit(0)


logger=get_logger(__name__)

class ModelTraining:
    def __init__(self,data_path):
        self.data_path=data_path

        self.experiment=comet_ml.Experiment(
            api_key="Gv4cVIjCKQTRqXwYF5Drx4qsy",
            project_name="Mlops-2",
            workspace="himanshub0810"
        )
        logger.info("Model Trainig & COMET-ML Initialized")

    def load_datasets(self):
        try:

            train_ds = tf.data.Dataset.load("artifacts/processed/data/train_ds")
            val_ds   = tf.data.Dataset.load("artifacts/processed/data/val_ds")

            logger.info("Successfully Loaded Train_ds and Val_ds in load_datasets")

            return train_ds,val_ds

        except Exception as e:
            raise CustomException("Failed to Load Data")
        
    def train_model(self):
        try:
            train_ds, val_ds = self.load_datasets()
            logger.info("Successfully Loaded Train_ds and Val_ds in train_model")

            n_users=len(joblib.load(USER2USER_ENCODED))
            n_anime=len(joblib.load(ANIME2ANIME_ENCODED))

            base_model=BaseModel(config_path=CONFIG_PATH)

            model = base_model.RecommenderNet(n_users=n_users,n_anime=n_anime)
    
            start_lr = 0.00001 # lr = learning_rate
            min_lr = 0.0001
            max_lr = 0.00005
            batch_size = 10000

            ramup_epochs = 5
            sustain_epochs = 0
            exp_decay = 0.8

            def lrfn(epoch): # gives the best epoch for our model
                if epoch<ramup_epochs:
                    return (max_lr-start_lr)/ramup_epochs*epoch+start_lr
                elif epoch<ramup_epochs+sustain_epochs:
                    return max_lr
                else:
                    return (max_lr-min_lr)*exp_decay ** (epoch-ramup_epochs-sustain_epochs)+min_lr
                
            lr_callback = LearningRateScheduler(lambda epoch:lrfn(epoch), verbose=0)

            model_checkpoint = ModelCheckpoint(filepath=CHECKPOINT_FILEPATH,save_weights_only=True,monitor="val_loss",mode="min",save_best_only=True)

            early_stopping = EarlyStopping(patience=2,monitor="val_loss",mode="min",restore_best_weights=True)

            my_callbacks=[model_checkpoint,lr_callback,early_stopping]

            os.makedirs(os.path.dirname(CHECKPOINT_FILEPATH),exist_ok=True)
            os.makedirs(MODEL_DIR,exist_ok=True)
            os.makedirs(WEIGHTS_DIR,exist_ok=True)

            try:
                history = model.fit(
                train_ds,
                batch_size=batch_size,           
                validation_data=val_ds, 
                epochs=20,
                verbose=1,
                callbacks=my_callbacks
            )
                model.load_weights(CHECKPOINT_FILEPATH)
                logger.info("Model Training Completed")

                for epoch in range(len(history.history['loss'])):
                    train_loss=history.history["loss"][epoch]
                    val_loss=history.history["val_loss"][epoch]

                    self.experiment.log_metric('train_loss',train_loss,step=epoch)
                    self.experiment.log_metric('val_loss',val_loss,step=epoch)


            except Exception as e:
                raise CustomException("Model Training Failed")
            
            self.save_model_weights(model)

        except Exception as e:
            logger.error(str(e))
            raise CustomException("Error occured during Model Training Process",e)

    def extract_weights(self,layer_name,model):
            try:      
                weight_layer=model.get_layer(layer_name)
                weights = weight_layer.get_weights()[0]
                weights = weights/np.linalg.norm(weights,axis=1).reshape((-1,1))
                logger.info(f"Extracting weights for {layer_name}")
                return weights 
            except  Exception as e:
                logger.error(str(e))
                raise CustomException("Error while Extracting weights")
              
    def save_model_weights(self,model):
        try:
            model.save(MODEL_PATH)
            logger.info(f"Model saved to {MODEL_PATH}")

            user_weights=self.extract_weights("user_embedding",model)
            anime_weights=self.extract_weights("anime_embedding",model)

            joblib.dump(user_weights,USER_WEIGHTS_PATH)
            joblib.dump(anime_weights,ANIME_WEIGHTS_PATH)

            self.experiment.log_asset(MODEL_PATH)
            self.experiment.log_asset(ANIME_WEIGHTS_PATH)
            self.experiment.log_asset(USER_WEIGHTS_PATH)

            logger.info("User and Anime weights saved successfully")
        except  Exception as e:
                logger.error(str(e))
                raise CustomException("Error while saving model and weights",e)


if __name__=="__main__":
    model_trainer=ModelTraining(PROCESSED_DIR)
    model_trainer.train_model()