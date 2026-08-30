-- seed.sql —— 和 semantic_core.py 里 DEMO 数据一致,方便对照
INSERT INTO product VALUES
  (447, 'SKU-447', '牙膏-447', 'finished_good', 14),
  (500, 'SKU-500', '铝管-500', 'raw_material',  3);

INSERT INTO resource VALUES
  (7, 'line-7', 'production_line'),
  (1, 'warehouse-a', 'warehouse');

INSERT INTO product_resource VALUES (447, 7);

INSERT INTO supplier VALUES (1, 'us-plants');
INSERT INTO product_supplier VALUES (447, 1);

INSERT INTO purchase_order VALUES (1042, 447, 5000, 'high');

INSERT INTO forecast VALUES (1, 447, '2026-06', 4200);

INSERT INTO capacity VALUES (1, 7, '2026-06', 1200, 3.5);
