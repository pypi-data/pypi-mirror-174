from setuptools import setup

setup(
  name='Dmr',
  version='0.1.0',
  author='Angkana Suchaimanacharoen',
  author_email='angkana.suc@eastspring.com',
  packages=['dmr'],
  license='LICENSE',
  description='ESTHDMR utility',
  long_description=open('README.md').read(),
  install_requires=[
      "pandas",
      "numpy",
      "pytest",
  ],
)