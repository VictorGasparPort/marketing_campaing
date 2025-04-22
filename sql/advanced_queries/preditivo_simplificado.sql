-- Query: Modelo Preditivo Simplificado (Probabilidade de Resposta)
WITH CustomerMetrics AS (
    /* Normalização de variáveis-chave para o modelo */
    SELECT 
        CustomerID,
        (MntWines - (SELECT AVG(MntWines) FROM main_table)) / (SELECT STDDEV(MntWines) FROM main_table) AS wine_zscore,
        LOG(Income + 1) AS log_income,
        EXTRACT(DAY FROM NOW() - DtCustomer) / 365.25 AS tenure_years,
        CASE WHEN Complain = 1 THEN 1 ELSE 0 END AS has_complained
    FROM main_table
)
SELECT 
    cm.CustomerID,
    1 / (1 + EXP(-(
        0.5 * wine_zscore +
        0.3 * log_income -
        0.4 * tenure_years -
        0.6 * has_complained
    )) AS response_probability,
    NTILE(100) OVER (ORDER BY response_probability DESC) AS percentile_rank
FROM CustomerMetrics cm;
-- Fórmula inspirada em regressão logística com pesos empíricos