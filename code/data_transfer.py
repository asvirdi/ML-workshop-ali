import logging
import urllib3
import gzip
import shutil


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


logger = logging.getLogger('data_transfer_module')
logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s')
logger.setLevel(logging.DEBUG)



## function to decompress data file
def decompressDataFile():
    with gzip.open('data/test_data.gz') as f_in:
        with open('data/test_data.csv', 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)




def main():
    decompressDataFile()

if __name__=="__main__":
    main()