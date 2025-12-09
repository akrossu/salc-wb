import numpy as np

# needed for jpg images
def srgb_to_linear(img):
    img = img.astype(np.float32) / 255.0
    mask = img <= 0.04045
    linear = np.empty_like(img, dtype=np.float32)
    linear[mask] = img[mask] / 12.92
    linear[~mask] = ((img[~mask] + 0.055) / 1.055) ** 2.4
    return linear

def linear_to_srgb(img):
    img = np.where(img <= 0.0031308,
                    12.92 * img,
                    1.055 * np.power(img, 1/2.4) - 0.055)
    return np.clip(img, 0, 1)

