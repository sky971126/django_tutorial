# Meeting 6 Exercise (Windows)

In this assignment you will

* Set up a custom test runner that works with unmanaged models
* Fix broken `heritagesites` views
* Fix broken `heritagesites` tests and then run the tests
* Fix broken `heritagesites` templates
* Update URL paths
* Choose a stylish website color scheme for your `heritagesites` app
* Override bits of Bootstrap 4 with a custom `heritagesites` css file
* Creat a `<uniqname>-heritage_sites_mtg6.zip`of your work and submit it for evaluation

## 1.0 Test setup

### 1.1 Running Tests Against Unmanaged Models
In the [Model Meta options](https://docs.djangoproject.com/en/2.1/ref/models/options/#managed) section of the Django documentation one reads the following:

> For tests involving models with managed=False, it’s up to you to ensure the correct tables are created as part of the test setup.

Bummer. Luckily, some bright fellows developed a custom test runner that temporarily resets 
unmanaged Models to managed for the duration of the test. In order to implement this nifty 
workaround you will need to install a new package, add some Python code, and tweak `settings.py`.

### 1.2 Install django-test-without-migrations package
Activate your heritagesites virtualenv and install the [django-test-without-migrations](https://pypi.org/project/django-test-without-migrations/) package.

```commandline
(venv) > pip install django-test-without-migrations
```

#### 1.3 Update settings.py
Add `test_without_migrations` to the `INSTALLED_APPS` list:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'heritagesites.apps.HeritagesitesConfig',
    'test_without_migrations',
]
```

Next, add a new TEST_RUNNER setting:

```python
# Add a custom test runner for converting unmanaged models to managed before
# running a test and then revert the effect afterwards.

TEST_RUNNER = 'heritagesites.utils.UnManagedModelTestRunner'
```

#### 1.4 Create a custom test runner class
:bulb: You will find copies of all files referenced in this assignment in the SI664-docs repo in 
the `misc/` directory.  See [https://github.com/arwhyte/SI664-docs/tree/master/misc](https://github.com/arwhyte/SI664-docs/tree/master/misc).

Copy `utils.py` to the `heritagesites` app directory. This code implements a custom test runner that
 loops through the `heritagesite` unmanaged models and changes their Meta `managed` option value 
 from False to True for the duration of the test. This file is whole and does not require fixing.
 
| File | Disposition |
|:---- | :--------- |
| [utils\.py](../misc/utils.py) | Ready for action. | 
 
Location:
 
```
heritagesites/          <-- project
    heritagesites/      <-- app
        ...
        urls.py
        utils.py        <-- here
        views.py     
    mysite/
    ...   
``` 

## 2.0 Views

### 2.1 Add views.py
Copy the broken `views.py` file to the `heritagesites` app directory. Two classes are in need of 
repair.   

| File | Disposition |
|:---- | :--------- |
| [views\.py](../misc/views.py) | The `SiteListView()` class requires an ORM query that retrieves all HeritageSite records. `SiteDetailView()` needs its missing `template_name` value restored. |

### 2.2 Document SiteListView() fix in \<uniqname\>-heritage_sites_mtg6.txt
Once you have added the missing `SiteListView()` ORM query copy the `SiteListView()` class in 
its entirety and paste it into `<uniqname>-heritage_sites_mtg6.txt`.

## 3.0 URLS
Replace mysite/urls.py with the following `urlpatterns`:

```python
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import path, include

urlpatterns = [
    path('', lambda r: HttpResponseRedirect('heritagesites/')),
    path('admin/', admin.site.urls),
    path('heritagesites/', include('heritagesites.urls')),
]
```

Next replace `heritagesites/urls.py` with the following `urlpatterns`:

```python
from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('about/', views.AboutPageView.as_view(), name='about'),
    path('sites/', views.SiteListView.as_view(), name='sites'),
    path('sites/<int:pk>/', views.SiteDetailView.as_view(), name='site_detail'),
]
```

## 4.0 Templates 
Next, you will fix broken template files that the `heritagesites` app utilizes to display the 
views that you repaired earlier.

### 4.1 Create a templates directory
Create the following directory structure and add a set of *.html files. This is the Django default location for `heritagesites` app templates.

```
heritagesites/                  <-- project
    heritagesites/              <-- app
        templates/
            heritagesites/
                about.html
                base.html
                home.html
                site.html
                site_detail.html  
    mysite/
    ...   
