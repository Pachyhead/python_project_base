from dataclasses import dataclass

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

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


def plot_to_array(plot_func, *args, **kwargs):
    """
    Convert a matplotlib figure to a numpy array without PIL.
    """
    fig, ax = plt.subplots()
    plot_func(ax, *args, **kwargs)

    fig.canvas.draw()

    img = np.array(fig.canvas.buffer_rgba()) # type: ignore

    plt.close(fig)
    
    return img

def draw_hist(ax, df: pd.DataFrame, title: str = "Histogram", color: str="skyblue"):
    """
    Draw a histogram using a DataFrame.
    Columns must be: 'Bin' (구간) and 'Frequency' (빈도).
    """
    required_cols = ['Bin', 'Frequency']
    if not all(col in df.columns for col in required_cols):
        raise ValueError(f"DataFrame must have columns: {required_cols}")
    
    sorted_df = df.sort_values(by='Bin', ascending=True)
    n_bins = len(sorted_df)

    indices = np.arange(n_bins)

    step = max(1, n_bins // 10)
    x = [str(val) if i % step == 0 else "" for i, val in enumerate(sorted_df['Bin'])]
    y = sorted_df['Frequency']

    width = 0.8 / (1 + 0.1 * (n_bins - 1))
    ax.bar(indices, y, width=width, color=color, edgecolor='black', alpha=0.8)
    
    ax.set_xticks(indices)
    ax.set_xticklabels(x)
    
    ax.set_title(title)
    ax.set_xlabel("Bin")
    ax.set_ylabel("Frequency")