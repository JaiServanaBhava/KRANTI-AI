import os

def search_files(directory, keyword):
    return [f for f in os.listdir(directory) if keyword.lower() in f.lower()]

