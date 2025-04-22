-- Particionamento: Segmentação por Comportamento de Compra
CREATE TABLE main_table_partitioned PARTITION BY LIST (deal_usage_ratio_group) (
    PARTITION heavy_deal_users VALUES IN ('High'),
    PARTITION moderate_deal_users VALUES IN ('Medium'),
    PARTITION low_deal_users VALUES IN ('Low')
) AS
SELECT *,
    CASE 
        WHEN NumDealsPurchases > (SELECT AVG(NumDealsPurchases) + STDDEV(NumDealsPurchases) FROM main_table) THEN 'High'
        WHEN NumDealsPurchases < (SELECT AVG(NumDealsPurchases) - STDDEV(NumDealsPurchases) FROM main_table) THEN 'Low'
        ELSE 'Medium'
    END AS deal_usage_ratio_group
FROM main_table;
/* Motivo: Isola grupos extremos para estratégias de promoção diferenciadas */