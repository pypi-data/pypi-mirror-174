# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tonie_api', 'tonie_api.docs', 'tonie_api.tonie_api']

package_data = \
{'': ['*'], 'tonie_api': ['tonie_api.egg-info/*']}

modules = \
['toniepodcastsync', 'podcast']
install_requires = \
['beautifulsoup4>=4.10.0,<5.0.0',
 'config-with-yaml>=0.1.0,<0.2.0',
 'requests-oauthlib>=1.3.0,<2.0.0',
 'requests>=2.25.1,<3.0.0',
 'wget>=3.2,<4.0']

setup_kwargs = {
    'name': 'tonie-podcast-sync',
    'version': '1.0.1',
    'description': 'allows synching podcast episodes to creative tonies',
    'long_description': '# tonie-podcast-sync\n\ntonie-podcast-sync allows synching podcast episodes to [creative tonies](https://tonies.com).\n\nThis is a purely private project and has no association with Boxine GmbH.\n\n# Constraints and Limitations\n\n- currently limited to podcasts providing mp3 files\n- tested with the following podcasts:\n    - [WDR: Gute Nacht mit der Maus](https://www.wdrmaus.de/hoeren/gute_nacht_mit_der_maus.php5)\n    - [Bayern 2: Pumuckl - Der Hörspiel-Klassiker](https://www.br.de/mediathek/podcast/pumuckl/830)\n    - [Checker Tobi Podcast](https://www.br.de/mediathek/podcast/checkpod-der-podcast-mit-checker-tobi/859)\n    - [Anna und die wilden Tiere - der Podcast](https://www.br.de/mediathek/podcast/anna-und-die-wilden-tiere/858)\n- ... but in general, it should hopefully work with all podcasts out there\n\n# Usage\n\ntonie-podcast-sync is available as [a pip package on pypi](https://pypi.org/project/tonie-podcast-sync). Install via\n\n`pip install tonie-podcast-sync`\n\nThen, use it as shown in the following example code:\n\n```python\nfrom toniepodcastsync import ToniePodcastSync, Podcast\n\n# create two Podcast objects, providing the feed URL to each\npumuckl = Podcast("https://feeds.br.de/pumuckl/feed.xml")\nmaus = Podcast("https://kinder.wdr.de/radio/diemaus/audio/gute-nacht-mit-der-maus/diemaus-gute-nacht-104.podcast")\n\n# create instance of ToniePodcastSync\ntps = ToniePodcastSync("<toniecloud-username>", "<toniecloud-password>")\n\n# for an overview of your creative tonies and their IDs\ntps.printToniesOverview()\n\n# define creative tonies based on their ID\ngreenTonie = "<your-tonieID>"\norangeTonie = "<your-tonieID>"\n\n# Fetch new podcast episodes and copy them to greenTonie.\n# The tonie will be filled with as much episodes as fit (90 min max).\n# Episode are ordered with newest first.\ntps.syncPodcast2Tonie(pumuckl, greenTonie)\n\n# Kid\'s should fall asleep, so let\'s limit the podcast \n# episodes on this tonie to 60 minutes in total.\n# Use the optional parameter for this:\ntps.syncPodcast2Tonie(maus, orangeTonie, 60)  \n```\n\nFor the tonie to fetch new content from tonie-cloud, you have to press one ear for 3s (until the "ping" sound) with no tonie on the box (refer also to TonieBox manual).\n\n\n# builds upon work of / kudos to\n- moritj29\'s awesome [tonie_api](https://github.com/moritzj29/tonie_api)\n- [Tobias Raabe](https://tobiasraabe.github.io/blog/how-to-download-files-with-python.html)\n- [Matthew Wimberly](https://codeburst.io/building-an-rss-feed-scraper-with-python-73715ca06e1f)',
    'author': 'Alexander Hartmann',
    'author_email': '16985220+alexhartm@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/alexhartm/tonie-podcast-sync',
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.9.2,<4.0.0',
}


setup(**setup_kwargs)
