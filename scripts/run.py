""""
Copyright(C) Venidera Research & Development, Inc - All Rights Reserved
Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Marcos Leone Filho <marcos@venidera.com>
"""

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

NAMING = PlantNaming(CON)
MATCH = NAMING.match_dict
PLANTS = NAMING.miran_plants
