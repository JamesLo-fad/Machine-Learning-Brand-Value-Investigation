import re
import time
import pandas as pd
import mysql.connector
from gcloud import storage
import os

os.environ.setdefault("GCLOUD_PROJECT", "heroic-climber-347106")
storage_client = storage.Client.from_service_account_json("heroic-climber-347106-b0f1ec68d8cc.json")
bucket = storage_client.get_bucket('mobile_raw')
blob = bucket.blob(f'Mobile_raw.csv')
blob.upload_from_filename(f'./Mobile_raw.csv')