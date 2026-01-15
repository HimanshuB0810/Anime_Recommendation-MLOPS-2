import os
import pandas as pd
from src.custom_exception import CustomException
from src.logger import get_logger
from config.path_config import *
from utils.common_functions import read_yaml
from minio import Minio


logger=get_logger(__name__)

class DataIngestion:
    def __init__(self,config):
        self.config = config["data_ingestion"]
        self.bucket_name = self.config["bucket_name"]
        self.file_names = self.config["bucket_file_name"]

        os.makedirs(RAW_DIR,exist_ok=True)

        logger.info("Data Ingestion Started")

    
    def download_csv_from_minio(self):
        try:
            client = Minio(
                        "localhost:9000",
                        access_key="minioadmin",
                        secret_key="minioadmin",
                        secure=False                           
            )

            for file_name in self.file_names:
                file_path = os.path.join(RAW_DIR, file_name)

                if file_name == "animelist.csv":
                    client.fget_object(
                        bucket_name=self.bucket_name,
                        object_name=file_name,
                        file_path=file_path
                    )

                    data = pd.read_csv(file_path, nrows=5_000_000)
                    data.to_csv(file_path, index=False)
                    logger.info("Large file detected only downloading 5M rows")
                
                else:
                    client.fget_object(
                        bucket_name=self.bucket_name,
                        object_name=file_name,
                        file_path=file_path
                    )
                    logger.info("Downloading smaller files ie anime and anime_with_synopsis")


        except Exception as e:
            logger.error("Error while downloading file from Minio")
            raise CustomException("Error downloading from MinIO:", e)
        
    def run(self):
        try:
            logger.info("Starting data ingestion process")
            self.download_csv_from_minio()
            logger.info("data ingestion completed")
        except CustomException as ce:
            logger.error(f"Custom Exception : {str(ce)}")
        finally:
            logger.info("Data Ingestion Done......")


if __name__=="__main__":
    data_ingestion = DataIngestion(read_yaml(CONFIG_PATH))
    data_ingestion.run()



        