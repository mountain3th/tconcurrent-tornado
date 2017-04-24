import pip
from setuptools import setup, find_packages


links = []
requires = []


requirements = pip.req.parse_requirements(
    'requirements.txt', session=pip.download.PipSession())

for item in requirements:
    # we want to handle package names and also repo urls
    if getattr(item, 'url', None):  # older pip has url
        links.append(str(item.url))
    if getattr(item, 'link', None): # newer pip has link
        links.append(str(item.link))
    if item.req:
        requires.append(str(item.req))

setup(
        name='tconcurrent-tornado',
        version='0.0.1',
        author='SAM',
        author_email='mountainking@126.com',
        description='A multi-threads future based on tornado\'s coroutine',
        license='MIT',
        packages=find_packages('tconcurrent'),
        package_dir={'': 'tconcurrent'},
        test_suite="tests",
        install_requires=requires,
        dependency_links=links
)
