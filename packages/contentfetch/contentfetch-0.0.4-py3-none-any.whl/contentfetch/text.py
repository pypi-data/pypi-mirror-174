"""Uses the newsfetch api to parse the content of a list"""

from newsfetch.news import newspaper
import subprocess
import multiprocessing
# from settings import BASE_DIR


def parse_content_url(url):
    '''
    Parse content using modified version of the newsfetch library.
    
    Args:
        url (str): A string providing a URL.

    Returns:
        dict: Parsed results from newsfetch.newspaper.
    '''
    return newspaper(uri=url).get_dict


def parse_content_html(html_path):
    '''
    Parse content using modified version of the newsfetch library.
    
    Args:
        url (str): A path to an HTML file on disk to parse.

    Returns:
        dict: Parsed results from newsfetch.newspaper.
    '''
    return newspaper(uri='', from_html=html_path).get_dict


def extract_content(html= None, url=None):

    """
    
    Parse content using modified version of the newsfetch library.

    Args:
        html (str): A path to an HTML file on disk to parse
        url (str): The actual webpage link 
    
    Returns:

        dict: Parsed results from newsfetch.newspaper.
    
    """



    if url is None:
        fetched = parse_content_html(html)
    else:
        fetched = parse_content_url(url)
    return {
        'title': fetched['title'],
        'author': fetched['author'],
        'date_publish': fetched['date_publish'],
        'top_image': fetched['top_image'],
        'all_images': fetched['all_images'],
        'description': fetched['description'],
        'article': fetched['article'],
        'keywords': fetched['keyword'],
        # 'url': item['url'],
        # 'domain': item['current_domain'],
        # 'crawl_timestamp': item['unix_timestamp'],
        # 'crawler_name': item['crawler_name'],
        # 'country_code': item['country_code']
    }


def _extract_content_safe(cmd):
    try:
        process = subprocess.call(cmd, shell=True)
    except Exception as e:
        print(f'ERROR: {e} raised for {cmd}')


# def extract_content_parallel(paths, num_cpus=multiprocessing.cpu_count()):
#     '''
#     Takes a list of paths to crawled data and extracts the content
#     in parallel.

#     Args:
#         paths (list of str): Paths to crawled URLs and HTML.
#         num_cps (int): Number of CPUs to use. Defaults to the system maximum.
#     '''
#     # Make cmd list
#     commands = []
#     for path in paths:
#         # Set working directory
#         csd = f'cd {BASE_DIR}'
    
#         # Call string
#         call_str = f'python extract_content.py {path}'
#         commands.append(f'{csd}; {call_str}')
    
#     p = multiprocessing.Pool(num_cpus)
#     p.map(_extract_content_safe, commands)
#     return commands