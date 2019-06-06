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



def dataConversion(data):
    logger.warning('converting elastic data to dataframe')
    dataframe = pandas.DataFrame(data)
    return dataframe


def oneHotEncoding(data):
    logger.warning(msg='one hot encoding')
    encodedData = pandas.get_dummies(data)
    return encodedData


def randomForestTrain():
    data = data_transfer.get_data_from_elastic(index='kddcup-data')
    #print(len(data))
    dataframe = dataConversion(data)
    encodedData = oneHotEncoding(dataframe)
    #print(list(encodedData))
    #del dataframe

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
    testData =  data_transfer.get_data_from_elastic(index='kddcup-data-full')
    logger.warning('converting test data into relevant data structures')
    testDataframe = dataConversion(testData)
    logger.warning('one hot encoding test data')
    encodedTestData = oneHotEncoding(testDataframe)

    ## free up resources used in training
    del encodedLabels, encodedData, dataframe, data

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
    confusionMatrix1 = multilabel_confusion_matrix(encodedTestLabels, predictionsrf1)
    #print(confusionMatrix1)

    confusionMatrix2 = multilabel_confusion_matrix(encodedTestLabels, predictionsrf2)
    #print(confusionMatrix2)

    confusionMatrix3 = multilabel_confusion_matrix(encodedTestLabels, predictionsrf3)
    #print(confusionMatrix3)

    confusionMatrix4 = multilabel_confusion_matrix(encodedTestLabels, predictionsrf4)
    #print(confusionMatrix4)

    confusionMatrix5 = multilabel_confusion_matrix(encodedTestLabels, predictionsrf5)
    print(confusionMatrix5)



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






def main():
    starttime = time.time()
    logger.info('start time: {}'.format(starttime))
    randomForestTrain()
    endtime = starttime - time.time()
    logger.info('run time: {}'.format(endtime))

if __name__=="__main__":
    main()
