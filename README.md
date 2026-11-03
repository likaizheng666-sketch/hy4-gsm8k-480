# HY4 GSM8K 480

用于 HY4 原始 Top32 模型 RL 实验的 GSM8K 训练子集：**480 道题，2-shot prompt**。

## 下载与使用

- [train.parquet](data-2shot/train.parquet)：训练输入，包含 2-shot prompt 和标准答案。
- [questions.jsonl](data-2shot/questions.jsonl)：题目、标准答案、参考解答及筛选依据，便于人工检查。
- [ids.jsonl](data-2shot/ids.jsonl)：样本 ID、来源和匹配信息。
- [完整 ZIP](gsm8k-easier480-2shot-local-20261103.zip)：原始数据文件及筛选清单的本地备份包。

将下载后的 `data-2shot/train.parquet` 路径传给训练配置的 `data.train_files`。


## 来源与许可

原始数据来源：[OpenAI GSM8K](https://github.com/openai/grade-school-math)。原始项目的许可与版权声明保存在 [LICENSE-GSM8K.txt](LICENSE-GSM8K.txt)。
