import numpy as np
from config_loader import load_config
from bandstructure import compute_band_structure

config = load_config()

# Reciprocal lattice vectors (in 1/Å)
a_star = 4 * np.pi / (np.sqrt(3) * config['a'])
c_star = 2 * np.pi / config['c']

# k_Lp = np.array([0.5 * a_star, 0.0, -0.5 * c_star])
# k_Gamma = np.array([0.0, 0.0, 0.0])
# k_L = np.array([0.5 * a_star, 0.0, 0.5 * c_star])

# Lp = np.array([-np.pi/a, -np.pi/(np.sqrt(3)*a), -np.pi/c])  # L'
# G  = np.array([0.0, 0.0, 0.0])                              # Gamma
# L  = np.array([np.pi/a, np.pi/(np.sqrt(3)*a), np.pi/c])     # L

# num_kpts = 100
# k_path = np.concatenate([
#     np.linspace(k_Lp, k_Gamma, num_kpts),
#     np.linspace(k_Gamma, k_L, num_kpts)
# ])

# k_labels = {
#     "$L'$": 0,
#     "$\\Gamma$": num_kpts - 1,
#     "$L$": 2 * num_kpts - 1
# }

prefix = config['orbital1'] + '_' + config['orbital2']
compute_band_structure(config, prefix)
