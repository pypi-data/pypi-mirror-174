# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['py621dl']

package_data = \
{'': ['*']}

install_requires = \
['Pillow', 'numpy', 'opencv-python', 'pandas', 'requests']

setup_kwargs = {
    'name': 'py621dl',
    'version': '0.1a0.dev3',
    'description': 'A downloader for e621.net with meant for iterability, using e621 db post exports, designed for deep learning.',
    'long_description': '# py621dl - an iterable E621 downloader\n\nThis package is meant to be used in deep learning applications and automation,\nnot as a means to download specific images and post IDs or searching for tags.\nFor that application, please check out [py621](https://pypi.org/project/py621/)\nwhich is not related to this package in any way.\n\nThe package is meant to be used with the official db export format from E621,\nposts information. See [here](https://e621.net/db_export/) for available db exports\nand [here](https://e621.net/help/api) for general information on the API.\n\n!! This is a pre-release version, and is not meant for production use !!\n\nProper documentation, tests, and automated updates to the package will be added later.\n\n## Usage\n\nThe E621Downloader class must be initialized using the Reader class, to which\nthe csv file must be passed. The Reader supports only the official db export csv files\nof the format "posts-YYYY-MM-DD.csv.gz", either compressed or uncompressed.\n\nThe [E621Downloader](https://github.com/slobodaapl/py621dl/blob/90228111c166926f63f0cf3b991d9c82ca79e6e8/src/py621dl/downloader.py#L12-L14)\nclass can be initialized with the following parameters:\n\n- `csv_reader`:\n  the [Reader](https://github.com/slobodaapl/py621dl/blob/90228111c166926f63f0cf3b991d9c82ca79e6e8/src/py621dl/reader.py#L10-L13)\n  object\n- `timeout`: the timeout for the requests, in seconds\n- `retries`: the number of retries for the requests\n\nIt can be used as an iterable, yielding lists of `np.ndarray` objects of the images. The list size\nwill depend on your `batch_size` specified for `Reader`. The images are of opencv BGR format.\nThe downloader automatically handles and filters deleted or flagged posts, and will attempt to fill\nthe batch with new images so that it will always yield a full batch.\n\nThe [Reader](https://github.com/slobodaapl/py621dl/blob/90228111c166926f63f0cf3b991d9c82ca79e6e8/src/py621dl/reader.py#L10-L13)\nclass can be initialized with the following parameters:\n\n- `csv_file`: the path to the csv file\n- `batch_size`: the size of the batch to be returned by the `E621Downloader`\n- `excluded_tags`: a list of E621 tags to be excluded from the results\n- `minimum_score`: the minimum score of the posts to be included in the results\n- `chunk_size`: the size of the chunk to be read from the csv file at once\n- `checkpoint_file`: the path to the checkpoint file, to resume from any point. If path doesn\'t exist, a new file will\n  be created.\n- `repeat`: whether to repeat from the beginning of the csv file when the end is reached automatically.\n  Otherwise `StopIteration` is raised.\n  `E621Downloader` handles this exception and raises its own `StopIteration` when the end is reached.\n\n# Example use\n\n```python\nfrom py621dl import Reader, E621Downloader\n\nreader = Reader("posts-2022-10-30.csv.gz")\ndownloader = E621Downloader(reader, timeout=10, retries=3)\n\nfor batch in downloader:\n    # do something with the batch\n    pass\n```',
    'author': 'slobodaapl',
    'author_email': 'slobodaapl@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://pypi.org/project/py621dl',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11',
}


setup(**setup_kwargs)
