import numpy as np  # 导入NumPy用于数值计算
import matplotlib  # 导入matplotlib用于绘图

matplotlib.use('Agg')  # 设置matplotlib后端为'Agg'，适合无GUI环境下保存图片
import matplotlib.pyplot as plt  # 导入pyplot用于绘图
from matplotlib.dates import DateFormatter  # 导入日期格式化工具
import matplotlib.dates as mdates  # 导入日期定位器
from datetime import datetime, timedelta  # 导入日期时间相关模块

def generate_simulated_data(num_days):
    """生成模拟的道琼斯指数数据（含趋势和不同频率成分）"""
    np.random.seed(42)  # 固定随机种子，保证实验可复现
    days = np.arange(num_days)  # 生成天数序列
    low_freq = 10000 + 200 * np.sin(days * 2 * np.pi / 1000)  # 低频趋势（周期约1000天）
    mid_freq = 100 * np.sin(days * 2 * np.pi / 100)  # 中频波动（周期约100天）
    high_freq = 50 * np.sin(days * 2 * np.pi / 10) + np.random.normal(0, 20, num_days)  # 高频噪声（周期约10天）+正态噪声
    data = low_freq + mid_freq + high_freq  # 合成最终模拟数据
    return data  # 返回模拟数据

def perform_fourier_filtering(data, retention_ratio):
    """执行傅立叶滤波，保留指定比例的低频系数"""
    coeff = np.fft.rfft(data)  # 对数据做快速傅立叶变换，得到实数部分频域系数
    cutoff = int(len(coeff) * retention_ratio)  # 计算需要保留的低频系数数量
    coeff[cutoff:] = 0  # 将高于截止点的高频系数全部置零
    filtered_data = np.fft.irfft(coeff)  # 逆变换回时域，得到滤波后的数据
    return filtered_data, retention_ratio  # 返回滤波后的数据和保留比例

def generate_dates(num_days):
    """生成从2006年7月1日开始的日期序列"""
    start_date = datetime(2006, 7, 1)  # 设置起始日期
    return [start_date + timedelta(days=i) for i in range(num_days)]  # 生成日期列表

def load_data(filepath):
    """从文本文件加载一维数据，每行一个数"""
    with open(filepath, 'r') as f:  # 打开文件
        data = [float(line.strip()) for line in f if line.strip()]  # 读取每行并转为float
    return np.array(data)  # 返回NumPy数组

def fourier_filter(data, retention_ratio):
    """返回滤波后数据和保留的系数（用于测试）"""
    coeff = np.fft.rfft(data)  # 对数据做快速傅立叶变换
    cutoff = int(len(coeff) * retention_ratio)  # 计算保留的低频系数数量
    coeff_filtered = coeff.copy()  # 复制一份系数
    coeff_filtered[cutoff:] = 0  # 高频部分置零
    filtered_data = np.fft.irfft(coeff_filtered, n=len(data))  # 逆变换回时域
    return filtered_data, coeff_filtered  # 返回滤波后数据和滤波系数

def plot_data(data, filtered_data=None, retention_ratio=None, save_path=None):
    """支持只传原始数据，返回Figure对象；如有参数则保存图片"""
    fig, ax = plt.subplots(figsize=(12, 6))  # 创建画布和坐标轴
    dates = generate_dates(len(data))  # 生成日期序列
    ax.plot(dates, data, 'b-', alpha=0.7, label='Original Data')  # 绘制原始数据曲线
    if filtered_data is not None and retention_ratio is not None:  # 如果有滤波数据
        ax.plot(dates, filtered_data, 'r-', label=f'Filtered (Retain {retention_ratio * 100:.0f}% Low Frequency)')  # 绘制滤波曲线
    ax.set_title('Dow Jones Index Fourier Filtering Simulation', fontsize=14)  # 设置标题
    ax.set_xlabel('Date', fontsize=12)  # 设置x轴标签
    ax.set_ylabel('Index Value', fontsize=12)  # 设置y轴标签
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m'))  # 设置x轴日期格式
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=6))  # 每6个月一个主刻度
    ax.grid(True, linestyle='--', alpha=0.6)  # 添加网格线
    ax.legend(loc='upper right')  # 添加图例
    if save_path is not None and filtered_data is not None and retention_ratio is not None:
        # 如果指定保存路径且有滤波数据，则保存图片
        filename = f'filter_{int(retention_ratio * 100)}_simulated.png'
        full_path = f'{save_path}/{filename}'
        plt.savefig(full_path, dpi=300, bbox_inches='tight')  # 保存图片
        print(f"Image saved: {full_path}")  # 打印保存路径
        plt.close(fig)  # 关闭画布释放内存
        return None  # 不返回Figure对象
    return fig  # 返回Figure对象

def plot_comparison(original, filtered, dates=None, title=None):
    """返回Figure对象，绘制原始与滤波数据对比"""
    if dates is None:
        dates = np.arange(len(original))  # 默认x轴为序号
    fig, ax = plt.subplots(figsize=(10, 5))  # 创建画布
    ax.plot(dates, original, label='Original')  # 绘制原始数据
    ax.plot(dates, filtered, label='Filtered')  # 绘制滤波数据
    if title:
        ax.set_title(title)  # 设置标题
    ax.legend()  # 添加图例
    return fig  # 返回Figure对象

def main():
    save_path = r'C:\Users\31025\OneDrive\桌面\t'  # 目标保存路径
    import os  # 导入os模块
    os.makedirs(save_path, exist_ok=True)  # 确保保存目录存在
    num_days = 1000  # 模拟数据天数
    data = generate_simulated_data(num_days)  # 生成模拟数据
    # 保存原始数据图
    fig = plot_data(data)  # 只绘制原始数据
    fig.savefig(f"{save_path}/original_dow_simulated.png", dpi=300, bbox_inches='tight')  # 保存原始数据图
    plt.close(fig)  # 关闭画布
    # 执行滤波任务
    for ratio in [0.1, 0.02]:  # 分别保留10%和2%低频系数
        filtered_data, retention_ratio = perform_fourier_filtering(data, ratio)  # 滤波
        plot_data(data, filtered_data, retention_ratio, save_path)  # 绘制并保存滤波结果

if __name__ == "__main__":
    main()  # 作为主程序运行
