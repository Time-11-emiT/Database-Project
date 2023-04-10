
CALL insertInvestment(1,'Lakshit', 'Sethi', 'lakshit@gmai.com','Sethi', 1, 'laks', 'APPL', 'Stock', 10, '2023-04-10', 35.52, 10.05, 7262.92,689,38,292);
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
