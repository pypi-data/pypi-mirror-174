"""Functions to setup crawlers."""
import os
from sys import path
import pandas as pd
from settings import BASE_DIR
from settings import DATA_DIR
import tldextract
from urllib.parse import urlparse
from utils import mongo
from utils import utils
import argparse


def load_seed_list(path_to_seed_list):
    '''
    Load a seed list CSV and prepare it for initialization.

    Arguments:
        path_to_seed_list (str): Path to the seed list to import.
    
    Returns:
    list of dicts: seed list data in the appropriate format.
    '''
    seed_list = pd.read_csv(path_to_seed_list, keep_default_na=False)
    # Add additional fields
    seed_list['updated_date'] = ''
    # Remove social media
    seed_list = seed_list[seed_list['social_media'] == '']
    return seed_list.to_dict('records')


def setup_data_dir(path_to_data, crawler_name, verbose=False):
    '''
    Setup data directory for the domain if one does not already
    exist.
    
    Args:
        path_to_data (str): Absolute path to scrapy spiders
        crawler_name (str): Crawler name -- defaults to the domain name.
    '''
    if not os.path.exists(f'{path_to_data}/{crawler_name}'):
        os.makedirs(f'{path_to_data}/{crawler_name}/html')
    else:
        if verbose:
            print(f'{path_to_data}/{crawler_name} already exists.')


def setup_crawler(seed_data_dict, crawler_type='uagent', create_data_dir=True, add_source = True, depth = 0):
    '''
    Takes a row (dictionary) from the seed list data and sets up
    a crawler.

    Args:
        seed_data_dict (dict): A row from the ExID seed list data. The 
                               dictionary has the following keys:
                               "country_code",
                               "updated_date" (defaults to ""),
                               "start_url",
                               "outlet_name",
                               "crawler_name" (defaults to ""),
                               "allow_regex" (defaults to ""),
                               "deny_regex" (defaults to ""),
                               "social_media" (defaults to ""),
                               "forum" (defaults to "no")
                               "shop" (defaults to "no"),
                               "active" (defaults to "yes"),
                               "notes" (defaults to "")
        crawler_type (str): The type of crawler to use (uagent, proxies, or splash)
        create_data_dir (bool): Set to false if you do not want to create a new data
            directory for the crawler. Default = True.
    
    Returns: 
        dict: Dictionary holding information on crawler's configuration.
    '''
    if seed_data_dict['start_url'] == '':
        raise Exception(
            f'The start_url is empty. You have to specify a start_url.'
        )
    # Parse URL, extract crawler name, and the domain
    extracted_url = tldextract.extract(seed_data_dict['start_url'])
    # Get name of the crawler and the domain
    if extracted_url.subdomain == '' or extracted_url.subdomain == 'www':
        crawler_name = extracted_url.domain
        domain = f'{extracted_url.domain}.{extracted_url.suffix}'
    else:
        crawler_name = f'{extracted_url.subdomain}_{extracted_url.domain}'
        domain = f'{extracted_url.subdomain}.{extracted_url.domain}.{extracted_url.suffix}'
    
    # Create data directory if it does not already exist
    if create_data_dir:
        setup_data_dir(f'{DATA_DIR}/{seed_data_dict["country_code"]}', crawler_name=crawler_name)
    
    # Create spider. First, check if there is an allow_regex
    if seed_data_dict['allow_regex'] == '':
        # Check if the start URL includes a subpage (or path)
        parsed_url = urlparse(seed_data_dict['start_url'])
        if parsed_url.path == '' or parsed_url.path == '/':
            allow_regex = []
        else:
            allow_regex = [r'{}'.format(parsed_url.path)]
    else:
        allow_regex = [r'{}'.format(seed_data_dict['allow_regex'])]
    
    # Next, check if there is the deny_regex
    if seed_data_dict['deny_regex'] == '':
        deny_regex = []
    else:
        deny_regex = [r'{}'.format(seed_data_dict['deny_regex'])]
    
    # Generate the domain spider
    path_to_spiders = f'{BASE_DIR}/scrapy_crawlers/crawler_{crawler_type}/crawler_{crawler_type}/spiders'
    path_to_html = f'{DATA_DIR}/{seed_data_dict["country_code"]}/{crawler_name}/html'
    generate_spider(
        path_to_spiders=path_to_spiders,
        crawler_name=crawler_name,
        allowed_domain=domain,
        start_urls=[seed_data_dict['start_url']],
        crawler_type=crawler_type,
        crawl_depth=depth,
        allow_regex=allow_regex,
        deny_regex=deny_regex,
        path_to_html=path_to_html
        )
    
    # Save crawl parameters to database and return
    parms = {
        'country_code': seed_data_dict['country_code'],
        'crawler_name': crawler_name,
        'crawler_type': crawler_type,
        'domain': domain,
        'outlet_name': seed_data_dict['outlet_name'],
        'start_url': seed_data_dict['start_url'],
        'allow_regex': allow_regex,
        'deny_regex': deny_regex,
        'depth': depth,
        'notes': seed_data_dict['notes'],
        'spider_path': f'{path_to_spiders}/{crawler_name}.py',
        'html_path': path_to_html,
        'active': seed_data_dict['active']
        }
    if add_source:
        mongo.add_source(parms)
    return parms


