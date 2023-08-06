from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='PivotGauss',
  version='1.0.0',
  description='The Gauss Elimination Methods.',
  long_description= open('README.md').read() + '\n\n',
  url='',  
  author='Moussa JAMOR',
  author_email='moussajamorsup@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='Pivot Gauss, Elimination, Linear system, inverse of matrix', 
  packages=find_packages(),
  install_requires=['numpy'] 
)
