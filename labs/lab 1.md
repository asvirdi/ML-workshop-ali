# Lab 1

## Estimated time for completion: 30 minutes
## Some Background

The problem under focus in this workshop is how to detect an intrusion in a network using network traffic data. We will build a predictive model using open source Python libraries that will help us solve this problem.

To be able to build our machine learning model, we require data on which we can train it. This data is critical to the predictions our model will make because it is our algorithm's only source of 'truth'.

Before proceeding further, lets hammer out some machine learning lingo:
* Dataset: A set of data examples, that contain features important to solving the problem
* Features: Important pieces of data that help us understand a problem that are fed in to a Machine Learning algorithm to help it learn.
Chossing the right features can help distinguish useful data from the noise
* Model: The internal representation of a phenomenon that a Machine Learning algorithm has learnt. It learns this from the data it is shown during training. The model is the output you get after training an algorithm. For example, a decision tree algorithm would be trained and produce a decision tree model.

There are more resources present at [Toward Data Science](https://towardsdatascience.com) for those anyone interested in digging deeper.

## The Dataset

The network traffic data set we will use today was used for the The Third International Knowledge Discovery and Data Mining Tools Competition in 1999.
This dataset has been used widely in the data science community for research purposes. The task description for the competition (and our workshop :) ) can be found [here](http://kdd.ics.uci.edu/databases/kddcup99/task.html).

### Getting up close with our data
* Open the [link](http://kdd.ics.uci.edu/databases/kddcup99/task.html) to the task description and go over it
* The data is about 4 gigabytes of compressed binary TCP dump data from 7 weeks of network traffic. A LAN simulating a typical US Air Force LAN was setup by Lincoln Labs and the network was peppered with multiple attacks to collect and label this data.
* What is a connection? 
    * A connection is a sequence of packets starting and ending at some well defined times
* Network traffic can be categorized into normal connections and malicious connections
* The malicious traffic can be further sub-categorized into 4 main categories:
    * DOS - Denial of Service attack
    * R2L - unauthorized access from a remote machine
    * U2R - unauthorized access to local superuser (root) 
    * Probing, for example port scanning
    

The rest of this section will dig deeper into the sub-categories of malicious traffic for those interested. Feel free to jump to the next section.

### Deriving Features from our data

Circling back to our earlier definition of features, they are critical in helping us shape our problem and as input parameter to our algorithm.
Some features can be derived from our dataset, which is present [here](http://kdd.ics.uci.edu/databases/kddcup99/kddcup99.html).

We will divide the features into 3 main categorizes: Basic, Content and Traffic. For example, Basic Features are:


| Feature name | Description | Type
-------------- | ----------- | ----
| duration | length (number of seconds) of the connection | continuous
| protocol_type |	type of the protocol, e.g. tcp, udp, etc. |	discrete
| service | network service on the destination, e.g., http, telnet, etc. |discrete
| src_bytes |	number of data bytes from source to destination  |	continuous
| dst_bytes |	number of data bytes from destination to source  | continuous
| flag | normal or error status of the connection  | discrete 
| land | 1 if connection is from/to the same host/port; 0 otherwise | discrete
| wrong_fragment | number of ``wrong'' fragments  | continuous
| urgent | number of urgent packets  | continuous


<!-- differentiate between continous and discrete -->

To gain more insight into the different kinds of features dervied from domain knowledge, you can revisit the task description.


**Wait for further instructions**


## Digging into the data

The instructor will load a sample dataset into a Pandas DataFrame and will observe the data with the class.

<!-- tell students that they do not need to follow but can if they want to -->

```python
## importing pandas
import pandas


## pointing to directory where the data file was downloaded
data_dir = "~/Downloads/"
train_data_10_percent = data_dir + "kddcup.data_10_percent"


## function to read data into a Pandas Data Frame 
data = pandas.read_csv(train_data_10_percent, header=None)


## looking into the data frame
data.describe()
data.head()


## there are no column headers!
## getting column headers from task description from the competitions' website
headers = ["duration","protocol_type", "service", "flag", "src_bytes","dst_bytes","land", "wrong_fragment", "urgent", "hot", "num_failed_logins"\
                    ,"logged_in", "num_compromised", "root_shell", "su_attempted", "num_root", "num_file_creations", "num_shells", "num_access_files", "num_outbound_cmds"\
                    ,"is_host_login", "is_guest_login", "count", "srv_count", "serror_rate", "srv_serror_rate", "rerror_rate", "srv_rerror_rate", "same_srv_rate"\
                    , "diff_srv_rate", "srv_diff_host_rate", "dst_host_count", "dst_host_srv_count", "dst_host_same_srv_rate", "dst_host_diff_srv_rate", "dst_host_same_src_port_rate"\
                    , "dst_host_srv_diff_host_rate", "dst_host_serror_rate", "dst_host_srv_serror_rate", "dst_host_rerror_rate", "dst_host_srv_rerror_rate", "label"]


## printing the number of headers for a sanity check    
print(len(headers))


## setting the column headers
data.columns = headers
data.describe()
 ```

### End of Lab 1
