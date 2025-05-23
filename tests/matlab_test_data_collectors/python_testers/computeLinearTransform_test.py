import logging
import os
from pathlib import Path

import numpy as np

from kwave.utils.math import compute_rotation_between_vectors
from tests.matlab_test_data_collectors.python_testers.utils.record_reader import TestRecordReader


def test_compute_linear_transform():
    test_record_path = os.path.join(Path(__file__).parent, "collectedValues/computeLinearTransform.mat")
    reader = TestRecordReader(test_record_path)

    for i in range(len(reader)):
        params = reader.expected_value_of("params")
        if len(params) == 2:
            pos1, pos2 = params
            pos1, pos2 = pos1.astype(float), pos2.astype(float)

            rot_mat, direction = compute_rotation_between_vectors(pos1, pos2)
            offset_pos = 0

        else:
            pos1, pos2, offset = params
            pos1, pos2, offset = pos1.astype(float), pos2.astype(float), float(offset)
            rot_mat, direction = compute_rotation_between_vectors(pos1, pos2)
            offset_pos = pos1 + offset * direction

        if not np.any(np.isnan(reader.expected_value_of("rotMat"))):
            assert np.allclose(rot_mat, reader.expected_value_of("rotMat"))
            assert np.allclose(offset_pos, reader.expected_value_of("offsetPos"))
        reader.increment()

    logging.log(logging.INFO, "compute_rotation_between_vectors(..) works as expected!")


if __name__ == "__main__":
    test_compute_linear_transform()
