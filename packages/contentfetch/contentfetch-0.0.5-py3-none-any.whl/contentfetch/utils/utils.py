import os
import json
import pandas as pd
from glob import glob
from settings import DATA_DIR


def read_json(path_):
    '''
    TODO:
        1. Add docstring
    '''
    with open(path_, 'r') as f:
        jdata = json.load(f)
    return jdata


def write_json(path, content):
    '''
    Takes a path and list of dictionaries and writes a pretty, POSIX
    compatiable JSON file.

    Arguments:
        path (str): Path to file where JSON should be written
        content (list of dicts): Content to write.
    '''

    with open(path, 'w') as f:
        json.dump(content, f, indent=4, separators=(',', ': '), sort_keys=True)
        # add trailing newline for POSIX compatibility
        f.write('\n')


def read_csv(path):
    '''
    Helper function to take a path to crawled URLs and return a 
    list of dicts with the results.
    '''
    try:
        items = pd.read_csv(path, keep_default_na=False).to_dict('records')
    except pd.errors.EmptyDataError:
        items = None
    return items


def get_failed_crawls(country_code, cutoff=0, verbose=False):
    '''
    Return the crawls that failed to collect data by country
    code.

    Arguments:
        country_code (str): 3 digit ISO country code (e.g., gbr)
        cutoff (int): Number of rows to determine "failed".
        verbose (bool): Set to true to print failed crawls to the
            console.
    
    Returns:
        list of str: List of the crawler names that failed.
    '''
    paths = glob(f'{DATA_DIR}/domains/{country_code}/*')
    failed = []
    for path in paths:
        crawler_name = path.split('/')[-1]
        try:
            urls = pd.read_csv(f'{path}/{crawler_name}_urls.csv', nrows=cutoff+1)
        except Exception as e:
            if verbose:
                print(f'Crawler {crawler_name} failed with {cutoff} urls.')
            failed.append(crawler_name)
    return failed


def delete_file(file):
    if os.path.exists(file):
        os.remove(file)
    else:
        print(f'{file} does not exists')
