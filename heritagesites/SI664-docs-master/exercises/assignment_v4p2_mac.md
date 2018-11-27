# Meeting 4 Exercise (macOS)

You will draw on your hard-won knowledge to perform the following tasks:

* set up a Django development environment called "heritagesites"
* create a Django `mysites` project and `heritagesites` app
* create a MySQL `unesco_heritage_sites` database
* import the database schema and data from a *.sql dump file (provided)
* update `mysite/settings.py` including connecting the `heritagesites` app to the `unesco_heritage_sites` database
* run the `inspectdb` utility to create a models.py file based on the database run migrations
* create a "superuser" account
* write a SQL statement that returns a list of UNESCO heritage sites located in China
* write Python code in Django's interactive shell that uses Django's data API to return a matching result set of Chinese heritage sites
* upload a *.txt file that includes the SQL statement + result set output and Django QuerySet code + result set output

## 1.0 Back-end

### 1.1 Create a UNESCO/UNSD heritage sites database and load with data
Create a new database called `unesco_heritage_sites`:

```commandline
mysql> CREATE DATABASE unesco_heritage_sites;
Query OK, 1 row affected (0.07 sec)
```

Next, download the following *.sql dump file:  

[unesco_heritage_sites_dump-201809241832.sql](https://umich.instructure.com/courses/245664/files/8624407/download?download_frd=1)

Start a _new_ terminal session. Change directories to where you downloaded the *.sql dump file.  
Run the following command from the terminal in order to import the schema and data into the 
`unesco_heritage_sites` database:

```
mysql -u[account_name] [database_name] < [sql_dump_file].sql
```

:warning: Do not attempt to execute this command while in a MySQL shell session (it will fail).  Run it in a new terminal session.

```commandline
$ cd path/to/sql/dump/file
$ mysql -uarwhyte unesco_heritage_sites < unesco_heritage_sites_dump-201809241832.sql
```

### 1.2 Check import
In the MySQL shell issue the following commands:

```commandline
mysql> USE unesco_heritage_sites;
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Database changed
```

Run the following query (you've seen it before):

```mysql
SELECT sr.sub_region_name AS 'sub region', ROUND(CAST(SUM(hs.area_hectares) AS DECIMAL(10,1))) AS
       area_hectares
  FROM heritage_site hs
       LEFT JOIN heritage_site_jurisdiction hsj 
              ON hs.heritage_site_id = hsj.heritage_site_id
       LEFT JOIN country_area ca 
              ON hsj.country_area_id = ca.country_area_id
       LEFT JOIN sub_region sr 
              ON ca.sub_region_id = sr.sub_region_id
 WHERE sr.sub_region_name LIKE '%asia%'
 GROUP BY sr.sub_region_name
 ORDER BY area_hectares DESC;
```

If the result set matches the output below you are good to go. 

```commandline
mysql> SELECT sr.sub_region_name AS 'sub region', ROUND(CAST(SUM(hs.area_hectares) AS DECIMAL(10,1))) AS
    ->        area_hectares
    ->   FROM heritage_site hs
    ->        LEFT JOIN heritage_site_jurisdiction hsj
    ->               ON hs.heritage_site_id = hsj.heritage_site_id
    ->        LEFT JOIN country_area ca
    ->               ON hsj.country_area_id = ca.country_area_id
    ->        LEFT JOIN sub_region sr
    ->               ON ca.sub_region_id = sr.sub_region_id
    ->  WHERE sr.sub_region_name LIKE '%asia%'
    ->  GROUP BY sr.sub_region_name
    ->  ORDER BY area_hectares DESC;
+--------------------+---------------+
| sub region         | area_hectares |
+--------------------+---------------+
| Eastern Asia       |       8547176 |
| South-eastern Asia |       7149778 |
| Southern Asia      |       4080770 |
| Central Asia       |       3150430 |
| Western Asia       |        833377 |
+--------------------+---------------+
5 rows in set (0.01 sec)
```

### 2.0 Front-end

### 2.1 Development environment prep
Open a new terminal session and create a `heritagesites` directory in your development directory of choice.

```commandline
$ cd /Users/arwhyte/Development/repos/github/UMSI-SI664-2018Fall
$ mkdir heritagesites
```

Create a Python 3.7 virtual environment and activate it:

```commandline
$ cd heritagesites
$ virtualenv venv
$ source venv/bin/activate
(venv) $
```

Install the `Django` and `mysqlclient` packages:

```commandline
(venv) $ pip3 install Django mysqlclient
```

Confirm installs:

```commandline
(venv) $ pip3 list
Package     Version
----------- -------
Django      2.1.1
mysqlclient 1.3.13
pip         18.0
pytz        2018.5
setuptools  40.4.3
wheel       0.31.1
```

### 2.2 Create mysite project
From within your Django `heritagesites` project directory, create the "mysite" project by issuing the django-admin "startproject" command. Note the inclusion of a trailing dot ('.') following "mysite":

```commandline
(venv) $ django-admin startproject mysite .
```

:warning: Do not forget to include the trailing dot ('.') in the command.  If you neglect to include the dot, delete the directories and files that were created (except 'venv') and run the command again along with the trailing doc ('.').

### 2.3 Create heritagesites app
Create the heritagesites app:

```commandline
(venv) $ python3 manage.py startapp heritagesites
```

### 2.4 Update mysite settings.py
Update the mysite `settings.py` file with the following tweaks:

#### Allowed hosts 
Add an ngrok-friendly, autograder-friendly, wildcard ('*') to ALLOWED_HOSTS:

```python
ALLOWED_HOSTS = ['*']
```

#### Application definitions
Add `heritagesites.apps.HeritagesitesConfig` to INSTALLED_APPS:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'heritagesites.apps.HeritagesitesConfig',
]
```

#### Database connection
Point to the `unesco_heritage_sites` database.  Set the `USER` to your new "django" account.

:warning: change `USER` value to your MySQL user account.

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'unesco_heritage_sites',
        'USER': 'arwhyte',
        'OPTIONS': {
            'read_default_file': '/etc/mysql/my.cnf',
        },
    }
}
```

#### Time zone
Change the timezone from `UTC` to 'America/New_York':

```python
TIME_ZONE = 'America/New_York'
```                
                
#### Static files
Add a `STATIC_ROOT` setting:

:warning: Eo not delete `STATIC_URL`.

```python
STATIC_ROOT = os.path.join(BASE_DIR, "static")
```     

### 2.5 Start the Django development server
Once `settings.py` is updated, start up the development server and confirm that Django is up and 
running on [http://localhost:8000/](http://localhost:8000/) or [http://127.0.0.1:8000/](http://127.0.0.1:8000/):

:bulb: Ignore the 15 unapplied migrations warning.  You will deal with those in a later step.

```commandline
(venv) $ python3 manage.py runserver
Performing system checks...

System check identified no issues (0 silenced).

You have 15 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, auth, contenttypes, sessions.
Run 'python manage.py migrate' to apply them.

September 23, 2018 - 16:40:26
Django version 2.1.1, using settings 'mysite.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
[23/Sep/2018 16:40:39] "GET / HTTP/1.1" 200 16348
[23/Sep/2018 16:40:39] "GET /static/admin/css/fonts.css HTTP/1.1" 200 423
```

Once confirmed that all is well, shut down the development server by holding down the "Control" and "c" keys (CTRL - c).

### 2.6 Auto-generate UNESCO/UNSD models
From the `heritagesites` root directory (where `manage.py` lives) run Django's `inspectdb` 
utility. If all goes well `inspectdb` will traverse the `unesco_heritage_sites` database and 
create a `models.py` file composed of model classes of the table entities encountered.

```commandline

(venv) $ python3 manage.py inspectdb > heritagesites/models.py
```

`inspectdb` default behavior is to create unmanaged models.  The `Meta` class of each model 
generated has its `managed` property set to "False" as is illustrated below. This is as it should 
be. You not Django will be responsible for managing the UNESCO/UNSD database entities (at least for now). 

```python
class CountryArea(models.Model):
    country_area_id = models.AutoField(primary_key=True)
    country_area_name = models.CharField(unique=True, max_length=100)
    m49_code = models.SmallIntegerField()
    iso_alpha3_code = models.CharField(max_length=3)
    dev_status = models.ForeignKey('DevStatus', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'country_area'

```

:warning: Run `inspectdb` *before* running any migrations.
 
:warning: `inspectdb` is a cool utility but treat the auto-generated `models.py` with caution.  The new models are no more than draft classes that will require inspection, line by line and adjustment. If `inspectb` is unable to map a table column type to a Django model field type, it will default to `TextField` and flag the line with a comment: 

```python
date_inscribed = models.TextField(blank=True, null=True)  # This field type is a guess.
```

The utility is also likely to fail to describe compound keys in associative entities (i.e., junction tables) correctly. Manual fixes will be required.

Read "[Integrating Django with a legacy database](https://docs.djangoproject.com/en/2.1/howto/legacy-databases/)" as well as the `inspectdb` [documentation](https://docs.djangoproject.com/en/2.1/ref/django-admin/#django-admin-inspectdb) to learn more more about Django database introspection and the model auto-generation process. 

### 2.7 Tidy up models.py
Suspend disbelief and pretend you've just edited `models.py` as illustrated below in order to add
 a few `META` properties to each model class and, critically, add a `models.ManyToManyField()` 
 property to the `HeritageSite` class.

In other words, copy the code below and replace the code in the auto-generated `models.py` file.

```python
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

from django.db import models


class CountryArea(models.Model):
    country_area_id = models.AutoField(primary_key=True)
    country_area_name = models.CharField(unique=True, max_length=100)
    region = models.ForeignKey('Region', models.DO_NOTHING, blank=True, null=True)
    sub_region = models.ForeignKey('SubRegion', models.DO_NOTHING, blank=True, null=True)
    intermediate_region = models.ForeignKey('IntermediateRegion', models.DO_NOTHING, blank=True, null=True)
    m49_code = models.SmallIntegerField()
    iso_alpha3_code = models.CharField(max_length=3)
    dev_status = models.ForeignKey('DevStatus', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'country_area'
        ordering = ['country_area_name']
        verbose_name = 'UNSD M49 Country or Area'
        verbose_name_plural = 'UNSD M49 Countries or Areas'

    def __str__(self):
        return self.country_area_name


'''   
class CountryArea(models.Model):
    country_area_id = models.AutoField(primary_key=True)
    country_area_name = models.CharField(unique=True, max_length=100)
    region = models.ForeignKey('Region', models.DO_NOTHING, blank=True, null=True)
    sub_region = models.ForeignKey('SubRegion', models.DO_NOTHING, blank=True, null=True)
    intermediate_region = models.ForeignKey('IntermediateRegion', models.DO_NOTHING, blank=True, null=True)
    m49_code = models.SmallIntegerField()
    iso_alpha3_code = models.CharField(max_length=3)
    dev_status = models.ForeignKey('DevStatus', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'country_area'
'''


class DevStatus(models.Model):
    dev_status_id = models.AutoField(primary_key=True)
    dev_status_name = models.CharField(unique=True, max_length=25)

    class Meta:
        managed = False
        db_table = 'dev_status'
        ordering = ['dev_status_name']
        verbose_name = 'UNSD M49 Country or Area Development Status'
        verbose_name_plural = 'UNSD M49 Country or Area Development Statuses'

    def __str__(self):
        return self.dev_status_name


'''
class DevStatus(models.Model):
    dev_status_id = models.AutoField(primary_key=True)
    dev_status_name = models.CharField(unique=True, max_length=25)

    class Meta:
        managed = False
        db_table = 'dev_status'
'''


class HeritageSite(models.Model):
    heritage_site_id = models.AutoField(primary_key=True)
    site_name = models.CharField(unique=True, max_length=255)
    description = models.TextField()
    justification = models.TextField(blank=True, null=True)
    date_inscribed = models.TextField(blank=True, null=True)  # This field type is a guess.
    longitude = models.DecimalField(max_digits=11, decimal_places=8, blank=True, null=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=8, blank=True, null=True)
    area_hectares = models.FloatField(blank=True, null=True)
    heritage_site_category = models.ForeignKey('HeritageSiteCategory', models.DO_NOTHING)
    transboundary = models.IntegerField()

    # Intermediate model (country_area -> heritage_site_jurisdiction <- heritage_site)
    country_area = models.ManyToManyField(CountryArea, through='HeritageSiteJurisdiction')

    class Meta:
        managed = False
        db_table = 'heritage_site'
        ordering = ['site_name']
        verbose_name = 'UNESCO Heritage Site'
        verbose_name_plural = 'UNESCO Heritage Sites'

    def __str__(self):
        return self.site_name

    def country_area_display(self):
        """Create a string for country_area. This is required to display in the Admin view."""
        return ', '.join(
            country_area.country_area_name for country_area in self.country_area.all()[:25])

    country_area_display.short_description = 'Country or Area'


'''
class HeritageSite(models.Model):
    heritage_site_id = models.AutoField(primary_key=True)
    site_name = models.CharField(unique=True, max_length=255)
    description = models.TextField()
    justification = models.TextField(blank=True, null=True)
    date_inscribed = models.TextField(blank=True, null=True)  # This field type is a guess.
    longitude = models.DecimalField(max_digits=11, decimal_places=8, blank=True, null=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=8, blank=True, null=True)
    area_hectares = models.FloatField(blank=True, null=True)
    heritage_site_category = models.ForeignKey('HeritageSiteCategory', models.DO_NOTHING)
    transboundary = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'heritage_site'
'''


class HeritageSiteCategory(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(unique=True, max_length=25)

    class Meta:
        managed = False
        db_table = 'heritage_site_category'
        ordering = ['category_name']
        verbose_name = 'UNESCO Heritage Site Category'
        verbose_name_plural = 'UNESCO Heritage Site Categories'

    def __str__(self):
        return self.category_name


'''
class HeritageSiteCategory(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(unique=True, max_length=25)

    class Meta:
        managed = False
        db_table = 'heritage_site_category'
'''


class HeritageSiteJurisdiction(models.Model):
    heritage_site_jurisdiction_id = models.AutoField(primary_key=True)
    heritage_site = models.ForeignKey(HeritageSite, models.DO_NOTHING)
    country_area = models.ForeignKey(CountryArea, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'heritage_site_jurisdiction'
        ordering = ['heritage_site', 'country_area']
        verbose_name = 'UNESCO Heritage Site Jurisdiction'
        verbose_name_plural = 'UNESCO Heritage Site Jurisdictions'


'''
class HeritageSiteJurisdiction(models.Model):
    heritage_site_jurisdiction_id = models.AutoField(primary_key=True)
    heritage_site = models.ForeignKey(HeritageSite, models.DO_NOTHING)
    country_area = models.ForeignKey(CountryArea, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'heritage_site_jurisdiction'
'''

class IntermediateRegion(models.Model):
    intermediate_region_id = models.AutoField(primary_key=True)
    intermediate_region_name = models.CharField(unique=True, max_length=100)
    sub_region = models.ForeignKey('SubRegion', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'intermediate_region'
        ordering = ['intermediate_region_name']
        verbose_name = 'UNSD M49 Intermediate Region'
        verbose_name_plural = 'UNSD M49 Intermediate Regions'

    def __str__(self):
        return self.intermediate_region_name


'''
class IntermediateRegion(models.Model):
    intermediate_region_id = models.AutoField(primary_key=True)
    intermediate_region_name = models.CharField(unique=True, max_length=100)
    sub_region = models.ForeignKey('SubRegion', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'intermediate_region'
'''


class Region(models.Model):
    region_id = models.AutoField(primary_key=True)
    region_name = models.CharField(unique=True, max_length=100)

    class Meta:
        managed = False
        db_table = 'region'
        ordering = ['region_name']
        verbose_name = 'UNSD M49 Region'
        verbose_name_plural = 'UNSD M49 Regions'

    def __str__(self):
        return self.region_name


'''
class Region(models.Model):
    region_id = models.AutoField(primary_key=True)
    region_name = models.CharField(unique=True, max_length=100)

    class Meta:
        managed = False
        db_table = 'region'
'''


class SubRegion(models.Model):
    sub_region_id = models.AutoField(primary_key=True)
    sub_region_name = models.CharField(unique=True, max_length=100)
    region = models.ForeignKey(Region, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'sub_region'
        ordering = ['sub_region_name']
        verbose_name = 'UNSD M49 Subregion'
        verbose_name_plural = 'UNSD M49 Subregions'

    def __str__(self):
        return self.sub_region_name


'''
class SubRegion(models.Model):
    sub_region_id = models.AutoField(primary_key=True)
    sub_region_name = models.CharField(unique=True, max_length=100)
    region = models.ForeignKey(Region, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'sub_region'
'''
```

### 2.8 Install the core Django tables
Now you can add the Django admin site and other app tables to the `unesco_heritage_sites` database:

```commandline
(venv) $ python3 manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions
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
  Applying sessions.0001_initial... OK
```
 
### 2.9 Create a Django superuser account
Create a Django superuser account in order to access the Django administration site. Provide a username, email address, and password:

```commandline
(venv) $ python3 manage.py createsuperuser
Username (leave blank to use 'arwhyte'):
Email address: arwhyte@umich.edu
Password:
Password (again):
Superuser created successfully.
``` 

## 3.0 Chinese heritage site queries
Now that the `heritagesites` app is installed and connected to the `unesco_heritage_sites` 
database, two tasks remain for completing the assignment.

### 3.1 Write a SQL statement
Start the MySQL shell and issue a SQL SELECT statement that returns a result set of all heritage 
sites located in the three Chinese country/area records.  This query builds on a SQL SELECT 
statement discussed in class.

:bulb: Remember to point the MySQL shell at the unesco_heritage_sites database before issuing your 
SELECT statement.

```commandline
mysql> USE unesco_heritage_sites;
Database changed
``` 

The result set must include the following columns displayed in the following order:

1. region.region_name 
2. sub_region.sub_region_name, 
3. country_area.country_area_name, 
4. heritage_site.site_name
5. heritage_site_category.category_name

You must also sort the result set in the following order:

1. region.region_name 
2. sub_region.sub_region_name, 
3. country_area.country_area_name, 
4. heritage_site.site_name

Execute the query. Then cut and paste the shell output into a *.txt file named

`<uniqname>-china_heritage_sites.txt`

__Please include _both_ the SQL statement and the result set in the *.txt file.__

```commandline
mysql> SELECT . . . ;
+-------------+-----------------+-------------------+---------------------------+
| region_name | sub_region_name | country_area_name | site_name | category_name |
+-------------+-----------------+-------------------+---------------------------+
| ...         | ...             | ...               | ...       | ...           |
. . .

```

### 3.2 Create a matching Django QuerySet
While in your Django `heritagesites` app virtual environment, start the Python interactive shell and write a query that returns a matching `QuerySet` using the database API (ORM). 

```commandline
(venv) $ python3 manage.py shell
Python 3.7.0 (default, Jun 29 2018, 20:13:13)
[Clang 9.1.0 (clang-902.0.39.2)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>>
```

Utilize the following method chaining to create your `QuerySet`:

`hs = Model.objects.select_related(...).filter(...).values_list(...)`

```commandline
>>> from heritagesites.models import HeritageSite . . .
>>> hs = HeritageSite.objects.select_related(...).filter(...).values_list(...)
>>> for s in hs:
...     print(...)   <-- indent 4 spaces
...                  <-- indent 4 spaces  
. . .                <-- hit [enter] 
```

Loop through the `QuerySet` and print out the tuple values.  Then *append* the shell output to 
your `<uniqname>-china_heritage_sites.txt` file. 

__Please include _both_ the Python code typed into the shell and the result set in the *.txt file.__
 
### 3.3 Submit assignment 
Submit `<uniqname>-china_heritage_sites.txt` to Canvas via the assignment page.
