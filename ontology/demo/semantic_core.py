#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
semantic_core.py —— 本体语义层(DEMO 模式,无需数据库)

这一层代表系统里的「语义层」:把系统记录(数据库表)的"事实",
按本体(sc-planning.ttl)对齐成 三元组/结构化事实,并提供查询 + 简单推理。

「DEMO 模式」:内置一份和 db/seed.sql 一模一样的演示数据,方便你这台
没有数据库的机器直接跑起来,看它怎么接进 AI agent。
接上 PostgreSQL 后,把 DATASET 换成读库(见 api/server.py 的说明)。

纯 Python、零依赖,直接:
    python3 semantic_core.py
"""

# ---------------------------------------------------------------------------
# 1) 系统记录(数据库表的行)= system of record。字段名尽量贴近本体术语。
# ---------------------------------------------------------------------------
PRODUCTS = {   # product 表
    447: {"sku": "SKU-447", "name": "牙膏-447", "type": "finished_good", "lead_time_days": 14},
    500: {"sku": "SKU-500", "name": "铝管-500", "type": "raw_material",  "lead_time_days": 3},
}
ORDERS = {     # purchase_order 表
    1042: {"product_id": 447, "qty": 5000, "priority": "high"},
}
FORECASTS = {  # forecast 表
    1: {"product_id": 447, "period": "2026-06", "qty": 4200},
}
RESOURCES = {  # resource 表
    7: {"name": "line-7", "type": "production_line"},
    1: {"name": "warehouse-a", "type": "warehouse"},
}
PRODUCT_RESOURCE = {  # product_resource 表: 哪个产品在哪个资源上生产
    447: 7,
}
SUPPLIERS = { 1: {"name": "us-plants"} }
PRODUCT_SUPPLIER = {447: 1}
CAPACITY = {   # capacity 表(再化类 CapacityAllocation)
    1: {"resource_id": 7, "period": "2026-06", "qty": 1200, "cost": 3.5},
}

# ---------------------------------------------------------------------------
# 2) 语义函数:把行 → 本体化的事实(agent 可直接消费的结构)
# ---------------------------------------------------------------------------

def product_facts(product_id):
    """返回一个产品在本体里的结构化事实(类、数据属性、对象属性)。"""
    if product_id not in PRODUCTS:
        return None
    p = PRODUCTS[product_id]
    cls = "FinishedGood" if p["type"] == "finished_good" else "RawMaterial"
    return {
        "iri": f"http://example.org/sc#product-{product_id}",
        "class": cls,
        "facts": [
            f"product-{product_id}  a  {cls}",
            f"product-{product_id}  :hasLeadTime  {p['lead_time_days']}",
        ],
        "supplier": [SUPPLIERS[PRODUCT_SUPPLIER[product_id]]["name"]]
                   if product_id in PRODUCT_SUPPLIER else [],
        "produced_on": f"line-{PRODUCT_RESOURCE[product_id]}"
                       if product_id in PRODUCT_RESOURCE else None,
    }

def order_facts(order_id):
    """订单的本体化事实:需要哪个产品、多少量。"""
    if order_id not in ORDERS:
        return None
    o = ORDERS[order_id]
    return [
        f"order-{order_id}  a  Order",
        f"order-{order_id}  :requiresProduct  product-{o['product_id']}",
        f"order-{order_id}  :hasQuantity  {o['qty']}",
        f"order-{order_id}  :hasPriority  \"{o['priority']}\"",
    ]

def resource_has_capacity(resource_id, period):
    """资源在某时段的产能(再化类 CapacityAllocation)。"""
    for c in CAPACITY.values():
        if c["resource_id"] == resource_id and c["period"] == period:
            return c
    return None

# ---------------------------------------------------------------------------
# 3) 一个"意图 → 事实 + 推理"的查询(配合本体 / 推理器)
# ---------------------------------------------------------------------------

def answer_can_fulfill(order_id, period):
    """
    对应 agent 的问题:「7 号线下个月能满足订单 1042 吗?」
    沿本体关系将事实串起来,再做一次简单推理(产能 vs 需求)。
    """
    if order_id not in ORDERS:
        return {"error": f"no order {order_id}"}
    o = ORDERS[order_id]
    product_id = o["product_id"]
    res_id = PRODUCT_RESOURCE.get(product_id)
    if res_id is None:
        return {"error": f"no resource produces product-{product_id}"}
    cap = resource_has_capacity(res_id, period)
    if cap is None:
        return {"error": f"no capacity allocation for line-{res_id} in {period}"}

    need = o["qty"]
    avail = cap["qty"]
    ok = avail >= need
    return {
        "question": f"line-{res_id} {period} 能否满足 order-{order_id}?",
        "facts": order_facts(order_id) + [
            f"product-{product_id}  :isProducedOn  line-{res_id}",
            f"capacity-{cap['resource_id']}-{cap['period']}  a  CapacityAllocation",
            f"capacity-{cap['resource_id']}-{cap['period']}  :hasCapacityValue  {cap['qty']}",
        ],
        "reasoning": f"order-{order_id} 需要 {product_id} × {need};"
                     f" line-{res_id} 在 {period} 产能 {avail}"
                     f" ⇒ { '可满足' if ok else '不足,排不下' }",
        "can_fulfill": ok,
        "shortage": max(0, need - avail),
    }

# ---------------------------------------------------------------------------
# 4) 一个"三元组查询"(对应 SPARQL 模式匹配,这里是演示实现)
# ---------------------------------------------------------------------------

def query_triples(pattern):
    """
    极简三元组模式查询。pattern 形如:
       ("order-1042", "requiresProduct", None)   # None = 通配变量
       (None, "hasLeadTime", None)
    返回匹配的三元组列表。真实落地时这里换成 SPARQL(交给 agent / Ontop 改写)。
    """
    s, p, o = pattern
    triples = []
    # 汇总所有已知三元组
    for pid in PRODUCTS:
        triples += [f"product-{pid}  a  {('FinishedGood' if PRODUCTS[pid]['type']=='finished_good' else 'RawMaterial')}",
                    f"product-{pid}  :hasLeadTime  {PRODUCTS[pid]['lead_time_days']}",
                    f"product-{pid}  :hasSupplier  supplier-{PRODUCT_SUPPLIER[pid]}"
                    if pid in PRODUCT_SUPPLIER else None]
    for oid in ORDERS:
        triples += order_facts(oid)
    triples += [f"line-{c['resource_id']}  :hasCapacityValue  {c['qty']}" for c in CAPACITY.values()]
    triples = [t for t in triples if t]

    def matches(t):
        # 三元组形如 "s  p  o",用双空格分隔
        parts = [x.strip() for x in t.split("  ") if x.strip()]
        if len(parts) < 3:
            return False
        pred = parts[1].lstrip(':')     # 谓词可能带 : 前缀,统一比对
        return ((s is None or s == parts[0]) and
                (p is None or p == pred) and
                (o is None or o in parts[2]))
    return [t for t in triples if matches(t)]


# ---------------------------------------------------------------------------
# 5) 演示入口
# ---------------------------------------------------------------------------
def main():
    print("=" * 66)
    print("本体语义层 DEMO —— 供应链计划(sc-planning)")
    print("=" * 66)

    print("\n[1] 产品 447 的本体化事实:")
    for f in product_facts(447)["facts"]:
        print("   ", f)

    print("\n[2] 三元组模式查询:所有 hasLeadTime")
    for t in query_triples((None, "hasLeadTime", None)):
        print("   ", t)

    print("\n[3] 意图推理:「7 号线下个月能满足订单 1042 吗?」")
    a = answer_can_fulfill(1042, "2026-06")
    for f in a["facts"]:
        print("   (事实) ", f)
    print("   (推理) ", a["reasoning"])
    print("   => can_fulfill:", a["can_fulfill"], "| 缺口:", a["shortage"])

    print("\n[4] 推断规则(本体 domain)示例:")
    print("    因为 order-1042 :requiresProduct product-447,且 hasLeadTime 的 range 是 integer,")
    print("   可推出 product-447 是 FinishedGood(若未显式声明)。")

    print("\n说明:接上 PostgreSQL 后,这些函数问 DB 而不是内置数据;"
          "API 与 MCP server 都复用本模块,是同一套语义层。")


if __name__ == "__main__":
    main()
