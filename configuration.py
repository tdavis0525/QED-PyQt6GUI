# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import json
import numpy as np

class MoleculeConfig:
    def __init__(self, name, atom_configs, electron_configs):
        self.name = name
        self.atom_configs = atom_configs
        self.electron_configs = electron_configs

    def to_dict(self):
        return {
            'name': self.name,
            'atoms': self.atom_configs,
            'electrons': self.electron_configs
        }

    @staticmethod
    def from_dict(mol_data):
        return MoleculeConfig(mol_data['name'], mol_data['atoms'], mol_data['electrons'])


class Configuration:
    def __init__(self,
                 mongodb_uri="mongodb://localhost:27017/",
                 database_name="qed_adamant",
                 collection_name="simulation_results",
                 num_steps=1000,
                 dt=0.01,
                 molecule_configs=None):

        self.mongodb_uri = mongodb_uri
        self.database_name = database_name
        self.collection_name = collection_name
        self.num_steps = num_steps
        self.dt = dt
        self.molecule_configs = molecule_configs if molecule_configs is not None else []

    def to_dict(self):
        return {
            "mongodb": {
                "uri": self.mongodb_uri,
                "database": self.database_name,
                "collection": self.collection_name
            },
            "simulation": {
                "num_steps": self.num_steps,
                "dt": self.dt
                # ... other simulation parameters
            },
            "molecules": [mol.to_dict() for mol in self.molecule_configs]
        }

    def from_dict(self, config_dict):
        mongodb_config = config_dict.get("mongodb", {})
        simulation_config = config_dict.get("simulation", {})
        molecules_config = config_dict.get("molecules", [])

        self.mongodb_uri = mongodb_config.get("uri", "mongodb://localhost:27017/")
        self.database_name = mongodb_config.get("database", "qed_adamant")
        self.collection_name = mongodb_config.get("collection", "simulation_results")
        self.num_steps = simulation_config.get("num_steps", 1000)
        self.dt = simulation_config.get("dt", 0.01)
        self.molecule_configs = [MoleculeConfig.from_dict(mol_data) for mol_data in molecules_config]

    def __str__(self):
        return json.dumps(self.to_dict(), indent=4)