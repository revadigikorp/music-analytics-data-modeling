import pandas as pd
import glob
import os

def extract_json_data(filepath):
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root, '*.json'))
        for f in files:
            all_files.append(os.path.abspath(f))
    
    if not all_files:
        return pd.DataFrame()
        
    df_list = [pd.read_json(f, lines=True) for f in all_files]
    return pd.concat(df_list, ignore_index=True)