DROP procedure IF EXISTS createInvestor;
DROP procedure IF EXISTS createPortfolio;
DROP procedure IF EXISTS insertInvestment;
DROP procedure IF EXISTS updateNumberOfShares;
DROP procedure IF EXISTS deleteInvestment;
DROP procedure IF EXISTS getTotalReturns;
DROP procedure IF EXISTS getStockPrices;
DROP procedure IF EXISTS getAverageAnnualizedReturn;
DROP procedure IF EXISTS filterByRiskLevel;
DROP procedure IF EXISTS findTotalValueOfAllInvestments;
DROP procedure IF EXISTS findOverallAnnualizedReturns;
DROP procedure IF EXISTS findCorrelation;
DROP procedure IF EXISTS getInflationRate;
DROP procedure IF EXISTS filterStockPrice;
DROP procedure IF EXISTS percentageChangeInStockPrice;
DROP procedure IF EXISTS calculateVolatility;
DROP procedure IF EXISTS getTopPerformingStocks;
DROP procedure IF EXISTS numberOfSharesForEachInvestmentType;


DELIMITER $$
CREATE PROCEDURE createInvestor (
    IN p_email VARCHAR(50),
    IN p_password VARCHAR(50),
    IN p_first_name VARCHAR(50),
    IN p_last_name VARCHAR(50)
)
BEGIN
    -- insert investor
    INSERT INTO Investor (MyPassword, FirstName, LastName, Email)
    VALUES (p_password, p_first_name, p_last_name, p_email);
    -- commit transaction
    COMMIT;
END$$
DELIMITER ;

DELIMITER $$

CREATE PROCEDURE createPortfolio (
    IN p_investor_id INT,
    IN p_portfolio_name VARCHAR(50)
)
BEGIN
    -- check if investor exists
    IF EXISTS (SELECT * FROM Investor WHERE InvestorID = p_investor_id) THEN        
		-- insert portfolio
		INSERT INTO Portfolio (InvestorID, PortfolioName)
		VALUES (p_investor_id, p_portfolio_name);
    END IF;
    -- commit transaction
    COMMIT;
END$$
DELIMITER;

DELIMITER $$
CREATE PROCEDURE insertInvestment (
    IN p_portfolio_id INT,
    IN p_investment_name VARCHAR(50),
    IN p_investment_type VARCHAR(50),
    IN p_num_shares INT
)
BEGIN
    DECLARE v_investor_id INT;
    -- get investor id from portfolio id
    SELECT InvestorID INTO v_investor_id FROM Portfolio WHERE PortfolioID = p_portfolio_id;
    -- check if investor exists
    IF v_investor_id IS NOT NULL THEN
		-- insert investment
		INSERT INTO Investment (PortfolioID, InvestmentName, InvestmentType, NumShares)
		VALUES (p_portfolio_id, p_investment_name, p_investment_type, p_num_shares);
    END IF;
    -- commit transaction
    COMMIT;
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
CREATE PROCEDURE DeleteInvestment (
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
	SELECT i.InvestmentName, pm.TotalReturn, pm.AnnualizedReturn FROM Investment i JOIN Performance_Metrics pm ON i.InvestmentID = pm.InvestmentID ORDER BY pm.RiskLevel DESC LIMIT 10;
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
	SELECT (((SELECT StockPrice FROM Market_Data WHERE InvestmentID = p_invextmentID AND InvDate = p_dateNew) - (SELECT StockPrice FROM Market_Data WHERE InvestmentID = p_invextmentID AND InvDate = p_oldNew)) / (SELECT StockPrice FROM Market_Data WHERE InvestmentID = p_invextmentID AND InvDate = p_dateOld)) * 100 AS percentage_change FROM Market_Data WHERE InvestmentID = p_investmentID AND Date = p_dateNew UNION ALL SELECT (((SELECT StockPrice FROM Market_Data WHERE InvestmentID = p_invextmentID AND InvDate = p_dateNew) - (SELECT StockPrice FROM Market_Data WHERE InvestmentID = p_invextmentID AND InvDate = p_dateOld)) / (SELECT StockPrice FROM Market_Data WHERE InvestmentID = p_invextmentID AND InvDate = p_dateOld)) * 100 AS percentage_change FROM Market_Data WHERE InvestmentID = p_investmentID AND InvDate = (SELECT StockPrice FROM Market_Data WHERE InvestmentID = p_invextmentID AND InvDate = p_dateOld);
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




With these queries, write 5 call statements to add investors
