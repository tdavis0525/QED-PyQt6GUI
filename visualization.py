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
import mayavi.mlab as mlab
import numpy as np
import threading
from io import BytesIO
from PIL import ImageGrab
import base64

def visualize_data(filename):
    try:
        with open(filename, 'r') as f:
            data = json.load(f)

        atom_positions = []
        electron_positions = []
        for molecule_data in data['molecules']:
            for atom_data in molecule_data.get('atoms', []):
                atom_positions.append(atom_data['position'])
            for electron_data in molecule_data.get('electrons', []):
                electron_positions.append(electron_data['position'])

        # Create a new Mayavi figure
        mlab.figure(size=(800, 600))

        if atom_positions:
            mlab.points3d(np.array(atom_positions)[:, 0],
                          np.array(atom_positions)[:, 1],
                          np.array(atom_positions)[:, 2],
                          scale_factor=0.2, color=(0, 1, 0), name='Atoms')

        if electron_positions:
            mlab.points3d(np.array(electron_positions)[:, 0],
                          np.array(electron_positions)[:, 1],
                          np.array(electron_positions)[:, 2],
                          scale_factor=0.1, color=(1, 0, 0), name='Electrons')

        mlab.show()

        # Capture thumbnail after the window is shown
        thumbnail_image = ImageGrab.grab()
        thumbnail = base64.b64encode(thumbnail_image.tobytes()).decode()
        return thumbnail

    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error visualizing data: {e}")
        return None