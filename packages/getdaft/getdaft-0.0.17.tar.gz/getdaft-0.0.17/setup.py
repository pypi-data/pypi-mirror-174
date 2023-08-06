# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['daft',
 'daft.dataframe',
 'daft.execution',
 'daft.experimental',
 'daft.experimental.serving',
 'daft.experimental.serving.backends',
 'daft.experimental.serving.static',
 'daft.internal',
 'daft.internal.kernels',
 'daft.logical',
 'daft.runners',
 'daft.viz']

package_data = \
{'': ['*']}

install_requires = \
['fsspec',
 'loguru>=0.6.0,<0.7.0',
 'numpy>=1.16.6,<2.0.0',
 'pandas>=1.3.5,<2.0.0',
 'polars[timezone]>=0.14.12,<0.15.0',
 'protobuf>=3.19.0,<3.20.0',
 'pyarrow>=6,<7',
 'pydot>=1.4.2,<2.0.0',
 'ray==1.13.0',
 'tabulate>=0.8.10,<0.9.0']

extras_require = \
{':python_version < "3.8"': ['typing-extensions>=4.0.0',
                             'pickle5>=0.0.12,<0.0.13'],
 'aws': ['boto3>=1.23.0,<2.0.0', 's3fs'],
 'experimental': ['fastapi>=0.79.0,<0.80.0',
                  'docker>=5.0.3,<6.0.0',
                  'uvicorn>=0.18.2,<0.19.0',
                  'cloudpickle>=2.1.0,<3.0.0',
                  'boto3>=1.23.0,<2.0.0',
                  'PyYAML>=6.0,<7.0',
                  'icebridge>=0.0.4,<0.0.5',
                  'Pillow>=9.2.0,<10.0.0'],
 'iceberg': ['icebridge>=0.0.4,<0.0.5'],
 'serving': ['fastapi>=0.79.0,<0.80.0',
             'docker>=5.0.3,<6.0.0',
             'uvicorn>=0.18.2,<0.19.0',
             'cloudpickle>=2.1.0,<3.0.0',
             'boto3>=1.23.0,<2.0.0',
             'PyYAML>=6.0,<7.0']}

entry_points = \
{'console_scripts': ['build_inplace = build:build_inplace']}

