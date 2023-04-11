DROP DATABASE IF EXISTS Portfolio;
CREATE DATABASE Portfolio;
USE Portfolio;
CREATE TABLE Investor (
  InvestorID INT PRIMARY KEY AUTO_INCREMENT,
  MyPassword VARCHAR(50),
  FirstName VARCHAR(50),
  LastName VARCHAR(50),
  Email VARCHAR(50)
);
CREATE TABLE Portfolio (
  PortfolioID INT PRIMARY KEY AUTO_INCREMENT,
  InvestorID INT,
  PortfolioName VARCHAR(50),
  FOREIGN KEY (InvestorID) REFERENCES Investor(InvestorID) ON DELETE CASCADE
);
CREATE TABLE Investment (
  InvestmentID INT PRIMARY KEY AUTO_INCREMENT,
  PortfolioID INT,
  InvestmentName VARCHAR(50),
  InvestmentType VARCHAR(50),
  NumShares INT,
  FOREIGN KEY (PortfolioID) REFERENCES Portfolio(PortfolioID) ON DELETE CASCADE
);
CREATE TABLE Market_Data (
  MarketDataID INT PRIMARY KEY AUTO_INCREMENT,
  InvestmentID INT,
  InvDate DATE,
  StockPrice FLOAT,
  ExchangeRate FLOAT,
  CommodityPrice FLOAT,
  FOREIGN KEY (InvestmentID) REFERENCES Investment(InvestmentID) ON DELETE CASCADE
);
CREATE TABLE Performance_Metrics (
  PerformanceMetricsID INT PRIMARY KEY AUTO_INCREMENT,
  InvestmentID INT,
  TotalReturn FLOAT,
  AnnualizedReturn FLOAT,
  RiskLevel FLOAT,
  FOREIGN KEY (InvestmentID) REFERENCES Investment(InvestmentID) ON DELETE CASCADE
);
CREATE TABLE Other_Financial_Information (
	InvDate DATE PRIMARY KEY,
    Interest_Rate FLOAT,
    Inflation_Rate FLOAT,
    GDP_Growth_Rate FLOAT
);
INSERT INTO Investor (MyPassword, FirstName, LastName, Email)
VALUES 
("mypassword1", "John", "Doe", "johndoe@example.com"),
("mypassword2", "Jane", "Smith", "janesmith@example.com"),
("mypassword3", "Bob", "Johnson", "bobjohnson@example.com"),
("mypassword4", "Alice", "Williams", "alicewilliams@example.com"),
("mypassword5", "David", "Brown", "davidbrown@example.com"),
("mypassword6", "Amy", "Taylor", "amytaylor@example.com"),
("mypassword7", "Mark", "Davis", "markdavis@example.com"),
("mypassword8", "Emily", "Jackson", "emilyjackson@example.com"),
("mypassword9", "Tom", "Lee", "tomlee@example.com"),
("mypassword10", "Karen", "Wilson", "karenwilson@example.com");
INSERT INTO Portfolio (InvestorID, PortfolioName)
VALUES 
(1, "Tech Stocks"),
(2, "Real Estate"),
(3, "Commodities"),
(4, "Foreign Exchange"),
(5, "Mutual Funds"),
(6, "Bonds"),
(7, "Options"),
(8, "Cryptocurrencies"),
(9, "Index Funds"),
(10, "Blue Chip Stocks");
INSERT INTO Investment (PortfolioID, InvestmentName, InvestmentType, NumShares)
VALUES 
(1, "Apple Inc.", "Stocks", 100),
(1, "Microsoft Corporation", "Stocks", 50),
(2, "Apartment Complex", "Real Estate", 1),
(3, "Gold", "Commodities", 10),
(3, "Crude Oil", "Commodities", 5),
(4, "Euro/US Dollar", "Forex", 1000),
(5, "Fidelity Blue Chip Growth Fund", "Mutual Funds", 100),
(6, "10-Year Treasury Note", "Bonds", 5),
(7, "Call Option on Tesla Inc.", "Options", 1),
(8, "Bitcoin", "Cryptocurrencies", 0.5),
(9, "Vanguard S&P 500 ETF", "Index Funds", 50),
(10, "Johnson & Johnson", "Stocks", 25);
INSERT INTO Market_Data (InvestmentID, InvDate, StockPrice, ExchangeRate, CommodityPrice)
VALUES 
(1, "2022-01-01", 180.32, 1.23, NULL),
(1, "2022-01-02", 185.17, 1.25, NULL),
(1, "2022-01-03", 182.34, 1.24, NULL),
(2, "2022-01-01", 334.66, 0.85, NULL),
(2, "2022-01-02", 337.52, 0.86, NULL),
(2, "2022-01-03", 335.14, 0.87, NULL),
(3, "2022-01-01", NULL, 1.05, 1700.25),
(3, "2022-01-02", NULL, 1.06, 1695.75),
(3, "2022-01-03", NULL, 1.04, 1698.50),
(4, "2022-01-01", NULL, 0.77, NULL),
(4, "2022-01-02", NULL, 0.76, NULL),
(4, "2022-01-03", NULL, 0.78, NULL),
(5, "2022-01-01", 120.25, NULL, NULL),
(5, "2022-01-02", 121.50, NULL, NULL),
(5, "2022-01-03", 119.75, NULL, NULL),
(6, "2022-01-01", NULL, NULL, NULL),
(6, "2022-01-02", NULL, NULL, NULL),
(6, "2022-01-03", NULL, NULL, NULL),
(7, "2022-01-01", NULL, NULL, NULL),
(7, "2022-01-02", NULL, NULL, NULL),
(7, "2022-01-03", NULL, NULL, NULL),
(8, "2022-01-01", 35000.00, NULL, NULL),
(8, "2022-01-02", 36000.00, NULL, NULL),
(8, "2022-01-03", 36500.00, NULL, NULL),
(9, "2022-01-01", 500.00, NULL, NULL),
(9, "2022-01-02", 495.00, NULL, NULL),
(9, "2022-01-03", 510.00, NULL, NULL),
(10, "2022-01-01", 157.24, NULL, NULL),
(10, "2022-01-02", 159.63, NULL, NULL),
(10, "2022-01-03", 160.01, NULL, NULL);
INSERT INTO Performance_Metrics (InvestmentID, TotalReturn, AnnualizedReturn, RiskLevel)
VALUES 
(1, 12.54, 20.18, 1.23),
(2, 7.32, 11.87, 0.85),
(3, 6.78, 10.98, 0.92),
(4, -2.10, -3.41, 1.14),
(5, 4.25, 6.89, 0.75),
(6, NULL, NULL, NULL),
(7, NULL, NULL, NULL),
(8, 9.63, 15.59, 0.96),
(9, 2.10, 3.41, 1.05),
(10, 8.50, 13.76, 1.28);
INSERT INTO Other_Financial_Information (InvDate, Interest_Rate, Inflation_Rate, GDP_Growth_Rate)
VALUES 
("2022-01-01", 3.5, 2.1, 4.5),
("2022-02-01", 3.6, 2.2, 4.8),
("2022-03-01", 3.4, 2.4, 4.6),
("2022-04-01", 3.3, 2.5, 4.3),
("2022-05-01", 3.4, 2.6, 4.1),
("2022-06-01", 3.2, 2.7, 4.2),
("2022-07-01", 3.1, 2.8, 4.0),
("2022-08-01", 3.0, 2.9, 3.9),
("2022-09-01", 3.2, 2.5, 4.2),
("2022-10-01", 3.1, 2.6, 4.0);
