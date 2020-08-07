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
        self.miran_plants = dict()
        self.plant_variables = ['cepelid', 'cepelname', 'cepelbus',
                                'ons_sagic', 'ananame', 'anaid', 'ceg']
        self.match_dict = {'uhe': {}, 'ute': {}}
        for _, item in self.match_dict.items():
            for i in self.plant_variables:
                item['by_' + i] = dict()
        self.__load_miran_plants()
        self.__compute_cepel_map()

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
                if tipo not in self.miran_plants:
                    self.miran_plants[tipo] = dict()
                self.miran_plants[tipo][entity['ids']['ceg_norm']] = entity
        logging.debug('Finished indexing plant data. %d indexed plants.',
                      total)

    def __fill_match_dict(self, plant_type, data):
        """ Fill match dictionary.
            Obs.: if name shows up again, this means that this hydro/thermal
            plant is a equivalent one (two or more hydro/thermal plants
            combined in one plant). since we want to sum these
            series (in the case of generation) or discard these items with more
            than one one plant (in the case of hydro variables),
            we add them to the list """
        for from_data_var in self.plant_variables:
            for i in data[from_data_var]:
                if i in self.match_dict[plant_type][
                        'by_' + from_data_var]:
                    for to_data_var in self.plant_variables:
                        self.match_dict[plant_type]['by_' + from_data_var][
                            i][to_data_var] += deepcopy(data[to_data_var])
                        self.match_dict[plant_type]['by_' + from_data_var][
                            i][to_data_var] = list(set(self.match_dict[
                                plant_type]['by_' + from_data_var][
                                    i][to_data_var]))
                else:
                    for to_data_var in self.plant_variables:
                        if i not in self.match_dict[plant_type][
                                'by_' + from_data_var]:
                            self.match_dict[plant_type]['by_' + from_data_var][
                                i] = dict()
                        self.match_dict[plant_type]['by_' + from_data_var][
                            i][to_data_var] = list(set(data[to_data_var]))

    def __compute_cepel_map(self):
        """ retorna o arquivo de-para do sagic<->dessem"""
        for plant_type in self.miran_plants:
            for ceg_norm, plant in self.miran_plants[plant_type].items():
                if 'cepel' not in plant['data'] or 'ons' not in plant['data']:
                    continue
                sagic_names = list()
                for _, sagic_item in plant['data']['ons'].items():
                    sagic_names += sagic_item['sagic_nome_id']
                sagic_names = list(set(sagic_names))
                ana_names = list()
                ana_ids = list()
                if 'ana' in plant['data']:
                    for ana_id, ana_item in plant['data']['ana'].items():
                        ana_ids.append(int(ana_id))
                        ana_names += ana_item['nome_id']
                sagic_names = list(set(sagic_names))
                ana_names = list(set(ana_names))
                ana_ids = list(set(ana_ids))
                for cepel_num, cepel_item in plant['data']['cepel'].items():
                    barras_anarede = list()
                    if 'barras_anarede' in cepel_item:
                        barras_anarede += cepel_item['barras_anarede']
                        barras_anarede = list(set(barras_anarede))
                    if 'nome_id' in cepel_item:
                        for nome_id in cepel_item['nome_id']:
                            data = {
                                'cepelid': [int(cepel_num)],
                                'cepelname': [nome_id],
                                'cepelbus': barras_anarede,
                                'ons_sagic': sagic_names,
                                'ananame': ana_names,
                                'anaid': ana_ids,
                                'ceg': [ceg_norm]}
                            self.__fill_match_dict(plant_type, data)
                    elif 'nome' in cepel_item:
                        nome_id = name_to_id(cepel_item['nome'])
                        data = {
                            'cepelid': [int(cepel_num)],
                            'cepelname': [nome_id],
                            'cepelbus': barras_anarede,
                            'ons_sagic': sagic_names,
                            'ananame': ana_names,
                            'anaid': ana_ids,
                            'ceg': [ceg_norm]}
                        self.__fill_match_dict(plant_type, data)
