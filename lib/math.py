import numpy as np
from scipy.ndimage import uniform_filter

def log_chroma(img, eps=1e-8):
    R = img[...,0].astype(np.float32) + eps
    G = img[...,1].astype(np.float32) + eps
    B = img[...,2].astype(np.float32) + eps

    u = np.log(R / G)
    v = np.log(B / G)
    return u, v, R, G, B

def sliding_box_mean(u, v, block_size, max_uv_shift):
    if block_size % 2 == 0:
        block_size += 1
    u_mean = uniform_filter(u, size=block_size, mode='reflect')
    v_mean = uniform_filter(v, size=block_size, mode='reflect')

    # clamp large chroma shifts
    u_mean = np.clip(u_mean, -max_uv_shift, max_uv_shift)
    v_mean = np.clip(v_mean, -max_uv_shift, max_uv_shift)

    return u_mean, v_mean