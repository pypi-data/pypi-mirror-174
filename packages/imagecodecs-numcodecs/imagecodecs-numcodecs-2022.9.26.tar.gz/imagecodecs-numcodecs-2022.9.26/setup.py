import inspect
import pprint

from setuptools import setup

import imagecodecs
import imagecodecs.numcodecs

entry_points = [
    f'{cls.codec_id} = imagecodecs.numcodecs:{name}'
    for name, cls in inspect.getmembers(imagecodecs.numcodecs)
    if hasattr(cls, 'codec_id') and name != 'Codec'
]

pprint.pprint(entry_points)

setup(
    name='imagecodecs-numcodecs',
    version=imagecodecs.__version__,
    description='Numcodecs entry points for the imagecodecs package',
    author='Christoph Gohlke',
    author_email='cgohlke@cgohlke.com',
    url='https://www.cgohlke.com',
    project_urls={
        'Bug Tracker': 'https://github.com/cgohlke/imagecodecs/issues',
        'Source Code': 'https://github.com/cgohlke/imagecodecs',
        # 'Documentation': 'https://',
    },
    python_requires='>=3.8',
    install_requires=['numcodecs', f'imagecodecs>={imagecodecs.__version__}'],
    entry_points={'numcodecs.codecs': entry_points},
    platforms=['any'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: BSD License',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)
