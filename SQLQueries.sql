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
DROP procedure IF EXISTS insertMarketData;

DELIMITER $$
CREATE PROCEDURE insertMarketData (
    IN p_investment_id INT,
    IN p_date DATE,
    IN p_stock_price FLOAT,
    IN p_exchange_rate FLOAT,
    IN p_commodity_price FLOAT
)
BEGIN
    -- check if investment exists
    IF EXISTS(SELECT * FROM Investment WHERE InvestmentID = p_investment_id) THEN
		-- insert market data
		INSERT INTO Market_Data (InvestmentID, InvDate, StockPrice, ExchangeRate, CommodityPrice)
		VALUES (p_investment_id, p_date, p_stock_price, p_exchange_rate, p_commodity_price);
    END IF;
    -- commit transaction
    COMMIT;
END$$
DELIMITER ;


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
    IN p_num_shares INT,
    IN p_date DATE,
    IN p_stock_price FLOAT,
    IN p_exchange_rate FLOAT, 
    IN p_commodity_price FLOAT
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
        CALL insertMarketData(v_investor_id, p_date, p_stock_price,p_exchange_rate, p_commodity_price);
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


SELECT * FROM Investor;
CALL createInvestor('johndoe123@gmail.com', 'JohnDoe123', 'John', 'Doe');
CALL createInvestor('janedoe456@gmail.com', 'JaneDoe456', 'Jane', 'Doe');
CALL createInvestor('bobsmith789@gmail.com', 'BobSmith789', 'Bob', 'Smith');
CALL createInvestor('amandabrown234@gmail.com', 'AmandaBrown234', 'Amanda', 'Brown');
CALL createInvestor('michaeljones567@gmail.com', 'MichaelJones567', 'Michael', 'Jones');
CALL createInvestor('YashBarge@gmail.com', 'Yash123', 'Yash', 'Barge');
CALL createInvestor('SourabhB@gmail.com', 'Sourabh12345', 'Sourabh', 'Bhandari');
CALL createInvestor('bobshoe@gmail.com', 'bobs789', 'Bob', 'Shoe');
CALL createInvestor('alicelee@gmail.com', 'alicelee246', 'Alice', 'Lee');
CALL createInvestor('davidkim@gmail.com', 'davidkim135', 'David', 'Kim');
SELECT * FROM Investor;


SELECT * FROM PORTFOLIO;
CALL createPortfolio(1, 'JohnDoePortfolio1');
CALL createPortfolio(1, 'JohnDoePortfolio2');
CALL createPortfolio(2, 'JaneDoePortfolio1');
CALL createPortfolio(3, 'BobSmithPortfolio1');
CALL createPortfolio(4, 'AmandaBrownPortfolio1');
CALL createPortfolio(4, 'AmandaBrownPortfolio2');
SELECT * FROM PORTFOLIO;

SELECT * FROM INVESTMENT;
CALL insertInvestment(1, 'APPL', 'STOCK', 50, '2023-04-11', 98, 3431, 8234);
CALL insertInvestment(2, 'APPL', 'STOCK', 20, '2023-04-11', 8,31411,8221);
CALL insertInvestment(2, 'GOOG', 'STOCK', 10, '2023-04-11', 698,3132,8264);
CALL insertInvestment(3, 'TSLA', 'STOCK', 15, '2023-04-11', 928,3142,8212);
CALL insertInvestment(4, 'JPMC', 'STOCK', 5, '2023-04-11', 981,314,8452);
CALL insertInvestment(5, 'RELI', 'STOCK', 40, '2023-04-11', 9348,3221,582);
CALL insertInvestment(5, 'TATA', 'STOCK', 60, '2023-04-11', 928,351,8);
SELECT * FROM INVESTMENT;

CALL updateNumberOfShares(1, 10);
CALL updateNumberOfShares(3, 5);
CALL updateNumberOfShares(4, 50);
SELECT * FROM investment;

CALL deleteInvestment(1);
SELECT * FROM investment;

-- CALL getTotalReturns(); This query will not work currently as our queries have only taken values at one date, and for performance metrics, we need multiple date data.
