-- Query: Análise de Recência vs. Compras
/* Propósito: Entender padrões de recompra */
SELECT 
    CASE 
        WHEN Recency <= 30 THEN '0-30 dias'
        WHEN Recency <= 60 THEN '31-60 dias'
        ELSE '61+ dias'
    END AS recency_group,
    AVG(NumWebVisitsMonth) AS avg_web_visits,
    AVG(NumStorePurchases) AS avg_store_purchases
FROM main_table
GROUP BY 1
ORDER BY MIN(Recency);