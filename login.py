import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog
import mysql.connector
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import os
import math
from mysql.connector import Error
import statistics
cwd = os.getcwd()
os.chdir('/home/harsh/dbmsproj')

#Enter the password for root access to MySQL
root_password="password_for_root_access"

# Create a MySQL database connection
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password=root_password
)

# Create a cursor to execute SQL queries
mycursor = mydb.cursor()
mycursor.execute("SHOW DATABASES LIKE 'Portfolio'")
data=mycursor.fetchall()
if len(data)==0:
    with open ('database.sql','r') as sql_file:
        sql_script=sql_file.read()
        sql_commands=sql_script.split(';')
        for command in sql_commands:
            try:
                mycursor.execute(command)
            except Exception as e:
                print(f"An error occurred: {str(e)}")
    mydb.commit()
mycursor.close()
mydb.close()
# Create a function to handle login button click
def login():
    username = username_entry.get()
    password = password_entry.get()

    try:
        cnx = mysql.connector.connect(user='root', password=root_password,
                                  host='localhost', database='Portfolio')
        cursor = cnx.cursor()

        query = "SELECT * FROM Investor WHERE Email = %s AND Password = %s"
        cursor.execute(query, (username, password))
        result = cursor.fetchone()

        if result:
            # Login successful
            # ...
            investor_id = result[0] # Extract the investor_id from the result

            portfolio_management_window = tk.Toplevel(root)
            portfolio_management_window.title("Portfolio Management System")
            portfolio_management_window.geometry("800x600")

            # Create buttons for each functionality
            portfolio_button = tk.Button(portfolio_management_window, text="View Portfolio", command=lambda: view_portfolio(investor_id))
            portfolio_button.grid(row=0, column=0, pady=10)

            add_portfolio_button = tk.Button(portfolio_management_window, text="Add Portfolio", command=lambda: call_add_portfolio(investor_id))
            add_portfolio_button.grid(row=1, column=0, pady=10)

            add_investment_button = tk.Button(portfolio_management_window, text="Add Investment", command=lambda: call_add_investment(investor_id))
            add_investment_button.grid(row=2, column=0, pady=10)

            delete_investment_button = tk.Button(portfolio_management_window, text="Delete Investment", command=lambda: call_delete_investment(investor_id))
            delete_investment_button.grid(row=3, column=0, pady=10)

            update_shares_button = tk.Button(portfolio_management_window, text="Update number of shares", command=update_num_shares)
            update_shares_button.grid(row=0, column=1, pady=10)

            total_return_button = tk.Button(portfolio_management_window, text="Total return for each investment", command=get_investment_returns)
            total_return_button.grid(row=1, column=1, pady=10)

            stock_prices_button = tk.Button(portfolio_management_window, text="Retrieve Stock Prices by date", command=get_stock_prices)
            stock_prices_button.grid(row=2, column=1, pady=10)

            return_type_button = tk.Button(portfolio_management_window, text="Avg Annualized return by type", command=display_avg_annualized_returns)
            return_type_button.grid(row=3, column=1, pady=10)

            top_invest_button = tk.Button(portfolio_management_window, text="Top Performing Investments", command=display_top_performing_investments)
            top_invest_button.grid(row=0, column=2, pady=10)

            portfolio_value_button = tk.Button(portfolio_management_window, text="Portfolio Value", command=calculate_portfolio_value)
            portfolio_value_button.grid(row=1, column=2, pady=10)

            ann_return_button = tk.Button(portfolio_management_window, text="Portfolio Annualized Return", command=calculate_portfolio_annualized_return)
            ann_return_button.grid(row=2, column=2, pady=10)

            correlation_button = tk.Button(portfolio_management_window, text="Correlation Between Investments", command=calculate_correlation)
            correlation_button.grid(row=3, column=2, pady=10)

            inflation_rate_button = tk.Button(portfolio_management_window, text="Inflation Rate", command=get_inflation_rate)
            inflation_rate_button.grid(row=4, column=0, pady=10)

            performance_metrics_button = tk.Button(portfolio_management_window, text="View Performance Metrics", command=view_performance_metrics)
            performance_metrics_button.grid(row=4, column=1, pady=10)

            investment_opportunities_button = tk.Button(portfolio_management_window, text="View Investment Opportunities", command=view_opportunities)
            investment_opportunities_button.grid(row=4, column=2, pady=10)

            fin_info_button = tk.Button(portfolio_management_window, text="Fill Financial Information", command=fill_other_financial_info)
            fin_info_button.grid(row=5, column=0, pady=10)

            filter_button = tk.Button(portfolio_management_window, text="Filter Market Data", command=filter_market_data_by_date_and_investment)
            filter_button.grid(row=5, column=1, pady=10)

            sprice_change_button = tk.Button(portfolio_management_window, text="Calculate Stock Price Percentage Change", command=calculate_stock_price_percentage_change)
            sprice_change_button.grid(row=5, column=2, pady=10)

            volatility_button = tk.Button(portfolio_management_window, text="Calculate Volatility", command=calculate_volatility)
            volatility_button.grid(row=6, column=0, pady=10)

            top_button = tk.Button(portfolio_management_window, text="Top Performing Investments", command=top_performing_investments)
            top_button.grid(row=6, column=1, pady=10)

            group_button = tk.Button(portfolio_management_window, text="Group", command=group_by_type)
            group_button.grid(row=6, column=2, pady=10)


        else:
            # Login failed
            # ...
            error_label.config(text="Invalid email or password")


            # Ask if the user wants to sign up a new investor
            if messagebox.askyesno("Sign up", "Do you want to sign up as a new investor?"):
                portfolio_management_window = tk.Toplevel(root)
                portfolio_management_window.title("Portfolio Management System")
                portfolio_management_window.geometry("800x600")

                #Adding appropriate widgets for making entry for new Investor
                first_name_entry = tk.Entry(portfolio_management_window, width=30)
                last_name_entry = tk.Entry(portfolio_management_window, width=30)
                email_entry = tk.Entry(portfolio_management_window, width=30)
                first_name_label = tk.Label(portfolio_management_window, text="First name:")
                last_name_label = tk.Label(portfolio_management_window, text="Last name:")
                email_label = tk.Label(portfolio_management_window, text="Email:")

                # Place the Entry widgets in the window
                first_name_label.pack()
                first_name_entry.pack(pady=10)
                last_name_label.pack()
                last_name_entry.pack(pady=10)
                email_label.pack()
                email_entry.pack(pady=10)

                # Create a "Sign Up" button
                sign_up_button = tk.Button(portfolio_management_window, text="Sign Up",command=lambda:on_sign_up(first_name_entry,last_name_entry,email_entry))
                sign_up_button.pack(pady=10)
            else: 
                root.destroy()


    except mysql.connector.Error as err:
        print(err)

    finally:
        cursor.close()
        cnx.close()


