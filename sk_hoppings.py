import numpy as np

sqrt3 = np.sqrt(3)

# Slater-Koster hij expressions per orbital pair
SK_HIJ_EXPRESSIONS = {
    "dxy_px":   lambda l, m, n, ts, tp: sqrt3 * l**2 * m * ts + m * (1 - l**2) * tp,
    "dxy_py":   lambda l, m, n, ts, tp: sqrt3 * m**2 * l * ts + l * (1 - m**2) * tp,
    "dxy_pz":   lambda l, m, n, ts, tp: sqrt3 * l * m * n * ts - 2 * l * m * n * tp,
    "dyz_px":   lambda l, m, n, ts, tp: sqrt3 * m * n * l * ts - 2 * m * n * l * tp,
    "dyz_py":   lambda l, m, n, ts, tp: sqrt3 * m**2 * n * ts + n * (1 - 2 * m**2) * tp,
    "dyz_pz":   lambda l, m, n, ts, tp: sqrt3 * m * n**2 * ts + m * (1 - 2 * n**2) * tp,
    "dxz_px":   lambda l, m, n, ts, tp: sqrt3 * l**2 * n * ts + n * (1 - 2 * l**2) * tp,
    "dxz_py":   lambda l, m, n, ts, tp: sqrt3 * l * m * n * ts - 2 * l * m * n * tp,
    "dxz_pz":   lambda l, m, n, ts, tp: sqrt3 * l * n**2 * ts + l * (1 - 2 * n**2) * tp,
    "dx2y2_px": lambda l, m, n, ts, tp: sqrt3/2 * l * (l**2 - m**2) * ts + l * (1 - l**2 + m**2) * tp,
    "dx2y2_py": lambda l, m, n, ts, tp: sqrt3/2 * m * (l**2 - m**2) * ts - m * (1 + l**2 - m**2) * tp,
    "dx2y2_pz": lambda l, m, n, ts, tp: sqrt3/2 * n * (l**2 - m**2) * ts - n * (l**2 - m**2) * tp,
    "dz2_px":   lambda l, m, n, ts, tp: l * (n**2 - 0.5 * (l**2 + m**2)) * ts - sqrt3 * l * n**2 * tp,
    "dz2_py":   lambda l, m, n, ts, tp: m * (n**2 - 0.5 * (l**2 + m**2)) * ts - sqrt3 * m * n**2 * tp,
    "dz2_pz":   lambda l, m, n, ts, tp: n * (n**2 - 0.5 * (l**2 + m**2)) * ts + sqrt3 * n * (l**2 + m**2) * tp,
    # Add more entries here...
}

def compute_w_v(kx, ky, kz, a, c, tpd_sigma, tpd_pi, R_Ni_S, R_Nip_S, hij_func):
    def sk_sum(R_list):
        H = 0.0 + 0.0j
        for Ri in R_list:
            norm = np.linalg.norm(Ri)
            l, m, n = Ri / norm
            hij = hij_func(l, m, n, tpd_sigma, tpd_pi)
            phase = np.exp(1j * (kx * Ri[0] + ky * Ri[1] + kz * Ri[2]))
            H += hij * phase
        return H

    w = sk_sum(R_Ni_S)
    v = sk_sum(R_Nip_S)
    return w, v

def compute_w_v_dispatch(kx, ky, kz, config):
    key = f"{config['orbital1']}_{config['orbital2']}"
    if key not in SK_HIJ_EXPRESSIONS:
        raise NotImplementedError(f"No SK expression defined for orbital pair: {key}")

    return compute_w_v(
        kx, ky, kz,
        config["a"], config["c"],
        config["tns_sigma"], config["tns_pi"],
        config["R_Ni_S"], config["R_Nip_S"],
        SK_HIJ_EXPRESSIONS[key]
    )