import os
import logging
from googleapiclient.discovery import build
from google.oauth2 import service_account

SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'service_account.json'
PARENT_FOLDER_ID = "1S7vU89bYwiaXv6DHrIu3pt7qMnSPN3oG"

creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
dir_path = "images/"

def initLogger():
    logger = logging.getLogger('autoBackupLogger')
    log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    logger.setLevel(logging.DEBUG)
    
    file_handler = logging.FileHandler('auto_backup.log')
    file_handler.setFormatter(log_formatter)
    
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger

def readFile(dir_path):
    try:
        files = [file for file in os.listdir(dir_path)]
    except Exception as e:
        log.error("Could not list the directory: %s", e)
    else:
        if len(files) == 0:
            log.error("The directory %s is empty", dir_path)
        for file in files:
            file_path = os.path.join(dir_path, file)
            uploadFile(file_path)
    finally:
        exit()
        
def uploadFile(file_path):
    file_name = os.path.basename(file_path)
    service = build('drive', 'v3', credentials=creds)

    file_metadata = {
        'name': file_name,
        'parents': [PARENT_FOLDER_ID]
    }

    try:
        file = service.files().create(
            body=file_metadata,
            media_body=file_path
        ).execute()
    except Exception as e:
        log.error("failed to upload %s: %s", file_name, e)
    else:
        log.info("File uploaded: %s", file_name)
        deleteFile(file_path)

def deleteFile(file_path):
    try:
        os.remove(file_path)
    except Exception as e:
        log.error("failed to delete %s: %s", file_path, e)
    else:
        log.info("Deleted file: %s", file_path)
        



log = initLogger()
readFile(dir_path)