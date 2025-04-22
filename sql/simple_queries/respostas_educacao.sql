-- Query: Taxa de Resposta por Educação
/* Propósito: Identificar grupos demográficos mais receptivos */
SELECT 
    Education,
    COUNT(*) AS total_customers,
    SUM(Response) AS responders,
    ROUND(SUM(Response) * 100.0 / COUNT(*), 2) AS response_rate
FROM main_table
GROUP BY Education
ORDER BY response_rate DESC;