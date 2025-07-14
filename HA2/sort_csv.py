import pandas as pd

# 读取 CSV 文件
df = pd.read_csv("tuner_results.csv")

# 按 val_acc 降序排序
df_sorted = df.sort_values(by="val_acc", ascending=False)

# 显示前几行（或保存到新文件）
print(df_sorted.head(10))

# 保存排序后的结果
df_sorted.to_csv("tuner_results_sorted.csv", index=False)
