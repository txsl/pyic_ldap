from setuptools import setup
# from distutils.core import setup

setup(name='pyic_ldap',
      # version='0.1',
      description='LDAP Functions to work with Imperial College LDAP',
      url='https://github.com/txsl/pyic_ldap',
      author='Thomas Lim',
      author_email='txl11@ic.ac.uk',
      license='MIT',
      install_requires=['python-ldap'],
      packages=['pyic_ldap'],
      )