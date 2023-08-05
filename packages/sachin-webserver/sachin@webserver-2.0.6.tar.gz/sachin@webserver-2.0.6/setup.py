from setuptools import setup
from pathlib import Path

this_directory = Path(__file__).parent
long_desciption = (this_directory / "README.md").read_text()

setup(
    name='sachin@webserver',
    version='2.0.6',
    description='This is a small web server to serve PHP/Web files',
    long_description=long_desciption,
    long_description_content_type='text/markdown',
    keywords='php webserver localhost',
    author='Sachin Acharya',
    author_email='acharyaraj71+webserver@gmail.com',
    packages=['webserver'],
    install_requires = ['py_setenv', 'colorama'], # pathlib2
    url='https://github.com/sachin-acharya-projects/webserver',
    package_data={
        '': ['Liscence.md', 'php-cli-server.ini', 'README.md', 'settings.json']
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    entry_points = {
        'console_scripts': [
            'server = webserver.__main__:main'
        ]
    }
)

# python .\setup.py sdist bdist_wheel