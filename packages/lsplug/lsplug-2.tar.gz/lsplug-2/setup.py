from setuptools import setup

setup(name='lsplug',
      version='2',
      description='Nicer version of lsusb',
      url='https://git.sr.ht/~martijnbraam/lsplug',
      author='Martijn Braam',
      author_email='martijn@brixit.nl',
      packages=['lsplug'],
      classifiers=[
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
      ],
      entry_points={
          'console_scripts': ['lsplug=lsplug.__main__:main'],
      })