def group_by_type():
    # Connect to the database
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password=root_password,
        database="Portfolio"
    )

    # Create a cursor object
    mycursor = mydb.cursor()

    # Execute the query to group investments by type and retrieve the total number of shares held for each type
    sql = "SELECT InvestmentType, SUM(NumShares) FROM Investment GROUP BY InvestmentType"
    mycursor.execute(sql)
    results = mycursor.fetchall()

    # Create a new window to display the result
    window = tk.Toplevel()
    window.title("Total Shares by Investment Type")

    # Create a label to display the result
    result_label = tk.Label(window, text="Total Shares by Investment Type:")
    result_label.pack()

    # Create a table to display the result
    table = tk.Frame(window)
    table.pack()

    # Create column headers for the table
    header1 = tk.Label(table, text="Investment Type", borderwidth=1, relief="solid")
    header1.grid(row=0, column=0, padx=5, pady=5)
    header2 = tk.Label(table, text="Total Shares", borderwidth=1, relief="solid")
    header2.grid(row=0, column=1, padx=5, pady=5)

    # Display the result in the table
    row = 1
    for investment_type, total_shares in results:
        type_label = tk.Label(table, text=investment_type, borderwidth=1, relief="solid")
        type_label.grid(row=row, column=0, padx=5, pady=5)
        shares_label = tk.Label(table, text=total_shares, borderwidth=1, relief="solid")
        shares_label.grid(row=row, column=1, padx=5, pady=5)
        row += 1

    # Close the database connection
    mydb.close()



def top_performing_investments():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password=root_password,
        database="Portfolio"
    )
    # create a new window for input/output
    top_investments_window = Tk()
    top_investments_window.title("Top Performing Investments")

    # create labels and entries for user input
    annualized_return_label = Label(top_investments_window, text="Minimum Annualized Return:")
    annualized_return_label.grid(row=0, column=0, padx=10, pady=10)
    annualized_return_entry = Entry(top_investments_window)
    annualized_return_entry.grid(row=0, column=1, padx=10, pady=10)

    risk_level_label = Label(top_investments_window, text="Maximum Risk Level:")
    risk_level_label.grid(row=1, column=0, padx=10, pady=10)
    risk_level_entry = Entry(top_investments_window)
    risk_level_entry.grid(row=1, column=1, padx=10, pady=10)

    # create a Listbox widget to display the results
    results_listbox = Listbox(top_investments_window, width=80)
    results_listbox.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    # create a function to retrieve the top performing investments
    def retrieve_top_investments():
        # retrieve the user input
        min_annualized_return = float(annualized_return_entry.get())
        max_risk_level = float(risk_level_entry.get())

        # retrieve the top performing investments from the database
        with connection.cursor() as cursor:
            sql = """
                SELECT InvestmentName, AnnualizedReturn, RiskLevel 
                FROM Investment i 
                JOIN Performance_Metrics pm ON i.InvestmentID = pm.InvestmentID 
                WHERE AnnualizedReturn >= %s AND RiskLevel <= %s 
                ORDER BY AnnualizedReturn DESC 
                LIMIT 10
            """
            cursor.execute(sql, (min_annualized_return, max_risk_level))
            results = cursor.fetchall()

        # display the results in the Listbox widget
        results_listbox.delete(0, END)
        for row in results:
            result_string = f"{row[0]}: Annualized Return={row[1]}, Risk Level={row[2]}"
            results_listbox.insert(END, result_string)

    # create a button to retrieve the top performing investments
    retrieve_button = Button(top_investments_window, text="Retrieve", command=retrieve_top_investments)
    retrieve_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    # run the main loop of the top_investments_window
    top_investments_window.mainloop()


def calculate_volatility():
    # Connect to the database
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password=root_password,
        database="Portfolio"
    )
    
    # Create the GUI window
    window = Tk()
    window.title("Calculate Volatility")
    
    # Add labels and input fields for user input
    investment_label = Label(window, text="Enter Investment Name:")
    investment_label.pack()
    investment_entry = Entry(window)
    investment_entry.pack()
    
    # Create a function to calculate the volatility and display the result
    def calculate():
        investment_name = investment_entry.get()
        
        # Execute SQL query to retrieve the investment ID
        cursor = mydb.cursor()
        query = f"SELECT InvestmentID FROM Investment WHERE InvestmentName = '{investment_name}'"
        cursor.execute(query)
        result = cursor.fetchone()
        if result is None:
            result_label.config(text="Investment not found.")
            return
        
        investment_id = result[0]
        
        # Execute SQL query to retrieve the performance metrics for the investment
        query = f"SELECT AnnualizedReturn FROM Performance_Metrics WHERE InvestmentID = {investment_id}"
        cursor.execute(query)
        results = cursor.fetchall()
        
        # Calculate the volatility of the investment's returns
        returns = []
        for r in results:
            returns.append(r[0])
        
        volatility = 0
        if len(returns) > 1:
            mean_return = sum(returns) / len(returns)
            deviations = [(r - mean_return)**2 for r in returns]
            variance = sum(deviations) / (len(returns) - 1)
            volatility = variance**0.5
        
        # Display the result
        result_label.config(text=f"Volatility: {volatility}")
    
    # Add a button to calculate the result
    calculate_button = Button(window, text="Calculate", command=calculate)
    calculate_button.pack()
    
    # Add a label to display the result
    result_label = Label(window)
    result_label.pack()
    
    # Run the GUI window
    window.mainloop()



