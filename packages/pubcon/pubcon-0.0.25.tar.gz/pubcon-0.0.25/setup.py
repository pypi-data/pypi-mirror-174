from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='pubcon',
  version='0.0.25',
  description='Conversion code for pubchem database',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Ahmed Alhilal',
  author_email='aalhilal@kfu.edu',
  license='MIT', 
  classifiers=classifiers,
  keywords='chemiformatics, pubchem, conversion', 
  packages=find_packages(),
  install_requires=['requests'], 
)
