"""CAED 统计脚本 —— 合并样本、统计 ASR、输出基准报告数据。

用法:
    python scripts/stats.py              # 统计 data/ 下所有样本
    python scripts/stats.py --out report.md   # 输出 markdown 报告
"""
import argparse
import glob
import json
import os
from collections import Counter, defaultdict


def load_samples(data_dir: str = "data") -> list:
    """合并 data 目录下所有 JSONL，按 id 去重。"""
    seen = set()
    samples = []
    for f in sorted(glob.glob(os.path.join(data_dir, "**", "*.jsonl"), recursive=True)):
        for line in open(f, encoding="utf-8"):
            if line.strip():
                s = json.loads(line)
                if s.get("id") not in seen:
                    seen.add(s["id"])
                    samples.append(s)
    return samples


def stats_by_category(samples):
    """按类别统计 ASR。"""
    total = Counter(s["attack_category"] for s in samples)
    succ = Counter(s["attack_category"] for s in samples if s["judge_label"] == "attack_success")
    rows = []
    for cat in sorted(total):
        t, s = total[cat], succ.get(cat, 0)
        rows.append((cat, t, s, s / t if t else 0))
    return rows


def stats_by_technique(samples):
    """按技术统计 ASR。"""
    total = Counter(s["attack_technique"] for s in samples)
    succ = Counter(s["attack_technique"] for s in samples if s["judge_label"] == "attack_success")
    rows = []
    for tech, t in total.most_common():
        s = succ.get(tech, 0)
        rows.append((tech, t, s, s / t if t else 0))
    return rows


def main():
    parser = argparse.ArgumentParser(description="CAED 统计")
    parser.add_argument("--data", default="data")
    parser.add_argument("--out", default=None, help="输出 markdown 报告路径")
    args = parser.parse_args()

    samples = load_samples(args.data)
    if not samples:
        print("无样本")
        return

    total_succ = sum(1 for s in samples if s["judge_label"] == "attack_success")
    asr = total_succ / len(samples)

    print(f"总样本: {len(samples)}，整体 ASR = {total_succ}/{len(samples)} = {asr:.1%}\n")

    print("=== 按类别 ASR ===")
    for cat, t, s, r in stats_by_category(samples):
        print(f"  {cat}: {s}/{t} = {r:.0%}")

    print("\n=== 按技术 ASR（有效技术优先）===")
    for tech, t, s, r in stats_by_technique(samples):
        mark = "✅" if s > 0 else "  "
        print(f"  {mark} {tech}: {s}/{t} = {r:.0%}")

    if args.out:
        os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(f"# CAED 统计报告\n\n总样本 {len(samples)}，整体 ASR {asr:.1%}\n\n")
            f.write("## 按类别\n\n| 类别 | 成功/总数 | ASR |\n|------|----------|-----|\n")
            for cat, t, s, r in stats_by_category(samples):
                f.write(f"| {cat} | {s}/{t} | {r:.0%} |\n")
            f.write("\n## 按技术\n\n| 技术 | 成功/总数 | ASR |\n|------|----------|-----|\n")
            for tech, t, s, r in stats_by_technique(samples):
                f.write(f"| {tech} | {s}/{t} | {r:.0%} |\n")
        print(f"\n报告已输出: {args.out}")


if __name__ == "__main__":
    main()