def calculate_stock_price_percentage_change():
    # create a new window
    stock_price_window = tk.Toplevel()
    stock_price_window.title("Stock Price Percentage Change")

    # create a label and entry for investment ID
    investment_id_label = tk.Label(stock_price_window, text="Enter Investment ID:")
    investment_id_label.pack(pady=10)
    investment_id_entry = tk.Entry(stock_price_window)
    investment_id_entry.pack()

    # create labels and entries for date range
    start_date_label = tk.Label(stock_price_window, text="Enter start date (YYYY-MM-DD):")
    start_date_label.pack(pady=10)
    start_date_entry = tk.Entry(stock_price_window)
    start_date_entry.pack()
    end_date_label = tk.Label(stock_price_window, text="Enter end date (YYYY-MM-DD):")
    end_date_label.pack(pady=10)
    end_date_entry = tk.Entry(stock_price_window)
    end_date_entry.pack()

    # function to calculate the percentage change in stock price
    def calculate_percentage_change():
        # retrieve input values
        investment_id = investment_id_entry.get()
        start_date = start_date_entry.get()
        end_date = end_date_entry.get()

        # connect to database
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password=root_password,
            database="Portfolio"
        )

        # create cursor
        mycursor = mydb.cursor()

        # execute query to retrieve stock prices for investment between date range
        sql = "SELECT StockPrice FROM Market_Data WHERE InvestmentID = %s AND Date BETWEEN %s AND %s"
        val = (investment_id, start_date, end_date)
        mycursor.execute(sql, val)
        stock_prices = mycursor.fetchall()

        # calculate percentage change in stock price
        if len(stock_prices) >= 2:
            start_price = stock_prices[0][0]
            end_price = stock_prices[-1][0]
            percentage_change = ((end_price - start_price) / start_price) * 100
            result_label.config(text="Percentage Change: {:.2f}%".format(percentage_change))
        else:
            result_label.config(text="Not enough data to calculate percentage change")

        # close database connection
        mydb.close()

    # create button to calculate percentage change
    calculate_button = tk.Button(stock_price_window, text="Calculate", command=calculate_percentage_change)
    calculate_button.pack(pady=10)

    # create label to display result
    result_label = tk.Label(stock_price_window)
    result_label.pack(pady=10)



def filter_market_data_by_date_and_investment():
    # establish connection to database
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password=root_password,
        database="Portfolio"
    )
    cursor = db.cursor()

    # create GUI for input
    root = tk.Tk()
    root.title("Filter Market Data")
    root.geometry("400x300")

    investment_label = tk.Label(root, text="Investment Name:")
    investment_label.pack(pady=10)

    investment_entry = tk.Entry(root, width=30)
    investment_entry.pack()

    start_date_label = tk.Label(root, text="Start Date (YYYY-MM-DD):")
    start_date_label.pack(pady=10)

    start_date_entry = tk.Entry(root, width=30)
    start_date_entry.pack()

    end_date_label = tk.Label(root, text="End Date (YYYY-MM-DD):")
    end_date_label.pack(pady=10)

    end_date_entry = tk.Entry(root, width=30)
    end_date_entry.pack()

    def retrieve_stock_prices():
        # get user input
        investment_name = investment_entry.get()
        start_date = start_date_entry.get()
        end_date = end_date_entry.get()

        # query database to retrieve stock prices
        query = f"SELECT Date, StockPrice FROM Market_Data JOIN Investment ON Market_Data.InvestmentID = Investment.InvestmentID WHERE Investment.InvestmentName = '{investment_name}' AND Date BETWEEN '{start_date}' AND '{end_date}';"
        cursor.execute(query)
        stock_prices = cursor.fetchall()

        # display results in a new window
        results_window = tk.Toplevel(root)
        results_window.title("Stock Prices")
        results_window.geometry("400x300")

        results_label = tk.Label(results_window, text="Stock Prices:")
        results_label.pack(pady=10)

        for date, price in stock_prices:
            result = f"{date}: {price}"
            result_label = tk.Label(results_window, text=result)
            result_label.pack()

    retrieve_button = tk.Button(root, text="Retrieve Stock Prices", command=retrieve_stock_prices)
    retrieve_button.pack(pady=10)

    root.mainloop()

    # close database connection
    cursor.close()
    db.close()



def get_inflation_rate():
    # Connect to database
    cnx = mysql.connector.connect(user='root', password=root_password,
                                  host='localhost', database='Portfolio')
    cursor = cnx.cursor()

    # Create new tkinter window
    window = tk.Toplevel()
    window.title("Get Inflation Rate")

    # Execute query to retrieve most recent inflation rate
    query = "SELECT Inflation_Rate FROM Other_Financial_Information"
    cursor.execute(query)
    result = cursor.fetchone()

    # Create label to display inflation rate
    if result:
        inflation_rate = result[0]
        output_label = ttk.Label(window, text=f"Most recent inflation rate: {inflation_rate}")
        output_label.pack(padx=10, pady=10)
    else:
        output_label = ttk.Label(window, text="Error: No inflation rate found.")
        output_label.pack(padx=10, pady=10)

    # Run tkinter event loop
    window.mainloop()

    # Close database connection
    cursor.close()
    cnx.close()




def calculate_correlation():
    # Connect to database
    cnx = mysql.connector.connect(user='root', password=root_password,
                                  host='localhost', database='Portfolio')
    cursor = cnx.cursor()

    # Create new tkinter window
    window = tk.Tk()
    window.title("Calculate Correlation")

    # Create labels and entry boxes for input
    investment1_label = ttk.Label(window, text="Investment 1:")
    investment1_label.grid(row=0, column=0, padx=10, pady=10)
    investment1_entry = ttk.Entry(window)
    investment1_entry.grid(row=0, column=1, padx=10, pady=10)

    investment2_label = ttk.Label(window, text="Investment 2:")
    investment2_label.grid(row=1, column=0, padx=10, pady=10)
    investment2_entry = ttk.Entry(window)
    investment2_entry.grid(row=1, column=1, padx=10, pady=10)

    # Function to calculate correlation
    def calculate():
        # Retrieve input values
        investment1 = investment1_entry.get()
        investment2 = investment2_entry.get()

        # Execute query to retrieve performance metrics for investment 1
        query1 = f"""SELECT TotalReturn
                    FROM Investment i
                    JOIN Performance_Metrics p
                    ON i.InvestmentID = p.InvestmentID
                    WHERE i.InvestmentID = '{investment1}'"""
        cursor.execute(query1)
        results1 = cursor.fetchall()

        # Execute query to retrieve performance metrics for investment 2
        query2 = f"""SELECT TotalReturn
                    FROM Investment i
                    JOIN Performance_Metrics p
                    ON i.InvestmentID = p.InvestmentID
                    WHERE i.InvestmentID = '{investment2}'"""
        cursor.execute(query2)
        results2 = cursor.fetchall()

        # Calculate correlation coefficient
        if len(results1) > 1 and len(results2) > 1:
            x = [result[0] for result in results1]
            y = [result[0] for result in results2]
            n = len(x)

            sum_x = sum(x)
            sum_y = sum(y)
            sum_xy = sum([x[i]*y[i] for i in range(n)])
            sum_x_squared = sum([x[i]**2 for i in range(n)])
            sum_y_squared = sum([y[i]**2 for i in range(n)])

            r = (n * sum_xy - sum_x * sum_y) / ((n * sum_x_squared - sum_x ** 2) * (n * sum_y_squared - sum_y ** 2)) ** 0.5

            # Display output
            output_label.config(text=f"Correlation Coefficient: {r:.2f}")
        else:
            output_label.config(text="Error: Invalid Input")


    # Create button to calculate correlation
    calculate_button = ttk.Button(window, text="Calculate", command=calculate)
    calculate_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    # Create label for output
    output_label = ttk.Label(window, text="")
    output_label.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    # Run tkinter event loop
    window.mainloop()

    # Close database connection
    cursor.close()
    cnx.close()



