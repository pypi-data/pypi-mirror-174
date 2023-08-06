from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='numcek',
  version='2.0.1',
  description='This is a python module for all number checks.',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Subhodeep Moitra',
  author_email='subhodeep2000@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='numcek', 
  packages=find_packages(),
  install_requires=[''] 
)