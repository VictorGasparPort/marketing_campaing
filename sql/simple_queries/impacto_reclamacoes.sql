-- Query: Impacto de Reclamações na Retenção
/* Propósito: Medir efeito de reclamações na atividade do cliente */
SELECT 
    Complain,
    AVG(Recency) AS avg_recency,
    AVG(MntWines) AS avg_wine_spending,
    COUNT(*) FILTER (WHERE Response = 1) * 100.0 / COUNT(*) AS response_rate
FROM main_table
GROUP BY Complain;