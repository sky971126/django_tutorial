# macOS 10.13.x (High Sierra): Setting up a Python 3.7.x, Django 2.1.x, MySQL 8.0.x Development 
I do my development work on a Mac. I use [Homebrew](https://brew.sh/), a macOS package manager, to acquire and maintain a good deal of the software I use on a daily basis, including Python and Git. An exception is MySQL.  I use the [MySQL 8.0.x installer](https://dev.mysql.com/downloads/windows/installer/8.0.html) to install MySQL Server, MySQL Workbench and other related MySQL products. 

The Homebrew approach is but one way to manage software installs.  In the case of Python on a Mac
 it is often described as the [recommended way](https://python-docs.readthedocs.io/en/latest/starting/install3/osx.html) to install and maintain it. That said, you may already have [Python 3.7.x](https://www.python.org/downloads/windows/) and [Git](https://git-scm.com/download/win) installed, and perhaps [MySQL 8.0.x](https://dev.mysql.com/downloads/windows/installer/8.0.html) too using each product's own installers.  If so, you can proceed directly to section 4.0 and review/follow the set up instructions for installing Django, initializing a Git working directory, and connecting your Django project to a MySQL 8.0.x database.

## TOC
* 1.0 [Install Xcode](#xcodeinstall)
* 2.0 [Install Homebrew](#homebrewinstall)
* 3.0 [Install Homebrew Python and Git Packages](#homebrewpkgs)
* 4.0 [Create a Git Working directory](#gitworkingdir)
* 5.0 [Create a Django Project Virtual Environment](#venv)
* 6.0 [Generate the mysite project](#djangomysite)
* 7.0 [Install MySQL](#mysqlinstall)
* 8.0 [Create a MySQL User Account](#mysqluser)
* 9.0 [Create a MySQL Options File](#mysqloptions)
* 10.0 [Create the Polls Database](#pollsdb)
* 11.0 [Install the Python mysqlclient Connector](#mysqlclient)
* 12.0 [Connect Django to MySQL](#connectdjangomysql)


## <a name="xcodeinstall">1.0 Install Xcode</a>
[Xcode](https://developer.apple.com/xcode/) is Apple's integrated development environment (IDE). Homebrew requires access to Xcode's developer tools.  First, check if Xcode is already installed:
 
```commandline
$ xcode-select -p
```

If the command outputs

```
/Applications/Xcode.app/Contents/Developer
```

then the full Xcode package is installed and you are ready to install Homebrew.  If, on the other
 hand, Xcode is not installed on your machine visit the Apple App Store, search for "Xcode", and install it (it's free).

## <a name="homebrewinstall">2.0 Install Homebrew</a>
[Homebrew](https://brew.sh/) describes itself as "the missing package manager for macOS".  I use it to manage curl, Git, GnuPG, Heroku, Hugo, Maven, nano, OpenSSL, Pandoc, PHP, Python, Ruby, SQLite and a number of other software installs.  

Open the terminal (I use [iTerm2](https://www.iterm2.com/)) and run the following script to install Homebrew:  

```commandline
$ /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

Confirm that Homebrew is healthy and ready to `brew`:

```commandline
$ brew doctor
```

If the command outputs

```commandline
Your system is ready to brew
```

the install was successful.

### 2.1 Update the PATH Environment Variable
Homebrew requires that the `/usr/local/bin` directory be listed first in your `PATH` environment 
variable. 

Use the command line text editor [nano](https://www.nano-editor.org/) to open your ~/.bash_profile:  

```commandline
$ nano ~/.bash_profile
```

If nano is not installed (e.g., the command fails) install it using the following nano [formula]
(http://brewformulas.org/Nano):

```commandline
$ brew install nano
```

Once ~/.bash_profile is open, add or edit `PATH` environment variable listing `usr/local/bin` 
before any other directories referenced in `PATH`.

```bash
export PATH="/usr/local/bin:$PATH"
``` 

Write out the change by holding down the "control" and "o" keys (CTRL - o), then press the return 
key when "File Name to Write: .bash_profile" is displayed. Then exit nano by holding down the 
"control" and "x" keys (CTRL - x).

To activate the changes in your current terminal session, issue the `source` command:

```commandline
$ source ~/.bash_profile
```

## <a name="homebrewpkgs">3.0 Install Homebrew Python and Git Packages</a>
Now let's install Python and Git.

### 3.1 Python 3.7.x
First confirm your existing Python installs:

Python 2.x (the default version installed on all Macs)
```commandline
$ python --version
Python 2.7.15
```

Python 3.x 
```commandline
$ python3 --version
Python 3.7.0
```

:bulb: If Python 3.x is installed but the version is not the latest (currently 3.7.0), consider running Dr Chuck's Python 3 [uninstaller](https://github.com/csev/uninstall-python3) shell script. Then reinstall Python 3 using Homebrew.  

Issue the following [formula](http://brewformulas.org/Python) to install Python 3.7.x (pip and Setuptools are included)

```commandline
$ brew install python
```

Next, confirm which Python location your terminal session recognizes:

```commandline
$ which python3
```

If the output is `/usr/local/bin/python3` your `PATH` variable in `~/.bash_profile` is set 
correctly. If a different path is returned recheck your `~/.bash_profile` as described above.

:bulb: The "python3" brew [formula](http://brewformulas.org/Python3) is now inactive.

:warning: When you `brew install` formulae that provide Python bindings, you should not be in an active virtual environment.  See Homebrew Documentation: [Python](https://docs.brew.sh/Homebrew-and-Python.html).

### 3.3 Git
Issue the following [formula](http://brewformulas.org/Git) to install Git 2.1.x

```commandline
$ brew install git
```

### 3.4 Confirm Homebrew package installs
Enter `brew list` in the terminal to return a list of package installs:

```commandline
$ brew list --versions
```

### 3.5 Ugrading Homebrew packages
Run the following commands periodically (I do so daily) to update formulas, upgrade packages, confirm installs, and delete outdated packages.

```commandline
$ brew update
$ brew upgrade
$ brew doctor
$ brew cleanup
```

For other `brew` commands see Tom O'Dwyer's [Useful homebrew commands](https://tomodwyer.com/post/2017-02-19-useful-homebrew-commands/).

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
$ mkdir ~/Development/repos/github/arwhyte/django_tutorial
```

Next, I initialize the empty django_tutorial directory as a Git repo:

```commandline
$ cd ~/Development/repos/github/arwhyte/django_tutorial
kathrada:django_tutorial arwhyte$ git init
Initialized empty Git repository in /Users/arwhyte/Development/repos/github/arwhyte/django_tutorial/.git/
```

You do the same.  Decide on a directory location for the Django project work.  Then initialize the directory as an empty Git repo.

That's enough Git for now.  We will do more with Git and Github later.  For a useful Git primer read Roger Dudler's [git - the simple guide](http://rogerdudler.github.io/git-guide/).

## <a name="venv">5.0 Create a Django Project Virtual Environment</a>
Next, create a virtual environment in order to isolate the Django project development work from other Python projects using the `virtualenv` package. If you are fuzzy on the purpose of virtual environments review Real Python's [Python Virtual Environments: a Primer](https://realpython.com/python-virtual-environments-a-primer/)

### 5.1 Upgrade pip
However, before installing `virtualenv` make sure that the latest version of `pip`, Python's own package manager, is installed locally:

```commandline
$ python3 -m pip install --upgrade pip
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
$ pip3 install virtualenv
```

### 5.3 Create the Virtual Environment
Now create a virtual environment for your django project.  Create it from within the project root directory:

```commandline
$ cd ~/Development/repos/github/arwhyte/django_tutorial
kathrada:django_tutorial arwhyte$ virtualenv venv
Using base prefix '/usr/local/Cellar/python/3.7.0/Frameworks/Python.framework/Versions/3.7'
New python executable in /Users/arwhyte/Development/repos/github/arwhyte/django_tutorial/venv/bin/python3.7
Also creating executable in /Users/arwhyte/Development/repos/github/arwhyte/django_tutorial/venv/bin/python
Installing setuptools, pip, wheel...done.
```

### 5.4 Activate the Virtual Environment
You __must__ activate the virtual environment before adding project-specific Python packages such
 as Django.

```commandline
$ source venv/bin/activate
(venv) $
```

When activated the prompt is prefixed with the name of the virtual environment (e.g., "(venv)").

To deactivate the virtual environment run:

```commandline
(venv) $ deactivate
```

### 5.5 Install Django
After activating the django_tutorial virtual environment, install Django:

```commandline
(venv) $ pip3 install Django
```

### 5.6 Confirm Virtual Environment Installed Packages
Check the installed packages in your django project virtual environment:

```commandline
(venv) $ pip3 list
Package    Version
---------- -------
Django     2.1.1
pip        18.0
pytz       2018.5
setuptools 39.2.0
virtualenv 16.0.0
wheel      0.31.1
```

## <a name="djangomysite">6.0 Generate the mysite project</a>
From within your Django project root directory, create the "mysite" project by issuing the 
django-admin "startproject" command. Note the inclusion of a trailing dot ('.') following "mysite":

```commandline
(venv) $ django-admin startproject mysite .
```

:warning: Make sure you include the trailing dot ('.') in the command.  The dot creates the new project with a directory structure that simplifies deployment to a server.  If you neglect to include the dot, delete the directories and files that were created (except 'venv') and run the command again along with the trailing doc ('.').

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
(venv) $ python manage.py runserver
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
Once confirmed, shut down the development server by holding down the "Control" and "c" keys (CTRL -
 c).

## <a name="mysqlinstall">7.0 Install MySQL</a>
I don't use Homebrew for installing and maintaining MySQL.  Instead, [download](https://dev.mysql.com/downloads/mysql/) and install the MySQL Server Community Edition 8.0.x (currently 8.0.12), macOS 10.13 (x86, 64-bit) `mysql-8.0.12-macos10.13-x86_64.dmg` archive file.

You will be prompted to sign in or create an Oracle account prior to performing this operation. Once authenticated, click the fat blue "Download Now" button to initiate the install process. 

:bulb: You can also click "No thanks, just start my download" to bypass account creation/login.

Double-click the *.dmg archive file to open it, and then click on the *.pkg file to start the installer. Click through to the license screen, accept it, then click the "Install" button (do not change the install location). After the installer prompts you for your password, the installation process will commence.

### 7.1 Authentication Method Screen
Select "Use Strong Password Encryption for Authentication". Click the "Next" button.

### 7.2 Root User Password Screen
Provide a password for the "root" user.  
  
:warning: Write this password down and store it in a safe place.  You *will need it* later.

:warning: Leave checked "Start MySQL Server once the installation is complete."

Click the "Finish" button and then provide your system password if prompted in order to complete the installation.

:bulb: If you choose not to move the installer *.dmg to the Trash, remember to eject the mounted 
volume via the Finder. 

### 7.3 MySQL installation location
The default installation directory is `/usr/local/`.

```commandline
$ cd /usr/local
kathrada:local arwhyte$ ls -la
total 0
drwxr-xr-x   21 root     wheel   672 Aug 10 21:54 .
drwxr-xr-x@  10 root     wheel   320 Mar 23 14:49 ..
...
lrwxr-xr-x    1 root     wheel    30 Aug 10 20:54 mysql -> mysql-8.0.12-macos10.13-x86_64
drwxr-xr-x   13 root     wheel   416 Aug 10 20:55 mysql-8.0.12-macos10.13-x86_64
...
```

### 7.4 MySQL Preference Pane
The default installation also install a [MySQL Preference Pane](https://dev.mysql
.com/doc/mysql-osx-excerpt/8.0/en/osx-installation-prefpane.html) in your Mac's System 
Preferences. You can use it to start/stop MySQL Server, initialize the 
database (recreate the /data directory), tweek configurations, and uninstall MySQL Server.

Open System Preferences and check the MySQL Preference Pane and confirm that MySQL Server is 
running (green indicator icon is good).

Read more about the MySQL Preference Pane [here](https://dev.mysql.com/doc/mysql-osx-excerpt/8.0/en/osx-installation-prefpane.html).

### 7.5 Add /usr/local/mysql/bin to PATH
Open ~/.bash_profile with nano in the terminal and add MySQL to the `PATH` environment variable 
in order to simplify referencing MySQL client applications when using the terminal:

```commandline
$ nano ~/.bash_profile
```

Add the following lines:

```bash
# MySQL
export MYSQL_HOME="/usr/local/mysql"
```
Then add the "$MYSQL_HOME" variable to `PATH`:

```bash
export PATH="/usr/local/bin:$MYSQL_HOME/bin:$PATH"
```

Your `PATH` may include other directives.  Currently mine looks like this:

```bash
export PATH="/usr/local/bin:/usr/local/sbin:$JAVA_HOME/bin:$MYSQL_HOME/bin:$(brew --prefix homebrew/php/php72)/bin:$PATH"
```

Write out the change by holding down the "control" and "o" keys (CTRL - o), then press the return 
key when "File Name to Write: .bash_profile" is displayed. Then exit nano by holding down the 
"control" and "x" keys (CTRL - x).

To activate the changes in your current terminal session, issue the `source` command:

```commandline
$ source ~/.bash_profile
```

### 7.6 Install MySQL Workstation
Also [download](https://dev.mysql.com/downloads/workbench/) and install the MySQL Workbench Community Edition 8.0.x (currently 8.0.12), macOS (x86, 64-bit) `mysql-workbench-community-8.0.12-macos-x86_64.dmg` archive file.

As with the SQL Server Community Edition download you will be prompted to sign in or create an Oracle account prior to performing this operation. Once authenticated, click the fat blue "Download Now" button to initiate the install process. 

:bulb: You can also click "No thanks, just start my download" to bypass account creation/login.

Double-click the *.dmg archive file to open it, and then drag the Workbench.app icon to the 
Applications folder.

:warning: To log in to the Workstation as root you will need the root user password you created earlier.

:bulb: If you choose not to move the installer *.dmg to the Trash, remember to eject the mounted volume via the Finder.

## <a name="mysqluser">8.0 Create a MySQL User Account</a>
To confirm that all is well with the install log into the shell as the root user and issue the 
`SHOW DATABASES` statement.

:bulb: `mysql -uroot -p` is equivalent to `mysql --user root --password`

```commandline
$ mysql -uroot -p
Enter password:
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 10
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

If by chance you make a mistake and garble a statement, press the "Control" and "c" keys (CTRL - c)
 to exit the input block.  Then start anew.

:confused: Originally I used the new [caching SHA-2 pluggable authentication](https://dev.mysql.com/doc/refman/8.0/en/caching-sha2-pluggable-authentication.html) algorithm to create my password (example statement below).  However, I encountered connection issues so switched back to MySQL's [native pluggable authentication](https://dev.mysql.com/doc/refman/8.0/en/native-pluggable-authentication.html) in the statement issued above.

```mysql
CREATE USER 'arwhyte'@'127.0.0.1' IDENTIFIED WITH caching_sha2_password BY 'MyPassword';
GRANT ALL PRIVILEGES ON *.* TO 'arwhyte'@'127.0.0.1' WITH GRANT OPTION;
FLUSH PRIVILEGES;
```

To check on the current set of MySQL users issue the following statement:

```commandline
mysql> SELECT User, Host FROM mysql.user;
+------------------+-----------+
| User             | Host      |
+------------------+-----------+
| arwhyte          | %         |
| arwhyte          | localhost |
| mysql.infoschema | localhost |
| mysql.session    | localhost |
| mysql.sys        | localhost |
| root             | localhost |
+------------------+-----------+
6 rows in set (0.00 sec)

```

Then exit the MySQL shell:

```commandline
mysql> exit
Bye
$
```

For additional information on adding users see the MySQL 8.0 Reference Documentation [6.3.2 Adding User Accounts](https://dev.mysql.com/doc/refman/8.0/en/adding-users.html).

### 8.2 Obfuscate User Password
Next, use the `mysql_config_editor` client utility to store your user account's authentication 
credentials in an obfuscated login path file named `.mylogin.cnf`. The file location is your home
 directory.
 
:bulb: Do not attempt to run the `mysql_config_editor` while logged in to MySQL shell (it will 
fail to execute).  Open a new terminal session or close your existing MySQL shell session before running it.

:warning: Replace 'arwhyte' with the name of the user account you created above and then add the password you earlier created when prompted.
  
```commandline
$ mysql_config_editor set --login-path=client --host=localhost --user=arwhyte --password
```

To confirm that the operation was successful invoke the `print` method:

```commandline
$ mysql_config_editor print --all
[client]
user = arwhyte
password = *****
host = localhost
```

With your password obfuscated you can now log into the MySQL shell without specifying a password 
argument:

```commandline
$ mysql -uarwhyte
```

:bulb: As an added benefit, if you specify this MySQL user account (or another using the same 
password) as the database user in your Django project's mysite `settings.py` file, you will not need to reference the user's password in the settings file.

For additional information on obfuscating passwords see the MySQL 8.0 Reference Documentation [4.6.7 mysql_config_editor — MySQL Configuration Utility](https://dev.mysql.com/doc/refman/8.0/en/mysql-config-editor.html).

## <a name="mysqloptions">9.0 Create a MySQL Options File</a>
MySQL is designed to read startup options from options files. This ability simplifies the task of 
configuring both MySQL Server and MySQL client programs like the `mysql` shell and `mysqldump` 
database backup/restore tool.

For additional information on option files see the MySQL 8.0 Reference Documentation [4.2.7 Using Option Files](https://dev.mysql.com/doc/refman/8.0/en/option-files.html).

### 9.1 Create my.cnf
Change directories to `/etc` and create a "mysql" directory using `sudo`:

```commandline
$ cd /etc
$ sudo mkdir mysql
Password:
```

Then change directories to `/etc/mysql` and create a `my.cnf` options file using nano.

:warning: You must start nano using `sudo` to ensure you have the proper write permissions.  

```commandline
$ cd mysql
$ sudo nano my.cnf
```

Copy the annotated MySQL client, server and mysqldump options in the code blow below into nano and then change the default user "arwhyte" to the user account you created earlier.

:warning: Change the default user "arwhyte" to the user account created earlier.

```
# ------------------------
# MYSQL CLIENT APP OPTIONS
# ------------------------
[client]

# MySQL Server will listen on this TCP/IP port.
port=3306

# MySQL Server will utilize this pipe.
socket=/tmp/mysql.sock

# The default non-root user.
user=arwhyte

# If you use LOAD DATA LOCAL INFILE in scripts that read the [client] group from option
# files, you can add an local-infile option setting to that group. To prevent problems
# for programs that do not understand this option, specify it using the loose- prefix.
# See https://dev.mysql.com/doc/refman/8.0/en/load-data-local.html
# Values
# 0 disabled
# 1 enabled
loose-local-infile=1

# --------------------
# MYSQL SERVER OPTIONS
# --------------------
[mysqld]

# MySQL Server will listen on this TCP/IP port.
port=3306

# MySQL Server will utilize this pipe.
socket=/tmp/mysql.sock

# The Key Buffer is used to cache index blocks for MyISAM tables. Do not set it larger
# than 30% of your available memory, as some memory is also required by the OS to cache
# rows. Even if you're not using MyISAM tables, you should still set it to 8-64M as it
# will also be used for internal temporary disk tables.
key_buffer_size=16M

# Enable local-infile if LOAD DATA INFILE statements are scoped with the LOCAL keyword.
# See https://dev.mysql.com/doc/refman/8.0/en/load-data.html
# See https://stackoverflow.com/questions/36023339/mysql-python-load-data-local-infile-error
# Values
# 0 disabled
# 1 enabled
local-infile=1

# Specifies how database, table and table alias names are stored in the metadata.
# Values
# 0 will throw an error on case-insensitive operative systems
# 1 table names are stored in lowercase on disk and comparisons are not case sensitive.
# 2 table names are stored as given but compared in lowercase.
#lower_case_table_names=1

# Max size of 1 packet or any generated or intermediate string, or any parameter
# sent by the mysql_stmt_send_long_data() C API function.
max_allowed_packet=128M

# Limits which directories you can load files from when using LOAD DATA INFILE.
# See https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html#sysvar_secure_file_priv
# Values
# ''       disabled. No restrictions placed on file locations.  This is NOT a secure setting.
# dir_name MySQL Server limits import/export operations to work only with files in the named
#          directory. The directory must exist; the server will not create it.
# Null     import/output operations are not permitted.
secure-file-priv=''

# -------------------------
# MYSQLDUMP UTILITY OPTIONS
# See https://dev.mysql.com/doc/refman/8.0/en/mysqldump.html
# -------------------------
[mysqldump]

# quick option dumps tables row by row.
quick
```

After pasting the MySQL options above into nano and replacing the user name value, write out the change by holding down the "control" and "o" keys (CTRL - o), then press the return key when "File Name to Write: my.cnf" is displayed. Then exit nano by holding down the "control" and "x" keys (CTRL - x).

### 9.2 Restart MySQL Server
With `/etc/mysql/my.cnf` created, use the Apple System Preferences MySQL Preference Pane to stop 
and then restart MySQL Server with the new startup options defined in your newly minted `my.cnf`.

If the restart fails (e.g., alternating green/red indicator icons = bad), stop MySQL server and 
recheck 
`/etc/mysql/my.cnf` for syntax errors.

## <a name="pollsdb">10.0 Create the Polls Database</a>

With MySQL Server restarted, log into the `mysql` shell with your non-root user and create a database 
named "polls":

```commandline
$ mysql -uarwhyte
```

```commandline
mysql> CREATE DATABASE polls;
Query OK, 1 row affected (0.04 sec)
```

:warning: You must terminate the SQL statement with a semi-colon (";").

## <a name="mysqlclient">11.0 Install the Python mysqlclient Connector</a>
The Django Team [recommends](https://docs.djangoproject.com/en/2.1/ref/databases/#mysql-notes) 
using the [mysqlclient](https://pypi.python.org/pypi/mysqlclient) to connect to MySQL. 
Activate your Django project virtual environment and install it using `pip`.

```commandline
$ cd ~/Development/repos/github/arwhyte/django_tutorial
$ source venv/bin/activate
$ pip3 install mysqlclient
```

## <a name="connectdjangomysql">12.0 Connect Django to MySQL</a>
Now connect the Django project to the MySQL polls database.

### 12.1 Update settings.py
Comment out or replace the default SQLite connection settings in databases section of the Django 
mysite `settings.py` file with the following Python dictionary, replacing the 'USER' value with 
your MySQL user account name:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'polls',
        'USER': '<YER USER>',
        'OPTIONS': {
            'read_default_file': '/etc/mysql/my.cnf',
        },
    }
}
```

Note that the `read_default_file` property is set to the path to your `my.cnf` options file.

:bulb: Later you will create a 'django' user with reduced privileges that are scoped to certain 
database schemas only (e.g., polls, test_polls).

### 12.2 Run migrations
Next, populate the polls database with the tables required to support both the app and Django's adminstration site using the `migrate` command.  If you earlier created a polls app when working with the default SQLite back-end, the polls models will be included in the migration.

:warning: You must activate the virtual environment before issuing this and the other `manage.py` commands described below.


```commandline
$ cd ~/Development/repos/github/arwhyte/django_tutorial
$ source venv/bin/activate
(venv) $ python manage.py migrate
```

:warning: :rage: The migration will likely fail with a long traceback that I've trimmed to the last two lines: 

```
...
django.core.exceptions.ImproperlyConfigured
Did you install mysqlclient?
```

The error is due to Django's failure to locate the runtime library `libmysqlclient.21.dylib` (or an earlier version if using MySQL 5.x).  This is due to the Mac OS [System Itegrity Protection](https://support.apple.com/en-us/HT204899) (SIP) which blocks write access to certain system directories such as `/usr`. Writing to `/usr/local` is however permitted.

:wink: One workaround discussed on [stackoverflow](https://stackoverflow
.com/questions/14363522/django-dev-server-error-image-not-found) is to create a number of symbolic links that point to `/usr/local`.  

In my case I had to create symbolic links for `
* `libmysqlclient.21.dylib` 
* `libssl.1.0.0.dylib` 
* `libcrypto.1.0.0.dylib`  

Check `/usr/local/mysql/lib` and confirm that you have the same named lib files and open a new 
terminal session and create the symbolic links (`ln -s source_file sym_link`) using `sudo`:

```commandline
$ sudo ln -s /usr/local/mysql/lib/libmysqlclient.21.dylib /usr/local/lib/libmysqlclient.21.dylib
$ sudo ln -s /usr/local/mysql/lib/libssl.1.0.0.dylib /usr/local/lib/libssl.1.0.0.dylib
$ sudo ln -s /usr/local/mysql/lib/libcrypto.1.0.0.dylib /usr/local/lib/libcrypto.1.0.0.dylib
$ sudo ln -s /usr/local/mysql/lib /usr/local/mysql/lib/mysql
```

With the sym links created your `/usr/local/mysql/lib` directory should look like this: 

```commandline
$ cd /usr/local/mysql/lib
$ ls
total 42208
drwxr-xr-x  13 root  wheel       416 Aug 10 20:54 .
drwxr-xr-x  13 root  wheel       416 Aug 10 20:55 ..
-rw-r--r--   1 root  wheel   2065200 Jun 28 13:53 libcrypto.1.0.0.dylib
lrwxr-xr-x   1 root  wheel        21 Aug 10 20:54 libcrypto.dylib -> libcrypto.1.0.0.dylib
-rwxr-xr-x   1 root  wheel   5833744 Jun 28 14:24 libmysqlclient.21.dylib
-rw-r--r--   1 root  wheel  13246088 Jun 28 14:19 libmysqlclient.a
lrwxr-xr-x   1 root  wheel        23 Aug 10 20:54 libmysqlclient.dylib -> libmysqlclient.21.dylib
-rw-r--r--   1 root  wheel     35824 Jun 28 14:19 libmysqlservices.a
-rw-r--r--   1 root  wheel    421344 Jun 28 13:53 libssl.1.0.0.dylib
lrwxr-xr-x   1 root  wheel        18 Aug 10 20:54 libssl.dylib -> libssl.1.0.0.dylib
drwxr-xr-x   4 root  wheel       128 Jun 28 14:19 mecab
drwxr-xr-x   3 root  wheel        96 Jun 28 14:19 pkgconfig
drwxr-xr-x  55 root  wheel      1760 Aug 10 20:54 plugin
```

Now that the sym links in place, return to your Django terminal session and reissue the `migrate` command.

```commandline
(venv) $ python manage.py migrate
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

### Create a Django superuser account
Create a Django superuser account in order to access the Django administration site. Provide a username, email address, and password:

```commandline
(venv) $ python manage.py createsuperuser
Username (leave blank to use 'arwhyte'):
Email address: arwhyte@umich.edu
Password:
Password (again):
Superuser created successfully.
```

### 12.4 Create the Django tutorial polls app
If you have not done so already, create a skeletal implementation of the Django tutorial polls app:

```commandline
(venv) $ python manage.py startapp polls
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

## 12.5 Start/Continue the Django Team Polls Tutorial
Either start or continue working on the Django Team's Polls [tutorial](https://docs.djangoproject.com/en/2.1/intro/tutorial01/). You may need to run additional migrations to update the MySQL polls database and/or recreate questions created earlier when the polls app was connected to the SQLite database.

## License
<a rel="license" href="http://creativecommons.org/licenses/by/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International License</a>.
