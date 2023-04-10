DROP procedure insertInvestment;

DELIMITER $$
CREATE PROCEDURE insertInvestment(
IN p_InvestorID INT,
IN p_PortfolioID INT,
IN p_PortfolioName VARCHAR(50),
IN p_InvestmentName VARCHAR(50),
IN p_InvestmentType VARCHAR(50),
IN p_NumShares INT,
IN p_Date DATE,
IN p_StockPrice FLOAT,
IN p_ExchangeRate FLOAT,
IN p_CommodityPrice FLOAT,
IN p_TotalReturn FLOAT,
IN p_AnnualizedReturn FLOAT,
IN p_RiskLevel FLOAT
)
BEGIN
-- Insert the investment into the Investment table
INSERT INTO portfolio (PortfolioID, InvestorID, PortfolioName) 
VALUES (p_PortfolioID, p_InvestorID, p_PortfolioName);

INSERT INTO Investment (PortfolioID, InvestmentName, InvestmentType, NumShares)
VALUES (p_PortfolioID, p_InvestmentName, p_InvestmentType, p_NumShares);

-- Get the InvestmentID of the newly inserted investment
SET @InvestmentID = LAST_INSERT_ID();

-- Insert market data for the investment into the Market_Data table
INSERT INTO Market_Data (InvestmentID, Date, StockPrice, ExchangeRate, CommodityPrice)
VALUES (@InvestmentID, p_Date, p_StockPrice, p_ExchangeRate, p_CommodityPrice);

-- Insert performance metrics for the investment into the Performance_Metrics table
INSERT INTO Performance_Metrics (InvestmentID, TotalReturn, AnnualizedReturn, RiskLevel)
VALUES (@InvestmentID, p_TotalReturn, p_AnnualizedReturn, p_RiskLevel);
END$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE updateNumberOfShares(
IN p_investmentID INT,
IN new_num_shares INT
)
BEGIN
-- Update the investment in the Investment table where InvestmentID = p_investmentID
update investment SET ivestment.NumShares = new_num_shares WHERE investment.InvestmentID=p_investmentID;
END$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE DeleteInvestment(
IN p_investmentID INT
)
BEGIN
	-- Delete the investment in the Market_Data table where InvestmentID = p_investmentID
	DELETE FROM Market_Data
	WHERE InvestmentID = p_InvestmentID;
	-- Delete the investment in the Performance_Metrics table where InvestmentID = p_investmentID
	DELETE FROM Performance_Metrics
	WHERE InvestmentID = p_InvestmentID;
	-- Delete the investment in the Investment table where InvestmentID = p_investmentID
	DELETE FROM investment WHERE investment.InvestmentID=p_investmentID;
END$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE getTotalReturns()
BEGIN
	SELECT i.InvestmentName, pm.TotalReturn FROM Investment i JOIN Performance_Metrics pm ON i.InvestmentID = pm.InvestmentID;
END$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE getStockPrices(
  IN p_Date DATE
)
BEGIN
  -- Join the Investment and Market_Data tables and retrieve the StockPrice column for the specified date
SELECT i.InvestmentName, md.StockPrice FROM Investment i JOIN Market_Data md ON i.InvestmentID = md.InvestmentID WHERE md.Date = p_Date;

END$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE getAverageAnnualizedReturn()
BEGIN
	SELECT i.InvestmentType, AVG(pm.AnnualizedReturn) as AvgAnnualizedReturn FROM Investment i JOIN Performance_Metrics pm ON i.InvestmentID = pm.InvestmentID GROUP BY i.InvestmentType;
END$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE filterByRiskLevel()
BEGIN
	SELECT i.InvestmentName, pm.TotalReturn, pm.AnnualizedReturn FROM Investment i JOIN Performance_Metrics pm ON i.InvestmentID = pm.InvestmentID ORDER BY pm.AnnualizedReturn DESC LIMIT 10;
END$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE findTotalValueOfAllInvestments()
BEGIN
	SELECT SUM(i.NumShares * md.StockPrice) AS TotalValue FROM Investment i JOIN Market_Data md ON i.InvestmentID = md.InvestmentID;

