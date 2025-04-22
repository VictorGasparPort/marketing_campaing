-- Tabela: Perfil de Gastos por Categoria (Agrega comportamento de compra)
CREATE TABLE spending_profiles (
    customer_id INT PRIMARY KEY,
    food_spending NUMERIC,
    premium_spending NUMERIC,
    deal_usage_ratio NUMERIC
);
/* Propósito: Criar grupos para personalização de ofertas */
INSERT INTO spending_profiles
SELECT 
    CustomerID,
    (MntFruits + MntMeatProducts + MntFishProducts) AS food_spending,
    (MntWines + MntGoldProds) AS premium_spending,
    NumDealsPurchases * 1.0 / GREATEST(NumStorePurchases + NumWebPurchases, 1) AS deal_usage_ratio
FROM main_table;
-- Ratios ajudam a identificar dependência em promoções vs. compras premium