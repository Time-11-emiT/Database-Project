DROP DATABASE IF EXISTS Portfolio;
CREATE DATABASE Portfolio;
USE Portfolio;
CREATE TABLE Investor (
  InvestorID INT PRIMARY KEY AUTO_INCREMENT,
  Password VARCHAR(50),
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
  Date DATE,
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
	Date DATE PRIMARY KEY,
    Interest_Rate FLOAT,
    Inflation_Rate FLOAT,
    GDP_Growth_Rate FLOAT
);