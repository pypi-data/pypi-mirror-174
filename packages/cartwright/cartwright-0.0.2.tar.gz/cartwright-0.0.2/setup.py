# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cartwright',
 'cartwright.categories',
 'cartwright.datasets',
 'cartwright.models',
 'cartwright.resources']

package_data = \
{'': ['*']}

install_requires = \
['arrow==1.0.3',
 'faker>=14.0',
 'fuzzywuzzy==0.18.0',
 'joblib==1.0.1',
 'numpy>=1.19',
 'pandas>=1.1',
 'pydantic==1.8.2',
 'python-levenshtein==0.20.7',
 'scipy>=1.5',
 'torch>=1.8',
 'torchvision>=0.9']

entry_points = \
{'console_scripts': ['cartwright = cartwright.categorize:main']}

setup_kwargs = {
    'name': 'cartwright',
    'version': '0.0.2',
    'description': 'A recurrent neural network paired with heuristic methods that automatically infer geospatial, temporal and feature columns',
    'long_description': '\n# Cartwright\n![Tests](https://github.com/jataware/geotime_classify/actions/workflows/tests.yml/badge.svg)\n\nCartwirght categorizes spatial and temporal features in a dataset. \n\nCartwright uses natural language processing and heuristic \nfunctions to determine the best guess categorization of a feature. \nThe goal of this project was for a given dataframe where we expect\nsome kind of geospatial and temporal columns, automatically infer:\n\n-   Country\n-   Admin levels (0 through 3)\n-   Timestamp (from arbitrary formats)\n-   Latitude\n-   Longitude\n-   Dates (including format)\n-   Time resolution for date columns\n\n\n The model and transformation code can be used locally by installing\n the pip package or downloaded the github repo and following the directions\n found in /docs.\n\n# Simple use case\n\nCartwright has the ability to classify features of a dataframe which can help\nwith automation tasks that normally require a human in the loop.\nFor a simple example we have a data pipeline that ingests dataframes and\ncreates a standard timeseries plots or a map with datapoints. The problem is these new dataframes\nare not standarized, and we have no way of knowing which columns contain dates or locations data.\nBy using Cartwright we can automatically infer which columns are dates or coordinate values and \ncontinue with our pipeline.\n\nHere is the dataframe with :\n\n| x_value  |  y_value   | date_value | Precip |\n|:---------|:----------:|-----------:|--------|\n| 7.942658 | 107.240322 | 07/14/1992 | .2     |\n| 7.943745 | 137.240633 | 07/15/1992 | .1     |\n| 7.943725 | 139.240664 | 07/16/1992 | .3     |\n\n\npython code example and output.\n    \n    from cartwright import categorize\n    cartwright = categorize.CartwrightClassify()\n    categorizations = cartwright.columns_categorized(path="path/to/csv.csv")\n    for column, category in categorization.items():\n        print(column, category)\n\nYou can see from the output we were able to infer that x_value and y_values were geo category with subcategory of latitude and longitude. In some cases these can be impossible to tell apart since all latitude values are valid longitude values. For our date feature the category is time and the subcategory is date. The format is correct and we were able to pick out the time resolution of one day.  \n\n\n    x_value {\'category\': <Category.geo: \'geo\'>, \'subcategory\': <Subcategory.latitude: \'latitude\'>, \'format\': None, \'time_resolution\': {\'resolution\': None, \'unit\': None, \'density\': None, \'error\': None}, \'match_type\': [<Matchtype.LSTM: \'LSTM\'>], \'fuzzyColumn\': None}\n    \n    y_value {\'category\': <Category.geo: \'geo\'>, \'subcategory\': <Subcategory.longitude: \'longitude\'>, \'format\': None, \'time_resolution\': {\'resolution\': None, \'unit\': None, \'density\': None, \'error\': None}, \'match_type\': [<Matchtype.LSTM: \'LSTM\'>], \'fuzzyColumn\': None}\n\n    date_value {\'category\': <Category.time: \'time\'>, \'subcategory\': <Subcategory.date: \'date\'>, \'format\': \'%m/%d/%Y\', \'time_resolution\': {\'resolution\': TimeResolution(uniformity=<Uniformity.PERFECT: 1>, unit=<TimeUnit.day: 86400.0>, density=1.0, error=0.0), \'unit\': None, \'density\': None, \'error\': None}, \'match_type\': [<Matchtype.LSTM: \'LSTM\'>], \'fuzzyColumn\': None}\n\n    precip_value {\'category\': None, \'subcategory\': None, \'format\': None, \'time_resolution\': {\'resolution\': None, \'unit\': None, \'density\': None, \'error\': None}, \'match_type\': [], \'fuzzyColumn\': None}\n\nWith this information we can now convert the date values to a timestamp and plot a timeseries with other features.\n\n',
    'author': 'Kyle Marsh',
    'author_email': 'kyle@jataware.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
