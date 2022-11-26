from kwave.utils.maputils import make_bowl

from scipy.io import loadmat
import numpy as np
import os
from pathlib import Path



def test_makeBowl():
    collected_values_folder = os.path.join(Path(__file__).parent, 'collectedValues/makeBowl')

    num_collected_values = len(os.listdir(collected_values_folder))

    for i in range(num_collected_values):
        print(i)
        filepath = os.path.join(collected_values_folder, f'{i:06d}.mat')
        recorded_data = loadmat(filepath)

        params = recorded_data['params'][0]
        grid_size, bowl_pos, radius, diameter, focus_pos = params[:5]
        grid_size, bowl_pos, diameter, focus_pos = grid_size[0], bowl_pos[0], int(diameter), focus_pos[0]

        try:
            radius = int(radius)
        except OverflowError:
            radius = float(radius)

        binary = bool(params[6])
        remove_overlap = bool(params[8])
        expected_bowl = recorded_data['bowl']

        bowl = make_bowl(grid_size, bowl_pos, radius, diameter, focus_pos, binary=binary, remove_overlap=remove_overlap)

        assert np.allclose(expected_bowl, bowl)

    print('make_bowl(..) works as expected!')