END$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE findOverallAnnualizedReturns()
BEGIN
	SELECT SUM(i.NumShares * pm.AnnualizedReturn) / SUM(i.NumShares) AS PortfolioAnnualizedReturn FROM Investment i JOIN Performance_Metrics pm ON i.InvestmentID = pm.InvestmentID;
END$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE findCorrelation(
	IN p_investmentID1 INT,
    IN p_investmentID2 INT
)
BEGIN
	SELECT CORR(pm1.AnnualizedReturn, pm2.AnnualizedReturn) AS Correlation FROM Performance_Metrics pm1 JOIN Performance_Metrics pm2 ON pm1.PerformanceMetricsID <> pm2.PerformanceMetricsID WHERE pm1.InvestmentID = p_investmentID1 AND pm2.InvestmentID = p_investmentID2;
END$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE getInflationRate()
BEGIN
  -- Return the most recent inflation rate from the Other_Financial_Information table
  SELECT Inflation_Rate FROM Other_Financial_Information ORDER BY Date DESC LIMIT 1;
END$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE filterStockPrice(
	IN p_investmentID INT,
    IN p_date1  DATE,
    IN p_date2 DATE
)
BEGIN	
	SELECT StockPrice FROM Market_Data WHERE InvestmentID = p_investmentID AND Date BETWEEN p_date1 AND p_date2;
END$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE percentageChangeInStockPrice(
	IN p_investmentID INT,
    IN p_dateOld  DATE,
    IN p_dateNew DATE
)
BEGIN	
	SELECT ((new_stock_price - old_stock_price) / old_stock_price) * 100 AS percentage_change FROM Market_Data WHERE InvestmentID = p_investmentID AND Date = p_dateNew UNION ALL SELECT ((new_stock_price - old_stock_price) / old_stock_price) * 100 AS percentage_change FROM Market_Data WHERE InvestmentID = p_investmentID AND Date = p_dateOld;
END$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE calculateVolatility(
	IN p_investmentID INT
)
BEGIN	
	SELECT STDDEV(TotalReturn) as Volatility FROM Performance_Metrics WHERE InvestmentID = p_investmentID;
END$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE getTopPerformingStocks()
BEGIN	
	SELECT InvestmentID, TotalReturn, AnnualizedReturn, RiskLevel FROM Performance_Metrics ORDER BY AnnualizedReturn DESC, RiskLevel DESC LIMIT 10;
END$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE numberOfSharesForEachInvestmentType()
BEGIN	
	SELECT InvestmentType, SUM(NumShares) AS TotalShares FROM Investment GROUP BY InvestmentType;
END$$
DELIMITER ;

CALL insertInvestment(1, 1, 'laks', 'APPL', 'Stock', 10, '2023-04-10', 35.52, 10.05, 7262.92,689,38,292);
CALL insertInvestment(1, 1, 'laks',1, 'GOOG', 'Stock', 11, '2023-03-10', 376, 1.05, 72.9642,89,378,473);
CALL insertInvestment(1, 1, 'laks',2, 'APPL', 'Stock', 123, '2023-02-10', 3645.2, 2630.05, 7642.942,289,38,2182);
CALL insertInvestment(1, 1, 'laks',3, 'HOAK', 'Stock', 154, '2023-01-10', 3.2, 1037.05, 7212.92,894,38,234);
CALL insertInvestment(4, 'PALS', 'Stock', 144, '2023-07-10', 39.76, 1092.05, 762.92,893,38,22);
CALL insertInvestment(5, 'AYSH', 'Stock', 12, '2022-08-10', 30.5, 1120.05, 723.92,893,38,29);
CALL insertInvestment(6, 'DHYE', 'Stock', 1223, '2022-02-10', 4325.2, 23630.05, 76542.942,28359,328,2182);
CALL insertInvestment(6, 'RAKS', 'Stock', 1544, '2022-01-10', 43.2, 1735.05, 7212.9562,89423,338,234);
CALL insertInvestment(6, 'SHUB', 'Stock', 1441, '2022-07-10', 3439.76, 1352.05, 7624.92,53893,383,22);
CALL insertInvestment(7, 'HARS', 'Stock', 124, '2022-08-10', 30.55, 12120.05, 7232.92,8393,38,239);
