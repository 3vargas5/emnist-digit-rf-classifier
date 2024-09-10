import numpy as np
import os
import requests
import zipfile
import io
import gzip

def download_and_extract_emnist():
    url = "https://biometrics.nist.gov/cs_links/EMNIST/gzip.zip"
    if not os.path.isdir(os.path.join(os.getcwd(), "gzip")):
        response = requests.get(url)
        with zipfile.ZipFile(io.BytesIO(response.content)) as z:
            z.extractall()

def get_images_and_labels(subset_name:str,type:str):
    images_file = f"emnist-{subset_name}-{type}-images-idx3-ubyte.gz"
    labels_file = f"emnist-{subset_name}-{type}-labels-idx1-ubyte.gz"
    gzip_folder = os.path.join(os.getcwd(), "gzip")
    images_path = os.path.join(gzip_folder, images_file)
    labels_path = os.path.join(gzip_folder, labels_file)

    #The code in this video was used to process the .gz files:
    #https://www.youtube.com/watch?v=TswQj9bgbSg
    with gzip.open(images_path,'rb') as f:
        images = np.frombuffer(f.read(),np.uint8,offset=16)
        images = images.reshape(-1,28,28)
    with gzip.open(labels_path,'rb') as g:
        labels = np.frombuffer(g.read(),np.uint8,offset=8)
    return images, labels


class ExtractTrainSamples:
    def __init__(self, subset_name:str):
        download_and_extract_emnist()
        self.images, self.labels = get_images_and_labels(subset_name,"train")
    
    def __iter__(self):
        return iter((self.images, self.labels))

class ExtractTestSamples:
    def __init__(self, subset_name:str):
        download_and_extract_emnist()
        self.images, self.labels = get_images_and_labels(subset_name,"test")
    
    def __iter__(self):
        return iter((self.images, self.labels))