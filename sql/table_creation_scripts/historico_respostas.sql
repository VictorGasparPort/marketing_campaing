-- Tabela: Histórico de Resposta a Campanhas (Armazena engajamento histórico)
CREATE TABLE campaign_response_history AS
/* Propósito: Rastrear padrões de aceitação ao longo do tempo para modelagem preditiva */
SELECT 
    CustomerID,
    DtCustomer,
    EXTRACT(YEAR FROM DtCustomer) AS enrollment_year,
    AcceptedCmp1 + AcceptedCmp2 + AcceptedCmp3 + AcceptedCmp4 + AcceptedCmp5 AS total_acceptances,
    CASE  -- Classificação de engajamento multicampanha
        WHEN (AcceptedCmp1 + AcceptedCmp2 + AcceptedCmp3 + AcceptedCmp4 + AcceptedCmp5) >= 3 THEN 'Super Responder'
        WHEN (AcceptedCmp1 + AcceptedCmp2 + AcceptedCmp3 + AcceptedCmp4 + AcceptedCmp5) = 0 THEN 'Não Respondedor'
        ELSE 'Respondedor Ocasional'
    END AS engagement_tier
FROM main_table;
-- Permite segmentação baseada em histórico de respostas para estratégias de retargeting
