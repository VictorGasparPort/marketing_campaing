-- Tabela: Valor do Cliente (CLV) e Risco de Churn
CREATE TABLE customer_lifetime_value AS
/* Propósito: Priorizar clientes para retenção e upselling */
SELECT 
    CustomerID,
    (MntWines * 0.4 + MntMeatProducts * 0.3 + MntGoldProds * 0.3) AS clv_score,
    CASE  -- Fórmula de risco adaptativa
        WHEN Complain = 1 AND Recency > 60 THEN 0.7
        WHEN Recency > 90 THEN 0.5
        ELSE 0.1 * (EXTRACT(DAY FROM NOW() - DtCustomer)/365)
    END AS churn_risk,
    NTILE(5) OVER (ORDER BY Income DESC) AS income_quintile
FROM main_table;
-- Combina dados demográficos, comportamentais e transacionais para scoring