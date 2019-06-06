import data_transfer
from sklearn.ensemble import RandomForestClassifier
import urllib3
import logging
import pandas
from warnings import simplefilter
from sklearn.metrics import multilabel_confusion_matrix, accuracy_score
import time

# ignore all future warnings
simplefilter(action='ignore', category=FutureWarning)

logger = logging.getLogger('intrusion_detection_module')
logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s')
logger.setLevel(logging.DEBUG)




urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)