def calculate_portfolio_annualized_return():
    # Connect to database
    cnx = mysql.connector.connect(user='root', password=root_password,
                                  host='localhost', database='Portfolio')
    cursor = cnx.cursor()

    # Create new tkinter window
    window = tk.Tk()
    window.title("Calculate Portfolio Annualized Return")

    # Create labels and entry widgets for input
    portfolio_id_label = ttk.Label(window, text="Portfolio ID:")
    portfolio_id_label.grid(column=0, row=0, padx=5, pady=5)

    portfolio_id_entry = ttk.Entry(window, width=10)
    portfolio_id_entry.grid(column=1, row=0, padx=5, pady=5)

    # Create function to calculate and display annualized return
    def calculate_and_display_annualized_return():
        # Get user input from entry widgets
        portfolio_id = portfolio_id_entry.get()

        # Execute query to retrieve portfolio's total return and value
        query = f"""SELECT SUM(i.NumShares * m.StockPrice * p.TotalReturn) / SUM(i.NumShares * m.StockPrice) AS portfolio_return
                    FROM Investment i
                    JOIN Performance_Metrics p
                    ON i.InvestmentID = p.InvestmentID
                    JOIN Market_Data m
                    ON i.InvestmentID = m.InvestmentID
                    WHERE i.PortfolioID = {portfolio_id}"""
        cursor.execute(query)
        portfolio_return = cursor.fetchone()[0]

        # Execute query to retrieve investment's average annualized return
        query = f"""SELECT AVG(p.AnnualizedReturn) AS avg_annualized_return
                    FROM Investment i
                    JOIN Performance_Metrics p
                    ON i.InvestmentID = p.InvestmentID
                    WHERE i.PortfolioID = {portfolio_id}"""
        cursor.execute(query)
        avg_annualized_return = cursor.fetchone()[0]

        # Calculate portfolio's overall annualized return
        portfolio_annualized_return = (1 + portfolio_return) * (1 + avg_annualized_return) - 1

        # Display result in a label widget
        result_label.config(text=f"Portfolio Annualized Return: {portfolio_annualized_return:.2%}")

    # Create button to calculate annualized return
    calculate_button = ttk.Button(window, text="Calculate", command=calculate_and_display_annualized_return)
    calculate_button.grid(column=0, row=1, columnspan=2, padx=5, pady=5)

    # Create label to display result
    result_label = ttk.Label(window, text="")
    result_label.grid(column=0, row=2, columnspan=2, padx=5, pady=5)

    # Run tkinter event loop
    window.mainloop()

    # Close database connection
    cursor.close()
    cnx.close()


def calculate_portfolio_value():
    # Connect to database
    cnx = mysql.connector.connect(user='root', password=root_password,
                                  host='localhost', database='Portfolio')
    cursor = cnx.cursor()

    # Create new tkinter window
    window = tk.Tk()
    window.title("Calculate Portfolio Value")

    # Create labels and entry boxes for user input
    portfolio_label = ttk.Label(window, text="Portfolio Name:")
    portfolio_label.grid(row=0, column=0, padx=10, pady=10)

    portfolio_entry = ttk.Entry(window)
    portfolio_entry.grid(row=0, column=1, padx=10, pady=10)

    date_label = ttk.Label(window, text="Date (YYYY-MM-DD):")
    date_label.grid(row=1, column=0, padx=10, pady=10)

    date_entry = ttk.Entry(window)
    date_entry.grid(row=1, column=1, padx=10, pady=10)

    # Function to calculate total value of investment
    def calculate_total_value():
        # Get user input
        portfolio_name = portfolio_entry.get()
        date = date_entry.get()

        # Execute query to get investments in portfolio
        query = f"""SELECT i.InvestmentName, i.NumShares, m.StockPrice
                    FROM Investment i
                    JOIN Market_Data m
                    ON i.InvestmentID = m.InvestmentID
                    JOIN Portfolio p
                    ON i.PortfolioID = p.PortfolioID
                    WHERE p.PortfolioName = '{portfolio_name}' AND m.Date = '{date}'"""
        cursor.execute(query)

        # Retrieve results
        results = cursor.fetchall()

        # Calculate total value
        total_value = sum(num_shares * stock_price for _, num_shares, stock_price in results)

        # Display total value
        total_value_label = ttk.Label(window, text=f"Total value: ${total_value:.2f}")
        total_value_label.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    # Create button to calculate total value
    calculate_button = ttk.Button(window, text="Calculate", command=calculate_total_value)
    calculate_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    # Run tkinter event loop
    window.mainloop()


def get_top_performing_investments(risk_level):
    # Connect to database
    cnx = mysql.connector.connect(user='root', password=root_password,
                                  host='localhost', database='Portfolio')
    cursor = cnx.cursor()

    # Execute query
    query = f"""SELECT i.InvestmentName, p.TotalReturn
                FROM Investment i
                JOIN Performance_Metrics p
                ON i.InvestmentID = p.InvestmentID
                WHERE p.RiskLevel <= {risk_level}
                ORDER BY p.TotalReturn DESC
                LIMIT 10"""
    cursor.execute(query)

    # Retrieve results
    results = cursor.fetchall()

    # Close database connection
    cursor.close()
    cnx.close()

    return results

def display_top_performing_investments():
    # Create new tkinter window
    window = tk.Tk()
    window.title("Top Performing Investments")

    # Create a label and entry box to get user input for risk level
    risk_label = ttk.Label(window, text="Enter risk level:")
    risk_label.pack(padx=10, pady=10)
    risk_entry = ttk.Entry(window)
    risk_entry.pack(padx=10, pady=10)

    # Create a button to trigger the query and display results
    button = ttk.Button(window, text="Search", command=lambda: display_results())
    button.pack(padx=10, pady=10)

    # Create table to display results
    table = ttk.Treeview(window, columns=("Investment Name", "Total Return"))
    table.heading("#0", text="Investment Type")
    table.heading("Investment Name", text="Investment Name")
    table.heading("Total Return", text="Total Return")

    def display_results():
        risk_level = float(risk_entry.get())
        results = get_top_performing_investments(risk_level)

        # Clear previous results from table
        for item in table.get_children():
            table.delete(item)

        # Add new rows to table
        for investment_name, total_return in results:
            investment_type = investment_name.split()[0]  # Get investment type from name
            table.insert("", "end", text=investment_type, values=(investment_name, total_return))

    # Pack and display table
    table.pack(padx=10, pady=10)

    # Run tkinter event loop
    window.mainloop()



