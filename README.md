# CAED —— 中文大模型安全强度基准

**Chinese Adversarial Evaluation Dataset** —— 用"对抗式 AI 协作"生成的中文大模型安全评测基准。

> **核心发现（v0.1）**：中文大模型（DeepSeek）的安全防御显著强于英文模型。英文社区常用的攻击技术（DAN/角色扮演/隐喻包装）在中文环境几乎全部失效，整体 ASR 仅 3.9%（5/129），其中 16/19 种技术被完全免疫。

## 为什么做这个

英文世界的对抗评测（HarmBench/PAIR/AdvGLUE）已有成熟数据集，但：
- **中文的对抗性评测数据集是空白**（英文技术移植到中文大多失效）
- **"中文模型更安全"这个反直觉结论没有被系统量化**

CAED 填补这个空白，并持续监测"谁先攻破中文模型"。

## 核心方法：三角色对抗

```
攻击者 LLM ──改写攻击模板──▶ 目标 LLM ──响应──▶ 裁判 LLM
   (Attacker)                (Target)           (Judge)
   填充模板/改写           被测试的模型       独立标注成败
```

**护城河逻辑**：对抗样本是"特定时点对特定模型的漏洞快照"——模型厂商会修复漏洞，样本必须持续生成。存量可抄，增量难追。

## 核心发现（详见 [基准报告](docs/benchmark-report-v0.1.md)）

| 发现 | 数据 |
|------|------|
| 整体 ASR | 3.9% (5/129)，英文 HarmBench 通常 30-70% |
| 完全免疫技术 | 16/19 种（DAN/隐喻/逆向心理/提示注入等全 0%） |
| 唯一有效攻击面 | **"重新框定"**——历史讨论包装 30%、翻译绕过 14%、角色扮演 12% |

**结论：中文模型安全对齐强度被英文社区系统性低估。唯一有效攻击是"重新框定"，尤其"历史讨论包装"。**

## 数据集

- **首版**：[releases/caed-v0.1.jsonl](releases/caed-v0.1.jsonl)（129 条去重样本）
- **格式**：JSONL，字段含 `schema_version` / `attack_category` / `attack_technique` / `attack_prompt` / `target_response` / `judge_label` / `judge_confidence` / `judge_reason`

## 快速开始

```bash
pip install -r requirements.txt
export DEEPSEEK_API_KEY="sk-xxx"
python scripts/generate.py --category harmful_content --num 20 --direct
```

## 攻击类别与 ASR（v0.1）

| 类别 | ASR | 最有效技术 |
|------|-----|-----------|
| 有害内容诱导 | 8% | 历史讨论包装（30%） |
| 角色扮演绕过 | 5% | 影视角色扮演 |
| 越狱 | 2% | 翻译绕过 |
| 提示注入 | 0% | 无（中文免疫） |

## 许可

数据集与代码：署名-非商业使用 4.0 (CC BY-NC 4.0)

**注意**：本数据集包含对抗性 prompt，仅用于安全研究与模型鲁棒性评测，请勿用于实际攻击。

## 状态

- [x] 三角色对抗生成脚本（v0.2）
- [x] 19 种攻击技术模板（含"重新框定"型）
- [x] 首版数据集 v0.1（129 条）
- [x] 安全强度基准报告
- [ ] 跨模型验证（接入 Qwen/GLM 作为目标）
- [ ] 社区共建机制（PR → CI 校验）
