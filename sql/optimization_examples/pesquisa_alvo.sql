-- Índice: Pesquisa Rápida de Clientes-Alvo
CREATE INDEX idx_high_value_targets ON main_table (Income, Response)
INCLUDE (Recency, MntWines)
WHERE Response = 1 AND Income > 90000;
/* Motivo: Acelera queries de prospecção focando nos 20% que geram 80% do ROI */
