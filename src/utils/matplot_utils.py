from dataclasses import dataclass

import matplotlib.pyplot as plt
import numpy as np

@dataclass
class ImageResult:
    image: np.ndarray
    description: str

def show_images(results: list[ImageResult], grid: tuple[int, int], fig_size: int=5):
    rows, cols = grid
    fig, axes = plt.subplots(rows, cols, figsize=(cols * fig_size, rows * fig_size))

    if rows * cols > 1:
        axes_flat = axes.flatten()
    else:
        axes_flat = [axes]

    for i in range(rows * cols):
        ax = axes_flat[i]

        if i < len(results):
            res = results[i]
            
            if len(res.image.shape) == 2:
                img_display = res.image
                cmap = 'gray'
            else:
                img_display = res.image
                cmap = None
            
            ax.imshow(img_display, cmap=cmap)
            ax.set_title(res.description, y=-0.15)
        
        ax.axis('off')

    plt.tight_layout()
    plt.show()
