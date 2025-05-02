import akshare as ak
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

def get_stock_data():
    """获取股票数据"""
    # 股票代码列表
    stocks = {
        '贵州茅台': '600519',
        '五粮液': '000858',
        '洋河股份': '002304',
        '泸州老窖': '000568',
        '山西汾酒': '600809'
    }
    
    # 存储所有股票数据的列表
    all_data = []
    
    # 获取每只股票的数据
    for name, code in stocks.items():
        try:
            # 获取前复权数据
            df = ak.stock_zh_a_hist(symbol=code, period="daily", 
                                  start_date="20210101", 
                                  end_date=datetime.now().strftime("%Y%m%d"),
                                  adjust="qfq")
            
            # 重命名列并选择需要的列
            df = df[['日期', '收盘']]
            df.columns = ['date', name]
            df['date'] = pd.to_datetime(df['date'])
            df.set_index('date', inplace=True)
            
            all_data.append(df)
        except Exception as e:
            print(f"获取{name}({code})数据时出错: {e}")
    
    # 合并所有股票数据
    if all_data:
        merged_df = pd.concat(all_data, axis=1)
        return merged_df
    else:
        return None

def calculate_returns(df):
    """计算每日收益率"""
    returns = df.pct_change()
    return returns

def calculate_correlation_matrix(returns):
    """计算相关性矩阵"""
    return returns.corr()

def calculate_covariance_matrix(returns):
    """手动计算协方差矩阵"""
    # 移除包含NaN的行
    returns_clean = returns.dropna()
    
    # 计算每只股票的平均收益率
    mean_returns = returns_clean.mean()
    
    # 计算协方差矩阵
    n = len(returns_clean)
    cov_matrix = np.zeros((len(returns_clean.columns), len(returns_clean.columns)))
    
    for i in range(len(returns_clean.columns)):
        for j in range(len(returns_clean.columns)):
            # 计算协方差
            cov = np.sum((returns_clean.iloc[:, i] - mean_returns[i]) * 
                        (returns_clean.iloc[:, j] - mean_returns[j])) / (n - 1)
            cov_matrix[i, j] = cov
    
    # 转换为DataFrame
    cov_df = pd.DataFrame(cov_matrix, 
                         index=returns_clean.columns, 
                         columns=returns_clean.columns)
    return cov_df

def plot_correlation_heatmap(corr_matrix):
    """绘制相关性热力图"""
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0)
    plt.title('白酒板块股票收益率相关性热力图')
    plt.tight_layout()
    plt.savefig('correlation_heatmap.png')
    plt.close()

def main():
    # 获取股票数据
    print("正在获取股票数据...")
    stock_data = get_stock_data()
    
    if stock_data is not None:
        # 保存收盘价数据
        stock_data.to_csv('stock_prices.csv')
        print("已保存收盘价数据到 stock_prices.csv")
        
        # 计算收益率
        returns = calculate_returns(stock_data)
        returns.to_csv('daily_returns.csv')
        print("已保存收益率数据到 daily_returns.csv")
        
        # 计算并保存相关性矩阵
        corr_matrix = calculate_correlation_matrix(returns)
        print("相关性矩阵：")
        print(corr_matrix)
        
        # 绘制并保存热力图
        plot_correlation_heatmap(corr_matrix)
        print("已保存相关性热力图到 correlation_heatmap.png")
        
        # 计算并保存协方差矩阵
        cov_matrix = calculate_covariance_matrix(returns)
        cov_matrix.to_csv('covariance_matrix.csv')
        print("已保存协方差矩阵到 covariance_matrix.csv")
    else:
        print("获取股票数据失败")

if __name__ == "__main__":
    main() 