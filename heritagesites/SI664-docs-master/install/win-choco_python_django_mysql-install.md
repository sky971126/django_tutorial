# Windows 10: Setting up a Python 3.7.x, Django 2.1.x, MySQL 8.0.x Development Environment

I do my development work on a Mac. But I also run Windows 10 using [Parallels Desktop](https://www.parallels.com/).  What follows are the steps I took to set up a Python 3.x/Django 2.x dev environment in Windows, based in part on Lisa Tagliaferri's excellent [guide](#tagliaferri).
 
Outside the Parallels virtual machine (VM) I use [Homebrew](https://brew.sh/), a macOS package manager, to acquire and maintain a good deal of the software I use on a daily basis. Within Windows I turned to [Chocolatey](https://chocolatey.org/) to manage my installs of nano, Python and Git.  I use the [MySQL 8.0.x installer](https://dev.mysql.com/downloads/windows/installer/8.0.html) to install MySQL Server, MySQL Workbench and other related MySQL products. 

I installed Chocolatey using Windows [PowerShell](https://docs.microsoft.com/en-us/powershell/scripting/getting-started/getting-started-with-windows-powershell?view=powershell-6). Chocolatey can also be installed using `cmd.exe`. See the Chocolatey [install page](https://chocolatey.org/docs/installation) for directions.

The Chocolatey approach is but one way to manage software installs.  You may already have [Python 3.7.x](https://www.python.org/downloads/windows/), [nano](https://www.nano-editor.org/download.php), and [Git](https://git-scm.com/download/win) installed, and perhaps [MySQL 8.0.x](https://dev.mysql.com/downloads/windows/installer/8.0.html) too using each product's own installers.  If so, you can proceed directly to section 4.0 and review/follow the set up instructions for installing Django, initializing a Git working directory, and connecting your Django project to a MySQL 8.0.x database.

## TOC
* 1.0 [Configure Windows PowerShell](#powershell)
* 2.0 [Install Chocolatey](#chocoinstall)
* 3.0 [Add Chocolatey Packages](#chocopkgs)
* 4.0 [Create a Git Working directory](#gitworkingdir)
* 5.0 [Create a Django Project Virtual Environment](#venv)
* 6.0 [Generate the mysite project](#djangomysite)
* 7.0 [Install MySQL](#mysqlinstall)
* 8.0 [Create a MySQL User Account](#mysqluser)
* 9.0 [Create the Polls Database](#pollsdb)
* 10.0 [Install the Python mysqlclient Connector](#mysqlclient)
* 11.0 [Connect Django to MySQL](#connectdjangomysql)

## <a name="powershell">1.0 Configure Windows PowerShell</a>
Windows PowerShell is a command line shell for system administrators built on top of .Net. Administrative tasks are performed by running `cmdlets` (pronounced "command-lets").

### 1.1 Open PowerShell
Click the start menu icon (lower left corner).  Type "PowerShell" in the search box.  Then *right-click* on the "Windows PowerShell Desktop app" option and select "Run as administrator".  If prompted, click "Yes" to allow PowerShell to make changes to your device.  The PowerShell command line shell will then open displaying a prefix prompt of "PS".

:warning: Be sure that you are running PowerShell _as an administrator_ before executing the following commands.

```commandline
Windows PowerShell
Copyright (C) Microsoft Corporation. All rights reserved.

PS C:\Windows\system32>
```

Enter the following command in order to change directories to your user directory:

```commandline
PS C:\Windows\system32> cd ~
PS C:\Users\arwhyte>
```

When done with PowerShell (though not now), type "exit" and click enter.

```commandline
PS C:\Users\arwhyte> exit
```

### 1.2 Change PowerShell's Execution Policy
"Restricted" is the default execution policy.  It prevents you from running scripts.  Change PowerShell's execution policy to "RemoteSigned".  "RemoteSigned" will let you run scripts and configuration files downloaded from the Internet and signed by trusted publishers.

:warning: Note that a "trusted" script could still include malicious code so consider carefully what scripts you choose to execute when running under the new execution policy.

First, set the scope of the new execution policy to the current user (i.e., you).

```commandline
PS C:\Users\arwhyte> Set-ExecutionPolicy -Scope CurrentUser
```

PowerShell will then prompt you to select an Execution Policy.  Type "RemoteSigned" and then press `Enter`. PowerShell will then ask if you to change the current execution policy.  Type "y" (yes) and the "RemoteSigned" execution policy will be instituted.  To confirm the policy change enter the following command:

```commandline
PS C:\Users\arwhyte> Get-ExecutionPolicy -List
```

PowerShell's response should resemble the following output:

```
        Scope ExecutionPolicy
        ----- ---------------
MachinePolicy       Undefined
   UserPolicy       Undefined
      Process       Undefined
  CurrentUser    RemoteSigned
 LocalMachine       Undefined
```

## <a name="chocoinstall">2.0 Install Chocolatey</a>
[Chocolatey](https://chocolatey.org/) is a package manager for Windows. Like [Homebrew]
(https://brew.sh/) it simplifies installing, configuring, updating, and removing Windows software. Before downloading and running the Chocolatey install script, create a WebClient object called `$script` in order to share the Internet connection settings with Internet Explorer:

```commandline
PS C:\Users\arwhyte> $script = New-Object Net.WebClient
```

Then review the available properties and methods of the `$script` object by piping it to the `Get-Member` class:

```commandline
$script | Get-Member
```

A long list of methods and properties will be outputed to the screen. The `DownloadString` method 
is what we will use to download the Chocolatey install script.

```
...
DownloadString Method string DownloadString(string address), string DownloadString(uri address)
...
```

Implement the method:

```commandline
PS C:\Users\arwhyte> $script.DownloadString("https://chocolatey.org/install.ps1")
```

Then install Chocolatey:

```commandline
PS C:\Users\arwhyte> iwr https://chocolatey.org/install.ps1 -UseBasicParsing | iex
```

The `iwr`("Invoke-WebRequest") cmdlet will download and parse the Chocolatey install script before piping it on to the `iex` (Invoke-Expression) cmdlet which will execute install script.

Allow PowerShell to install Chocolatey.

## <a name="chocopkgs">3.0 Add Chocolatey Packages</a>
Now let's install nano, Python and Git.

### 3.1 nano
nano is a text editor with a command line interface that can be invoked within PowerShell to 
write programs.

:bulb: nano is not required for this exercise but since it can be [run inside](#masek) PowerShell as a file editor I went ahead and installed it. 

Issue the following `choco` command to install the nano [package](https://chocolatey.org/packages/nano):

```commandline
PS C:\Users\arwhyte> choco install -y nano
```

_Note_: The `-y` flag tells Chocolatey to execute the script without a formal confirmation prompt.

### 3.2 Python 3.7.x
Issue the following `choco` command to install the latest version of Python 3.7.x (currently 3.7.0) using the Chocolatey Python [package](https://chocolatey.org/packages/python):

```commandline
PS C:\Users\arwhyte> choco install -y python
```

_Note_: The default location of the Chocolatey Python 3.7.x install is:

```
C:\Python37
```

If you want to install Python in another location set the `/InstallDir` parameter to the location of your choice.

```commandline
PS C:\Users\arwhyte> choco install python3 --params "/InstallDir:C:\your\install\path"
```

The Windows `Path` environment variable is also updated as is indicated in the install output:

```
Chocolatey v0.10.11
Installing the following packages:
python
By installing you accept licenses for the packages.
Progress: Downloading python3 3.7.0... 100%
Progress: Downloading python 3.7.0... 100%

python3 v3.7.0 [Approved]
python3 package files install completed. Performing other installation steps.
Installing 64-bit python3...
python3 has been installed.
Installed to: 'C:\Python37'
  python3 can be automatically uninstalled.
Environment Vars (like PATH) have changed. Close/reopen your shell to
 see the changes (or in powershell/cmd.exe just type `refreshenv`).
 The install of python3 was successful.
  Software installed as 'exe', install location is likely default.

python v3.7.0 [Approved]
python package files install completed. Performing other installation steps.
 The install of python was successful.
  Software install location not explicitly set, could be in package or
  default install location if installer.

Chocolatey installed 2/2 packages.
 See the log for details (C:\ProgramData\chocolatey\logs\chocolatey.log).
 ```
You can check the Python installation location by starting Python in the shell and returning the path to the system executable:

```commandline
PS C:\> python
Python 3.7.0 (v3.7.0:1bf9cc5093, Jun 27 2018, 04:59:51) [MSC v.1914 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> import os
>>> import sys
>>> os.path.dirname(sys.executable)
'C:\\Python37'
>>> exit()
```

You can also confirm if the `PATH` environment variable has been updated by clicking the start menu icon (lower left corner) and searching for the "SystemPropertiesAdvanced" run command.  Then *right-click* on the "SystemPropertiesAdvanced" option and select "Run as administrator" to open the System Properties Advanced tab.  Click "Environment Variables . . ." and check the System variables `PATH` variable.  It should include paths to the Python 3.7.x directory:

```
C:\Python37\Scripts;
C:\Python37\;
```

Confirm that Python has been successfully installed by typing the command `refreshenv` to close/reopen PowerShell.

```commandline
PS C:\Users\arwhyte> refreshenv
Refreshing environment variables from registry for cmd.exe. Please wait...Finished..
PS C:\Users\arwhyte> python -V
Python 3.7.0
```

:confused: Running `refreshenv` did not work for me.  I had to exit PowerShell and then restart it
 (as administrator) in order to get it to recognize the addition of Python in the `PATH` environment variable.

### 3.3 Git
Issue the following `choco` command to install the Git [package](https://chocolatey.org/packages/git):

```commandline
PS C:\Users\arwhyte> choco install git -params "/GitAndUnixToolsOnPath"
```

Chocolatey will install git, the BASH tools and add each to your `PATH` environment variable.

### 3.4 Confirm Chocolatey package installs
Let's check what packages we've installed so far:

```commandline
PS C:\Users\arwhyte> choco list --local-only
Chocolatey v0.10.11
chocolatey 0.10.11
chocolatey-core.extension 1.3.3
git 2.18.0
git.install 2.18.0
nano 2.5.3
python 3.7.0
python3 3.7.0
7 packages installed.
```

Looks good. By the way, upgrading Chocolatey itself is easy:

```commandline
PS C:\Users\arwhyte> choco upgrade chocolatey
```

For other `choco` commands see the [Chocolatey Wiki](https://github.com/chocolatey/choco/wiki/CommandsReference) on Github.

## <a name="gitworkingdir">4.0 Create a Git Working directory</a>
I use [Git](https://git-scm.com/) as my distributed version control system and [Github](https://github.com/) to store and share my work.  If you don't have a Github account create one (it's free). I organize my development work locally by service (e.g., Bitbucket, Github) and by the organization or user account whose repos I choose to fork.  I offer this approach merely as an example; choose a directory structure for organizing your project work that makes sense to you.

```
Development\
    repos\
        bitbucket\
          ...
        github\
          apereo\
          arwhyte\
          csev\
          IMSGlobal\
          tsugiproject\
          ...
```

In my case, since I'm not basing my django project on some other individual's or organization's 
forked repo I'll create my project in the arwhyte\ folder:

```commandline
PS C:\Users\arwhyte> mkdir Development/repos/github/arwhyte/django_tutorial
```

Next, I initialize the empty django_tutorial directory as a Git repo:

```commandline
PS C:\Users\arwhyte> cd Development/repos/github/arwhyte/django_tutorial
PS C:\Users\arwhyte\Development\repos\github\arwhyte\django_tutorial> git init
Initialized empty Git repository in C:/Users/arwhyte/Development/repos/github/arwhyte/django_tutorial/.git/
```

You do the same.  Decide on a directory location for the Django project work.  Then initialize the directory as an empty Git repo.

That's enough Git for now.  We will do more with Git and Github later.  For a useful Git primer read Roger Dudler's [git - the simple guide](http://rogerdudler.github.io/git-guide/).

## <a name="venv">5.0 Create a Django Project Virtual Environment</a>
Next, create a virtual environment in order to isolate the Django project development work from other Python projects using the `virtualenv` package. If you are fuzzy on the purpose of virtual environments review Real Python's [Python Virtual Environments: a Primer](https://realpython.com/python-virtual-environments-a-primer/)

### 5.1 Upgrade pip
However, before installing `virtualenv` make sure that the latest version of `pip`, Python's own package manager, is installed locally:

```commandline
PS C:\Users\arwhyte> python -m pip install --upgrade pip
Collecting pip
  Using cached https://files.pythonhosted.org/packages/5f/25/e52d3f31441505a5f3af41213346e5b6c221c9e086a166f3703d2ddaf940/pip-18.0-py2.py3-none-any.whl
Installing collected packages: pip
  Found existing installation: pip 10.0.1
    Uninstalling pip-10.0.1:
      Successfully uninstalled pip-10.0.1
Successfully installed pip-18.0
```

### 5.2 Install virtualenv
Once `pip` is updated, use it to install the `virtualenv` package.

```commandline
PS PS C:\Users\arwhyte> pip install virtualenv
```

### 5.3 Create the Virtual Environment
Now create a virtual environment for your django project.  Create it from within the project root directory:

```commandline
PS C:\Users\arwhyte> cd Development\repos\github\arwhyte\django_tutorial
PS C:\Users\arwhyte\Development\repos\github\arwhyte\django_tutorial> virtualenv venv
Using base prefix 'c:\\python37'
New python executable in C:\Users\arwhyte\Development\repos\github\arwhyte\django_tutorial\venv\Scripts\python.exe
Installing setuptools, pip, wheel...done.
```

### 5.4 Activate the Virtual Environment
:warning: You __must__ activate the virtual environment before adding project-specific Python 
packages such as Django.

```commandline
PS C:\Users\arwhyte\Development\repos\github\arwhyte\django_tutorial> venv\Scripts\activate
(venv) PS C:\Users\arwhyte\Development\repos\github\arwhyte\django_tutorial>
```

When activated the prompt is prefixed with the name of the virtual environment (e.g., "(venv)").

To deactivate the virtual environment run:

```commandline
(venv) PS C:\Users\arwhyte\Development\repos\github\arwhyte\django_tutorial> deactivate
PS C:\Users\arwhyte\Development\repos\github\arwhyte\django_tutorial>
```

### 5.5 Install Django
After activating the django_tutorial virtual environment, install Django:

```commandline
(venv) PS C:\Users\arwhyte\Development\repos\github\arwhyte\django_tutorial> pip install Django
```

### 5.6 Confirm Virtual Environment Installed Packages
Check the installed packages in your django project virtual environment:

```commandline
(venv) PS C:\Users\arwhyte\Development\repos\github\arwhyte\django_tutorial> pip list
Package    Version
---------- -------
Django     2.1.1
pip        18.0
pytz       2018.5
setuptools 40.2.0
wheel      0.31.1
```

:bulb: You can also confirm that Django is installed this way:

```commandline
(venv) PS C:\Users\arwhyte\Development\repos\github\arwhyte\django_tutorial> python -m django --version
```

## <a name="djangomysite">6.0 Generate the mysite project</a>
From within your Django project root directory, create the "mysite" project by issuing the 
django-admin "startproject" command. Note the inclusion of a trailing dot ('.') following "mysite":

```commandline
(venv) PS C:\Users\arwhyte\Development\repos\github\arwhyte\django_tutorial> django-admin startproject mysite .
```

:warning: Make sure you include the trailing dot ('.') in the command.  The dot creates the new 
project with a directory structure that simplifies deployment to a server.  If you neglect to include the dot, delete the directories and files that were created (except 'venv') and run the command again along with the trailing doc ('.').

Generating `mysite` results in the following project layout:

```
django-tutorial/
    manage.py
    mysite/
        __init__.py
        settings.py
        urls.py
        wsgi.py
```

### 6.1 Start the Development Server
Start up the development server by issuing the `runserver` command:

```commandline
(venv) PS C:\Users\arwhyte\Development\repos\github\arwhyte\django_tutorial> python manage.py runserver
Performing system checks...

System check identified no issues (0 silenced).

You have 15 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, auth, contenttypes, sessions.
Run 'python manage.py migrate' to apply them.
September 05, 2018 - 23:14:55
Django version 2.1.1, using settings 'mysite.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
[05/Sep/2018 23:15:07] "GET / HTTP/1.1" 200 16348
[05/Sep/2018 23:15:07] "GET /static/admin/css/fonts.css HTTP/1.1" 200 423
[05/Sep/2018 23:15:07] "GET /static/admin/fonts/Roboto-Regular-webfont.woff HTTP/1.1" 200 80304
[05/Sep/2018 23:15:07] "GET /static/admin/fonts/Roboto-Bold-webfont.woff HTTP/1.1" 200 82564
[05/Sep/2018 23:15:07] "GET /static/admin/fonts/Roboto-Light-webfont.woff HTTP/1.1" 200 81348
```

:bulb: Ignore the database migration warnings; you will address them momentarily.

Open a web browser and point to `http://127.0.0.1:8000/`.  Confirm that the Django "The install worked successfully! Congratulations!" page successfully loads.

### 6.2 Stop the Development Server
Once confirmed, shut down the development server by typing `Control` - `c`.

## <a name="mysqlinstall">7.0 Install MySQL</a>
I don't use Chocolatey for installing and maintaining MySQL.  Instead, download and run the MySQL Community Edition 8.0.x Windows [installer](https://dev.mysql.com/downloads/windows/installer/8.0.html). See the MySQL 8.0 Reference Documentation for [Windows installation](https://dev.mysql.com/doc/refman/8.0/en/windows-installation.html) advice.

A useful short video that walks the install process can be watched [here](https://www.youtube.com/watch?v=Ddx13KlW8yQ).

:bulb: Choose the "mysql-installer-web-community-8.0.*.0.msi" file for online connections (\* = patch number, e.g. 8.0.12).

:warning: Run the installer as an administrator.

You will be prompted to sign in or create an Oracle account prior to performing this operation.  Once authenticated, click the fat blue "Download Now" button to initiate the install process.  

:bulb: You can also click "No thanks, just start my download" to bypass account creation/login.

Select "Run" when Windows asks what to do with the *.msi file and then select "Yes" when prompted to allow the installer to make changes to your device.

### 7.1 License Agreement Screen / Choosing a Setup Type Screen
The installer will search for previously installed packages.  Assuming previous installs are not found, agree to the license terms and then choose your setup type.  I chose "Custom".  Then click the "Next" button.

### 7.2 Select Products and Features Screen
The left-side box of the "Select Products and Features" screen lists the available products:

```
+ MySQL Servers
+ Applications
+ MySQL Connectors
+ Documentation
```

Click the "+" sign in front of "MySQL Servers" and select the appropriate MySQL Server for your machine.  Then click the green right arrow button to move the selection to the right-hand box.  Repeat the selection process for the following products, clicking through until you reach each of the featured product installs and then moving them to the right-hand box:

* MySQL Workbench 8.x
* MySQL Shell 8.0.x
* MySQL Router 8.x
* MySQL Documents 8.x
* MySQL Notifier 1.1.x
* MySQL Utilities

After completing selection of MySQL products to install click the "Next" button.

### 7.3 Check Requirements Screen
You may encounter a "Check Requirements" screen.  Depending on previous Window product installs you may need to install additional software (e.g., Microsoft Visual C++ 2015 Redistributable).  Select the required software and click the "Execute" button.  Once all the required software is installed click the "Next" button.

:warning: MySQL Server 8.0.X products *require* installation of the Microsoft Visual C++ 2015 Redistributable Package in order to run on Windows platforms. You should be prompted Make sure the package has been installed on the system before installing the server. The package is available at the Microsoft Download Center. Additionally, MySQL debug binaries require Visual Studio 2015 to be installed.

### 7.4 Installation Screen
Click the "Execute" button to initiate installation of the MySQL products you have selected.  Once all products are installed click the "Next" button.

### 7.5 Product Configuration
Use the configuration wizard to adjust product settings.  Click the "Next" button to begin.

#### 7.5.1 Group Replication Screen
Select "Standalone MySQL Server /Classic MySQL Replication".  Click the "Next" button.

#### 7.5.2 Type and Networking Screen
* Server Configuration Type
  - select "Development Computer"
* Connectivity
  - Accept defaults (TCP/IP; Port Number: 3306 (unless already in use), etc.)
* Advanced Configuration
  - Skip

Click the "Next" button.

#### 7.5.3 Authentication Method Screen
Select "Use Strong Password Encryption for Authentication". Click the "Next" button.

#### 7.5.4 Accounts and Roles Screen
* Root Account Password
  - Provide a password for the "Root" user.  
  - :warning: Write this password down and store it in a safe place.  You *will need it* later.
* MySQL User Accounts
  - Skip. You will add other users later.

Click the "Next" button.    

#### 7.5.5 Windows Service Screen
* Click the check box for "Configure MySQL as a Windows Service".  
  - :warning: Left unchecked MySQL Server will require a manual start in order to use it.
* Windows Service Details
  - Set Windows Service Name to "MySQL80"
  - Click the check box for "Start the MySQL Server at System Startup".
* Run Windows Service as ...
  - Select "Standard System Account".  

Click the "Next" button.

#### 7.5.6 Plugins and Extensions Screen
Ignore and click the "Next" button.

#### 7.5.7 Apply Configuration Screen
Click the "Execute" button to apply the configuration changes. Upon completion click the "Next" button.

#### 7.5.8 Installation Complete Screen
Click the "Finish" button.

## <a name="mysqluser">8.0 Create a MySQL User Account</a>
To confirm that all is well with the install log into the shell as the root user and issue the `SHOW DATABASES` command. You can use either PowerShell or cmd.exe.

```commandline
PS C:\> mysql --user=root --password
Enter password: *********
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 39
Server version: 8.0.12 MySQL Community Server - GPL

Copyright (c) 2000, 2018, Oracle and/or its affiliates. All rights reserved.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> SHOW DATABASES;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| sys                |
+--------------------+
4 rows in set (0.06 sec)
```

:warning: Also, confirm that you can see the `C:\ProgramData` directory (hidden by default) in 
the Windows File Explorer. MySQL databases as well as the `my.ini` options file are stored in 
`C:\ProgramData\MySQL\MySQL Server 8.0`. If `C:\ProgramData` is not visible, follow these 
[directions](https://www.tenforums.com/tutorials/9168-show-hidden-files-folders-drives-windows-10-a.html) to adjust the File Explorer view settings so that otherwise hidden directories and files
 are displayed.

### 8.1 Create User and Grant Privileges
I prefer to use a named user (arwhyte) rather than the root user for administering the MySQL 
server.  Using the MySQL shell issue the following three statements:

* CREATE USER . . . ;
* GRANT ALL PRIVILEGES ON . . . ;
* FLUSH PRIVILEGES . . . ; 

:warning: You must terminate each SQL statement with a semi-colon (";").

:bulb: Replace 'arwhyte' and 'MyPassword' with a name and password of your choosing.

```mysql
CREATE USER 'arwhyte'@'localhost' IDENTIFIED WITH mysql_native_password BY 'MyPassword';
GRANT ALL PRIVILEGES ON *.* TO 'arwhyte'@'localhost' WITH GRANT OPTION;
CREATE USER 'arwhyte'@'%' IDENTIFIED WITH mysql_native_password BY 'MyPassword';
GRANT ALL PRIVILEGES ON *.* TO 'arwhyte'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES;
```

:confused: Originally I used the new [caching SHA-2 pluggable authentication](https://dev.mysql.com/doc/refman/8.0/en/caching-sha2-pluggable-authentication.html) algorithm to create my password.  However, I encountered connection issues so switched back to MySQL's [native pluggable authentication](https://dev.mysql.com/doc/refman/8.0/en/native-pluggable-authentication.html) in the statement issued above.

```mysql
CREATE USER 'arwhyte'@'127.0.0.1' IDENTIFIED WITH caching_sha2_password BY 'somePassword';
GRANT ALL PRIVILEGES ON *.* TO 'arwhyte'@'127.0.0.1' WITH GRANT OPTION;
FLUSH PRIVILEGES;
```

For additional information on adding users see the MySQL 8.0 Reference Documentation [6.3.2 Adding User Accounts](https://dev.mysql.com/doc/refman/8.0/en/adding-users.html).

### 8.2 Obfuscate User Password
Next, use the `mysql_config_editor` client utility to store your user account's authentication credentials in an obfuscated login path file named `.mylogin.cnf`. The file location is the %APPDATA%\MySQL directory on Windows.

:bulb: Do not attempt to run the `mysql_config_editor` while logged in to MySQL shell (it will 
fail to execute).  Open a new terminal session or close your existing MySQL shell session before running it.

:warning: Replace 'arwhyte' with the name of the user account you created above and then add the 
password you earlier created when prompted.
  
```commandline
PS C:\> mysql_config_editor set --login-path=client --host=localhost --user=arwhyte --password
```

To confirm that the operation was successful invoke the `print` method:

```commandline
PS C:\> mysql_config_editor print --all
[client]
user = arwhyte
password = *****
host = localhost
```

With your password obfuscated you can now log into the MySQL shell without specifying a password 
argument:

```commandline
PS C:\> mysql --user=arwhyte
```

:bulb: As an added benefit, if you specify this MySQL user account (or another using the same password) as the database user in your Django project's mysite `settings.py` file, you will not need to reference the user's password in the settings file.

For additional information on obfuscating passwords see the MySQL 8.0 Reference Documentation [4.6.7 mysql_config_editor — MySQL Configuration Utility](https://dev.mysql.com/doc/refman/8.0/en/mysql-config-editor.html).

## <a name="pollsdb">9.0 Create the Polls Database</a>

Create a MySQL polls database by issuing the following command in the MySQL shell:

```mysql
CREATE DATABASE polls;
```

:warning: You must terminate the SQL statement with a semi-colon (";").

## <a name="mysqlclient">10.0 Install the Python mysqlclient Connector</a>
The Django Team [recommends](https://docs.djangoproject.com/en/2.1/ref/databases/#mysql-notes) 
using the [mysqlclient](https://pypi.python.org/pypi/mysqlclient) to connect to MySQL.  Install it using `pip`.

```commandline
(venv) PS C:\Users\arwhyte\Development\repos\github\arwhyte\django-tutorial-mysql> pip install mysqlclient
```

:warning: :rage: More than likely the install attempt will fail with an ugly error message that I've slimmed down to the following line:

```
...
 _mysql.c(29): fatal error C1083: Cannot open include file: 'mysql.h': No such file or directory
    error: command 'C:\\Program Files (x86)\\Microsoft Visual Studio\\2017\\BuildTools\\VC\\Tools\\MSVC\\14.15.26726\\bin\\HostX86\\x64\\cl.exe' failed with exit status 2
...
```

:wink: I was able to resolve this roadblock by resorting to Christoph Gohlke's collection of 
[Unoffical Windows Binaries for Python Extension Packages](https://www.lfd.uci.edu/~gohlke/pythonlibs/). Download the appropriate the [mysqlclient](https://www.lfd.uci.edu/~gohlke/pythonlibs/#mysqlclient) the wheel (*.whl) file.  For Python 3.7 click on "mysqlclient‑1.3.13‑cp37‑cp37m‑win_amd64.whl" and it will download to your machine.  Then perform a *manual install* of the package via `pip`:

```commandline
(venv) PS C:\Users\arwhyte\Development\repos\github\arwhyte\django-tutorial-mysql> pip install C:\Users\arwhyte\Downloads\mysqlclient-1.3.13-cp37-cp37m-win_amd64.whl
Processing c:\users\arwhyte\downloads\mysqlclient-1.3.13-cp37-cp37m-win_amd64.whl
Installing collected packages: mysqlclient
Successfully installed mysqlclient-1.3.13
```

## <a name="connectdjangomysql">11.0 Connect Django to MySQL</a>
Now connect the Django project to the MySQL polls database.

### 11.1 Update settings.py
Comment out or replace the default SQLite connection settings in databases section of the Django 
mysite `settings.py` file with the following Python dictionary, replacing the 'USER' value with 
your MySQL user account name:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'polls',
        'USER': 'arwhyte',
        'OPTIONS': {
            'read_default_file': 'C:\ProgramData\MySQL\MySQL Server 8.0\my.ini',
        }
    }
}
```

Note that the `read_default_file` property assumes a standard MySQL install path where the `my.ini` options file can be found.

:bulb: Later you will create a 'django' user with reduced privileges that are scoped to certain 
database schemas only (e.g., polls, test_polls).

### 11.2 Run migrations
Next, populate the polls database with the tables required to support both the app and Django's adminstration site using the `migrate` command.  If you earlier created a polls app when working with the default SQLite back-end, the polls models will be included in the migration.

:warning: You must activate the virtual environment before issuing this and the other `manage.py` commands described below.

```commandline
(venv) PS C:\Users\arwhyte\Development\repos\github\arwhyte\django-tutorial-mysql> python manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, polls, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying admin.0003_logentry_add_action_flag_choices... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying polls.0001_initial... OK
  Applying sessions.0001_initial... OK
```

### 11.3 Create a Django superuser account
To access the Django administration site, create a superuser account, providing a username, email address and password:

```commandline
(venv) PS C:\Users\arwhyte\Development\repos\github\arwhyte\django-tutorial-mysql> python manage.py createsuperuser
Username (leave blank to use 'arwhyte'):
Email address: arwhyte@umich.edu
Password:
Password (again):
Superuser created successfully.
```

### 11.4 Create the Django tutorial polls app
If you have not done so already, create a skeletal implementation of the Django tutorial polls app:

```commandline
(venv) PS C:\Users\arwhyte\Development1\repos\github\arwhyte\django_tutorial> python manage.py startapp polls
```

The skeletal polls app possesses the following structure:

```
polls/
    __init__.py
    admin.py
    apps.py
    migrations/
        __init__.py
    models.py
    tests.py
    views.py
```

### 11.5 Start/Continue the Django Team Polls Tutorial
Either start or continue working on the Django Team's Polls [tutorial](https://docs.djangoproject.com/en/2.1/intro/tutorial01/). You may need to run additional migrations to update the MySQL polls database and/or recreate questions created earlier when the polls app was connected to the SQLite database.

## Sources
<a name="masek">Masek, P</a>. Medium: [Text Editor inside PowerShell](https://medium.com/powershell-explained/text-editor-inside-powershell-22d2f5e748b8).  15 March 2017.

<a name="phpsword">PhpSword</a>. YouTube: [Download & Install MySQL 8.0.11 on Windows 10 Operating System](https://www.youtube.com/watch?v=Ddx13KlW8yQ). 25 April 2018.

<a name="tagliaferri">Tagliaferri, L.</a> Digital Ocean: 
[How to Install Python 3 and Set Up a Local Programming Environment in Windows 10](https://www.digitalocean.com/community/tutorials/how-to-install-python-3-and-set-up-a-local-programming-environment-on-windows-10). 24 October 2016.

## License
<a rel="license" href="http://creativecommons.org/licenses/by/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International License</a>.
