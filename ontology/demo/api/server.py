# -*- coding: utf-8 -*-
"""
api/server.py —— 语义层 HTTP 查询 API(FastAPI)

把 semantic_core 的"本体化事实 + 查询 + 推理"暴露成 REST 接口,
AI agent / 前端 / 其它系统都可以调用。默认走 DEMO 数据(无需数据库);
若设 DATABASE_URL=postgres://... ,尝试连真实 PostgreSQL(见 load_live)。

启动:  uvicorn api.server:app --reload
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 复用语义层(纯 Python 演示 + 真实库可插拔)
from semantic_core import (product_facts, order_facts,
                           answer_can_fulfill, query_triples)

try:
    from fastapi import FastAPI, Query, HTTPException
    from fastapi.responses import JSONResponse
    HAVE_FASTAPI = True
except Exception:                      # 没装 fastapi 也能 import/检查
    HAVE_FASTAPI = False

app = FastAPI(title="SC Plan Ontology Semantics", version="1.0") if HAVE_FASTAPI else None

# ---- 真实 PostgreSQL 路径(可选)------------------------------------
def load_live():
    """若配置了 DATABASE_URL,把表读进来;否则返回 None 走 DEMO。"""
    url = os.environ.get("DATABASE_URL")
    if not url:
        return None
    try:
        import psycopg2
    except Exception:
        return None
    # 说明:这里用一个极简读取,把 product/capacity 等表换成语义_core 的字典。
    # 完整做法是用 Ontop/R2RML 或在此做 SQL→三元组;为演示仅示意。
    raise NotImplementedError("live-DB via psycopg2: 见 README 的 Ontop/R2RML 路径")


if HAVE_FASTAPI:
    @app.get("/facts/product/{product_id}")
    def get_product_facts(product_id: int):
        r = product_facts(product_id)
        if r is None:
            raise HTTPException(404, "product not found")
        return r

    @app.get("/facts/order/{order_id}")
    def get_order_facts(order_id: int):
        r = order_facts(order_id)
        if r is None:
            raise HTTPException(404, "order not found")
        return {"facts": r}

    @app.get("/answer/can-fulfill")
    def can_fulfill(order_id: int = Query(...), period: str = Query(...)):
        return answer_can_fulfill(order_id, period)

    @app.get("/triples")
    def triples(s: str = Query(None), p: str = Query(None), o: str = Query(None)):
        return {"match": {"s": s, "p": p, "o": o},
                "triples": query_triples((s, p, o))}

    @app.get("/health")
    def health():
        return {"status": "ok", "mode": "demo" if not os.environ.get("DATABASE_URL") else "live",
                "ontology": "sc-planning.ttl"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.server:app", reload=True)
