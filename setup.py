""""
Copyright(C) Venidera Research & Development, Inc - All Rights Reserved
Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Marcos Leone Filho <marcos@venidera.com>
"""

import os
import atexit
import shutil
import logging
import tempfile
import subprocess
import distutils.cmd
import distutils.log

from setuptools import find_packages, setup
from setuptools.command.install import install


__name__ = 'vplantnaming'
__version__ = '0.0.1'
__author__ = 'Marcos Leone Filho'
__author_email__ = 'marcos@venidera.com'
__url__ = 'https://bitbucket.org/venidera/vplantnaming'
__description__ = 'A package for matching plant naming in Brazil'
__keywords__ = 'venidera plant naming matching operation planning standard'
__classifiers__ = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Intended Audience :: System Administrators',
    'Operating System :: Unix',
    'Topic :: Utilities'
]
__license__ = 'Proprietary'
__public_dependencies__ = [
    'unidecode',
    'git+https://git@bitbucket.org/venidera/barrel_client.git']
__private_dependencies__ = []


class PostInstallCommand(install):
    """ customizing post-install actions """
    def __init__(self, *args, **kwargs):
        super(PostInstallCommand, self).__init__(*args, **kwargs)
        atexit.register(PostInstallCommand._post_install)

    @staticmethod
    def _post_install():
        # Manually installing dependencies
        for dep in __private_dependencies__:
            if any([i + '://' in dep for i in ['ssh', 'http', 'https']]):
                os.system('pip install --upgrade %s' % dep)
            else:
                # Capturing access token
                token = os.environ.get('ACCESS_TOKEN', None)
                # Creating prefix dependency urls
                prefix = 'git+https://x-token-auth:%s@bitbucket.org/venidera' %\
                    token if token else 'git+ssh://git@bitbucket.org/venidera'
                os.system('pip install --upgrade %s/%s.git' % (prefix, dep))
        for dep in __public_dependencies__:
            if any([i + '://' in dep for i in ['ssh', 'http', 'https']]):
                os.system('pip install --upgrade %s' % dep)
        # Removing cache and egg files
        os.system('rm -vrf ./build ./dist ./*.pyc ./*.tgz ./*.egg-info')
        os.system('find ' + __name__ + ' | grep -E ' +
                  '"(__pycache__|\\.pyc|\\.pyo$)" | xargs rm -rf')


class PylintCommand(distutils.cmd.Command):
    """ customizing pylint checks """
    user_options = [('pylint-rcfile=', None, 'path to Pylint config file')]

    def initialize_options(self):
        """ Pre-process options. """
        import requests
        # Capturing pylint file
        resp = requests.get('https://drive.google.com/a/venidera.com/uc?id=' +
                            '1TLdYAyQLrxxaHtJQUFxUbrcUaolOfXcU&export=download')
        # Creating temporary repository
        repo = tempfile.mkdtemp()
        # Creating pylint file repository
        pylint = '%s/pylint.rc' % repo
        # Writing pylint file to temporary repository
        with open(pylint, 'wb') as pylintfile:
            pylintfile.write(resp.content)
        # Adding custom pylint file
        self.pylint_rcfile = pylint if os.path.isfile(pylint) else ''

    def finalize_options(self):
        """ Post-process options. """
        if self.pylint_rcfile:
            assert os.path.exists(self.pylint_rcfile), (
                'Pylint config file %s does not exist.' % self.pylint_rcfile)

    def run(self):
        # Executing custom pylint
        resp = subprocess.call('python setup.py lint --lint-rcfile %s' % (
            self.pylint_rcfile), shell=True)
        # Checking if call was executed with no errors
        if resp != 0:
            logging.critical('Por favor, cheque seu código, pois há %s',
                             'problemas de escrita de código no padrão PEP8!')
        else:
            logging.info('Parabéns! Não foram detectados problemas %s',
                         'com a escrita do seu código.')
        # Removing the temporary directory
        shutil.rmtree('/'.join(self.pylint_rcfile.split('/')[:-1]))


# Running setup
setup(
    name=__name__,
    version=__version__,
    url=__url__,
    description=__description__,
    long_description=open('README.md').read(),
    author=__author__,
    author_email=__author_email__,
    license=__license__,
    keywords=__keywords__,
    packages=find_packages(),
    install_requires=[
        'pylint',
        'requests',
        'setuptools-lint'
    ] + [p for p in __public_dependencies__ if not any(
        [i + '://' in p for i in ['ssh', 'http', 'https']])],
    classifiers=__classifiers__,
    cmdclass={
        'pylint': PylintCommand,
        'install': PostInstallCommand
    },
    test_suite='tests'
)
