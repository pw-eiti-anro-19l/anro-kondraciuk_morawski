#! /usr/bin/python

import json
from tf.transformations import *

xaxis, yaxis, zaxis = (1, 0, 0), (0, 1, 0), (0, 0, 1)

if __name__ == '__main__':
    params = {}
    results = ''
    with open('../dh_data.json', 'r') as file:
        params = json.loads(file.read())

    with open('../urdf.yaml', 'w') as file:
        for key in params.keys():
            a, d, alpha, theta = params[key]
            a, d, alpha, theta = float(a), float(d), float(alpha), float(theta)

            tz = translation_matrix((0, 0, d))
            rz = rotation_matrix(theta, zaxis)
            tx = translation_matrix((a, 0, 0))
            rx = rotation_matrix(alpha, xaxis)

            matrix = concatenate_matrices(tx, rx, tz, rz)

            rpy = euler_from_matrix(matrix)
            xyz = translation_from_matrix(matrix)

            file.write(key + ":\n")
            file.write("  j_xyz: {} {} {}\n".format(*xyz))
            file.write("  j_rpy: {} {} {}\n".format(*rpy))
            file.write("  l_xyz: 0 0 {}\n".format(-d/2))
            file.write("  l_rpy: 0 0 0\n")
	    file.write("  l_len: {}\n".format(d))