```

### 4.2 Add templates
A number of template files are missing bits of code that will require a bit of sleuthing on your part in 
order to effect the necessary fixes required to render them whole again and usable. Repairing 
these files requires a basic understanding of Django's templating language.

Add each of them to the `templates/heritagesites` directory:

| File | Disposition |
|:---- | :--------- |
| [base\.html](../misc/base.html) | Broken in two places; add Name/email to footer |
| [home\.html](../misc/home.html) | Broken in two places |
| [about\.html](../misc/about.html) | No missing code |
| [site\.html](../misc/site.html) | Broken in two places |
| [site_detail\.html](../misc/site_detail.html) | Broken in one place; HeritageSite and HeritageSiteCategory property values |

### 4.3 Repair templates
Fix each template.  This work involves adding missing template language to each file as well as 
missing properties in the `site_detail.html` page.

### 4.4 Check your changes
Start the development server and confirm that the views and templates have been repaired by 
traversing the `heritagesites` app, checking the nav bar, site list pagination and individual 
site entries.

```commandline
(venv) > python manage.py runserver
```

### 4.5 Document your template fixes in \<uniqname\>-heritage_sites_mtg6.txt
After confirming that your `heritagesites` app is in working order, describe the changes you made
 to fix it by adding the following section to `<uniqname>-heritage_sites_mtg6.txt`:

```txt
Template repair work
base.html: fixed ...
home.html: fixed ...
about.html: fixed ...
site.html: fixed ...
site_detail.html: fixed ...
```

After describing the fixes copy the `site_detail.html` template code in its entirety and paste it into `<uniqname>-heritage_sites_mtg6.txt`.

## 5.0 Tests
Confirm that the views are fixed by running an initial set of `heritagesites` app tests.  However, before the tests can be run, the `SiteModelTest` class will need to be fixed.

### 5.1 Add tests.py
Copy the broken `tests.py` file to the `heritagesites` app directory.   

| File | Disposition |
|:---- | :--------- |
| [tests\.py](../misc/tests.py) | Fix the `SiteModelTest` class. The `setUp()` method is broken. See in particular `HeritageSite.objects.create()` method. It is missing several required properties. Restore the missing properties and values. | 

### 5.2 Run tests
When you consider `tests.py` fixed run the tests. If test errors are encountered 
recheck the test classes and methods run the tests again. Repeat until all tests execute 
successfully.

```commandline
(venv) > python manage.py test -n
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
..................
----------------------------------------------------------------------
Ran 13 tests in 0.087s

OK
Destroying test database for alias 'default'...
```

### 5.3 Document SiteModelTest() fix and terminal output in \<uniqname\>-heritage_sites_mtg6.txt
After a successful test run, paste a copy of both the repaired `SiteModelTest` class _and_ the 
terminal output into `<uniqname>-heritage_sites_mtg6.txt`.

## 6.0 Static assets
Bootstrap 4 CSS and Javascript will provide basic styling for the `heritagesites` app.  We will 
forgo a local install in favor of linking to Bootstrap via a content delivery network (CDN). You 
will find CDN links to JQuery and Popper.js, and Bootstrap links in `base.html`.  They require no
 modification.

### 6.1 Choose a website color scheme
Conduct a browser-based search of "website color schemes" and select a pleasing color palette of 3-5 colors. I found mine by perusing Nayomi Chibana's [Color Schemes From Stunning Websites](https://blog.visme.co/website-color-schemes/). The only requirement is that you select a __different__ color scheme from the one [I chose](https://blog.visme.co/wp-content/uploads/2016/09/website19.jpg) for my `heritagesites` app.  

Copy the link to image of your chosen website color scheme and add it to `<uniqname>-heritage_sites_mtg6.txt`

```text
Selected Website color scheme
https://blog.visme.co/wp-content/uploads/2016/09/website40.jpg
``` 

### 6.2 Create a static directory 
Create the following directory structure to house static assets such as style sheets and images. 
This is the Django default location for `heritagesites` style sheets and images.

```
heritagesites/                  <-- project
    heritagesites/              <-- app
        static/
            css/
                heritagesites.css 
    mysite/
    ...   
