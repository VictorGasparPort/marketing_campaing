-- Query: Análise de Cohorte por Educação
SELECT 
    enrollment_cohort,
    education_level,
    response_rate,
    spending_growth
FROM (
    SELECT 
        EXTRACT(YEAR FROM DtCustomer) AS enrollment_cohort,
        Education AS education_level,
        AVG(Response::FLOAT) AS response_rate,
        (AVG(MntWines) - LAG(AVG(MntWines), 1) OVER (PARTITION BY Education ORDER BY EXTRACT(YEAR FROM DtCustomer)))
            / LAG(AVG(MntWines), 1) OVER (PARTITION BY Education ORDER BY EXTRACT(YEAR FROM DtCustomer)) AS spending_growth,
        COUNT(*) AS cohort_size
    FROM main_table
    GROUP BY 1,2
) AS cohort_data
WHERE cohort_size > 30
AND enrollment_cohort BETWEEN 2015 AND 2020;
-- Identifica tendências de longo prazo por nível educacional