# Lab 0 
## Estimated time for completion: 15 minutes

## Setup and pre-requisites for this lab

### Python 3

#### Check if your system already has python 3.x

#### On MacOS
* Run `python3 --version`. If python 3 is configured, you will get the version number. If you get an error, then follow the steps below to download Python

#### On Windows
* Run `python --version`. If python 3 is properly configured and add to your `PATH` variable, then you will get the version number. Otherwise, follow the steps below to download Python

Go to https://www.python.org/downloads/ and download Python 3.7.x (preferred)

#### Download and configure Python

#### On MacOS
* Open the downloaded file. 
* Get admin rights through *Make me Admin - Launcher* in *Self Service*
* Next,open the python installer, accept the license and follow the prompts to finish installation. 
* This will install Python 3 on your system along with Python 2.x already on your computer.


#### On Windows
* Download the python executable for windows. 
* Open it, accept the license and follow the prompts
* **if the installation does not continue due to no admin rights, follow these steps**
    * Uncheck "install for all users" option
    * Go for the custom installation
    * On next screen specify the directory path for which your user have full access on the computer
    * Uncheck "create shortcuts for installed application" option
    * Make sure "Add python to environment variable" option is Unchecked
    * complete the installation

#### Validate the python installation
* Run `python3 --version` in a terminal on Mac or `python --version` on Windows make sure python is installed and ready for use on your system     
        
    
### PIP configuration
* PIP is a python package manager
* Check if pip is configured by running `pip install elasticsearch`. If install fails, pip is not configured correctly.
* It needs to be configured to allow you to download python packages through the artifactory mirror
* Create a pip config file with one of the following configurations (you will need to make the directories if there are not existent):
    * Windows:   %APPDATA%\pip\pip.ini
    * Unix: $HOME/.config/pip/pip.conf
    * Mac:  $HOME/.pip/pip.conf   


* Open the file in your favorite text editor and add the following code:
```
[global]
index-url = https://rbcartifactory.fg.rbc.com/artifactory/api/pypi/pypi/simple
trusted-host = rbcartifactory.fg.rbc.com 
```   



    
    
### Git Setup

#### Windows
* Download the executable [for windows here](https://git-scm.com/download/win)
* Follow this document [git setup on windows](https://rbc-confluence.fg.rbc.com:8443/display/CPS/Installing+Git+Bash+On+Your+Local?preview=%2F38736323%2F38736322%2FInstalling+Git+Bash+On+Your+Local.docx)

#### MacOS
* Download Git from [git executable for Mac](https://git-scm.com/download/mac)
* Get admin rights through *Make me Admin - Launcher* in *Self Service*
* Open the .pkg and follow the prompts to install git

#### Setting credentials for git
* Open a terminal/command prompt and type `git config --global credential.helper store
`
* The next time you pull or push, git will prompt you for credentials
* Use the same credentials that you login with on your computer






