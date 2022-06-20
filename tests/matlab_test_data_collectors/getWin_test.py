from kwave.utils import get_win
from scipy.io import loadmat
import numpy as np
import pytest


@pytest.mark.skip(reason="Reference files to not always exist.")
def test_get_win():
    data = []
    for i in range(5440):
        print('i: => ', i)
        filepath = f'/data/code/Work/collectedValues/{i:06d}.mat'
        recorded_data = loadmat(filepath)

        N = recorded_data['N']
        input_args = recorded_data['input_args'][0]
        type_ = recorded_data['type_'][0]

        rotation = bool(input_args[1])
        symmetric = bool(input_args[3])
        square = bool(input_args[5])
        assert recorded_data['cg'].size == 1
        cg = float(recorded_data['cg'])
        win = recorded_data['win']

        if len(input_args) == 8:
            param = float(input_args[7])
        else:
            param = None
            assert len(input_args) == 6

        N = np.squeeze(N)

        data.append({
            'test_case_idx': i,
            'N': N,
            'type_': type_,
            'param': param,
            'rotation': rotation,
            'symmetric': symmetric,
            'square': square,
            'cg': cg,
            'win': win,
        })

        # print(N, type_, param, rotation, symmetric, square, win)

        win_py, cg_py = get_win(N, type_,
                                param=param, rotation=rotation,
                                symmetric=symmetric, square=square)

        assert np.allclose(win_py, win, equal_nan=True)
        assert np.allclose(cg_py, cg, equal_nan=True)
