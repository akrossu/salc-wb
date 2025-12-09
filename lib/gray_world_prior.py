import numpy as np

def compute_shades_of_gray_prior(R, G, B, ESP=1e-8):
    p = 4
    mean_r = np.mean(R ** p) ** (1.0/p)
    mean_g = np.mean(G ** p) ** (1.0/p)
    mean_b = np.mean(B ** p) ** (1.0/p)

    global_norm = (mean_r + mean_g + mean_b) / 3.0
    prior_gr = global_norm / (mean_r + ESP)
    prior_gg = global_norm / (mean_g + ESP)
    prior_gb = global_norm / (mean_b + ESP)
    
    # normalize normalize normalize normalize normalize normalize normalize 
    prior_scale = (prior_gr * prior_gg * prior_gb) ** (1.0/3.0)
    prior_gr /= prior_scale
    prior_gg /= prior_scale
    prior_gb /= prior_scale

    return prior_gr, prior_gg, prior_gb