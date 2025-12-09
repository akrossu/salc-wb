import numpy as np
import matplotlib.pyplot as plt

# ------------------------------------------
# The math in this file is over my head.
# Testing methodology will be listed
#   in the README.
# ------------------------------------------

def compute_image_illuminant(gr_s, gg_s, gb_s):
   # geometric mean vector
    eps = 1e-8
    R_mean = np.exp(np.mean(np.log(gr_s + eps)))
    G_mean = np.exp(np.mean(np.log(gg_s + eps)))
    B_mean = np.exp(np.mean(np.log(gb_s + eps)))
    
    return np.array([R_mean, G_mean, B_mean])

def angular_error(e_pred, e_gt):
    # angular error in degrees
    e_pred = np.asarray(e_pred, dtype=np.float64)
    e_gt = np.asarray(e_gt, dtype=np.float64)

    # Normalize
    e_pred /= (np.linalg.norm(e_pred) + 1e-8)
    e_gt /= (np.linalg.norm(e_gt) + 1e-8)

    cos_theta = np.clip(np.dot(e_pred, e_gt), -1.0, 1.0)
    theta_rad = np.arccos(cos_theta)
    return np.degrees(theta_rad)

# Credited to the implimentations of common color constancy datasets such as
# SFU Color Checker and NUS 8-Camera, and adaptated from standard ColorChecker-
# based illuminant estimation methods
def compute_color_checker_illuminant(raw16, checker_coords=None, patch_indices=None, visualize=True, bright_percentile=90):
    H, W, _ = raw16.shape

    y0, y1, x0, x1 = checker_coords if checker_coords is not None else (0, H, 0, W)
    if y0 > y1:
        y0, y1 = y1, y0
    if x0 > x1:
        x0, x1 = x1, x0

    checker = raw16[y0:y1, x0:x1, :]

    if patch_indices is None:
        patch_indices = [(i, 3) for i in range(6)]

    ph = checker.shape[0] // 6
    pw = checker.shape[1] // 4

    neutral_pixels = []
    patch_coords_list = []

    for r, c in patch_indices:
        y_start = r * ph
        y_end = (r+1) * ph
        x_start = c * pw
        x_end = (c+1) * pw

        patch = checker[y_start:y_end, x_start:x_end, :].reshape(-1,3)

        # Filter only bright pixels
        thr = np.percentile(patch, bright_percentile, axis=0)
        mask = np.all(patch >= thr, axis=1)
        patch_filtered = patch[mask]

        if patch_filtered.size > 0:
            neutral_pixels.append(patch_filtered)
            patch_coords_list.append((y_start+y0, y_end+y0, x_start+x0, x_end+x0))

    if len(neutral_pixels) == 0:
        raise ValueError("No neutral patch pixels found after bright filtering.")

    neutral_pixels = np.vstack(neutral_pixels)

    # Compute the per-channel gain
    patch_mean = neutral_pixels.mean(axis=0)
    e_gt = 1.0 / (patch_mean + 1e-8)  # gain to neutralize patch
    # Normalize geometric mean = 1
    geom = np.cbrt(np.prod(e_gt))
    e_gt /= geom

    if visualize:
        fig, ax = plt.subplots(1,1, figsize=(8,6))
        ax.imshow(np.clip(raw16,0,1))
        for yc0, yc1, xc0, xc1 in patch_coords_list:
            rect = plt.Rectangle((xc0, yc0), xc1-xc0, yc1-yc0, edgecolor='red', facecolor='none', linewidth=2)
            ax.add_patch(rect)
        ax.set_title("White/gray patches detected")
        ax.axis("off")
        plt.show()

    return e_gt, neutral_pixels
