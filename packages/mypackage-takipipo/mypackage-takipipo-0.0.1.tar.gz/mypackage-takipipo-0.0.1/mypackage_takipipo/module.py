
def add_one(num):
    return num + 1

def fetch_url(url):
    import requests
    response = requests.get(url)
    return response

def add_one_numpy(arr):
    import numpy as np
    return arr + 1