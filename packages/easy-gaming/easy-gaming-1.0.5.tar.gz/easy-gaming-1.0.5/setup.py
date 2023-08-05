from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='easy-gaming',
  version='1.0.5',
  description='A gaming automation library',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Luke Cheney',
  author_email='thestarfinder8@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='gaming', 
  packages=find_packages(),
  install_requires=['mouse', 'pynput', 'python-time'] 
)