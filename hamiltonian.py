import numpy as np
from sk_hoppings import compute_w_v_dispatch

def H_spin_block(kx, ky, kz, config, spin='up'):
    Delta_Ni = config['Delta_Ni']
    epsilon_Ni = config['epsilon_Ni']
    epsilon_S = config['epsilon_S']
    Type = config.get("hopping_sign", 1)
    if Type not in [1, 2]:
      raise ValueError("Invalid hopping_sign: must be 1 or 2")

    w, v = compute_w_v_dispatch(kx, ky, kz, config)
    w1, w2, v1, v2 = w.real, w.imag, v.real, v.imag

    

    if Type == 1:
        w3, w4 = w1, -w2
        v3, v4 = v1, -v2
    elif Type == 2:
        w3, w4 = -w1, w2
        v3, v4 = -v1, v2
    else:
        raise ValueError("Invalid Type. Must be 1 or 2.")

    if spin == 'up':
        delta1 = -Delta_Ni / 2 + epsilon_Ni
        delta2 = +Delta_Ni / 2 + epsilon_Ni
    elif spin == 'down':
        delta1 = +Delta_Ni / 2 + epsilon_Ni
        delta2 = -Delta_Ni / 2 + epsilon_Ni
    else:
        raise ValueError("Spin must be 'up' or 'down'")

    H = np.array([
        [delta1, 0, w1 + 1j * w2, w3 + 1j * w4],
        [0, delta2, v1 + 1j * v2, v3 + 1j * v4],
        [w1 - 1j * w2, v1 - 1j * v2, epsilon_S, 0],
        [w3 - 1j * w4, v3 - 1j * v4, 0, epsilon_S]
    ], dtype=complex)
    return H

def H_total(kx, ky, kz, config):
    H_up = H_spin_block(kx, ky, kz, config, spin='up')
    H_dn = H_spin_block(kx, ky, kz, config, spin='down')
    return np.block([
        [H_up, np.zeros((4, 4), dtype=complex)],
        [np.zeros((4, 4), dtype=complex), H_dn]
    ])