def display_avg_annualized_returns():
    # Connect to database
    cnx = mysql.connector.connect(user='root', password=root_password,
                                  host='localhost', database='Portfolio')
    cursor = cnx.cursor()

    # Execute query
    query = """SELECT InvestmentType, AVG(AnnualizedReturn)
               FROM Investment i
               JOIN Performance_Metrics p
               ON i.InvestmentID = p.InvestmentID
               GROUP BY InvestmentType"""
    cursor.execute(query)

    # Retrieve results
    results = cursor.fetchall()

    # Close database connection
    cursor.close()
    cnx.close()

    # Create new window to display results
    new_window = tk.Toplevel()
    new_window.title("Average Annualized Returns by Investment Type")

    # Create table to display results
    table = tk.Frame(new_window, padx=10, pady=10)
    table.pack()

    # Add column headers
    headers = ['Investment Type', 'Average Annualized Return']
    for i, header in enumerate(headers):
        tk.Label(table, text=header, font='Helvetica 12 bold').grid(row=0, column=i, padx=5, pady=5)

    # Add data rows
    for i, result in enumerate(results):
        for j, data in enumerate(result):
            tk.Label(table, text=data, font='Helvetica 12').grid(row=i+1, column=j, padx=5, pady=5)

    # Add button to close window
    close_button = tk.Button(new_window, text="Close", command=new_window.destroy, font='Helvetica 12')
    close_button.pack(pady=10)


def get_stock_prices():
    # Create tkinter window
    window = tk.Tk()
    window.title("Get Stock Prices")
    window.geometry("400x200")

    # Create labels and entry boxes for user inputs
    investment_id_label = tk.Label(window, text="Investment ID:")
    investment_id_label.pack()
    investment_id_entry = tk.Entry(window)
    investment_id_entry.pack()

    date_label = tk.Label(window, text="Date (yyyy-mm-dd):")
    date_label.pack()
    date_entry = tk.Entry(window)
    date_entry.pack()

    # Function to retrieve stock prices from database and display on messagebox
    def retrieve_stock_prices():
        # Connect to database
        cnx = mysql.connector.connect(user='root', password=root_password,
                                       host='localhost', database='Portfolio')
        cursor = cnx.cursor()

        # Execute query
        query = f"""SELECT InvestmentName, StockPrice
                    FROM Investment i
                    JOIN Market_Data m ON i.InvestmentID = m.InvestmentID
                    WHERE i.InvestmentID = {investment_id_entry.get()}
                    AND m.Date = '{date_entry.get()}'"""
        cursor.execute(query)

        # Retrieve results
        results = cursor.fetchall()

        # Close database connection
        cursor.close()
        cnx.close()

        # Display results on messagebox
        if results:
            message = "Investment Name\tStock Price\n"
            for result in results:
                message += f"{result[0]}\t{result[1]}\n"
            messagebox.showinfo("Stock Prices", message)
        else:
            messagebox.showerror("Error", "No results found.")

    # Create button to retrieve stock prices
    retrieve_button = tk.Button(window, text="Retrieve Stock Prices",
                                command=retrieve_stock_prices)
    retrieve_button.pack()

    # Run tkinter window
    window.mainloop()



def fill_other_financial_info():

     # Connect to the database
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password=root_password,
        database="Portfolio"
    )
    cursor=db.cursor()
    # Create a new window
    other_financial_info_window = tk.Toplevel(root)
    other_financial_info_window.title("Other Financial Information")

    # Create input fields and labels
    date_label = tk.Label(other_financial_info_window, text="Date (YYYY-MM-DD):")
    date_label.grid(row=0, column=0)
    date_entry = tk.Entry(other_financial_info_window)
    date_entry.grid(row=0, column=1)

    interest_rate_label = tk.Label(other_financial_info_window, text="Interest Rate:")
    interest_rate_label.grid(row=1, column=0)
    interest_rate_entry = tk.Entry(other_financial_info_window)
    interest_rate_entry.grid(row=1, column=1)

    inflation_rate_label = tk.Label(other_financial_info_window, text="Inflation Rate:")
    inflation_rate_label.grid(row=2, column=0)
    inflation_rate_entry = tk.Entry(other_financial_info_window)
    inflation_rate_entry.grid(row=2, column=1)

    gdp_growth_rate_label = tk.Label(other_financial_info_window, text="GDP Growth Rate:")
    gdp_growth_rate_label.grid(row=3, column=0)
    gdp_growth_rate_entry = tk.Entry(other_financial_info_window)
    gdp_growth_rate_entry.grid(row=3, column=1)

    # Define function to save the input data to the database
    def save_other_financial_info():
        # Get the input values
        date = date_entry.get()
        interest_rate = interest_rate_entry.get()
        inflation_rate = inflation_rate_entry.get()
        gdp_growth_rate = gdp_growth_rate_entry.get()

        # Validate the input values
        if not date or not interest_rate or not inflation_rate or not gdp_growth_rate:
            messagebox.showerror("Error", "Please fill all the fields.")
            return

        try:
            # Convert the input values to their appropriate data types
            interest_rate = float(interest_rate)
            inflation_rate = float(inflation_rate)
            gdp_growth_rate = float(gdp_growth_rate)

            # Save the data to the database
            cursor.execute(
                "INSERT INTO Other_Financial_Information (Date, Interest_Rate, Inflation_Rate, GDP_Growth_Rate) VALUES (%s, %s, %s, %s)",
                (date, interest_rate, inflation_rate, gdp_growth_rate)
            )
            db.commit()

            # Show success message box
            messagebox.showinfo("Success", "Other Financial Information saved successfully.")

            # Close the window
            other_financial_info_window.destroy()
        except ValueError:
            messagebox.showerror("Error", "Please enter valid values for Interest Rate, Inflation Rate, and GDP Growth Rate.")

    # Create a button to save the input data
    save_button = tk.Button(other_financial_info_window, text="Save", command=save_other_financial_info)
    save_button.grid(row=4, column=1, pady=10)



