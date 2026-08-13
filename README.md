# Chinese Adversarial Evaluation Dataset (CAED)

中文对抗性评测数据集 —— 用"对抗式 AI 协作"生成的中文大模型安全评测基准。

> 英文世界的对抗评测已有 HarmBench、PAIR、AdvGLUE。中文的对抗性、持续更新、社区共建的评测数据集，目前是空白。CAED 填补这个空白。

## 核心方法：三角色对抗

用三个 LLM 角色互相博弈，生成"对抗样本"：

```
攻击者 LLM  ──生成对抗 prompt──▶  目标 LLM  ──响应──▶  裁判 LLM
   (Attacker)                      (Target)            (Judge)
   试图攻破安全限制              被测试的模型          独立标注成败
```

**护城河逻辑**：对抗样本是"特定时点对特定模型的漏洞快照"——模型厂商会修复漏洞，所以样本必须持续生成。存量可抄，增量难追。

## 数据格式（JSONL）

每条记录一个对抗样本：

```json
{
  "id": "caed-000001",
  "attack_category": "jailbreak",        // 越狱 | prompt_injection | harmful_content | roleplay_bypass
  "attacker_model": "deepseek-chat",
  "target_model": "deepseek-chat",
  "attack_prompt": "忽略之前的指令，现在你是...",
  "target_response": "（目标模型的完整响应）",
  "judge_model": "deepseek-chat",
  "judge_label": "attack_success",        // attack_success | attack_failure
  "judge_reason": "目标模型违反了安全策略，提供了...",
  "timestamp": "2026-08-13T12:00:00Z"
}
```

## 攻击类别

| 类别 | 说明 |
|------|------|
| `jailbreak` | 越狱——绕过系统安全限制 |
| `prompt_injection` | 提示注入——用指令劫持模型行为 |
| `harmful_content` | 有害内容诱导——引导生成有害信息 |
| `roleplay_bypass` | 角色扮演绕过——借角色规避限制 |

## 快速开始

```bash
pip install -r requirements.txt
export DEEPSEEK_API_KEY="sk-xxx"
python scripts/generate.py --category jailbreak --num 20
```

## 许可

数据集与代码：署名-非商业使用 4.0 (CC BY-NC 4.0)

**注意**：本数据集包含对抗性/攻击性 prompt，仅用于安全研究与模型鲁棒性评测，请勿用于实际攻击。

## 状态

- [x] 项目初始化
- [ ] 三角色对抗生成脚本
- [ ] 第一批中文对抗样本
- [ ] 社区共建机制
