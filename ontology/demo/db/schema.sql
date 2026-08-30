-- schema.sql —— 供应链计划"系统记录"(system of record)
-- 这是闭世界、事务、权威数据所在。语义层(本体)通过 R2RML/OBDA 对齐到这里。
-- 用 PostgreSQL:psql -d scdb -f db/schema.sql

DROP TABLE IF EXISTS product, purchase_order, forecast, resource,
                     product_resource, supplier, product_supplier, capacity;

-- 产品
CREATE TABLE product (
    product_id      int PRIMARY KEY,
    sku             text,
    name            text,
    type            text,          -- finished_good | raw_material
    lead_time_days  int
);

-- 资源(产线/仓库/人力/供应商)
CREATE TABLE resource (
    resource_id   int PRIMARY KEY,
    name          text,
    resource_type text              -- production_line | warehouse | labor
);

-- 哪个产品在哪个资源上生产(本体: isProducedOn)
CREATE TABLE product_resource (
    product_id  int REFERENCES product(product_id),
    resource_id int REFERENCES resource(resource_id),
    PRIMARY KEY (product_id, resource_id)
);

-- 供应商
CREATE TABLE supplier (
    supplier_id int PRIMARY KEY,
    name        text
);
CREATE TABLE product_supplier (
    product_id  int REFERENCES product(product_id),
    supplier_id int REFERENCES supplier(supplier_id),
    PRIMARY KEY (product_id, supplier_id)
);

-- 采购订单(本体: Order)
CREATE TABLE purchase_order (
    order_id    int PRIMARY KEY,
    product_id  int REFERENCES product(product_id),
    qty         int,
    priority    text
);

-- 预测(本体: Forecast)
CREATE TABLE forecast (
    forecast_id int PRIMARY KEY,
    product_id  int REFERENCES product(product_id),
    period      text,
    qty         int
);

-- 产能(再化类 CapacityAllocation):资源 × 时段 × 数量 × 成本
CREATE TABLE capacity (
    capacity_id int PRIMARY KEY,
    resource_id int REFERENCES resource(resource_id),
    period      text,
    qty         numeric,
    cost        numeric
);
