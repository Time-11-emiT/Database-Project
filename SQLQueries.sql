DROP procedure IF EXISTS insertInvestment;
DROP procedure IF EXISTS updateNumberOfShares;

DELIMITER $$
CREATE PROCEDURE insertInvestment(
IN p_InvestorID INT,
IN p_FirstName VARCHAR(50),
IN p_LastName VARCHAR(50),
IN p_Email VARCHAR(50), 
IN p_Password VARCHAR(50),
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
INSERT INTO Investor(InvestorID, FirstName, LastName, Email, MyPassword)
VALUES (p_InvestorID, p_FirstName, p_LastName, p_Email, p_Password);

INSERT INTO Portfolio (PortfolioID, InvestorID, PortfolioName) 
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
update investment SET investment.NumShares = new_num_shares WHERE investment.InvestmentID=p_investmentID;
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
CREATE PROCEDURE CalculateCorrelation(IN id1 INT, IN id2 INT)
     BEGIN
         DECLARE x FLOAT;
         DECLARE y FLOAT;
         DECLARE x_sum FLOAT;
         DECLARE y_sum FLOAT;
         DECLARE x_squared_sum FLOAT;
         DECLARE y_squared_sum FLOAT;
         DECLARE xy_sum FLOAT;
         DECLARE n INT;
         
         SELECT COUNT(*) INTO n FROM Market_Data WHERE InvestmentID = id1 OR InvestmentID = id2;
         
         IF n < 2 THEN
             SELECT 'Not enough data points available' AS Error;
         ELSE
             SELECT SUM(CASE WHEN InvestmentID = id1 THEN StockPrice ELSE 0 END),
                    SUM(CASE WHEN InvestmentID = id2 THEN StockPrice ELSE 0 END),
                    SUM(CASE WHEN InvestmentID = id1 THEN StockPrice*StockPrice ELSE 0 END),
                    SUM(CASE WHEN InvestmentID = id2 THEN StockPrice*StockPrice ELSE 0 END),
                    SUM(CASE WHEN InvestmentID = id1 THEN StockPrice ELSE 0 END * CASE WHEN InvestmentID = id2 THEN StockPrice ELSE 0 END)
             INTO x_sum, y_sum, x_squared_sum, y_squared_sum, xy_sum
             FROM Market_Data
             WHERE InvestmentID = id1 OR InvestmentID = id2;
     
             SET x = (n * xy_sum - x_sum * y_sum) / (n * x_squared_sum - x_sum * x_sum);
             SET y = (y_sum - x * x_sum) / n;
     
             SELECT x AS Correlation;
         END IF;
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
	SELECT (((SELECT StockPrice FROM market_data WHERE InvestmentID = p_invextmentID AND InvDate = p_dateNew) - (SELECT StockPrice FROM market_data WHERE InvestmentID = p_invextmentID AND InvDate = p_oldNew)) / (SELECT StockPrice FROM market_data WHERE InvestmentID = p_invextmentID AND InvDate = p_dateOld)) * 100 AS percentage_change FROM Market_Data WHERE InvestmentID = p_investmentID AND Date = p_dateNew UNION ALL SELECT (((SELECT StockPrice FROM market_data WHERE InvestmentID = p_invextmentID AND InvDate = p_dateNew) - (SELECT StockPrice FROM market_data WHERE InvestmentID = p_invextmentID AND InvDate = p_dateOld)) / (SELECT StockPrice FROM market_data WHERE InvestmentID = p_invextmentID AND InvDate = p_dateOld)) * 100 AS percentage_change FROM Market_Data WHERE InvestmentID = p_investmentID AND InvDate = (SELECT StockPrice FROM market_data WHERE InvestmentID = p_invextmentID AND InvDate = p_dateOld);
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
