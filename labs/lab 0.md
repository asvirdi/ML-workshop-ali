# Lab 0 
## Estimated time for completion: 15 minutes

## Setup and pre-requisites for this lab

### Python 3

#### Check if your system already has python 3.x

#### On MacOS
* Run `python3 --version`. If python 3 is configured, you will get the version number. If you get an error, then follow the steps below to download Python

#### On Windows
* Run `python --version`. If python 3 is properly configured and added to your `PATH` variable, then you will get the version number. Otherwise, follow the steps below to download Python

Go to [this link](https://www.python.org/downloads/) and download Python 3.7.x (preferred)

#### Download and configure Python

#### On MacOS
* Open the downloaded file. 
* Get admin rights through *Make me Admin - Launcher* in *Self Service*
* Next, open the python installer, accept the license and follow the prompts to finish installation. 
* This will install Python 3 on your system along with Python 2.x already on your computer.


#### On Windows
* Download the **64 bit** python executable for windows. 
* Open it, accept the license and follow the prompts
* **if the installation does not continue due to no admin rights, follow these steps**
    * Uncheck "install for all users" option
    * Go for the custom installation
    * On next screen specify the directory path for which your user has full access on the computer
    * Uncheck "create shortcuts for installed application" option
    * Make sure "Add python to environment variable" option is Unchecked
    * complete the installation
<!-- validate custom install on windows -->

#### Validate the python installation
* Run `python3 --version` in a terminal on Mac or `python --version` in a command prompt on Windows make sure python is installed and ready for use on your system     
        
    
### PIP configuration
* PIP is a python package manager
* Check if pip is configured by running `pip install elasticsearch`. If install fails, pip is not configured correctly.
    * If install is successful, run `pip uninstall elasticsearch` to clean up.
#### If you are on firms' machine then do the following configuration
* Pip needs to be configured to allow you to download python packages through the mirror





    
    
### Git Setup or ask for a zipped version of the lab

#### Windows
* Download the executable [for windows here](https://git-scm.com/download/win)


#### MacOS
* Download Git from [git executable for Mac](https://git-scm.com/download/mac)
* Get admin rights through *Make me Admin - Launcher* in *Self Service*
* Open the .pkg and follow the prompts to install git

#### Setting credentials for git
* Open a terminal/command prompt and type `git config --global credential.helper store

* The next time you pull or push, git will prompt you for credentials
* Use the same credentials that you login with on your computer




#### Restart any open terminals so they can pick up the above changes

### End of Lab 0




