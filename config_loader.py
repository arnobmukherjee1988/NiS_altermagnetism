import json
import numpy as np

def evaluate_vectors(expr_vectors, a, c, a_star=None, c_star=None):
    local_dict = {
        'a': a, 'c': c, 'sqrt': np.sqrt,
        'a_star': a_star, 'c_star': c_star
    }
    return np.array([
        [eval(str(expr), {}, local_dict) for expr in vec]
        for vec in expr_vectors
    ])

def load_config(filename="input_config.json"):
    with open(filename, "r") as f:
        config = json.load(f)

    a = config["a"]
    c = config["c"]
    a_star = 4 * np.pi / (np.sqrt(3) * a)
    c_star = 2 * np.pi / c

    config["a_star"] = a_star
    config["c_star"] = c_star

    config["R_Ni_S"] = evaluate_vectors(config["R_Ni_S"], a, c)
    config["R_Nip_S"] = evaluate_vectors(config["R_Nip_S"], a, c)

    config["k_Lp"] = evaluate_vectors([config["k_Lp"]], a, c, a_star, c_star)[0]
    config["k_Gamma"] = evaluate_vectors([config["k_Gamma"]], a, c, a_star, c_star)[0]
    config["k_L"] = evaluate_vectors([config["k_L"]], a, c, a_star, c_star)[0]

    return config
