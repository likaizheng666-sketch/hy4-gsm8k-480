# HY4 GSM8K 480

用于 HY4 原始 Top32 模型 RL 实验的 **480 道 GSM8K 训练题**。基础题库与 few-shot 模板分别保存；仓库也提供可直接训练的 2-shot Parquet。

## 文件用途

| 文件 | 用途 |
|---|---|
| [data/questions.jsonl](data/questions.jsonl) | 基础题库：样本 ID、题目、标准答案、参考解答和原始索引；不含 few-shot 示例 |
| [prompts/2shot.json](prompts/2shot.json) | 两条独立示例及目标题的作答格式要求 |
| [data-2shot/train.parquet](data-2shot/train.parquet) | 已拼好 2-shot 的 verl 训练输入；与原实验文件逐字节一致 |
| [scripts/build_parquet.py](scripts/build_parquet.py) | 从题库与模板生成训练文件，也支持 0-shot |
| [metadata/selection.jsonl](metadata/selection.jsonl) | 每题的筛选依据及历史答题提示，通过 `sample_id` 与题库关联 |
| [dataset-manifest.json](dataset-manifest.json) | 数据数量、筛选分布、来源和文件 SHA256 |

直接训练时，将 `data-2shot/train.parquet` 的本机绝对路径传给 `data.train_files`。获取全部文件可使用 GitHub 的 **Code → Download ZIP**，或克隆仓库：

```bash
git clone https://github.com/likaizheng666-sketch/hy4-gsm8k-480.git
cd hy4-gsm8k-480
```

## 重新生成 prompt

构建脚本只依赖 PyArrow。在独立 Python 环境中安装后，运行：

```bash
python -m pip install pyarrow
python scripts/build_parquet.py --output build/train-2shot.parquet
python scripts/build_parquet.py --num-shots 0 --output build/train-0shot.parquet
```

默认读取 `data/questions.jsonl` 和 `prompts/2shot.json`，结果保持原题目顺序。0-shot 只移除示例，保留目标题的作答格式要求。替换示例时修改模板，或通过 `--template` 指定另一份同结构的 JSON；无需改动基础题库。模型的 chat template 仍由训练框架和 tokenizer 应用。

只有示例的答案会进入 prompt。当前题目的 `ground_truth` 用于奖励，`reference_solution` 用于审阅；构建脚本不会把它们拼进当前题目的输入。

## 来源与许可

原始数据来源：[OpenAI GSM8K](https://github.com/openai/grade-school-math)。原始项目的许可与版权声明保存在 [LICENSE-GSM8K.txt](LICENSE-GSM8K.txt)。
