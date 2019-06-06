# Lab 2

## Getting the code

* The project code is available on [RBC Enterprise Github](https://rbcgithub.fg.rbc.com/kft0/workshop)

* We are going to `clone` this code repository on our workstations using Git we setup earlier. Cloning gets us a copy of an exisiting Git repository.
    It is a smart way for developers and technicians to collaborate on work

1. Open terminal or command prompt 

2. Go to a directory of your preference (eg. C:/Development)

3. Run `git clone https://rbcgithub.fg.rbc.com/kft0/workshop` in a directory of your preference (eg. C:/Development)

4. If you are not able to clone, the repository folder is also available in your email. You can download and open this to continue.

5. Go into the **workshop** directory -- `cd workshop`

6. Install the virtualenv package using pip -- `pip3 install virtualenv --user`

7. You will setup a virtual environment. This makes sure any packages you install for this workshop do not intefere with your system's python packages

8. You should see 2 directories, `code` and `labs` and 1 `requirements.txt` file. The reqiurements file lists the packages you require for this workshop

9. Make a virtual environment in the workshop directory `python3 -m virtualenv venv`

10. Activate your virtual environment `source venv/bin/activate` on Macbook or `venv\bin\activate` on Windows

11. Run `pip install -r requirements.txt` to install packages in this virtual environment

12. Now we will go over the code. Data has been processed and made available in Elasticsearch for this workshop

13. Find `elasticPassword` (cmd+f `elasticPassword` on Mac or ctrl+f `elasticPassword` on Windows) in the `data_transfer` module.

14. Fill out the string with password on the white board

15. This is a temporary account configured to provide you access to Elasticsearch in this workshop

16. Step into the `code` directory

17. The `data_transfer` module is a python file that handles the data wrangling for our workshop. It is not our primal focus

18. The `intrusion_detection` file is where we will build our detection system

19. Lets add code step by step

20. The following code imports important modules and libraries that we will when building our models. Copy and paste this to the top of the `intrusion_detection` file




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


21.The following code disables some warnings and setups logging etc. to assist in our development. Copy and paste this.
  
  
  
  
   
```
simplefilter(action='ignore', category=FutureWarning)

logger = logging.getLogger('intrusion_detection_module')
logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s')
logger.setLevel(logging.DEBUG)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

```





22.We need a function to take data from Elastic and convert it into a Pandas DataFrame so its' easy to manipulate. Construct a function called `dataConversion` that will do this for us in `intrusion_detection`.

```
def dataConversion(data):
    logger.warning('converting elastic data to dataframe')
    dataframe = pandas.DataFrame(data)
    return dataframe
```


23.Circling back to the previous lab, you might have noticed some of the values in the dataset were non-numerical. This makes sense to us, but these values have no meaning to machines. We need to convert them to numerical values for the algorithm to make sense of the data.
What if we give numerical values to such data? For example, for days in a week - Mon, Tues, Wed; what if we assign 1 to Mon, 2 to Tues, 3 to Wed? 

24.This is a bad practice. It might lead to the algorithm placing more importance on higher numerical values

25.Instead we will use One Hot Encoding to pre-process our data. The process takes categorical variables and converts it into numerical representation without an arbitrary ordering

26.One Hot Encoding will take this table 

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


27.Write a function to one hot encode our dataframe. You should call it oneHotEncoding and it should accept a data frame to oneHotEncode. Pandas provides a helper function to do this.


```
def oneHotEncoding(data):
    logger.warning(msg='one hot encoding')
    encodedData = pandas.get_dummies(data)
    return encodedData
``` 

28.Next we will train our model using the Random Forest Classifier from scikit-learn. We will use our data to incrementally improve our model's ability to distinguish between normal and malicious connections
We can feed selective features to our training model based on domain knowledge and/or educated intuition

29.Write a function called `trainAndTestModel` . You will get data from elastic `data = data_transfer.get_data_from_elastic(index='kddcup-data')
`, followed by converting into dataframe `dataframe = dataConversion(data)` and then one-hot encoding `encodedData = oneHotEncoding(dataframe)
` . You will need to initialize a `rf = RandomForestClassifier()` and create a partial data frame of just the labels from the input encoded data.
After one-hot encoding, our labels will be 
```
'label_back.', 'label_buffer_overflow.', 'label_ftp_write.', 'label_guess_passwd.', 'label_imap.', 'label_ipsweep.', 'label_land.', \
'label_loadmodule.', 'label_multihop.', 'label_neptune.', 'label_nmap.', 'label_normal.', 'label_perl.', 'label_phf.', 'label_pod.',\
 'label_portsweep.', \
'label_rootkit.', 'label_satan.', 'label_smurf.', 'label_spy.', 'label_teardrop.', 'label_warezclient.', 'label_warezmaster.'                            
                                
```
Assign them to a variable called `encodedData`

```
encodedLabels = encodedData[['label_back.', 'label_buffer_overflow.', 'label_ftp_write.', 'label_guess_passwd.', 'label_imap.', 'label_ipsweep.', 'label_land.', \
                                 'label_loadmodule.', 'label_multihop.', 'label_neptune.', 'label_nmap.', 'label_normal.', 'label_perl.', 'label_phf.', 'label_pod.', 'label_portsweep.', \
                                 'label_rootkit.', 'label_satan.', 'label_smurf.', 'label_spy.', 'label_teardrop.', 'label_warezclient.', 'label_warezmaster.']]
```
30.Next, we will fit(train) our model on our training data set. The function will take features and labels as inputs. You can use any features that you think are the most important in grouping traffic data into malicious and normal buckets.

```
rf.fit(encodedData[['duration', 'logged_in']], encodedLabels)

```                             


31.Now, we will run our trained model on test data -- passing a similar data frame. The predict function will generate labels for the test data set based on the earlier training.

```
predictionsrf = rf.predict(encodedTestData[['duration', 'logged_in']])
```

32.You can find the accuracy score of your model by passing in the labels from the data ( the truth ) and the predictions returned by our model.

```
accuractyScorerf = accuracy_score(encodedTestLabels, predictionsrf)
print(accuracyScorerf)
```
    
    
33.Setup a main function and call the function you wrote to test it
```
def main():
    starttime = time.time()
    logger.info('start time: {}'.format(starttime))

    trainAndTestModel()

    endtime = time.time() - starttime
    logger.info('run time: {}'.format(endtime))

if __name__=="__main__":
    main()

```

34.We will now try a custom `trainAndTestModel` that tries out 5 different models  

```
def trainAndTestModel():
    data = data_transfer.get_data_from_elastic(index='kddcup-data')
    dataframe = dataConversion(data)
    encodedData = oneHotEncoding(dataframe)

    encodedLabels = encodedData[['label_back.', 'label_buffer_overflow.', 'label_ftp_write.', 'label_guess_passwd.', 'label_imap.', 'label_ipsweep.', 'label_land.', \
                                 'label_loadmodule.', 'label_multihop.', 'label_neptune.', 'label_nmap.', 'label_normal.', 'label_perl.', 'label_phf.', 'label_pod.', 'label_portsweep.', \
                                 'label_rootkit.', 'label_satan.', 'label_smurf.', 'label_spy.', 'label_teardrop.', 'label_warezclient.', 'label_warezmaster.']]

    logger.warning(msg='traing model rf1 on data')
    rf1 = RandomForestClassifier()
    rf1.fit(encodedData[['duration', 'logged_in']], encodedLabels)
    logger.warning(msg='training rf1 finished')


    logger.warning(msg='training model rf2 on data')
    rf2 = RandomForestClassifier()
    rf2.fit(encodedData[['duration', 'protocol_type_icmp', 'protocol_type_tcp', 'protocol_type_udp']], encodedLabels)
    logger.warning('training rf2 finised')


    ## basic features
    logger.warning(msg='training model rf3 on data')
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
    logger.warning('training rf3 finised')

    ## content features
    logger.warning(msg='training model rf4 on data')
    rf4 = RandomForestClassifier()
    rf4.fit(encodedData[['hot','num_failed_logins','logged_in', 'num_compromised', 'root_shell', 'su_attempted', 'num_root', 'num_file_creations', 'num_shells', 'num_access_files', \
                         'num_outbound_cmds', 'is_host_login', 'is_guest_login']], encodedLabels )
    logger.warning('training rf4 finished')

    ## traffic features
    logger.warning(msg='training model rf5 on data')
    rf5 = RandomForestClassifier()
    rf5.fit(encodedData[['count','serror_rate','rerror_rate','same_srv_rate','diff_srv_rate','srv_count','srv_serror_rate','srv_rerror_rate', 'srv_diff_host_rate']], encodedLabels )
    logger.warning('training rf5 finished')



    ## getting the test dataset from elastic
    logger.warning(' pulling in test data from elastic')
    testData = data_transfer.get_data_from_elastic(index='kddcup-data')
    logger.warning('converting test data into relevant data structures')
    testDataframe = dataConversion(testData)
    logger.warning('one hot encoding test data')
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
    print(accuractyScorerf1)

    accuractyScorerf2 = accuracy_score(encodedTestLabels, predictionsrf2)
    print(accuractyScorerf2)

    accuractyScorerf3 = accuracy_score(encodedTestLabels, predictionsrf3)
    print(accuractyScorerf3)

    accuractyScorerf4 = accuracy_score(encodedTestLabels, predictionsrf4)
    print(accuractyScorerf4)

    accuractyScorerf5 = accuracy_score(encodedTestLabels, predictionsrf5)
    print(accuractyScorerf5)



```