import numpy as np
import os
import requests
import zipfile
import io

def download_and_extract_emnist():
    url = "https://biometrics.nist.gov/cs_links/EMNIST/gzip.zip"
    if not os.path.isdir(os.path.join(os.getcwd(), "gzip")):
        response = requests.get(url)
        with zipfile.ZipFile(io.BytesIO(response.content)) as z:
            z.extractall()

class ExtractTrainSamples:
    def __init__(self, data_name:str):
        self.data_name = data_name
        download_and_extract_emnist()

    
class ExtractTestSamples:
    def __init__(self, data_name:str):
        self.data_name = data_name
        download_and_extract_emnist()