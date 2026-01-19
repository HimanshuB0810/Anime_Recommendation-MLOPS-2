import tensorflow as tf
from tensorflow.keras.models import Model 
from tensorflow.keras.layers import Input,Embedding,Dot,Flatten,Dense,Dropout
from tensorflow.keras.regularizers import l2
from utils.common_functions import read_yaml
from src.logger import get_logger
from src.custom_exception import CustomException

logger=get_logger(__name__)

class BaseModel:
    def __init__(self,config_path):
        try:
            self.config=read_yaml(config_path)
            logger.info("Loaded configuration from config.yaml")

        except Exception as e:
            raise CustomException("Error Loading Configurations",e)
    
    def RecommenderNet(self,n_users,n_anime):
        try:
            embedding_size=self.config["model"]["embedding_size"]
            l2_emb = self.config["model"]["l2_reg_embedding"]
            l2_dense = self.config["model"]["l2_reg_dense"]
            lr = self.config["model"]["learning_rate"]

            user = Input(name="user",shape=[1])

            user_embedding = Embedding(name="user_embedding",input_dim=n_users,output_dim=embedding_size,embeddings_regularizer=l2(l2_emb))(user)

            anime = Input(name="anime",shape=[1])

            anime_embedding = Embedding(name="anime_embedding",input_dim=n_anime,output_dim=embedding_size,embeddings_regularizer=l2(l2_emb))(anime)

            x = Dot(name="dot_product",normalize=True,axes=2)([user_embedding,anime_embedding])

            x = Flatten()(x)
            x = Dense(32,activation="relu",kernel_regularizer=l2(l2_dense))(x)
            x = Dropout(0.4)(x)
            x = Dense(1, activation='linear')(x)

            model = Model(inputs=[user,anime], outputs=x)
            model.compile(
                loss=self.config["model"]["loss"],
                optimizer=tf.keras.optimizers.Adam(learning_rate=lr),
                metrics=self.config["model"]["metrics"],
            )
            logger.info("Model Created Successfully")

            return model
        except Exception as e:
            logger.error(f"Error Occured during model architecture {e}")
            raise CustomException("Failed to create Model")

    
