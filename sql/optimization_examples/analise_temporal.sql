-- Índice: Otimização para Análise Temporal
CREATE INDEX idx_temporal_analysis ON main_table 
    (EXTRACT(YEAR FROM DtCustomer), Recency)
INCLUDE (NumWebVisitsMonth, NumStorePurchases);
/* Motivo: Consultas frequentes combinam ano de cadastro com atividade recente */