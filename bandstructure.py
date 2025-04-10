import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from hamiltonian import H_total

# Use LaTeX fonts for publication
plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Computer Modern Roman"],
    "axes.labelsize": 14,
    "font.size": 14,
    "legend.fontsize": 12,
    "xtick.labelsize": 12,
    "ytick.labelsize": 12
})

def compute_band_structure(config, filename_prefix):
    k_Lp = config["k_Lp"]
    k_Gamma = config["k_Gamma"]
    k_L = config["k_L"]
    
    num_kpts = 100
    k_path = np.concatenate([
        np.linspace(k_Lp, k_Gamma, num_kpts),
        np.linspace(k_Gamma, k_L, num_kpts)
    ])

    # Cumulative k-distance
    k_dist = np.zeros(len(k_path))
    for i in range(1, len(k_path)):
        dk = np.linalg.norm(k_path[i] - k_path[i-1])
        k_dist[i] = k_dist[i-1] + dk
    
    # High symmetry points for x-ticks
    k_Lp = k_dist[0]
    k_G  = k_dist[num_kpts - 1]
    k_L  = k_dist[-1]

    # Compute eigenvalues
    eigvals_list = []
    for k in k_path:
        Hk = H_total(*k, config=config)
        eigvals = np.linalg.eigvalsh(Hk)
        eigvals_list.append(np.sort(eigvals.real))
    eigvals_array = np.array(eigvals_list)
    
    # ------------------------
    # Save to file for Gnuplot
    # ------------------------
    with open(f"band_{filename_prefix}.dat", "w") as f:
        for i in range(len(k_path)):
            line = f"{k_dist[i]:.6f} " + " ".join(f"{e:.6f}" for e in eigvals_array[i])
            f.write(line + "\n")
    print(f"Band structure data saved in 'band_{filename_prefix}.dat'.")
    
    # ------------------------
    # Plotting and Saving
    # ------------------------
    plt.figure(figsize=(7, 8))    
    for i in range(eigvals_array.shape[1]):
        plt.plot(k_dist, eigvals_array[:, i], color='black', lw=1.0)

    plt.axvline(k_G,  color='gray', linestyle='--', linewidth=0.8)
    plt.xticks([k_Lp, k_G, k_L], [r"$L'$", r"$\Gamma$", r"$L$"])
    plt.ylabel(r"Energy (eV)")
    plt.xlim (np.min(k_dist), np.max(k_dist))
    # plt.ylim (-6,0)
    plt.title(f"Band structure: {filename_prefix}")
    plt.grid(True, linestyle='--', alpha=0.3)
    plt.tight_layout()
    plt.savefig(f"band_{filename_prefix}.pdf", dpi=300)
    plt.show()
    print(f"Band structure plot saved in 'band_{filename_prefix}.pdf'.")
    
    # ------------------------
    # Plotting and Saving
    # ------------------------
    colors = plt.get_cmap('tab10', 8)
    plt.figure(figsize=(7, 8))
    for i in range(eigvals_array.shape[1]):
        plt.plot(k_dist, eigvals_array[:, i], color=colors(i), lw=2.0, label=fr'Band {i+1}')

    plt.axvline(k_G,  color='gray', linestyle='--', linewidth=0.8)
    plt.xticks([k_Lp, k_G, k_L], [r"$L'$", r"$\Gamma$", r"$L$"])
    plt.ylabel(r"Energy (eV)")
    plt.xlim (np.min(k_dist), np.max(k_dist))
    # plt.ylim (-6,0)
    plt.title(f"Band structure: {filename_prefix}")
    plt.grid(True, linestyle='--', alpha=0.3)
    plt.legend(loc='best', frameon=False)
    plt.tight_layout()
    plt.savefig(f"band_color_{filename_prefix}.pdf", dpi=300)
    # plt.show()
    print(f"Band structure plot (in color) saved in 'band_color_{filename_prefix}.pdf'.")
