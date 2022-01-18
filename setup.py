from setuptools import setup, find_packages

requires = [
    'Flask',
    'flask-jsonpify',
    'flask-restx',
]

setup(
    name='starbuck-rest',
    version='0.1',
    description='Cassandra REST interface',
    author='James Randell',
    author_email='jamesrandell@me.com',
    keywords='Cassandra REST API JSON',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires
)