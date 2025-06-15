import logging
import os
from google.cloud import storage
from datetime import datetime

def setup_logging():
    """Configure logging for the data analyst agent."""
    # Create a logger
    logger = logging.getLogger('data_analyst')
    logger.setLevel(logging.DEBUG)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)

    # GCS handler
    bucket_name = os.getenv('GOOGLE_CLOUD_STORAGE_BUCKET')
    if bucket_name:
        try:
            storage_client = storage.Client()
            bucket = storage_client.bucket(bucket_name)
            
            class GCSHandler(logging.Handler):
                def emit(self, record):
                    msg = self.format(record)
                    date_str = datetime.now().strftime('%Y-%m-%d')
                    blob = bucket.blob(f'runtime_logs/{date_str}/agent.log')
                    
                    # Append to existing log or create new
                    try:
                        existing_content = blob.download_as_text()
                        content = existing_content + '\n' + msg
                    except Exception:
                        content = msg
                    
                    blob.upload_from_string(content)

            gcs_handler = GCSHandler()
            gcs_handler.setLevel(logging.DEBUG)
            gcs_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(filename)s:%(lineno)d')
            gcs_handler.setFormatter(gcs_format)
            logger.addHandler(gcs_handler)
        except Exception as e:
            print(f"Failed to setup GCS logging: {e}")

    return logger 