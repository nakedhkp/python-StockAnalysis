# 多股票相关性分析项目

本项目旨在使用 Python 工具对同一行业内的多只股票进行相关性分析，探索它们在每日收益率上的联动效应。数据来源于 [AKShare](https://github.com/akfamily/akshare)，并通过 Pandas、Seaborn、Numpy 进行数据处理与可视化。

## 项目目标

- 获取3~5只同一行业的A股（如白酒板块：贵州茅台、五粮液、洋河股份、泸州老窖、山西汾酒）收盘价
- 计算它们的每日收益率并求出相关性矩阵
- 绘制热力图展示股票间的相关性
- 手动实现收益率协方差矩阵的计算（使用 Numpy）

## 环境要求

- Python 3.8+
- 安装依赖：
  ```bash
  pip install akshare pandas matplotlib seaborn numpy
