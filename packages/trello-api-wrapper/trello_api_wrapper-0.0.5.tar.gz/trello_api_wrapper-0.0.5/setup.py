from setuptools import setup

with open("README.md", "r") as fh:
    readme = fh.read()

setup(name='trello_api_wrapper',
    version='0.0.5',
    url='https://github.com/JordyAraujo/Trello_Api_Wrapper',
    license='MIT License',
    author='Jordy Araújo',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='jordyaraujo@outlook.com',
    keywords='trello api wrapper',
    description=u'Object oriented Python wrapper for Trello API',
    packages=['trello_api_wrapper'],
    install_requires=['httpx'],)
