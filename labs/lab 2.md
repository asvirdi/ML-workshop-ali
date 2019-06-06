# Lab 2

## Getting the code

* The project code is available on [RBC Enterprise Github](https://rbcgithub.fg.rbc.com/kft0/workshop)

* We are going to `clone` this code repository on our workstations using Git we setup earlier. Cloning gets us a copy of an exisiting Git repository.
It is a smart way for developers and technicians to collaborate on work

* Open terminal or command prompt 

* Go to a directory of your preference (eg. C/Development)

* Run `git clone https://rbcgithub.fg.rbc.com/kft0/workshop` in a directory of your preference (eg. C/Development)

* If you are not able to clone, the repository folder is also available in your email. You can download and open this to continue.

* Go into the `workshop` directory

* You will setup a virutal environment. This makes sure any packages you install for this workshop do not intefere with your system's python packages

* Install the virtualenv package using pip -- `pip install virtualenv`

* You should see 2 directories, `code` and `labs` and 1 `requirements.txt` file. The reqiurements file lists the packages you require for this workshop

* Data has been processed and made available in Elasticsearch for this workshop

* Find `elasticPassword` (cmd+f `elasticPassword` on Mac or ctrl+f`elasticPassword` on Windows)

* Fill out the string with password on the white board

* This is a temporary account configured to provide you access to Elasticsearch in this workshop

* Step into the `code` directory

* The `data_transfer` module is a python file that handles the data wrangling for our workshop. It is not our primal focus

* The `intrusion_detection` file is where we will build our detection system


* Lets step into the code step by step

    * The following code imports important modules and libraries that we will when building our models

```
import data_transfer
from sklearn.ensemble import RandomForestClassifier
import urllib3
import logging
import pandas
from warnings import simplefilter
from sklearn.metrics import multilabel_confusion_matrix, accuracy_score
import time

```

   * The following code disables some warnings and setups up logging etc. to assist in our development
   
```
simplefilter(action='ignore', category=FutureWarning)

logger = logging.getLogger('intrusion_detection_module')
logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s')
logger.setLevel(logging.DEBUG)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

```

* The data conversion function takes data from Elastic and converts it into a Pandas DataFrame so its easy to manipulate


    