setup_kwargs = {
    'name': 'getdaft',
    'version': '0.0.17',
    'description': 'A Distributed DataFrame library for large scale complex data processing.',
    'long_description': '|Banner|\n\n|CI| |PyPI| |Latest Tag|\n\n`Website <https://www.getdaft.io>`_ • `Docs <https://www.getdaft.io>`_ • `Installation`_ • `10-minute tour of Daft <https://getdaft.io/learn/10-min.html>`_ • `Community and Support <https://github.com/Eventual-Inc/Daft/discussions>`_\n\nDaft: the distributed Python dataframe for media data\n=====================================================\n\n\n`Daft <https://www.getdaft.io>`_ is a fast, Pythonic and scalable open-source dataframe library built for Python and Machine Learning workloads.\n\n  **Daft is currently in its Alpha release phase - please expect bugs and rapid improvements to the project.**\n  **We welcome user feedback/feature requests in our** `Discussions forums <https://github.com/Eventual-Inc/Daft/discussions>`_\n\n**Table of Contents**\n\n* `About Daft`_\n* `Getting Started`_\n* `License`_\n\nAbout Daft\n----------\n\nThe Daft dataframe is a table of data with rows and columns. Columns can contain any Python objects, which allows Daft to support rich media data types such as images, audio, video and more.\n\n1. **Any Data**: Columns can contain any Python objects, which means that the Python libraries you already use for running machine learning or custom data processing will work natively with Daft!\n2. **Notebook Computing**: Daft is built for the interactive developer experience on a notebook - intelligent caching/query optimizations accelerates your experimentation and data exploration.\n3. **Distributed Computing**: Rich media formats such as images can quickly outgrow your local laptop\'s computational resources - Daft integrates natively with `Ray <https://www.ray.io>`_ for running dataframes on large clusters of machines with thousands of CPUs/GPUs.\n\nGetting Started\n---------------\n\nInstallation\n^^^^^^^^^^^^\n\nInstall Daft with ``pip install getdaft``.\n\nQuickstart\n^^^^^^^^^^\n\n  Check out our `full quickstart tutorial <https://getdaft.io/learn/quickstart.html>`_!\n\nLoad a dataframe - in this example we load the MNIST dataset from a JSON file, but Daft also supports many other formats such as CSV, Parquet and folders/buckets of files.\n\n.. code:: python\n\n  from daft import DataFrame\n\n  URL = "https://github.com/Eventual-Inc/mnist-json/raw/master/mnist_handwritten_test.json.gz"\n\n  df = DataFrame.from_json(URL)\n  df.show(4)\n\n|MNIST dataframe show|\n\nFilter the dataframe for rows where the ``"label"`` column is equal to 5\n\n.. code:: python\n\n  df = df.where(df["label"] == 5)\n  df.show(4)\n\n|MNIST filtered dataframe show|\n\nRun any function on the dataframe (here we convert a list of pixels into an image using Numpy and the Pillow libraries)\n\n.. code:: python\n\n  import numpy as np\n  from PIL import Image\n\n  def image_from_pixel_list(pixels: list) -> Image.Image:\n      arr = np.array(pixels).astype(np.uint8)\n      return Image.fromarray(arr.reshape(28, 28))\n\n  df = df.with_column(\n      "image_pil",\n      df["image"].apply(image_from_pixel_list),\n  )\n  df.show(4)\n\n|MNIST dataframe with Pillow show|\n\nMore Resources\n^^^^^^^^^^^^^^\n\n* `10-minute tour of Daft <https://getdaft.io/learn/10-min.html>`_ - learn more about Daft\'s full range of capabilities including dataloading from URLs, joins, user-defined functions (UDF), groupby, aggregations and more.\n* `User Guide <https://getdaft.io/learn/user_guides.html>`_ - take a deep-dive into each topic within Daft\n* `API Reference <https://getdaft.io/api_docs.html>`_ - API reference for public classes/functions of Daft\n\nLicense\n-------\n\nDaft has an Apache 2.0 license - please see the LICENSE file.\n\n\n.. |Banner| image:: https://user-images.githubusercontent.com/17691182/190476440-28f29e87-8e3b-41c4-9c28-e112e595f558.png\n   :target: https://www.getdaft.io\n   :alt: Daft dataframes can load any data such as PDF documents, images, protobufs, csv, parquet and audio files into a table dataframe structure for easy querying\n\n.. |CI| image:: https://github.com/Eventual-Inc/Daft/actions/workflows/python-package.yml/badge.svg\n   :target: https://github.com/Eventual-Inc/Daft/actions/workflows/python-package.yml?query=branch:main\n   :alt: Github Actions tests\n\n.. |PyPI| image:: https://img.shields.io/pypi/v/getdaft.svg?label=pip&logo=PyPI&logoColor=white\n   :target: https://pypi.org/project/getdaft\n   :alt: PyPI\n\n.. |Latest Tag| image:: https://img.shields.io/github/v/tag/Eventual-Inc/Daft?label=latest&logo=GitHub\n   :target: https://github.com/Eventual-Inc/Daft/tags\n   :alt: latest tag\n\n.. |MNIST dataframe show| image:: https://user-images.githubusercontent.com/17691182/197297244-79672651-0229-4763-9258-45d8afd48bae.png\n  :alt: dataframe of MNIST dataset with Python list of pixels\n\n.. |MNIST filtered dataframe show| image:: https://user-images.githubusercontent.com/17691182/197297274-3ae82ec2-a4bb-414c-b765-2a25c2933e34.png\n  :alt: dataframe of MNIST dataset filtered for rows where the label is the digit 5\n\n.. |MNIST dataframe with Pillow show| image:: https://user-images.githubusercontent.com/17691182/197297304-9d25b7da-bbbd-4f82-b9e1-97cd4fb5187f.png\n  :alt: dataframe of MNIST dataset with the Python list of pixel values converted to a Pillow image\n',
    'author': 'Eventual Inc',
    'author_email': 'daft@eventualcomputing.com',
    'maintainer': 'Sammy Sidhu',
    'maintainer_email': 'sammy@eventualcomputing.com',
    'url': 'https://getdaft.io',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<4.0.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
