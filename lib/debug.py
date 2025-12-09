import matplotlib.pyplot as plt

def debug_rgb(R, G, B):
    fig, axes = plt.subplots(1, 3, figsize=(18,6))
    axes[0].imshow(R)
    axes[1].imshow(G)
    axes[2].imshow(B)

    for ax in axes:
        ax.axis('off')
    plt.show()

def debug_log_chroma(u, v):
    plt.figure(figsize=(10,4))
    plt.subplot(1,2,1)
    plt.imshow(u, cmap='bwr')
    plt.colorbar()
    plt.title("Log-Chroma u")
    plt.axis('off')
    plt.subplot(1,2,2)
    plt.imshow(v, cmap='bwr')
    plt.colorbar()
    plt.title("Log-Chroma v")
    plt.axis('off')
    plt.show()

def debug_uv_mean(u_mean, v_mean):
    plt.figure(figsize=(10,4))
    plt.subplot(1,2,1)
    plt.imshow(u_mean, cmap='bwr')
    plt.colorbar()
    plt.title("Mean u")
    plt.subplot(1,2,2)
    plt.imshow(v_mean, cmap='bwr')
    plt.colorbar()
    plt.title("Mean v")
    plt.show()

def debug_gain_maps(gr, gg, gb):
    plt.figure(figsize=(12,4))
    plt.subplot(1,3,1)
    plt.imshow(gr, cmap='Reds')
    plt.colorbar()
    plt.title("R gain map")
    plt.subplot(1,3,2)
    plt.imshow(gg, cmap='Greens')
    plt.colorbar()
    plt.title("G gain map")
    plt.subplot(1,3,3)
    plt.imshow(gb, cmap='Blues')
    plt.colorbar()
    plt.title("B gain map")
    plt.show()

def debug_normal_gain_maps(gr, gg, gb):
    plt.figure(figsize=(12,4))
    plt.subplot(1,3,1)
    plt.imshow(gr, cmap='Reds')
    plt.colorbar()
    plt.title("Normal R gain map")
    plt.subplot(1,3,2)
    plt.imshow(gg, cmap='Greens')
    plt.colorbar()
    plt.title("Normal G gain map")
    plt.subplot(1,3,3)
    plt.imshow(gb, cmap='Blues')
    plt.colorbar()
    plt.title("Normal B gain map")
    plt.show()

def debug_linear_to_srgb(img_lin):
    plt.figure(figsize=(6,6))
    plt.imshow(img_lin)
    plt.title("Linear Gain Application Result")
    plt.axis('off')
    plt.show()