""""
Copyright(C) Venidera Research & Development, Inc - All Rights Reserved
Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Marcos Leone Filho <marcos@venidera.com>
"""

import unittest
import logging
import os
import getpass
from barrel_client import Connection
from vplantnaming.naming import PlantNaming

# General procedures to show the log
logging.basicConfig(
    format='%(asctime)s - %(levelname)s: ' +
    '(%(filename)s:%(funcName)s at %(lineno)d): %(message)s',
    datefmt='%b %d %H:%M:%S',
    level=logging.INFO)

SERVER = 'miran-barrel.venidera.net'
PORT = 9090
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')
if not USERNAME or not PASSWORD:
    USERNAME = input('Por favor, digite o email do usuario: ')
    PASSWORD = getpass.getpass('Por favor, digite a senha: ', stream=None)

CON = Connection(server=SERVER, port=PORT)
RES = CON.do_login(USERNAME, PASSWORD)
if not RES:
    raise Exception('Could not login into Venidera Miran')


class TestPlantNaming(unittest.TestCase):
    """ Tests the plant naming interface """
    def test_method(self):
        """ Basic test method """
        testobj = PlantNaming(CON)
        self.assertIsInstance(testobj.match_dict, dict,
                              'Error. Not a dictionary!')
        self.assertTrue('uhe' in testobj.match_dict and
                        'ute' in testobj.match_dict,
                        'Dictionary structure is corrupted')
