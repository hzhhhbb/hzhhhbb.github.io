#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
agent_orchestration.py —— 编排层:语义层之上、LLM 之前

这才是"接入 AI agent、组装上下文、调用 LLM"发生的地方。

分层:
   语义层 (semantic_core / api / mcp)  →  给出【确定事实 + 推理】,无 LLM
   ┌─ 编排层 (本文件) ──────────────┐
   │  ① 听懂问题 → 选工具            │
   │  ② 调 MCP/API 拿事实(无 LLM)   │
   │  ③ 组装上下文(system+事实)     │
   │  ④ 调用 LLM(可插拔)           │
   └──────────────────────────────┘

运行(零依赖,会打印出【组装好的 prompt】和"LLM 调用点"):
   python3 agent_orchestration.py
"""
import json
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from semantic_core import answer_can_fulfill   # 语义层(无 LLM)

# ---- skill = 给 agent 的"上下文一":领域词汇 + 调用规则 ---------------------
def load_skill():
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "skill", "sc-planning-agent.md")
    return open(p, encoding="utf-8").read()


# ---- ① 听懂问题 → 选工具(这里用简单规则;真实可用 LLM 做意图识别) ------
def choose_tool(question):
    q = question.lower()
    if "满足" in q or "排不排" in q or "排得下" in q or "产能" in q:
        return "can_fulfill"
    if "提前期" in q or "lead" in q:
        return "query_triples"
    if "订单" in q or "order" in q:
        return "order_facts"
    return "product_facts"


# ---- ② 调 MCP/API 拿事实(无 LLM)—— 真实落地时换成本模块/MCP 调用 -------
def call_semantic_tool(tool, args):
    # 演示:直接调语义层;真实用 mcp.client / requests 调 api
    if tool == "can_fulfill":
        return answer_can_fulfill(args["order_id"], args["period"])
    return {"tool": tool, "args": args}


# ---- ④ 调用 LLM —— 可插拔;不破坏"语义层零 LLM"的原则 --------------------
def call_llm(prompt, model="gpt-4o-mini"):
    """真实的 LLM 调用。此处返回一个占位,说明这是调用点。

    真实实现示例(任选其一):
      - OpenAI:  openai.chat.completions.create(model=model, messages=[{"role":"user","content":prompt}])
      - 或走你已有的 LLM 网关 / agent 运行时。
    """
    # 为了演示,这里不真正请求;返回一个"模拟"已回答。
    return ("模拟回答:「订单 1042 需要 SKU-447(牙膏-447) × 5000,"
            "生产资源 line-7 在 2026-06 的产能为 1200,缺口 3800," 
            "因此本月无法完全满足。」  (此处为真实 LLM 调用点)")


# ---- 组装上下文 + 调用 LLM ------------------------------------------------
def run(question, order_id=1042, period="2026-06"):
    print("=" * 66)
    print("编排层 —— 接入 AI agent 的完整链路(语义层之上)")
    print("=" * 66)

    # ① 选工具
    tool = choose_tool(question)
    print(f"\n[1] 听懂问题 → 选工具:  {tool}")

    # ② 从语义层拿确定事实(无 LLM)
    facts = call_semantic_tool(tool, {"order_id": order_id, "period": period})
    print(f"[2] 调语义层拿事实(无 LLM):")
    for f in facts.get("facts", []):
        print("      (事实) ", f)
    print("      (推理) ", facts.get("reasoning", ""))

    # ③ 组装上下文 = skill 指令 + 事实
    system = load_skill()
    context = f"{system}\n\n[当前问题]\n{question}\n\n[已取得的事实与推理]\n{json.dumps(facts, ensure_ascii=False, indent=2)}"
    print(f"[3] 组装上下文(system 长度 {len(system)} 字 + 事实)—— 这就是喂给 LLM 的 prompt")

    # ④ 调用 LLM
    print(f"[4] 调用 LLM(mock)……")
    print("\n" + call_llm(context))
    print("\n说明:第①②步无 LLM;③④步(选工具/组装上下文/调 LLM)才在 agent 层发生。")


if __name__ == "__main__":
    q = sys.argv[1] if len(sys.argv) > 1 else "7 号线下个月能满足订单 1042 吗?"
    run(q)
