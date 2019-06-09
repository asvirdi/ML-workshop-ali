# Lab 2

## Estimated time for completion: 45 minutes
## Getting the code

* The project code is available on [RBC Enterprise Github](https://rbcgithub.fg.rbc.com/kft0/workshop)

* We are going to `clone` this code repository on our workstations using Git we setup earlier. Cloning gets us a copy of an existing Git repository.
    It is a smart way for developers and technicians to collaborate on work

1. Open terminal or command prompt 

2. Go to a directory of your preference (eg. C:/Development)

3. Run `git clone https://rbcgithub.fg.rbc.com/kft0/workshop` in a directory of your preference (eg. C:/Development)

4. If you are not able to clone, we can email the repository to you. You can download and open this in a text editor/IDE to continue.

5. Go into the **workshop** directory -- `cd workshop`

6. Install the virtualenv package using pip -- `pip3 install virtualenv --user` on Mac or `pip install virtualenv --user` on Windows

7. You will setup a virtual environment. This makes sure any packages you install for this workshop do not mess with your system's python packages

8. You should see 2 directories, `code` and `labs` and 1 `requirements.txt` file. The `requirements` file lists the packages you require for this workshop

9. Make a virtual environment in the **workshop directory** `python3 -m virtualenv venv` on Mac or `python -m virtualenv venv` on Windows in a terminal

10. From the **workshop** directory, activate your virtual environment `source venv/bin/activate` on Mac or `venv\Scripts\activate.bat` on Windows in a terminal

11. Run `pip install -r requirements.txt` in a terminal to install packages in this virtual environment. Minimize your terminal window.

12. Now we will go over the code. Compressed data is present in the repo you cloned/downloaded. Open the **workshop** directory in an IDE or text editor. 

13. You will decompress it by running the `data_transfer` module. Run ` python 'code/data_transfer.py'` from a terminal from the **workshop** directory or just click play if you are in an IDE. \
The compressed file should have now been decompressed and a `test_data.csv` should appear in the `data` directory

15. Go back to your text editor/IDE

16. Open the `code` directory

17. The `data_transfer` module you ran handles the data wrangling for our workshop. It is not our prime focus

18. The `intrusion_detection` file is where we will build our detection system

## Starting to code

19. Lets add code step by step. We encourage you to write the code yourself - code snippets are provided at end of each step that can be copied over and a copy of the lab is also present in `reference.py` file. Remember indentation determines grouping of statements in Python!

20. The following code imports important modules and libraries that we will when building our models. Copy and paste this to the top of the `intrusion_detection` file




```python
from sklearn.ensemble import RandomForestClassifier
import urllib3
import logging
import pandas
from warnings import simplefilter
from sklearn.metrics import multilabel_confusion_matrix, accuracy_score
import time

```


21.The following code disables some warnings and setups logging etc. to assist in our development. Copy and paste this below the above snippet.
  
  
  
   
```python
simplefilter(action='ignore', category=FutureWarning)

logger = logging.getLogger('intrusion_detection_module')
logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s')
logger.setLevel(logging.DEBUG)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

```




22.Circling back to the previous lab, you might have noticed some of the values in the dataset were non-numerical. This makes sense to us, but these values have no meaning to machines. We need to convert them to numerical values for the algorithm to make sense of the data.
What if we give numerical values to such data? For example, for days in a week - Mon, Tues, Wed; what if we assign 1 to Mon, 2 to Tues, 3 to Wed? 

23.This is a bad practice. It might lead to the algorithm placing more importance on higher numerical values

## One Hot Encoding

24.Instead we will use One Hot Encoding to pre-process our data. The process takes categorical variables and converts it into numerical representation without an arbitrary ordering

25.One Hot Encoding will take this table 

| Week | 
| ----- |
| Mon |
| Tue |
| Wed |
| Thurs |
| Fri |


and convert it to

| Mon | Tues | Wed | Thu | Fri |
| --- | ---- | --- | --- | --- |
| 1 | 0 | 0 | 0 | 0 | 
| 0 | 1 | 0 | 0 | 0 | 
| 0 | 0 | 1 | 0 | 0 |
| 0 | 0 | 0 | 1 | 0 |
| 0 | 0 | 0 | 0 | 1 |


26.Write a function to one hot encode our dataframe in `intrusion_detection` module. You should call it oneHotEncoding and it should accept a data frame to one hot encode. Pandas provides a helper function to do this.


```python
def oneHotEncoding(data):
    logger.info(msg='one hot encoding')
    encodedData = pandas.get_dummies(data)
    return encodedData
``` 

27.Next we will train our model using the Random Forest Classifier from scikit-learn. We will use our data to incrementally improve our model's ability to distinguish between normal and malicious connections
We can feed selective features to our training model based on domain knowledge and/or educated intuition

28.**Write a function** called `learnToTrainAndTestModel` in `intrusion_detection.py` file. You will read the csv file into a dataframe in memory, `dataframe = pandas.read_csv('../data/test_data.csv')` and then
assign column headers like the instructor did in lab 1. The function is provided in `reference.py` for reference but try doing it by yourself before checking that.
```python
dataframe = pandas.read_csv('../data/test_data.csv')
headers = ["duration", "protocol_type", "service", "flag", "src_bytes", "dst_bytes", "land", "wrong_fragment",
               "urgent", "hot", "num_failed_logins" \
        , "logged_in", "num_compromised", "root_shell", "su_attempted", "num_root", "num_file_creations", "num_shells",
               "num_access_files", "num_outbound_cmds" \
        , "is_host_login", "is_guest_login", "count", "srv_count", "serror_rate", "srv_serror_rate", "rerror_rate",
               "srv_rerror_rate", "same_srv_rate" \
        , "diff_srv_rate", "srv_diff_host_rate", "dst_host_count", "dst_host_srv_count", "dst_host_same_srv_rate",
               "dst_host_diff_srv_rate", "dst_host_same_src_port_rate" \
        , "dst_host_srv_diff_host_rate", "dst_host_serror_rate", "dst_host_srv_serror_rate", "dst_host_rerror_rate",
               "dst_host_srv_rerror_rate", "label"]

    dataframe.columns = headers
```
 
 
29. Now you will need to do one-hot encoding `encodedData = oneHotEncoding(dataframe)` and then you will need to initialize a `rf = RandomForestClassifier()` and create a partial data frame of just the labels from the input encoded data.
After one-hot encoding, our labels will be 
```
'label_back.', 'label_buffer_overflow.', 'label_ftp_write.', 'label_guess_passwd.', 'label_imap.', 'label_ipsweep.', 'label_land.', \
'label_loadmodule.', 'label_multihop.', 'label_neptune.', 'label_nmap.', 'label_normal.', 'label_perl.', 'label_phf.', 'label_pod.',\
 'label_portsweep.', \
'label_rootkit.', 'label_satan.', 'label_smurf.', 'label_spy.', 'label_teardrop.', 'label_warezclient.', 'label_warezmaster.'                            
                                
```
Assign them to a variable called `encodedData`. The code is presented below:

```python
encodedData = oneHotEncoding(dataframe)
encodedLabels = encodedData[['label_back.', 'label_buffer_overflow.', 'label_ftp_write.', 'label_guess_passwd.', 'label_imap.', 'label_ipsweep.', 'label_land.', \
                             'label_loadmodule.', 'label_multihop.', 'label_neptune.', 'label_nmap.', 'label_normal.', 'label_perl.', 'label_phf.', 'label_pod.', 'label_portsweep.', \
                             'label_rootkit.', 'label_satan.', 'label_smurf.', 'label_spy.', 'label_teardrop.', 'label_warezclient.', 'label_warezmaster.']]
rf = RandomForestClassifier()                      
```
30.Next, we will fit(train) our model on our training data set. The function will take features and labels as inputs. You can use any features that you think are the most important in grouping traffic data into malicious and normal buckets. Add the following code to the same function:

```python
rf.fit(encodedData[['duration', 'logged_in']], encodedLabels)

```                             


31.Now, we will run our trained model on test data -- passing a similar data frame. The predict function will generate labels for the test data set. Add the following code to the same function.

```python
predictionsrf = rf.predict(encodedData[['duration', 'logged_in']])
```

32.You can find the accuracy score of your model by passing in the labels from the data ( the truth ) and the predictions returned by our model. Add the below code to our `learnToTrainAndTestModel` function.

```python
accuracyScorerf = accuracy_score(encodedLabels, predictionsrf)
logger.info("accuracy score for model {}:".format(accuracyScorerf))
```
    
    
33.Setup a main function and call the function you wrote to test it
```python
def main():
    starttime = time.time()
    logger.info('start time: {}'.format(starttime))

    learnToTrainAndTestModel()

    endtime = time.time() - starttime
    logger.info('run time: {}'.format(endtime))

if __name__=="__main__":
    main()

```

## Seeing ML in action

34.We will now try a custom `trainAndTestModel` that tries out 5 different models. Copy the code below into `intrustion_detection` module and modify your `main()` functions such that \
it calls `trainAndTestModel` instead of `learnToTrainAndTestModel`. **After coding, wait for further instructions.**

```python
def trainAndTestModel():
    dataframe = pandas.read_csv('../data/test_data.csv')
    headers = ["duration", "protocol_type", "service", "flag", "src_bytes", "dst_bytes", "land", "wrong_fragment",
               "urgent", "hot", "num_failed_logins" \
        , "logged_in", "num_compromised", "root_shell", "su_attempted", "num_root", "num_file_creations", "num_shells",
               "num_access_files", "num_outbound_cmds" \
        , "is_host_login", "is_guest_login", "count", "srv_count", "serror_rate", "srv_serror_rate", "rerror_rate",
               "srv_rerror_rate", "same_srv_rate" \
        , "diff_srv_rate", "srv_diff_host_rate", "dst_host_count", "dst_host_srv_count", "dst_host_same_srv_rate",
               "dst_host_diff_srv_rate", "dst_host_same_src_port_rate" \
        , "dst_host_srv_diff_host_rate", "dst_host_serror_rate", "dst_host_srv_serror_rate", "dst_host_rerror_rate",
               "dst_host_srv_rerror_rate", "label"]

    dataframe.columns = headers
    encodedData = oneHotEncoding(dataframe)

    encodedLabels = encodedData[['label_back.', 'label_buffer_overflow.', 'label_ftp_write.', 'label_guess_passwd.', 'label_imap.', 'label_ipsweep.', 'label_land.',\
                                 'label_loadmodule.', 'label_multihop.', 'label_neptune.', 'label_nmap.', 'label_normal.', 'label_perl.', 'label_phf.',\
                                  'label_pod.', 'label_portsweep.',\
                                 'label_rootkit.', 'label_satan.', 'label_smurf.', 'label_spy.', 'label_teardrop.', 'label_warezclient.', 'label_warezmaster.']]

    logger.info(msg='traing model rf1 on data')
    rf1 = RandomForestClassifier()
    rf1.fit(encodedData[['duration', 'logged_in']], encodedLabels)
    logger.info(msg='training rf1 finished')


    logger.info(msg='training model rf2 on data')
    rf2 = RandomForestClassifier()
    rf2.fit(encodedData[['duration', 'protocol_type_icmp', 'protocol_type_tcp', 'protocol_type_udp']], encodedLabels)
    logger.info('training rf2 finised')


    ## basic features
    logger.info(msg='training model rf3 on data')
    rf3 = RandomForestClassifier()
    rf3.fit(encodedData[['duration', 'protocol_type_icmp', 'protocol_type_tcp', 'protocol_type_udp',\
                         'service_IRC', 'service_X11', 'service_Z39_50', 'service_auth', 'service_bgp', 'service_courier', \
                         'service_csnet_ns', 'service_ctf', 'service_daytime', 'service_discard', 'service_domain', 'service_domain_u', \
                         'service_echo', 'service_eco_i', 'service_ecr_i', 'service_efs', 'service_exec', 'service_finger', 'service_ftp', \
                         'service_ftp_data', 'service_gopher', 'service_hostnames', 'service_http', 'service_http_443', 'service_imap4', 'service_iso_tsap', \
                         'service_klogin', 'service_kshell', 'service_ldap', 'service_link', 'service_login', 'service_mtp', 'service_name', 'service_netbios_dgm', \
                         'service_netbios_ns', 'service_netbios_ssn', 'service_netstat', 'service_nnsp', 'service_nntp', 'service_ntp_u', 'service_other', 'service_pm_dump',\
                         'service_pop_2', 'service_pop_3', 'service_printer', 'service_private', 'service_red_i', 'service_remote_job', 'service_rje', 'service_shell', 'service_smtp', \
                         'service_sql_net', 'service_ssh', 'service_sunrpc', 'service_supdup', 'service_systat', 'service_telnet', 'service_tftp_u', 'service_tim_i', 'service_time',\
                         'service_urh_i', 'service_urp_i', 'service_uucp', 'service_uucp_path', 'service_vmnet', 'service_whois',\
                         'src_bytes','dst_bytes',\
                         'flag_OTH', 'flag_REJ', 'flag_RSTO', 'flag_RSTOS0', 'flag_RSTR', 'flag_S0', 'flag_S1', 'flag_S2', 'flag_S3', 'flag_SF', 'flag_SH',\
                         'land','wrong_fragment','urgent']], encodedLabels)
    logger.info('training rf3 finised')

    ## content features
    logger.info(msg='training model rf4 on data')
    rf4 = RandomForestClassifier()
    rf4.fit(encodedData[['hot','num_failed_logins','logged_in', 'num_compromised', 'root_shell', 'su_attempted', 'num_root', 'num_file_creations', 'num_shells', 'num_access_files', \
                         'num_outbound_cmds', 'is_host_login', 'is_guest_login']], encodedLabels )
    logger.info('training rf4 finished')

    ## traffic features
    logger.info(msg='training model rf5 on data')
    rf5 = RandomForestClassifier()
    rf5.fit(encodedData[['count','serror_rate','rerror_rate','same_srv_rate','diff_srv_rate','srv_count','srv_serror_rate','srv_rerror_rate', 'srv_diff_host_rate']], encodedLabels )
    logger.info('training rf5 finished')



   

    testData = data
    logger.info('converting test data into relevant data structures')
    testDataframe = dataConversion(testData)
    logger.info('one hot encoding test data')
    encodedTestData = oneHotEncoding(testDataframe)

    ## free up resources used in training
    del encodedLabels, encodedData

    ## predictions
    logger.info('running rf1 on test data')
    predictionsrf1 = rf1.predict(encodedTestData[['duration', 'logged_in']])
    logger.info('running rf2 on test data')
    predictionsrf2 = rf2.predict(encodedTestData[['duration', 'protocol_type_icmp', 'protocol_type_tcp', 'protocol_type_udp']])
    logger.info('running rf3 on test data')
    predictionsrf3 = rf3.predict(encodedTestData[['duration', 'protocol_type_icmp', 'protocol_type_tcp', 'protocol_type_udp',\
                         'service_IRC', 'service_X11', 'service_Z39_50', 'service_auth', 'service_bgp', 'service_courier', \
                         'service_csnet_ns', 'service_ctf', 'service_daytime', 'service_discard', 'service_domain', 'service_domain_u', \
                         'service_echo', 'service_eco_i', 'service_ecr_i', 'service_efs', 'service_exec', 'service_finger', 'service_ftp', \
                         'service_ftp_data', 'service_gopher', 'service_hostnames', 'service_http', 'service_http_443', 'service_imap4', 'service_iso_tsap', \
                         'service_klogin', 'service_kshell', 'service_ldap', 'service_link', 'service_login', 'service_mtp', 'service_name', 'service_netbios_dgm', \
                         'service_netbios_ns', 'service_netbios_ssn', 'service_netstat', 'service_nnsp', 'service_nntp', 'service_ntp_u', 'service_other', 'service_pm_dump',\
                         'service_pop_2', 'service_pop_3', 'service_printer', 'service_private', 'service_red_i', 'service_remote_job', 'service_rje', 'service_shell', 'service_smtp', \
                         'service_sql_net', 'service_ssh', 'service_sunrpc', 'service_supdup', 'service_systat', 'service_telnet', 'service_tftp_u', 'service_tim_i', 'service_time',\
                         'service_urh_i', 'service_urp_i', 'service_uucp', 'service_uucp_path', 'service_vmnet', 'service_whois',\
                         'src_bytes','dst_bytes',\
                         'flag_OTH', 'flag_REJ', 'flag_RSTO', 'flag_RSTOS0', 'flag_RSTR', 'flag_S0', 'flag_S1', 'flag_S2', 'flag_S3', 'flag_SF', 'flag_SH',\
                         'land','wrong_fragment','urgent']])
    logger.info('running rf4 on test data')
    predictionsrf4 = rf4.predict(encodedTestData[['hot','num_failed_logins','logged_in', 'num_compromised', 'root_shell', 'su_attempted', 'num_root', 'num_file_creations', 'num_shells', 'num_access_files', \
                         'num_outbound_cmds', 'is_host_login', 'is_guest_login']])
    logger.info('running rf5 on test data')
    predictionsrf5 = rf5.predict(encodedTestData[['count','serror_rate','rerror_rate','same_srv_rate','diff_srv_rate','srv_count','srv_serror_rate','srv_rerror_rate', 'srv_diff_host_rate']])




    ## encoded test labels
    encodedTestLabels = encodedTestData[['label_back.', 'label_buffer_overflow.', 'label_ftp_write.', 'label_guess_passwd.', 'label_imap.', 'label_ipsweep.', 'label_land.', \
                                 'label_loadmodule.', 'label_multihop.', 'label_neptune.', 'label_nmap.', 'label_normal.', 'label_perl.', 'label_phf.', 'label_pod.', 'label_portsweep.', \
                                 'label_rootkit.', 'label_satan.', 'label_smurf.', 'label_spy.', 'label_teardrop.', 'label_warezclient.', 'label_warezmaster.']]




    logger.info('calculating confusion matrixes')
    ## comparing predictions with the true labels
    # confusionMatrix1 = multilabel_confusion_matrix(encodedTestLabels, predictionsrf1)
    # print(confusionMatrix1)
    #
    # confusionMatrix2 = multilabel_confusion_matrix(encodedTestLabels, predictionsrf2)
    # print(confusionMatrix2)
    #
    # confusionMatrix3 = multilabel_confusion_matrix(encodedTestLabels, predictionsrf3)
    # print(confusionMatrix3)
    #
    # confusionMatrix4 = multilabel_confusion_matrix(encodedTestLabels, predictionsrf4)
    # print(confusionMatrix4)
    #
    # confusionMatrix5 = multilabel_confusion_matrix(encodedTestLabels, predictionsrf5)
    # print(confusionMatrix5)



    logger.info('calcualting accuracy scores')


    accuractyScorerf1 = accuracy_score(encodedTestLabels, predictionsrf1)
    logger.info("accuracy score for model 1: {}".format(accuractyScorerf1))
    accuractyScorerf2 = accuracy_score(encodedTestLabels, predictionsrf2)
    logger.info("accuracy score for model 2: {}".format(accuractyScorerf2))

    accuractyScorerf3 = accuracy_score(encodedTestLabels, predictionsrf3)
    logger.info("accuracy score for model 3: {}".format(accuractyScorerf3))

    accuractyScorerf4 = accuracy_score(encodedTestLabels, predictionsrf4)
    logger.info("accuracy score for model 4: {}".format(accuractyScorerf4))

    accuractyScorerf5 = accuracy_score(encodedTestLabels, predictionsrf5)
    logger.info("accuracy score for model 5: {}".format(accuractyScorerf5))


```

```python

def main():
    starttime = time.time()
    logger.info('start time: {}'.format(starttime))

    trainAndTestModel()

    endtime = time.time() - starttime
    logger.info('run time: {}'.format(endtime))

if __name__=="__main__":
    main()
```


35.Close other programs before running the script. It is memory intensive and takes a few minutes to complete. Inspect the logs generated by the script. The function trained 5 models on different input features and then ran them on the test data set.
It calculated the accuracy score for each model by comparing the result vector from the predictions with the labels vector - (the `truth`) in our case.


### End of Lab 2
