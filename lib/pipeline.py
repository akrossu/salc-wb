import numpy as np
from scipy.ndimage import gaussian_filter

from lib.color_utils import linear_to_srgb
from lib.math import log_chroma, sliding_box_mean
from lib.gray_world_prior import compute_shades_of_gray_prior
from lib.debug import debug_rgb, debug_log_chroma, debug_uv_mean, debug_gain_maps, debug_normal_gain_maps, debug_linear_to_srgb

# Const definitions
block_size=151
smooth_sigma=3
prior_alpha=0.25
max_uv_shift=0.6
max_gain=3.0
min_gain=0.35
esp = 1e-8

def salc_wb_pipeline(img_srgb, debug=False):
    # Convert to log_chroma
    # Used in CCC approaches
    u, v, R, G, B = log_chroma(img_srgb)

    # local-mean statistical estimates
    # Retinex + log-chroma instead of histogram
    u_mean, v_mean = sliding_box_mean(u, v, block_size, max_uv_shift)

    # prior Shades-of-Gray Alogrithm across r,g,b using Minkowski p-norm
    prior_gr, prior_gg, prior_gb = compute_shades_of_gray_prior(R, G, B)

    # convert u_mean, v_mean -> per-pixel RGB gains
    gr = np.exp(-u_mean)
    gg = np.ones_like(gr)
    gb = np.exp(-v_mean)

    # normalize local gains so geometric mean = 1 (preserves luminance)
    geom = (gr * gg * gb) ** (1.0/3.0)
    gr = gr / (geom + esp)
    gg = gg / (geom + esp)
    gb = gb / (geom + esp)

    # Apply global prior
    # Similar to blending max-posterior FFCC uses (multiplicative blend keesp scale)
    alpha = np.clip(prior_alpha, 0.0, 1.0)
    gr = (prior_gr ** alpha) * (gr ** (1.0 - alpha))
    gg = (prior_gg ** alpha) * (gg ** (1.0 - alpha))
    gb = (prior_gb ** alpha) * (gb ** (1.0 - alpha))

    # smooth gains
    # IFFCC uses spatial interp + smoothing; this is a much more simple smooth without integral 3:
    gr_s = gaussian_filter(gr, sigma=smooth_sigma, mode='reflect')
    gg_s = gaussian_filter(gg, sigma=smooth_sigma, mode='reflect')
    gb_s = gaussian_filter(gb, sigma=smooth_sigma, mode='reflect')

    # clip gains (magenta clouds haunt my dreams)
    gr_s = np.clip(gr_s, min_gain, max_gain)
    gg_s = np.clip(gg_s, min_gain, max_gain)
    gb_s = np.clip(gb_s, min_gain, max_gain)

    # normalize green scale
    scale = gg_s.copy()
    gr_s = gr_s / (scale + esp)
    gg_s[:] = 1.0 # don't correct green since it's weighted heavy in Bayer
    gb_s = gb_s / (scale + esp)

    # apply gains
    img_out_lin = np.empty_like(img_srgb)
    img_out_lin[...,0] = img_srgb[...,0] * gr_s
    img_out_lin[...,1] = img_srgb[...,1] * gg_s
    img_out_lin[...,2] = img_srgb[...,2] * gb_s

    # simple linear -> srgb wtihtout anything fancy
    img_out_lin = np.clip(img_out_lin, 0.0, 1.0)
    img_out = linear_to_srgb(img_out_lin)

    if (debug):
        debug_rgb(R, G, B)
        debug_log_chroma(u, v)
        debug_uv_mean(u_mean, v_mean)
        debug_gain_maps(gr_s, gg_s, gb_s)
        debug_normal_gain_maps(gr, gg, gb)
        debug_linear_to_srgb(img_out_lin)

    return img_out, gr_s, gg_s, gb_s