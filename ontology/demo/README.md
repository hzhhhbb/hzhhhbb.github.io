# 供应链计划「本体语义层」落地示例

一个**能落地、能跑、能接进 AI agent** 的最小例子。展示:系统记录(PostgreSQL)
→ 本体语义层 → **API / MCP / skill** → AI agent 基于事实回答。

```
demo/
├── ontology/sc-planning.ttl   # 本体(语义层):类/属性/domain-range/公理
├── semantic_core.py           # 语义层核心(纯 Python,零依赖,开箱即跑)
├── db/schema.sql              # PostgreSQL 系统记录(表)
├── db/seed.sql                # 演示数据(与语义层内置一致)
├── db/mapping.r2rml           # R2RML:把表对准本体(W3C 标准打通)
├── api/server.py              # FastAPI:把语义层暴露成 REST 查询接口
├── mcp/server.py              # MCP server:把语义层封装成 agent 可调用的工具
└── skill/sc-planning-agent.md # skill:领域词汇 + 怎么调用 + 回答规范
```

## 它怎么"打通"

```
关系库(系统记录,闭世界)  ──R2RML/OBDA──▶  本体语义层(开放世界,可推理)  ──▶  AI agent(大语言模型)
  db/schema.sql                       ontology/sc-planning.ttl             mcp/server.py + skill
```

- **系统记录**:`purchase_order` 表有订单 1042 要 SKU-447 × 5000、`capacity` 表有 line-7 六月产能 1200。
- **语义层**:把这些"行"对齐本体,变成 `order-1042 :requiresProduct product-447`、`line-7 :hasCapacityValue 1200` 等**事实**。
- **推理**:"需要 5000、产能 1200 ⇒ 缺 3800,排不下"。
- **AI 取事实回答**,不靠猜。

## 一、立刻看效果(这台机器没库也能跑)

```bash
cd demo
python3 semantic_core.py            # 无任何依赖,直接看"产品事实/三元组查询/推理"
```

## 二、接进 AI agent(三种组件,任选或组合)

**A. MCP(推荐)—— agent 把语义层当工具调**
```bash
pip install mcp
python3 mcp/server.py               # 以 stdio 启动 MCP server
```
把 `mcp/server.py` 注册进你的 agent 的 MCP servers 列表(如 pi 的
`~/.config/pi/settings.json` 或 Claude/Cursor 的 MCP 配置)。注册后,agent 就
能调用 `product_facts / order_facts / can_fulfill / query_triples` 这四个工具。

**B. Skill —— 教 agent 怎么用、用什么词**
把 `skill/sc-planning-agent.md` 作为 skill 交给 agent。它会读"领域词汇 + 工具表 +
回答规范",从而**先取事实再回答、并保持口径一致**。

**C. API —— 任何系统/前端查询**
```bash
pip install fastapi uvicorn
uvicorn api.server:app --reload    # http://127.0.0.1:8000
# 浏览器/接口:
#   /facts/product/447
#   /facts/order/1042
#   /answer/can-fulfill?order_id=1042&period=2026-06
#   /triples?p=hasLeadTime          (三元组模式查询)
#   /health
```

## 三、接上真实 PostgreSQL

```bash
docker compose up -d db            # 启动 postgres(scdb),或用自己的库
psql -h localhost -U sc -d scdb -f db/schema.sql
psql -h localhost -U sc -d scdb -f db/seed.sql
# 若要语义层直接读库,设 DATABASE_URL 并参照 README 的 Ontop/R2RML 路径
```

> 生产级"数据不搬家"的打通,用 **Ontop(Ontology-Based Data Access)**:
> 它把关系库当**虚拟知识图谱**,sparql 查询自动转 sql,数据仍留在库中。
> 只需提供 `db/mapping.r2rml` + `ontology/sc-planning.ttl`。

## 关键概念对照(回顾课程)

| 组件 | 对应课程 |
|---|---|
| `ontology/sc-planning.ttl` | 0001–0004(类/属性/公理) |
| `db/mapping.r2rml` | 0010(R2RML 打通) |
| `semantic_core.py` 的推理 | 0002/0004(推理+推理器) |
| `answer_can_fulfill` | 0006/0007(SPARQL+开放世界→RAG) |
| `mcp/server.py` + `skill` | 0009/0010(接入 agent) |