def update_num_shares():
    # Connect to the database
    db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password=root_password,
        database="Portfolio"
    )

    # Create a new window
    update_window = Tk()
    update_window.title("Update Number of Shares")

    # Create labels and input fields for investment ID and new number of shares
    Label(update_window, text="Investment ID:").grid(row=0, column=0)
    investment_id_entry = Entry(update_window)
    investment_id_entry.grid(row=0, column=1)

    Label(update_window, text="New Number of Shares:").grid(row=1, column=0)
    num_shares_entry = Entry(update_window)
    num_shares_entry.grid(row=1, column=1)

    # Define a function to update the number of shares in the database
    def update():
        # Get the investment ID and new number of shares from the input fields
        investment_id = investment_id_entry.get()
        new_num_shares = num_shares_entry.get()

        # Update the number of shares in the database
        cursor = db_connection.cursor()
        query = "UPDATE Investment SET NumShares = %s WHERE InvestmentID = %s"
        values = (new_num_shares, investment_id)
        cursor.execute(query, values)
        db_connection.commit()

        # Close the update window
        update_window.destroy()

    # Create a button to update the number of shares
    update_button = Button(update_window, text="Update", command=update)
    update_button.grid(row=2, column=0, columnspan=2)

    # Run the window
    update_window.mainloop()


def add_portfolio(investor_id, portfolio_name):
    try:
        cnx = mysql.connector.connect(user='root', password=root_password,
                                  host='localhost', database='Portfolio')
        cursor = cnx.cursor()

        query = "INSERT INTO Portfolio (InvestorID, PortfolioName) VALUES (%s, %s)"
        data = (investor_id, portfolio_name)
        cursor.execute(query, data)
        cnx.commit()

        call_add_investment(investor_id)

        messagebox.showinfo("Success", "Portfolio added successfully!")
    except mysql.connector.Error as err:
        print(err)
        messagebox.showerror("Error", "Failed to add portfolio.")

    finally:
        cursor.close()
        cnx.close()
from tkinter import *

def call_add_market_data(investor_id,investment_id):
    # Get investment name and ID
    investment_names = get_investment_names(investor_id,investment_id)
    if not investment_names:
        messagebox.showerror("Error", "No investments found for the given investor.")
        return
    #investment_name = simpledialog.askstring("Investment Selection", "Enter the name of the investment:")
    #if investment_name not in investment_names:
    #    messagebox.showerror("Error", f"No investment found with name '{investment_name}'.")
    #    return
    #investment_id = get_investment_id(investor_id, investment_name)

    # Get market data
    date = simpledialog.askstring("Market Data", "Enter the date (YYYY-MM-DD):")
    stock_price = simpledialog.askfloat("Market Data", "Enter the stock price:")
    exchange_rate = simpledialog.askfloat("Market Data", "Enter the exchange rate:")
    commodity_price = simpledialog.askfloat("Market Data", "Enter the commodity price:")

    # Add market data to the table
    add_market_data(investment_id, date, stock_price, exchange_rate, commodity_price)
    messagebox.showinfo("Success", "Market data added successfully!")


def get_investment_names(investor_id, investment_id):
    try:
        cnx = mysql.connector.connect(user='root', password=root_password,
                                  host='localhost', database='Portfolio')
        cursor = cnx.cursor()

        query = "SELECT InvestmentName FROM Investment WHERE PortfolioID IN (SELECT PortfolioID FROM Portfolio WHERE InvestorID = %s) AND InvestmentID = %s"
        data = (investor_id, investment_id)
        cursor.execute(query, data)

        investment_names = [investment[0] for investment in cursor]
        return investment_names

    except mysql.connector.Error as err:
        print(err)
        return None

    finally:
        cursor.close()
        cnx.close()



def get_investment_id(portfolio_id, investment_name):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password=root_password,
        database="yourdatabase"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT InvestmentID FROM Investment WHERE PortfolioID = %s AND InvestmentName = %s",
                   (portfolio_id, investment_name))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result else None



def add_investment(investor_id,portfolio_id, investment_name, investment_type, num_shares):
    try:
        cnx = mysql.connector.connect(user='root', password=root_password,
                                  host='localhost', database='Portfolio')
        cursor = cnx.cursor()

        query = "INSERT INTO Investment (PortfolioID, InvestmentName, InvestmentType, NumShares) VALUES (%s, %s, %s, %s)"
        data = (portfolio_id, investment_name, investment_type, num_shares)
        cursor.execute(query, data)
        cnx.commit()

        # Retrieve the generated InvestmentID
        investment_id = cursor.lastrowid

        # Call call_add_market_data with the investment_id parameter
        call_add_market_data(investor_id,investment_id)
        calculate_performance_metrics(investment_id)

        messagebox.showinfo("Success", "Investment added successfully!")
    except mysql.connector.Error as err:
        print(err)
        messagebox.showerror("Error", "Failed to add investment.")

    finally:
        cursor.close()
        cnx.close()

def delete_investment(investor_id, investment_id):
    try:
        cnx = mysql.connector.connect(user='root', password=root_password,
                                  host='localhost', database='Portfolio')
        cursor = cnx.cursor()

        query = "DELETE FROM Investment WHERE InvestmentID=%s AND PortfolioID IN (SELECT PortfolioID FROM Portfolio WHERE InvestorID=%s);"
        data = (investment_id, investor_id)
        cursor.execute(query, data)
        cnx.commit()

        messagebox.showinfo("Success", "Investment deleted successfully!")
    except mysql.connector.Error as err:
        print(err)
        messagebox.showerror("Error", "Failed to delete investment.")

    finally:
        cursor.close()
        cnx.close()


def call_add_portfolio(investor_id):
    add_portfolio_window = tk.Toplevel(root)
    add_portfolio_window.title("Add Portfolio")
    add_portfolio_window.geometry("400x300")

    # Create labels and entry boxes for input
    portfolio_name_label = tk.Label(add_portfolio_window, text="Portfolio Name")
    portfolio_name_label.pack()
    portfolio_name_entry = tk.Entry(add_portfolio_window, width=30)
    portfolio_name_entry.pack(pady=10)

    # Create a button to submit the form
    submit_button = tk.Button(add_portfolio_window, text="Submit", command=lambda: add_portfolio(investor_id, portfolio_name_entry.get()))
    submit_button.pack(pady=10)

def call_add_investment(investor_id):
    add_investment_window = tk.Toplevel(root)
    add_investment_window.title("Add Investment")
    add_investment_window.geometry("400x400")

    # Create labels and entry boxes for input

    portfolio_name_label = tk.Label(add_investment_window, text="Portfolio ID")
    portfolio_name_label.pack()
    portfolio_id_entry = tk.Entry(add_investment_window, width=30)
    portfolio_id_entry.pack(pady=10)


    investment_name_label = tk.Label(add_investment_window, text="Investment Name")
    investment_name_label.pack()
    investment_name_entry = tk.Entry(add_investment_window, width=30)
    investment_name_entry.pack(pady=10)

    investment_type_label = tk.Label(add_investment_window, text="Investment Type")
    investment_type_label.pack()
    investment_type_entry = tk.Entry(add_investment_window, width=30)
    investment_type_entry.pack(pady=10)

    num_shares_label = tk.Label(add_investment_window, text="Number of Shares")
    num_shares_label.pack()
    num_shares_entry = tk.Entry(add_investment_window, width=30)
    num_shares_entry.pack(pady=10)

    # Create a button to submit the form
    submit_button = tk.Button(add_investment_window, text="Submit", command=lambda: add_investment(investor_id,portfolio_id_entry.get(), investment_name_entry.get(), investment_type_entry.get(), num_shares_entry.get()))
    submit_button.pack(pady=10)


