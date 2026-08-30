# -*- coding: utf-8 -*-
"""
mcp/server.py —— 把语义层封装成 MCP 工具,接入 AI agent

这是"接入 AI agent"的关键一环:任何支持 MCP 的 agent(pi、Claude、Cursor 等)
只要注册这个 server,就能调用下面的工具,拿到"本体化的真实事实"来回答业务问题,
而不是让大语言模型靠猜。

工具(都以本体为词汇基础):
  - product_facts         取一个产品的本体化事实(类/属性/关系)
  - order_facts           取一个订单的本体化事实
  - can_fulfill           推理:某资源某时段能否满足某订单(产能 vs 需求)
  - query_triples         按三元组模式过滤事实

运行:  python3 mcp/server.py
注册:  把它加进你的 agent 的 MCP servers 配置(见 README)。
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from semantic_core import (
    product_facts as product_facts_impl,
    order_facts as order_facts_impl,
    answer_can_fulfill as can_fulfill_impl,
    query_triples as query_triples_impl,
)

# 优先用官方 mcp SDK;没有就降级为 stdio 打印(便于本机先用 stdio 打通)。
try:
    from mcp.server.fastmcp import FastMCP
    HAVE_MCP = True
except Exception:
    HAVE_MCP = False


if HAVE_MCP:
    mcp = FastMCP("sc-plan-ontology")

    @mcp.tool()
    def product_facts(product_id: int) -> dict:
        """取一个产品在供应链本体里的结构化事实(类、提前期、供应商、产线)。"""
        return product_facts_impl(product_id)

    @mcp.tool()
    def order_facts(order_id: int) -> dict:
        """取一个订单的本体化事实(需求哪个产品、多少量、优先级)。"""
        return {"facts": order_facts_impl(order_id)}

    @mcp.tool()
    def can_fulfill(order_id: int, period: str) -> dict:
        """推理某资源在某时段能否满足某订单,返回依据事实+推理+是否可满足。"""
        return can_fulfill_impl(order_id, period)

    @mcp.tool()
    def query_triples(subject: str = None, predicate: str = None, object_: str = None) -> dict:
        """按三元组模式(主语/谓词/宾语,None 为通配)过滤本体事实。"""
        return {"match": {"s": subject, "p": predicate, "o": object_},
                "triples": query_triples_impl((subject, predicate, object_))}

    mcp.run()   # 默认 stdio,供 agent 子进程调用
else:
    # 降级:没有任何依赖,用 stdio 跑一个最小问答循环,方便先在本机"接通"。
    import sys
    print("[sc-plan-ontology] MCP SDK 未安装,使用 stdio 最小模式。"
          " 安装: pip install mcp", file=sys.stderr)
    print("输入形如: can_fulfill 1042 2026-06", file=sys.stderr)
    for line in sys.stdin:
        parts = line.strip().split()
        if not parts:
            continue
        cmd = parts[0]
        if cmd == "can_fulfill" and len(parts) >= 3:
            print(can_fulfill_impl(int(parts[1]), parts[2]))
        elif cmd == "product_facts" and len(parts) >= 2:
            print(product_facts_impl(int(parts[1])))
        elif cmd == "order_facts" and len(parts) >= 2:
            print(order_facts_impl(int(parts[1])))
        else:
            print("unknown command")
