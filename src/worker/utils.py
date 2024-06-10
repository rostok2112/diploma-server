from math import atan2, degrees
from numba import jit


@jit(nopython=True)
def compute_euler_angles(data_A, data_G, euler_degs_r, euler_degs_p, euler_degs_y, TAU, DT):
    Y, Z = 1, 2  # Индексы для доступа к элементам массивов
    
    accel_pitch = degrees(atan2(data_A[Y], data_A[Z]))
    accel_roll  = degrees(atan2(data_A[0], data_A[Z]))

    degs_r = TAU * (euler_degs_r - data_G[Y] * DT) + (1 - TAU) * accel_roll
    degs_p = TAU * (euler_degs_p + data_G[0] * DT) + (1 - TAU) * accel_pitch
    degs_y = euler_degs_y + data_G[Z] * DT
    
    return degs_r, degs_p, degs_y