def call_delete_investment(investor_id):
    delete_investment_window = tk.Toplevel(root)
    delete_investment_window.title("Delete Investment")
    delete_investment_window.geometry("400x400")

    # Create labels and entry boxes for input

    investment_id_label = tk.Label(delete_investment_window, text="Investment ID")
    investment_id_label.pack()
    investment_id_entry = tk.Entry(delete_investment_window, width=30)
    investment_id_entry.pack(pady=10)
    # Create a button to submit the form
    submit_button = tk.Button(delete_investment_window, text="Submit", command=lambda: delete_investment(investor_id,investment_id_entry.get()))
    submit_button.pack(pady=10)


def on_sign_up(first_name_entry, last_name_entry, email_entry):
    first_name = first_name_entry.get()
    last_name = last_name_entry.get()
    email = email_entry.get()
    password = password_entry.get()

    add_investor(first_name, last_name, email, password)

    messagebox.showinfo("Sign up", "You have been signed up as a new investor")


def view_opportunities():
    # Connect to database
    try:
        cnx = mysql.connector.connect(user='root', password=root_password,
                                  host='localhost', database='Portfolio')
        cursor = cnx.cursor()

        # Query to get all investment opportunities
        query = "SELECT * FROM Investment WHERE InvestmentType = 'Opportunity'"
        cursor.execute(query)
        result = cursor.fetchall()

        # Display the result in a new window
        opportunities_window = tk.Toplevel(root)
        opportunities_window.title("Investment Opportunities")
        opportunities_window.geometry("500x500")

        # Create a table to display the opportunities
        table = ttk.Treeview(opportunities_window, columns=('name', 'type', 'num_shares'), show='headings')
        table.heading('name', text='Name')
        table.heading('type', text='Type')
        table.heading('num_shares', text='Number of Shares')
        table.pack(padx=20, pady=20)

        # Insert each opportunity into the table
        for row in result:
            table.insert('', 'end', values=(row[2], row[3], row[4]))

    except mysql.connector.Error as err:
        print(err)

    finally:
        cursor.close()
        cnx.close()


def view_performance_metrics():
    # Create new window for displaying performance metrics
    performance_metrics_window = tk.Toplevel(root)
    performance_metrics_window.title("View Performance Metrics")

    # Create label and entry for investment ID
    investment_label = tk.Label(performance_metrics_window, text="Investment ID:")
    investment_label.grid(row=0, column=0, padx=5, pady=5)
    investment_entry = tk.Entry(performance_metrics_window)
    investment_entry.grid(row=0, column=1, padx=5, pady=5)

    # Create button to view performance metrics
    view_button = tk.Button(performance_metrics_window, text="View Performance Metrics",
                            command=lambda: display_performance_metrics(performance_metrics_window, investment_entry.get()))
    view_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

def display_performance_metrics(window, investment_id):
    # Retrieve performance metrics from database for specified investment ID
    try:
        cnx = mysql.connector.connect(user='root', password=root_password,
                                  host='localhost', database='Portfolio')
        cursor = cnx.cursor()

        query = "SELECT * FROM Performance_Metrics WHERE InvestmentID = %s"
        cursor.execute(query, (investment_id,))
        result = cursor.fetchone()

        if result:
            # Display performance metrics
            performance_metrics_label = tk.Label(window, text=f"Total Return: {result[1]}\n"
                                                              f"Annualized Return: {result[2]}\n"
                                                              f"Risk Level: {result[3]}")
            performance_metrics_label.grid(row=2, column=0, padx=5, pady=5)
        else:
            # Display error message if no performance metrics found for investment ID
            error_label = tk.Label(window, text="No performance metrics found for investment ID")
            error_label.grid(row=2, column=0, padx=5, pady=5)

    except mysql.connector.Error as err:
        print(err)

    finally:
        cursor.close()
        cnx.close()



def view_portfolio(investor_id):
    # Connect to the database
    cnx = mysql.connector.connect(user='root', password=root_password,
                                  host='localhost', database='Portfolio')
    cursor = cnx.cursor()

    # Retrieve the portfolio information
    query = "SELECT PortfolioName, InvestmentName, InvestmentType, NumShares, StockPrice, ExchangeRate, CommodityPrice FROM Portfolio JOIN Investment ON Portfolio.PortfolioID = Investment.PortfolioID JOIN Market_Data ON Investment.InvestmentID = Market_Data.InvestmentID WHERE InvestorID = %s"
    cursor.execute(query, (investor_id,))
    results = cursor.fetchall()

    # Create a new window to display the portfolio
    portfolio_window = tk.Toplevel(root)
    portfolio_window.title("Portfolio")

    # Create a table to display the portfolio data
    table = ttk.Treeview(portfolio_window)
    table["columns"] = ("1", "2", "3", "4", "5", "6", "7")
    table.column("#0", width=0, stretch=tk.NO)
    table.column("1", anchor=tk.W, width=100)
    table.column("2", anchor=tk.W, width=100)
    table.column("3", anchor=tk.W, width=100)
    table.column("4", anchor=tk.W, width=100)
    table.column("5", anchor=tk.W, width=100)
    table.column("6", anchor=tk.W, width=100)
    table.column("7", anchor=tk.W, width=100)
    table.heading("#0", text="", anchor=tk.W)
    table.heading("1", text="Portfolio Name", anchor=tk.W)
    table.heading("2", text="Investment Name", anchor=tk.W)
    table.heading("3", text="Investment Type", anchor=tk.W)
    table.heading("4", text="Num Shares", anchor=tk.W)
    table.heading("5", text="Stock Price", anchor=tk.W)
    table.heading("6", text="Exchange Rate", anchor=tk.W)
    table.heading("7", text="Commodity Price", anchor=tk.W)

    # Populate the table with the portfolio data
    for result in results:
        table.insert("", tk.END, text="", values=result)

    table.pack(expand=tk.YES, fill=tk.BOTH)

    # Close the database connection
    cursor.close()
    cnx.close()


def add_investor(first_name, last_name, email, password):
    try:
        cnx = mysql.connector.connect(user='root', password=root_password,
                                  host='localhost', database='Portfolio')
        cursor = cnx.cursor()

        query = "INSERT INTO Investor (FirstName, LastName, Email, Password) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (first_name, last_name, email, password))
        cnx.commit()

    except mysql.connector.Error as err:
        print(err)
        return False

    finally:
        cursor.close()
        cnx.close()

    return True


