# HY4 GSM8K 480

用于 HY4 原始 Top32 模型 RL 实验的 GSM8K 训练子集：**480 道题，2-shot prompt**。

## 下载与使用

- [train.parquet](data-2shot/train.parquet)：训练输入，包含 2-shot prompt 和标准答案。
- [questions.jsonl](data-2shot/questions.jsonl)：题目、标准答案、参考解答及筛选依据，便于人工检查。
- [ids.jsonl](data-2shot/ids.jsonl)：样本 ID、来源和匹配信息。
- [完整 ZIP](gsm8k-easier480-2shot-local-20261103.zip)：原始数据文件及筛选清单的本地备份包。

将下载后的 `data-2shot/train.parquet` 路径传给训练配置的 `data.train_files`。

## 筛选记录

这 480 题包含旧 320 题集合中的 132 题，以及新加入的 348 题。筛选结合历史答题结果与参考解答的算术、长度和步骤检查；不是全部经过原始 Top32 模型逐题校准的“必定能答对”题目。

[dataset-manifest.json](dataset-manifest.json) 保存筛选类别、来源和三个数据文件的 SHA256；[preparation-checks.json](preparation-checks.json) 保存当时的检查结果。两份文件保留生成时的状态与参数，后续训练的 batch size、采样次数、温度和步数由运行配置决定。

这是训练子集，不作为独立测试集使用。参考解答和历史答题信息用于审计；RL 输入不应包含当前题目的参考答案。

## 来源与许可

原始数据来源：[OpenAI GSM8K](https://github.com/openai/grade-school-math)。原始项目的许可与版权声明保存在 [LICENSE-GSM8K.txt](LICENSE-GSM8K.txt)。
