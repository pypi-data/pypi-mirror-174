"""Uses the newsfetch api to parse the content of a list"""

from extract.text import extract_content_html
from utils import utils
import argparse
from utils.mongo import add_content


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("inpath", type=str, help="Input path holding crawled URLs.")
    args = parser.parse_args()
    # Parse input path
    crawler_name = args.inpath.split('/')[-1]
    country_code = args.inpath.split('/')[-2]
    path = f'{args.inpath}/{crawler_name}_urls.csv'
    # Load data and check if CSV is empty
    items = utils.read_csv(path)
    if items == None:
        print(f'No crawled URLs found in {args.inpath}')
    else:
        for i,item in enumerate(items):
            try:
                item['crawler_name'] = crawler_name
                item['country_code'] = country_code
                add_content(extract_content_html(item))
                # Delete html
                utils.delete_file(item['html_path'])
            except:
                print(f'Failed to process item {i} for {country_code}, {crawler_name}')
        print(f'Finished processing {country_code}, {crawler_name}.')
