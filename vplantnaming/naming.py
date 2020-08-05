""""
Copyright(C) Venidera Research & Development, Inc - All Rights Reserved
Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Marcos Leone Filho <marcos@venidera.com>
"""

import logging
import re
import tempfile
from copy import deepcopy
from shutil import rmtree
from unidecode import unidecode
import barrel_client


def name_to_id(mystring):
    """ converts a name into an id-like string """
    mystring = re.sub(r'[\W_]+', ' ',
                      re.sub(r'\s+', ' ', unidecode(mystring))
                     ).lower().strip().replace(' ', '_')
    return mystring

def check_equivalent_gens(nome_id, dessem2sagic, sagic_names):
    """" if name shows up again, this means that this hydro
        plant is a equivalent one (two or more hydro plants
        combined in one plant). since we want to sum these
        series, we add them to the list """
    if nome_id in dessem2sagic:
        dessem2sagic[nome_id] += deepcopy(sagic_names)
        dessem2sagic[nome_id] = list(set(
            dessem2sagic[nome_id]))
    else:
        dessem2sagic[nome_id] = sagic_names

class PlantNaming():
    """ PlantNaming class for loading/matching plant info
        from Venidera Miran """
    def __init__(self, con):
        """ Sets basic data for the class """
        logging.debug('Setting basic data for PlantNaming class...')
        assert (isinstance(con, barrel_client.client.Connection) and
                con.is_logged()),\
            'con must be a valid logged-in barrel_client connection'
        self.con = con
        self.tmp_folder = tempfile.mkdtemp() + '/'
        self.plants_by_ceg = dict()
        self.__load_miran_plants()
        self.dessem_sagic_name = self.__get_dessem_sagic_map()

    def __del__(self):
        """ Destructor """
        rmtree(self.tmp_folder)

    def __load_miran_plants(self):
        """ Carrega as usinas da plataforma Venidera Miran """
        logging.info('Retrieving plant data from Miran...')
        types = ['Central_geradora_hidreletrica',
                 'Central_geradora_undieletrica',
                 'Central_geradora_eolica',
                 'Pequena_central_hidreletrica',
                 'Central_geradora_solar_fotovoltaica',
                 'Usina_hidreletrica',
                 'Usina_termeletrica',
                 'Usina_termonuclear']
        results = list()
        for tipo_barrel in types:
            res = self.con.get_entity(
                params={'type': tipo_barrel, 'files': False, 'ts': False})
            logging.debug('%s entities matching type %s.',
                          len(res), tipo_barrel)
            if res:
                results += res
        logging.info('%s plant data retrieved from Miran.', len(results))
        logging.debug('Indexing plant data...')
        total = 0
        for entity in results:
            if 'cepel' in entity['data']:
                total += 1
                if 'tipo' not in entity['data']:
                    tipo = entity['data']['aneel']['tipo'].lower()
                    entity['data']['tipo'] = tipo
                else:
                    tipo = entity['data']['tipo']
                if tipo in ['uhe', 'pch', 'cgh']:
                    tipo = 'uhe'
                elif tipo in ['ute', 'utn']:
                    tipo = 'ute'
                else:
                    continue
                if tipo not in self.plants_by_ceg:
                    self.plants_by_ceg[tipo] = dict()
                self.plants_by_ceg[tipo][entity['ids']['ceg_norm']] = entity
        logging.debug('Finished indexing plant data. %d indexed plants.',
                      total)

    def __get_dessem_sagic_map(self):
        """ retorna o arquivo de-para do sagic<->dessem"""
        dessem2sagic = {'uhe': {}, 'ute': {}}
        for plant_type in self.plants_by_ceg:
            for _, plant in self.plants_by_ceg[plant_type].items():
                if 'cepel' not in plant['data'] or 'ons' not in plant['data']:
                    continue
                sagic_names = list()
                for _, sagic_item in plant['data']['ons'].items():
                    sagic_names += sagic_item['sagic_nome_id']
                sagic_names = list(set(sagic_names))
                for _, cepel_item in plant['data']['cepel'].items():
                    if 'nome_id' in cepel_item:
                        for nome_id in cepel_item['nome_id']:
                            check_equivalent_gens(nome_id,
                                                  dessem2sagic[plant_type],
                                                  sagic_names)
                    elif 'nome' in cepel_item:
                        nome_id = name_to_id(cepel_item['nome'])
                        check_equivalent_gens(nome_id,
                                              dessem2sagic[plant_type],
                                              sagic_names)
        return dessem2sagic
