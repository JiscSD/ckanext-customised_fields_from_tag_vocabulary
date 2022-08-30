[![Tests](https://github.com/JiscSD/ckanext-customised_fields_from_tag_vocabulary/workflows/Tests/badge.svg?branch=main)](https://github.com/JiscSD/ckanext-customised_fields_from_tag_vocabulary/actions)

# ckanext-customised_fields_from_tag_vocabulary

The plugin is developed for the CKAN platforms for [UK Data Service](https://ukdataservice.ac.uk/), to handle the extra customised fields that CKAN does not support natively and customised taxonomies that is based on the vocabulary - tag list.

## What is vocabulary - tags ?
It is actually the same meaning as taxonomy. For example, the datasets we collected here by the UKDS ranged from 1971 to 2021 census data. The Taxonomy "Year" would contains a set of elements under it, i.e. 1971, 1981, 1991, 2001, 2011, 2021. In this case, "Year" would be called a "vocabulary" and "2021" is the tag under the vocabulary. This is how the relationship among tags are established on CKAN.


## Requirements

This plugin is developed and tested on CKAN version 2.9

Compatibility with core CKAN versions:

| CKAN version    | Compatible?   |
| --------------- | ------------- |
| 2.6 and earlier | no            |
| 2.7             | no            |
| 2.8             | not tested    |
| 2.9             | yes    	  |

## Installation

To install ckanext-customised_fields_from_tag_vocabulary:

1. Activate your CKAN virtual environment, for example:
```
     . /usr/lib/ckan/default/bin/activate
```
2. Clone the source and install it on the virtualenv
(make sure the pip here is using the CKAN virtual environment pip, instead of the system pip)
(to ensure the pip, one can specifically denoted the pip by using the pip under ckan folder)

```
    git clone https://github.com/JiscSD/ckanext-customised_fields_from_tag_vocabulary.git
    cd ckanext-customised_fields_from_tag_vocabulary
    pip install -e .
    pip install -r requirements.txt
```
3. Add `customised_fields_from_tag_vocabulary` to the `ckan.plugins` setting in your CKAN
   config file (by default the config file is located at
   `/etc/ckan/default/ckan.ini`).

4. Restart CKAN. For example if you've deployed CKAN with Apache on Ubuntu:
```
     sudo service apache2 reload
```
or if the server is on AWS, called
```
     sudo reboot now 
```

## Config settings

To make the extensions work, the corresponding vocabulary-tags must be loaded beforehand.
They are "Topics", "Year", "Unit" and "Area_type".


## Developer installation

To install ckanext-customised_fields_from_tag_vocabulary for development, activate your CKAN virtualenv and
do:
```
    git clone https://github.com//ckanext-customised_fields_from_tag_vocabulary.git
    cd ckanext-customised_fields_from_tag_vocabulary
    python setup.py develop
    pip install -r dev-requirements.txt
```

## Tests

To run the tests, do:
```
    pytest --ckan-ini=test.ini
```

## Releasing a new version of ckanext-customised_fields_from_tag_vocabulary

If ckanext-customised_fields_from_tag_vocabulary should be available on PyPI you can follow these steps to publish a new version:

1. Update the version number in the `setup.py` file. See [PEP 440](http://legacy.python.org/dev/peps/pep-0440/#public-version-identifiers) for how to choose version numbers.

2. Make sure you have the latest version of necessary packages:
```
    pip install --upgrade setuptools wheel twine
```
3. Create a source and binary distributions of the new version:
```
       python setup.py sdist bdist_wheel && twine check dist/*
```
   Fix any errors you get.

4. Upload the source distribution to PyPI:
```
       twine upload dist/*
```
5. Commit any outstanding changes:
```
       git commit -a
       git push
```
6. Tag the new release of the project on GitHub with the version number from
   the `setup.py` file. For example if the version number in `setup.py` is
   0.0.1 then do:
```
       git tag 0.0.1
       git push --tags
```
## License

[MIT](https://opensource.org/licenses/MIT)