def add_market_data(investment_id, date, stock_price, exchange_rate, commodity_price):
    try:
        cnx = mysql.connector.connect(user='root', password=root_password,
                                  host='localhost', database='Portfolio')
        cursor = cnx.cursor()

        query = "INSERT INTO Market_Data (InvestmentID, Date, StockPrice, ExchangeRate, CommodityPrice) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (investment_id, date, stock_price, exchange_rate, commodity_price))
        cnx.commit()

    except mysql.connector.Error as err:
        print(err)
        return False

    finally:
        cursor.close()
        cnx.close()

    return True


def get_market_data(investment_id):
    try:
        conn = mysql.connector.connect(host='localhost',
                                       database='Portfolio',
                                       user='root',
                                       password=root_password)
        if conn.is_connected():
            cursor = conn.cursor(dictionary=True)
            cursor.execute(f"SELECT Date, StockPrice FROM Market_Data WHERE InvestmentID = {investment_id}")
            market_data_list = cursor.fetchall()
            return market_data_list
    except Error as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

def insert_performance_metrics(investment_id, total_return, annualized_return, risk_level):
    # Establish database connection
    conn = mysql.connector.connect(user="root", password=root_password, host="localhost", database="Portfolio")
    cursor = conn.cursor()

    # Insert performance metrics into table
    query = "INSERT INTO Performance_Metrics (InvestmentID, TotalReturn, AnnualizedReturn, RiskLevel) VALUES (%s, %s, %s, %s)"
    values = (investment_id, total_return, annualized_return, risk_level)
    cursor.execute(query, values)

    # Commit changes and close connection
    conn.commit()
    cursor.close()
    conn.close()


def calculate_performance_metrics(investment_id):
    # Get market data
    market_data_list = get_market_data(investment_id)
    if not market_data_list:
        print("No market data found for investment with ID:", investment_id)
        return

    # Create new window to get user input
    performance_window = tk.Toplevel()
    performance_window.title("Calculate Performance Metrics")

    # Create labels and entry boxes for user input
    tk.Label(performance_window, text="Enter initial investment value:").grid(row=0, column=0)
    initial_value_entry = tk.Entry(performance_window)
    initial_value_entry.grid(row=0, column=1)

    tk.Label(performance_window, text="Enter current investment value:").grid(row=1, column=0)
    current_value_entry = tk.Entry(performance_window)
    current_value_entry.grid(row=1, column=1)

    tk.Label(performance_window, text="Enter date of initial investment (YYYY-MM-DD):").grid(row=2, column=0)
    initial_date_entry = tk.Entry(performance_window)
    initial_date_entry.grid(row=2, column=1)

    tk.Label(performance_window, text="Enter date of current investment (YYYY-MM-DD):").grid(row=3, column=0)
    current_date_entry = tk.Entry(performance_window)
    current_date_entry.grid(row=3, column=1)

    # Function to calculate performance metrics using user input
    def calculate():
        # Get user input
        initial_value = float(initial_value_entry.get())
        current_value = float(current_value_entry.get())
        initial_date = datetime.strptime(initial_date_entry.get(), '%Y-%m-%d').date()
        current_date = datetime.strptime(current_date_entry.get(), '%Y-%m-%d').date()

        # Calculate total return
        total_return = (current_value - initial_value) / initial_value

        # Calculate annualized return
        days_held = (current_date - initial_date).days
        years_held = days_held / 365
        annualized_return = ((1 + total_return) ** (1 / years_held)) - 1

        # Calculate standard deviation of returns
         # Calculate risk level
        returns = []
        for i in range(1, len(market_data_list)):
            returns.append((market_data_list[i]["StockPrice"] - market_data_list[i-1]["StockPrice"]) / market_data_list[i-1]["StockPrice"])
        
        if len(returns) < 2:
            returns_std = 0
        else:
            returns_std = statistics.stdev(returns)

        
        risk_level = returns_std * (years_held ** 0.5)

        # Create labels to display results
        total_return_label = tk.Label(performance_window, text=f"Total Return: {total_return}")
        total_return_label.grid(row=4, column=0)
        annualized_return_label = tk.Label(performance_window, text=f"Annualized Return: {annualized_return}")
        annualized_return_label.grid(row=5, column=0)
        risk_level_label = tk.Label(performance_window, text=f"Risk Level: {risk_level}")
        risk_level_label.grid(row=6, column=0)

        # Insert results into Performance_Metrics table
        insert_performance_metrics(investment_id,total_return, annualized_return, risk_level) 

    # Create button to calculate performance metrics
    calculate_button = tk.Button(performance_window, text="Calculate", command=calculate)
    calculate_button.grid(row=4, column=1)
    # Start mainloop to display window and wait for user input
    performance_window.mainloop()

def get_investment_returns():
    # Connect to database
    cnx = mysql.connector.connect(user='root', password=root_password,
                                  host='localhost', database='Portfolio')
    cursor = cnx.cursor()

    # Execute query
    query = """SELECT i.InvestmentID, i.InvestmentName, p.TotalReturn
               FROM Investment i
               JOIN Performance_Metrics p
               ON i.InvestmentID = p.InvestmentID"""
    cursor.execute(query)

    # Retrieve results
    results = cursor.fetchall()

    # Close database connection
    cursor.close()
    cnx.close()

    # Create new window to display results
    window = tk.Toplevel()
    window.title("Investment Returns")
    window.geometry("400x200")

    # Create treeview to display results
    tree = ttk.Treeview(window, columns=("Investment ID", "Investment Name", "Total Return"))
    tree.heading("Investment ID", text="Investment ID")
    tree.heading("Investment Name", text="Investment Name")
    tree.heading("Total Return", text="Total Return")

    for row in results:
        tree.insert("", "end", values=row)

    tree.pack()

    window.mainloop()



root = tk.Tk()
root.title("Portfolio Management System")
root.geometry("400x200")  # increased the size of the window

# create labels and entry boxes for email and password
username_label = tk.Label(root, text="Email:")
username_label.grid(row=0, column=0)

username_entry = tk.Entry(root)
username_entry.grid(row=0, column=1)

password_label = tk.Label(root, text="Password:")
password_label.grid(row=1, column=0)

password_entry = tk.Entry(root, show="*")
password_entry.grid(row=1, column=1)

error_label = tk.Label(root, fg="red")
error_label.grid(row=2, column=0, columnspan=2)

# create login button
login_button = tk.Button(root, text="Login", command=login)
login_button.grid(row=3, column=0, columnspan=2)

root.mainloop()