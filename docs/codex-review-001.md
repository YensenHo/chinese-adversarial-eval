# CAED 设计审查（Codex Review 001）

## 1. 三角色模型选型

**应分离，至少三方不同源。** 现状全部用 `deepseek-chat`，等于 DeepSeek 自攻自守，攻击多样性差、且只测自己。

- **Attacker**：追求多样性，用多模型混合——Qwen3（阿里）、GLM-4（智谱）、DeepSeek-R1（推理强，擅长构造隐喻越狱），轮换抽样。
- **Target**：被测对象，应支持任意模型（Qwen/GLM/Ernie/自部署），这是数据集的核心价值——不要固定。
- **Judge**：用最强独立模型（GPT-4o / Gemini / Claude），且**必须与 target 不同源**，避免裁判与被测对象同病相怜、漏判。

## 2. 质量度量

- **攻击成功率（ASR）**：按 `attack_category × target_model` 交叉统计，而非全局一个数。
- **多样性**：对 attack_prompt 做 embedding 去重 + self-BLEU（相似度越低越好）+ 关键词/手法聚类，防攻击者收敛到固定套路。
- **裁判可靠性**：抽 100 条人工复标，算 judge 与人工的一致性（Cohen's κ）。

## 3. 最小社区共建机制（MVP）

GitHub PR 流：贡献者提交 JSONL → CI 自动跑「schema 校验 + embedding 去重 + 标准 judge 复标」→ 通过即合并，并回写贡献者 ID 到 `contributor` 字段。配一个 leaderboard 页。无需论坛/账号体系，一个校验脚本即 MVP。

## 4. Schema 改进

- 加 `schema_version`；`id` 改用全 uuid（hex[:8] 易碰撞）。
- 补 `judge_confidence`（0-1）、`human_review` 标记、`attack_technique`（细分手法的子类）。
- 加 `prompt_embedding_hash` 供去重；`contributor` 字段。
- 补 `target_refusal_reason`（记录拒绝类型）。
- README 示例里的 `models` 与 generate.py 的 `attacker_model/target_model/judge_model` 不一致，需统一。
