"""Build verl input from the selected questions and an independent prompt template."""

import argparse
import json
from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq


ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--questions", type=Path, default=ROOT / "data/questions.jsonl")
    parser.add_argument("--template", type=Path, default=ROOT / "prompts/2shot.json")
    parser.add_argument("--num-shots", type=int, default=None)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    questions = [json.loads(line) for line in args.questions.read_text(encoding="utf-8").splitlines() if line.strip()]
    template = json.loads(args.template.read_text(encoding="utf-8"))
    shots = template["shots"]
    num_shots = len(shots) if args.num_shots is None else args.num_shots
    if not 0 <= num_shots <= len(shots):
        parser.error("--num-shots must be between zero and the number of examples in the template")
    if not questions or len({row["sample_id"] for row in questions}) != len(questions):
        parser.error("The question file must contain nonempty, unique sample IDs")
    if len({row["question"].strip() for row in questions}) != len(questions):
        parser.error("The question file contains duplicate questions")
    example_questions = {shot["question"].strip() for shot in shots[:num_shots]}
    if example_questions & {row["question"].strip() for row in questions}:
        parser.error("Prompt examples must not repeat a target question")

    prefix = []
    for shot in shots[:num_shots]:
        prefix.extend([
            {"role": "user", "content": shot["question"]},
            {"role": "assistant", "content": shot["answer"]},
        ])
    rows = []
    for question in questions:
        if not question["question"].strip() or not str(question["ground_truth"]).strip():
            parser.error("Each question must have a nonempty question and ground truth")
        # The target answer/reference solution never enters its prompt.
        prompt = [dict(message) for message in prefix]
        prompt.append({"role": "user", "content": question["question"] + template["user_suffix"]})
        rows.append({
            "prompt": prompt,
            "data_source": "gsm8k",
            "reward_model": {"style": "rule", "ground_truth": str(question["ground_truth"])},
            "extra_info": {"index": int(question["source_index"])},
        })

    schema = pa.schema([
        pa.field("prompt", pa.list_(pa.struct([pa.field("role", pa.string()), pa.field("content", pa.string())]))),
        pa.field("data_source", pa.string()),
        pa.field("reward_model", pa.struct([pa.field("style", pa.string()), pa.field("ground_truth", pa.string())])),
        pa.field("extra_info", pa.struct([pa.field("index", pa.int64())])),
    ])
    args.output.parent.mkdir(parents=True, exist_ok=True)
    pq.write_table(pa.Table.from_pylist(rows, schema=schema), args.output)
    print(json.dumps({"rows": len(rows), "shots": num_shots, "output": str(args.output)}, ensure_ascii=True))


if __name__ == "__main__":
    main()
