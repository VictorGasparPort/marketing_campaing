-- Query: Análise de Cesta de Compras (Market Basket)
SELECT 
    product_pair,
    support_count,
    confidence,
    lift_ratio
FROM (
    SELECT 
        product_pair,
        COUNT(*) AS support_count,
        COUNT(*) * 1.0 / total_customers AS support,
        COUNT(*) * 1.0 / product1_count AS confidence,
        (COUNT(*) * 1.0 / total_customers) / 
            ((product1_count * 1.0 / total_customers) * (product2_count * 1.0 / total_customers)) AS lift_ratio
    FROM (
        SELECT 
            UNNEST(ARRAY[
                CASE WHEN MntWines > 500 THEN 'Wine' END,
                CASE WHEN MntMeatProducts > 300 THEN 'Meat' END
            ]) AS product1,
            UNNEST(ARRAY[
                CASE WHEN MntGoldProds > 100 THEN 'Gold' END,
                CASE WHEN MntSweetProducts > 50 THEN 'Sweets' END
            ]) AS product2,
            COUNT(*) OVER () AS total_customers,
            SUM(CASE WHEN MntWines > 500 THEN 1 ELSE 0 END) OVER () AS product1_count,
            SUM(CASE WHEN MntGoldProds > 100 THEN 1 ELSE 0 END) OVER () AS product2_count
        FROM main_table
    ) AS pairs
    CROSS JOIN (SELECT COUNT(*) AS total_customers FROM main_table) t
    WHERE product1 IS NOT NULL AND product2 IS NOT NULL
    GROUP BY product1, product2, total_customers, product1_count, product2_count
) AS analysis
WHERE lift_ratio > 1;
-- Calcula associações entre produtos para estratégias de cross-selling