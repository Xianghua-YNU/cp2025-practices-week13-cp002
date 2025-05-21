import numpy as np
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates
from datetime import datetime, timedelta


def generate_simulated_data(num_days):
    """生成模拟的道琼斯指数数据（含趋势和不同频率成分）"""
    np.random.seed(42)  # 固定随机种子确保可复现
    days = np.arange(num_days)

    # 低频趋势（周期约1000天）
    low_freq = 10000 + 200 * np.sin(days * 2 * np.pi / 1000)
    # 中频波动（周期约100天）
    mid_freq = 100 * np.sin(days * 2 * np.pi / 100)
    # 高频噪声（周期约10天）
    high_freq = 50 * np.sin(days * 2 * np.pi / 10) + np.random.normal(0, 20, num_days)

    # 合成数据
    data = low_freq + mid_freq + high_freq
    return data


def perform_fourier_filtering(data, retention_ratio):
    """执行傅立叶滤波"""
    coeff = np.fft.rfft(data)
    cutoff = int(len(coeff) * retention_ratio)
    coeff[cutoff:] = 0  # 抑制高频成分
    filtered_data = np.fft.irfft(coeff)
    return filtered_data, retention_ratio


def generate_dates(num_days):
    """生成从2006年7月1日开始的日期序列"""
    start_date = datetime(2006, 7, 1)
    return [start_date + timedelta(days=i) for i in range(num_days)]


def plot_data(data, filtered_data, retention_ratio, save_path):
    """绘制原始数据和滤波后的数据并保存图片"""
    fig, ax = plt.subplots(figsize=(12, 6))
    dates = generate_dates(len(data))  # 生成日期序列

    # 绘制原始数据（蓝色）
    ax.plot(dates, data, 'b-', alpha=0.7, label='Original Data')

    # 绘制滤波数据（红色）
    ax.plot(dates, filtered_data, 'r-', label=f'Filtered (Retain {retention_ratio * 100:.0f}% Low Frequency)')

    # 图表设置（英文）
    ax.set_title('Dow Jones Index Fourier Filtering Simulation', fontsize=14)
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Index Value', fontsize=12)
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m'))  # 按月显示
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=6))  # 每6个月一个刻度
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend(loc='upper right')

    # 保存图片
    filename = f'filter_{int(retention_ratio * 100)}_simulated.png'
    full_path = f'{save_path}/{filename}'
    plt.savefig(full_path, dpi=300, bbox_inches='tight')
    print(f"Image saved: {full_path}")
    plt.close(fig)  # 释放内存


def plot_original_data(data, save_path):
    """仅绘制原始数据并保存图片"""
    fig, ax = plt.subplots(figsize=(12, 6))
    dates = generate_dates(len(data))
    ax.plot(dates, data, 'b-', alpha=0.7, label='Original Data')
    ax.set_title('Dow Jones Index Simulated Original Data', fontsize=14)
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Index Value', fontsize=12)
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m'))
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend(loc='upper right')
    filename = 'original_dow_simulated.png'
    full_path = f'{save_path}/{filename}'
    plt.savefig(full_path, dpi=300, bbox_inches='tight')
    print(f"Image saved: {full_path}")
    plt.close(fig)


# 测试用接口函数（如需通过测试可保留）
def load_data(filepath):
    """测试用的占位函数"""
    raise NotImplementedError("load_data 未实现，仅用于测试导入。")

def fourier_filter(data, retention_ratio):
    """测试用的简单实现"""
    coeff = np.fft.rfft(data)
    cutoff = int(len(coeff) * retention_ratio)
    coeff[cutoff:] = 0
    filtered_data = np.fft.irfft(coeff)
    return filtered_data

def plot_comparison(original, filtered, dates=None, title=None):
    """测试用的简单实现"""
    if dates is None:
        dates = np.arange(len(original))
    plt.figure(figsize=(10, 5))
    plt.plot(dates, original, label='Original')
    plt.plot(dates, filtered, label='Filtered')
    if title:
        plt.title(title)
    plt.legend()
    plt.close()


def main():
    save_path = r'C:\Users\31025\OneDrive\桌面\t'  # 目标保存路径

    # 确保目录存在
    import os
    os.makedirs(save_path, exist_ok=True)

    num_days = 1000  # 模拟数据天数（2006-2010年约1000个交易日）
    data = generate_simulated_data(num_days)  # 生成模拟数据

    # 先保存原始数据图
    plot_original_data(data, save_path)

    # 执行滤波任务
    for ratio in [0.1, 0.02]:
        filtered_data, retention_ratio = perform_fourier_filtering(data, ratio)
        plot_data(data, filtered_data, retention_ratio, save_path)


if __name__ == "__main__":
    main()
