
CALL insertInvestment(1,'Lakshit', 'Sethi', 'lakshit@gmai.com','Sethi', 1, 'laks', 'APPL', 'Stock', 10, '2023-04-10', 35.52, 10.05, 7262.92,689,38,292);
CALL insertInvestment(2, 'John', 'Doe', 'john.doe@gmail.com', 'Doe', 2, 'jdoe', 'MSFT', 'Stock', 15, '2023-04-10', 285.05, 8.23, 42814.77, 1201, 62, 357);
CALL updateNumberOfShares(1, 50);
CALL DeleteInvestment(1);
CALL getTotalReturns();
CALL getStockPrices('2023-04-10');
CALL getAverageAnnualizedReturn();
CALL filterByRiskLevel();
CALL findTotalValueOfAllInvestments();
CALL findOverallAnnualizedReturns();
CALL getInflationRate();
CALL filterStockPrice(1,'2023-04-01','2023-05-01');
CALL calculateVolatility(1);
call getTopPerformingStocks();
