

# A package for matching plant naming in Brazil

![GitHub Release](https://img.shields.io/badge/release-v0.0.1-blue.svg)
![GitHub license](https://img.shields.io/badge/license-Proprietary-yellow.svg)

This package retrieves plant data information from Venidera Miran and returns dictionaries for matching plant naming/coding across multiple formats, such as:

- ANEEL CEG
- CEPEL plant naming and coding standards (used in NEWAVE, SUISHI, DECOMP and DESSEM)
- ONS naming standards

## Table of contents
[TOC]

## Requirements

* Access to Venidera Miran infraestructure. Please [contact us for info regarding plans and pricing.](https://portal.venidera.com/contact/)
* Python 3.6 or superior (`sudo apt-get install python3.6` under Linux)
* Python virtual environment (`sudo apt-get install python3.6-venv` under Linux)

## Package structure

The initial directory structure should look like this:

- `vplantnaming` The top-level package directory.
    -   `README.md`  Description of the package -- should be written in Markdown.
    -   `setup.py` The script for building/installing the package.
    -   `LICENSE` Text of the license you choose.
    -   `.gitignore` Specifies untracked files that Git should ignore.
    -   `vplantnaming` Base package module. Must be all lowercase and no word separated.
        -   `naming.py`  Main package module.
    -   `scripts` Directory with top-level user scripts.
        -   `run.py` A standard script for running the application.
    -   `tests` Collection of general-purpose tests.
        -   `validate.py` Test script for module  `naming.py`.

### Customizing the setup.py file

The setup.py file is what describes the package, and tells setuptools how to package, build and install it. The setup script may include additional meta-data that must be set according to each project requirements. This information includes:

| Meta-Data | Description | Value | Notes
|--|--|--|--|
| name | name of the package | short string | The package should have short, all-lowercase names. Underscores can be used in the module name if it improves readability. |
| version | version of this release | short string | It is recommended that versions take the form _major.minor[.patch]_. See [PEP 440](https://www.python.org/dev/peps/pep-0440) for more details on versions. |
| author | package author's name | short string |  |
| author_email | email address of the package author | email address |  |
| url | the project's main homepage | URL | This will just be a link to GitHub, GitLab, Bitbucket, or similar code hosting service. |
| description | short, summary description of the package | short string |  |
| keywords | a list of keywords | list of strings | If you pass a comma-separated string `'foo,  bar'`, it will be converted to `['foo',  'bar']`, Otherwise, it will be converted to a list of one string. |
| classifiers | a list of classifiers | list of strings | The valid classifiers are listed on [PyPI](https://pypi.org/classifiers). |
| license | licence under which the project is released | short string | The `license` field is a text indicating the license covering the package and acts as an alias for the file `LICENSE`. |
| public_dependencies | a list of public Python [import packages](https://packaging.python.org/glossary/#term-import-package) | list of strings | | 
| private_dependencies | a list of private package dependencies | list of strings | These represent the private package names from Venidera on Bitbucket.| 

## Development and Tests

### 1. Cloning the repository
The first step aims to clone the `vplantnaming` repository from Bitbucket. If you don't have SSH configured, then you need to use the HTTPS protocol to communicate between your local system and Bitbucket Cloud. It is possible to change the current working directory to the location where you want the cloned directory to be made.
```bash
$ mkdir ~/git
$ git clone git@bitbucket.org:venidera/vplantnaming.git ~/git/vplantnaming
$ cd ~/git/vplantnaming
```

### 2. Installing the package
 Start by creating a new virtual environment for your project. Next, update the packages `pip` and `setuptools` to the latest version. Then install the package itself.
```bash
$ /usr/bin/python3.6 -m venv --prompt=" vplantnaming " venv
$ source venv/bin/activate
( vplantnaming ) $ pip install --upgrade setuptools pip
( vplantnaming ) $ python setup.py install
```

### 3. Code checking
It is also possible to check for errors in Python code using:
```bash
( vplantnaming ) $ python setup.py pylint
```
Pylint is a tool that tries to enforce a coding standard and looks for  [code smells](https://martinfowler.com/bliki/CodeSmell.html). Pylint will display several messages as it analyzes the code and it can also be used for displaying some statistics about the number of warnings and errors found in different files. The current package uses a custom [configuration file](https://drive.google.com/a/venidera.com/uc?id=1SeUYS-g-MTj-7a_XYwaXZUQpDiQ26JuW), tailored to Venidera code standard.


### 4. Testing package modules
Python tests are Python classes that reside in separate files from the code being tested. In this project, module tests are based on Python `unittest` package and are located in the `tests` directory. They can be run by the following code: 
```bash
( vplantnaming ) $ python setup.py test
```
In general, the developer can create and perform as many tests as he needs. However, it is important to validate them before committing a new change to the Bitbucket Cloud, as a way of avoiding errors. It is also important to mention that tests will only be performed if test classes extend the `unittest.TestCase` object.


### 5. Running the application
To run your package (and also to generate a script that helps other developers to execute your package), put your package's execution routines into `scripts/run.py` directory. Then, once package syntax is following Venidera code standards and all tests were performed, you can run the application by executing the following code:
```bash
( vplantnaming ) $ python scripts/run.py
```

Note that the `run.py` script contains basic code for understanding how this package works.

## Troubleshooting

Please file a BitBucket issue to [report a bug](https://bitbucket.org/venidera/data-models/issues?status=new&status=open).

## Maintainers

-   Marcos Leone Filho - [marcos@venidera.com](mailto:marcos@venidera.com)
-   Makoto Kadowaki -  [makoto@venidera.com](mailto:makoto@venidera.com)

## License

This package is released and distributed under the license  [GNU GPL Version 3, 29 June 2007](https://www.gnu.org/licenses/gpl-3.0.html).