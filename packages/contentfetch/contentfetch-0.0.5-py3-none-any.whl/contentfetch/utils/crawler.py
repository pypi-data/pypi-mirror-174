import os
import glob
import pandas as pd
import re
from settings import BASE_DIR
from settings import DATA_DIR
from pymongo import MongoClient
from utils.initialize import generate_spider
from urllib.parse import urlparse
import datetime

def dir_size(path):
    #initialize the size
    total_size = 0
    
    #use the walk() method to navigate through directory tree
    for dirpath, dirnames, filenames in os.walk(path):
        for i in filenames:
            
            #use join to concatenate all the components of path
            f = os.path.join(dirpath, i)
            
            #use getsize to generate size in bytes and add it to the total size
            total_size += os.path.getsize(f)
    # return total size in GBs
    return total_size * 9.313225746154785e-10


def remove_urls(urldata, allow_regex=None, deny_regex=None, remove_html=True):
    '''
    Clean URLs after the fact using a regex. Consider updating 
    deny_regex for future crawls.
    '''
    if allow_regex == deny_regex == None:
        print('Need to supply an allow_regex or a deny_regex')
        raise
    urldata_clean = []
    for row in urldata:
        if deny_regex != None:
            if re.search(deny_regex, row['url']) == None:
                urldata_clean.append(row)
            else:
                if remove_html:
                    if os.path.exists(row['html_path']):
                        os.remove(row['html_path'])
        if allow_regex != None:
            if re.search(allow_regex, row['url']) == None:
                if remove_html:
                    if os.path.exists(row['html_path']):
                        os.remove(row['html_path'])
            else:
                urldata_clean.append(row)
    
    return urldata_clean


def add_deny_regex(crawler_name, deny_regex, crawler_type = 'uagent'):
    # Connect to exid database
    client = MongoClient()
    db = client['exid']
    # Pull record for crawler
    source_dict = db.sources.find_one({'crawler_name': crawler_name})
    # Format the new deny_regex list
    deny_regex_raw = [r'{}'.format(el) for el in deny_regex]
    # Replace the record
    source_dict['deny_regex'] = deny_regex_raw
    db.sources.replace_one({'_id': source_dict['_id']}, source_dict)
    # Regenerate the crawler
    path_to_spiders = f'{BASE_DIR}/scrapy_crawlers/crawler_{crawler_type}/crawler_{crawler_type}/spiders'
    generate_spider(
        path_to_spiders = path_to_spiders, 
        crawler_name = crawler_name, 
        allowed_domain = source_dict['domain'], 
        start_urls = [source_dict['start_url']], 
        path_to_html = source_dict['html_path'], 
        crawler_type=crawler_type, 
        crawl_depth=0, 
        allow_regex=source_dict['allow_regex'], 
        deny_regex=deny_regex_raw)


def find_empty_url_lists(country_code, cut=0):
    '''Add docstring'''
    dirs = glob.glob(f'{DATA_DIR}/{country_code}/*')
    counts = []
    for dir in dirs:
        crawler_name = dir.split('/')[-1]
        path_to_csv = f'{dir}/{crawler_name}_urls.csv'
        if os.path.exists(path_to_csv):
            with open(path_to_csv) as f:
                url_count = len(f.readlines())
        else:
            url_count = 0

        counts.append({
            'crawler_name': crawler_name,
            'url_count': url_count
        })
    
    return [row for row in counts if row['url_count'] <= cut]


def count_urls(country_code):
    '''Add docstring'''
    dirs = glob.glob(f'{DATA_DIR}/{country_code}/*')
    counts = []
    for dir in dirs:
        crawler_name = dir.split('/')[-1]
        path_to_csv = f'{dir}/{crawler_name}_urls.csv'
        if os.path.exists(path_to_csv):
            with open(path_to_csv) as f:
                url_count = len(f.readlines())
        else:
            url_count = 0

        counts.append({
            'crawler_name': crawler_name,
            'url_count': url_count
        })
    
    return counts


def get_file_dates(root):
    paths = glob.glob(f'{root}/*')
    fdates = []
    for path in paths:
        mtime = max([os.stat(dir).st_mtime for dir in glob.glob(f'{path}/*')])
        fdates.append({
            'mtime': mtime,
            'path': path
        })
    return sorted(fdates, key=lambda d: -d['mtime']) 


counts_ = count_urls('fra')
counts_fra = [row for row in counts_ if row['url_count'] != 0]

counts_ = count_urls('gbr')
counts_gbr = [row for row in counts_ if row['url_count'] != 0]

url_counts = []
for row in counts_fra:
    row['country'] = 'fra'
    url_counts.append(row)

for row in counts_gbr:
    row['country'] = 'gbr'
    url_counts.append(row)

pd.DataFrame(url_counts).to_csv('url_counts.csv', index=False)

dates = get_file_dates('/home/exiddata/domains/gbr')

for d in dates[0:10]:
    print(datetime.datetime.fromtimestamp(d['mtime']), d['path'])

client = MongoClient()
db = client['exid']
source_lists = list(db.sources.find({'country_code': 'gbr', 'active': 'yes'}))
blogspot = [row['crawler_name'] for row in source_lists if '_blogspot' in row['crawler_name']]
for cname in blogspot:
    add_deny_regex(cname, deny_regex=['/search', '/feeds'])

paths = glob.glob('/home/exiddata/domains/gbr/*')
dsizes = []
for path in paths:
    dsize = dir_size(path)
    print(f'Path {path} is {dsize} GBs')
    dsizes.append({
        'path': path,
        'size': dsize
    })

dsizes_sorted = sorted(dsizes, key=lambda d: -d['size']) 

dsize = dsizes_sorted[6]

df_urls = pd.read_csv(f'/home/exiddata/domains/fra/rivarol/rivarol_urls.csv')
urls = df_urls.url.tolist()
parsed_urls = []
for url in urls:
    path = urlparse(url).path
    if path != '':
        parsed_urls.append(path)

pd.DataFrame({'path': parsed_urls}).value_counts()

urls_clean = remove_urls(df_urls.to_dict('records'), deny_regex=r'.php')

pd.DataFrame(urls_clean).to_csv(f'/home/exiddata/domains/fra/egaliteetreconciliation/egaliteetreconciliation_urls.csv', index=False)
add_deny_regex(crawler_name='egaliteetreconciliation', deny_regex='.php', crawler_type = 'uagent')

# TO-DO:
# add deny_regex = /search? to radioalbion
# add deny_regex = /search? | /feeds to 
# leejohnbarnes_blogspot
# wiganpatriot_blogspot
# lionheartuk_blogspot
# finalconflictblog_blogspot
# northwestnationalists_blogspot