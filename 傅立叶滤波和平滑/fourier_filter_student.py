import numpy as np
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates
from datetime import datetime, timedelta

def generate_simulated_data(num_days):
    """生成模拟的道琼斯指数数据（含趋势和不同频率成分）"""
    np.random.seed(42)
    days = np.arange(num_days)
    low_freq = 10000 + 200 * np.sin(days * 2 * np.pi / 1000)
    mid_freq = 100 * np.sin(days * 2 * np.pi / 100)
    high_freq = 50 * np.sin(days * 2 * np.pi / 10) + np.random.normal(0, 20, num_days)
    data = low_freq + mid_freq + high_freq
    return data

def perform_fourier_filtering(data, retention_ratio):
    coeff = np.fft.rfft(data)
    cutoff = int(len(coeff) * retention_ratio)
    coeff[cutoff:] = 0
    filtered_data = np.fft.irfft(coeff)
    return filtered_data, retention_ratio

def generate_dates(num_days):
    start_date = datetime(2006, 7, 1)
    return [start_date + timedelta(days=i) for i in range(num_days)]

# 测试用接口函数
def load_data(filepath):
    """从文本文件加载一维数据，每行一个数"""
    with open(filepath, 'r') as f:
        data = [float(line.strip()) for line in f if line.strip()]
    return np.array(data)

def fourier_filter(data, retention_ratio):
    """返回滤波后数据和保留的系数（用于测试）"""
    coeff = np.fft.rfft(data)
    cutoff = int(len(coeff) * retention_ratio)
    coeff_filtered = coeff.copy()
    coeff_filtered[cutoff:] = 0
    filtered_data = np.fft.irfft(coeff_filtered, n=len(data))
    return filtered_data, coeff_filtered

def plot_data(data, filtered_data=None, retention_ratio=None, save_path=None):
    """支持只传原始数据，返回Figure对象"""
    fig, ax = plt.subplots(figsize=(12, 6))
    dates = generate_dates(len(data))
    ax.plot(dates, data, 'b-', alpha=0.7, label='Original Data')
    if filtered_data is not None and retention_ratio is not None:
        ax.plot(dates, filtered_data, 'r-', label=f'Filtered (Retain {retention_ratio * 100:.0f}% Low Frequency)')
    ax.set_title('Dow Jones Index Fourier Filtering Simulation', fontsize=14)
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Index Value', fontsize=12)
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m'))
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend(loc='upper right')
    if save_path is not None and filtered_data is not None and retention_ratio is not None:
        filename = f'filter_{int(retention_ratio * 100)}_simulated.png'
        full_path = f'{save_path}/{filename}'
        plt.savefig(full_path, dpi=300, bbox_inches='tight')
        print(f"Image saved: {full_path}")
        plt.close(fig)
        return None
    return fig

def plot_comparison(original, filtered, dates=None, title=None):
    """返回Figure对象"""
    if dates is None:
        dates = np.arange(len(original))
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(dates, original, label='Original')
    ax.plot(dates, filtered, label='Filtered')
    if title:
        ax.set_title(title)
    ax.legend()
    return fig

def main():
    save_path = r'C:\Users\31025\OneDrive\桌面\t'
    import os
    os.makedirs(save_path, exist_ok=True)
    num_days = 1000
    data = generate_simulated_data(num_days)
    # 保存原始数据图
    fig = plot_data(data)
    fig.savefig(f"{save_path}/original_dow_simulated.png", dpi=300, bbox_inches='tight')
    plt.close(fig)
    # 执行滤波任务
    for ratio in [0.1, 0.02]:
        filtered_data, retention_ratio = perform_fourier_filtering(data, ratio)
        plot_data(data, filtered_data, retention_ratio, save_path)

if __name__ == "__main__":
    main()
