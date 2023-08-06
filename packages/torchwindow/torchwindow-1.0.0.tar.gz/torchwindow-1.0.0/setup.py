# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['torchwindow']

package_data = \
{'': ['*']}

install_requires = \
['cuda-python>=11.8.0,<12.0.0',
 'numpy>=1.23.4,<2.0.0',
 'pyopengl>=3.1.6,<4.0.0',
 'pysdl2-dll>=2.24.1,<3.0.0',
 'pysdl2>=0.9.14,<0.10.0',
 'torch==1.13.0+cu117']

setup_kwargs = {
    'name': 'torchwindow',
    'version': '1.0.0',
    'description': 'Display tensors directly from GPU',
    'long_description': '# TorchWindow\n\nTorchWindow is a Python library that enables viewing of PyTorch Cuda Tensors on screen directly from GPU memory (No copying back and forth between GPU and CPU) via OpenGL-Cuda interop.\n\n## Install\n\n```\npip install torchwindow\n```\n\n## Use\nTo create a window\n```\nfrom torchwindow import Window\nwindow = Window(640, 480, name="Torch Window")\n```\nTo display an image tensor in the window\n```\nwindow.draw(image)\n```\n`image` must be a tensor with the following properties:\n- 3 dimensions, specifically `(rows, columns, channels)` in that order.\n- `channels` dimension must be of size 4 (r, g, b, a)\n\n## Example\nTo check if torchwindow is properly installed try running\n```\npython3 -m torchwindow.example\n```\nYou should see this window appear for 5 seconds before closing\n![Example](example.png)',
    'author': 'Jeremy',
    'author_email': 'jbaron34@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/jbaron34/torchwindow',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
