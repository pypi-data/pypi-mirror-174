"""Check the status of running crawlers. """

import glob
import psutil
import time


def check_status(verbose=True, terminate=False):
    running = []
    current_time = time.time()
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        # Parse running scrapy processes
        if 'scrapy' in proc.info['name']:
            cmd = proc.info['cmdline']
            domain = cmd[-2].split('/')[-2]
            if cmd[-1] == 'in_crawler' or cmd[-1] == 'out_crawler':
                running.append({
                    'crawler_type': cmd[-1], 
                    'pid': proc.info["pid"],
                    'status': proc.status(),
                    'domain': domain,
                    'run_time': ((current_time - proc.create_time())/60)/60
                })
    
    if verbose:
        print('Crawlers in progress:')
        for proc in running:
            print(f'{proc["domain"]} {proc["pid"]}  {proc["crawler_type"]} {proc["status"]} {round(proc["run_time"], 2)} hours')
            if terminate:
                if proc["run_time"] > 48:
                    print(f'Consider killing {proc["pid"]}')
                    #psutil.Process(proc["pid"]).terminate()

    return running

if __name__ == "__main__":
    status_ = check_status(terminate=True)
    with open('/home/tcoan/log.txt', 'w') as f:
        f.write(f'Logging call time {time.time()}')

# END