def generate_spider(path_to_spiders, crawler_name, allowed_domain, start_urls, path_to_html, crawler_type='uagent', crawl_depth=0, allow_regex=(), deny_regex=()):
    '''
    Generates a crawler for a specific domain.

    Args:
        path_to_spiders (str): Absolute path to scrapy spiders.
        crawler_name (str): Crawler name -- defaults to the domain name.
        allowed_domain (str): Domain the crawler is allowed to visit.
        start_urls (list): Start URL (or URLs) for the crawl.
        path_to_html (str): Absolute path to directory in which to store the HTML.
        crawler_type (str): Type of crawler to use (proxies, splash, uagent). 
                            (Defaults to 'uagent')
        crawl_depth (int): Crawl depth from start URL. (Defaults to 0)
        allow_regex (list of str): Allowed links regular expression. (Defaults to [])
        deny_regex (list of str): Denied links regular expression. (Defaults to [])
    
    TODO:
        1. Add splash functionality. Note that we will need the crawler_type argument when we do.
    '''
    crawler_str = f'''# Generated automatically by utils.initialize.setup_crawler
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
import tldextract
import time
from bs4 import BeautifulSoup


class MySpider(CrawlSpider):
    name = '{crawler_name}'
    start_urls = {start_urls}
    allowed_domains = ['{allowed_domain}']

    rules = (
        Rule(LinkExtractor(allow={allow_regex}, deny={deny_regex}), callback='parse_url',follow=True),
        )
    
    custom_settings = dict()
    custom_settings['DEPTH_LIMIT'] = {crawl_depth}

    def extract_external_urls(self, response):
        links = LxmlLinkExtractor(deny=self.allowed_domains).extract_links(response)
        external_links = []
        for link in links:
            url = link.url
            external_links.append(url)
        return external_links
    
    def fetch_all_image_links(self, response):
        soup = BeautifulSoup(response.body)
        image_tags = soup.find_all('img')
        all_images = []
        if image_tags != []:
            for image_tag in image_tags:
                image_url = image_tag.get('src')
                if image_url == None:
                    image_url = image_tag.get('href')
                all_images.append(image_url)
        return all_images

    def parse_url(self, response):
        if response.status == 200:    
            item = dict()
            item['unix_timestamp'] = time.time()
            item['url'] = response.url
            item['links_in_webpage'] = self.extract_external_urls(response)
            item['image_urls'] = self.fetch_all_image_links(response)
            item['referer_url'] = response.request.headers.get('Referer')
            item['depth'] = response.meta.get('depth')
            item['current_domain'] = tldextract.extract(response.url).domain
            # Write HTML to disk
            filepath = '{path_to_html}' + '/' + str(item['unix_timestamp']) + '.html'
            item['html_path'] = filepath
            with open(filepath, 'w') as f:
                f.write(response.body.decode("utf-8"))
            yield item
'''
    # Output script to disk
    with open(f'{path_to_spiders}/{crawler_name}.py', 'w') as f:
        f.write(crawler_str)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("seed_list", type=str, help="A seed list CSV to initialize.")
    args = parser.parse_args()
    seed_dicts = load_seed_list(args.seed_list)
    for seed_dict in seed_dicts:
        res = setup_crawler(seed_dict)
        print(f'Initialized {res["crawler_name"]}')
