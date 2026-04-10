from dataclasses import dataclass
from typing import Callable

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


def plot_to_array(plot_func, *args, subplot_kw=None, **kwargs):
    """
    Matplotlib으로 그린 그래프를 NumPy 배열(RGBA)로 변환합니다.

    Args:
        plot_func (Callable): 그래프를 그리는 로직이 담긴 함수. 
            첫 번째 인자로 `matplotlib.axes.Axes` 객체를 받아야 함.
        *args: `plot_func`에 전달할 가변 위치 인자.
        subplot_kw (dict, optional): `plt.subplots()` 호출 시 전달할 설정값.
            예: 방사형 그래프의 경우 `{'projection': 'polar'}`를 전달.
        **kwargs: `plot_func`에 전달할 가변 키워드 인자.

    Returns:
        np.ndarray: 그래프 이미지가 담긴 NumPy 배열 (형태: [Height, Width, 4], RGBA 포맷).
    """
    fig, ax = plt.subplots(subplot_kw=subplot_kw)
    plot_func(ax, *args, **kwargs)

    fig.canvas.draw()

    img = np.array(fig.canvas.buffer_rgba()) # type: ignore

    plt.close(fig)
    
    return img

def draw_hist(ax, hist_data: pd.Series, title: str = "Histogram", color: str="skyblue"):
    """
    Draw a histogram using a DataFrame.
    hist_data = pd.Series(frequency, index=bins)
    """
    hist_data.sort_index()
    n_bins = len(hist_data)
    indices = np.arange(n_bins)

    width = 0.8 / (1 + 0.1 * (n_bins - 1))

    step = max(1, n_bins // 10)
    labels = [str(label) if i % step == 0 else "" for i, label in enumerate(hist_data.index)]

    ax.bar(indices, hist_data.values, width=width, color=color, edgecolor='black', alpha=0.8)
    
    ax.set_xticks(indices)
    ax.set_xticklabels(labels)
    
    ax.set_title(title)
    ax.set_xlabel("Bin")
    ax.set_ylabel("Frequency")

def draw_2d_functions(
    ax, 
    funcs: list[Callable[[np.ndarray], np.ndarray]],
    x_range: tuple[float, float], 
    n_points: int = 100, 
    title: str = "Multi-Function Plot", 
    colors: list[str] | None = None
):
    """
    하나의 좌표계에 여러 개의 수학 함수 $y = f(x)$를 겹쳐서 그립니다.

    Args:
        ax (matplotlib.axes.Axes): 그래프가 그려질 축 객체.
        funcs (list[Callable]): 시각화할 함수들의 리스트. 
            각 함수는 `np.ndarray`를 입력받아 동일한 크기의 `np.ndarray`를 반환해야 함.
        x_range (tuple[float, float]): $x$축의 시작점과 끝점 ($x_{start}, x_{end}$).
        n_points (int, optional): 그래프를 구성할 점의 개수. 값이 클수록 곡선이 매끄러움. 기본값은 100.
        title (str, optional): 그래프의 제목. 기본값은 "Multi-Function Plot".
        colors (list[str], optional): 각 함수에 순차적으로 적용할 색상 리스트. 
            제공되지 않을 경우 기본 색상 5종을 순환하며 사용함.
    """
    if colors is None:
        colors = ['red', 'blue', 'green', 'orange', 'purple']

    x = np.linspace(x_range[0], x_range[1], n_points)
    
    for i, func in enumerate(funcs):
        try:
            y = func(x)
            current_color = colors[i % len(colors)]
            
            # 함수 이름 추출 (람다식일 경우 f1, f2...로 표시)
            func_name = getattr(func, '__name__', f"f{i+1}")
            if func_name == "<lambda>":
                func_name = f"f{i+1}(x)"

            ax.plot(x, y, color=current_color, linewidth=2, label=func_name)
            
        except Exception as e:
            print(f"Error drawing function at index {i}: {e}")
    
    ax.set_title(title)
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.axhline(0, color='black', linewidth=0.5)
    ax.axvline(0, color='black', linewidth=0.5)
    ax.legend()

def draw_radar_chart(ax, radar_data: pd.DataFrame, title="Radar Chart", y_range=(0, 100), colors=None):
    """
    데이터프레임의 각 행(Row)을 개별 레이어로 하는 방사형 그래프(Radar Chart)를 그립니다.

    Args:
        ax (matplotlib.axes.Axes): 그래프가 그려질 Polar Projection 축 객체.
        radar_data (pd.DataFrame): 시각화할 데이터. 
            - 컬럼(Columns): 방사형 그래프의 각 꼭짓점(카테고리) 이름.
            - 인덱스(Index): 각 데이터 레이어의 이름 (범례에 표시됨).
        title (str, optional): 그래프 상단에 표시될 제목. 기본값은 "Radar Chart".
        y_range (tuple, optional): 반지름 축(Radial Axis)의 범위 (min, max). 기본값은 (0, 100).
        colors (list, optional): 각 레이어에 순차적으로 적용할 색상 리스트. 
            제공되지 않을 경우 기본 색상 5종을 순환하며 사용함.
    """
    if colors is None:
        colors = ['red', 'blue', 'green', 'orange', 'purple']
    radar_data = radar_data.sort_index(axis=1)

    categories = radar_data.columns.tolist()
    n_attributes = len(categories)

    angles = np.linspace(0, 2 * np.pi, n_attributes, endpoint=False).tolist()
    angles += angles[:1] # 루프 닫기

    for i, (idx, row) in enumerate(radar_data.iterrows()):
        values = row.values.tolist()
        values += values[:1] # 데이터 루프 닫기

        # 리스트 범위를 벗어나지 않도록 나머지 연산 사용 (Cycling colors)
        current_color = colors[i % len(colors)]

        # 선 그리기 및 영역 채우기 (Plotting and filling)
        ax.plot(angles, values, color=current_color, linewidth=2, label=str(idx))
        ax.fill(angles, values, color=current_color, alpha=0.15)
    
    ax.set_ylim(y_range[0], y_range[1])
    
    ax.set_theta_offset(np.pi / 2) # 12시 방향 시작 (Start at 12 o'clock)
    ax.set_theta_direction(-1)     # 시계 방향 (Clockwise)
    ax.set_thetagrids(np.degrees(angles[:-1]), categories)
    ax.set_title(title, y=1.1)
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1)) # 범례 추가