```

### 6.3 Add a CSS style sheet
Add the ready-made style sheet `heritagesites.css` to the `css/` directory. 

| File | Disposition |
|:---- | :--------- |
| [heritagesites\.css](../misc/heritagesites.css) | No missing code. Color values require updating.|

Now work your way through the CSS updating color values to match your chosen palette.

```css
body {
    background-color: #EAE7DC; /* start here */
}
```

### 6.4 Document styling changes in \<uniqname\>-heritage_sites_mtg6.txt
Once you have the site colors changed, take two screenshots:

| Filename | View | Link |
|:---- | :------- | :--- |
| `<uniqname>-heritage_sites_p12_mtg6.png` | Site List, page 12 | http://localhost:8000/heritagesites/sites/?page=12 |
| `<uniqname>-heritage_sites_site_569_mtg6.png` | Lake Turkana National Parks | http://localhost:8000/heritagesites/sites/569/ |

### 6.5 Upload assignment .zip file to Canvas
Create a .zip archive of 

* `<uniqname>-heritage_sites_mtg6.txt`
* `<uniqname>-heritage_sites_p12_mtg6.png`
* `<uniqname>-heritage_sites_site_569_mtg6.png`

called `<uniqname>-heritage_sites_mtg6.zip` and upload to the SI 664 Canvas site from the 
assignment page.

### Appendix A. Custom Test Runner
Running tests against unmanaged models requires a custom test runner that can change the Meta 
unmanaged option from False to True for the duration of the tests. You will find 
`UnManagedModelTestRunner()` class in `heritagesites/utils.py`. 

```python
from django.test.runner import DiscoverRunner


class UnManagedModelTestRunner(DiscoverRunner):
	"""
	A custom test runner for converting unmanaged models to managed before running a test
	and then revert the effect afterwards.

	Tell Django to use this runner by adding TEST_RUNNER setting to project settings.py
	TEST_RUNNER = 'app_name.utils.UnManagedModelTestRunner'

	Original: Tobias McNulty (now outdated)
	https://www.caktusgroup.com/blog/2010/09/24/simplifying-the-testing-of-unmanaged-database-models-in-django/

	Updated: Paul Vergeev
	https://dev.to/patrnk/testing-against-unmanaged-models-in-django

	Dependency: django-test-without-migrations
	https://pypi.org/project/django-test-without-migrations/

	Running
	$ python3 manage.py test -n (macOS)
	> python manage.py test --n (Windows)

	See also: https://stackoverflow.com/questions/18085245/running-tests-with-unmanaged-tables-in-django
	"""

	def setup_test_environment(self, *args, **kwargs):
		from django.apps import apps

		get_models = apps.get_models
		self.unmanaged_models = [m for m in get_models() if not m._meta.managed]

		for m in self.unmanaged_models:
			m._meta.managed = True

		super(UnManagedModelTestRunner, self).setup_test_environment(*args, **kwargs)

	def teardown_test_environment(self, *args, **kwargs):
		super(UnManagedModelTestRunner, self).teardown_test_environment(*args, **kwargs)

		for m in self.unmanaged_models:
			m._meta.managed = False
```

### Appendix B. Pagination template
The `site.html` file includes the following code for rendering the pagination bar. Pretty cool 
and leverages Bootstrap classes which simplifies styling.   

```html
<!-- WARNING: there is no missing code between <nav>...</nav> -->
  <nav>
    {% if is_paginated %}
      <ul class="pagination justify-content-center">
        {% if page_obj.has_previous %}
          <li class="page-item">
            <a class="page-link" href="?page={{ page_obj.previous_page_number }}"
              aria-label="Previous">
              <span aria-hidden="true">&laquo;</span>
              <span class="sr-only">Previous</span>
            </a>
          </li>
        {% else %}
          <li class="page-item disabled"><span>&laquo;</span></li>
        {% endif %}

        {% for i in paginator.page_range %}
          {% if page_obj.number == i %}
            <li class="page-item active">
              <span>{{ i }}
                <span class="sr-only">(current)</span>
              </span>
            </li>
          {% else %}
            <li class="page-item"><a class="page-link" href="?page={{ i }}">{{ i }}</a></li>
          {% endif %}
        {% endfor %}

        {% if page_obj.has_next %}
          <li class="page-item">
             <a class="page-link" href="?page={{ page_obj.next_page_number }}" aria-label="Next">
                 <span aria-hidden="true">&raquo;</span>
               <span class="sr-only">Next</span>
             </a>
          </li>
        {% else %}
            <li class="page-item disabled"><span>&raquo;</span></li>
        {% endif %}
      </ul>
    {% endif %}
  </nav>
```