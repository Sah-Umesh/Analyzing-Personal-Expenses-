import streamlit as st
import pandas as pd
st.title("Epenses Tracker")

import mysql.connector

connection = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,  
    user="root",
    password="root",
    database="exp_track_db"
)


cursor = connection.cursor()

with st.sidebar:

                options = st.selectbox("Queries",[
"1.What is the total amount spent in each category?",
"2.What is the total amount spent using each payment mode?",
"3.What is the total cashback received across all transactions?",
"4.Which are the top 5 most expensive categories in terms of spending?",
"5.How much was spent on transportation using different payment modes?",
"6. Which transactions resulted in cashback?",
"7.What is the total spending in each month of the year?",
"8.Which months have the highest spending in categories like 'Transport', 'Subscriptions', 'Bills'?",
"9.Are there any recurring expenses that occur during specific months of the year (e.g., insurance premiums, property taxes)?",
"10.How much cashback or rewards were earned in each month?",
"11.How has your overall spending changed over time (e.g., increasing, decreasing, remaining stable)?",
"12.What are the typical costs associated with different types of travel (e.g., flights, accommodation, transportation)?",
"13.Are there any patterns in grocery spending (e.g., higher spending on weekends, increased spending during specific seasons)?",
"14.Define High and Low Priority Categories",
"15.Which category contributes the highest percentage of the total spending?"
               ], placeholder='Select an option...', index=None)
                

if options == "1.What is the total amount spent in each category?":
                        cursor.execute('select Category, SUM(Amount) AS total_amount_spent from exp_track_db.exp_table group by Category')

                        result = cursor.fetchall()

                        columns = [desc[0] for desc in cursor.description]

                        data = pd.DataFrame(result,columns=columns)

                        st.dataframe(data) 

elif options == "2.What is the total amount spent using each payment mode?":
                        cursor.execute("select PaymentMode ,SUM(Amount) AS total_amount_spent from exp_track_db.exp_table group by PaymentMode")
                        result = cursor.fetchall()

                        columns = [desc[0] for desc in cursor.description]

                        data = pd.DataFrame(result,columns=columns)

                        st.dataframe(data) 
elif options == "3.What is the total cashback received across all transactions?":
                        cursor.execute("select SUM(Cashback) AS total_cashback_received from exp_track_db.exp_table")
                        result = cursor.fetchall()

                        columns = [desc[0] for desc in cursor.description]

                        data = pd.DataFrame(result,columns=columns)

                        st.dataframe(data) 
elif options == "4.Which are the top 5 most expensive categories in terms of spending?":
                        cursor.execute("SELECT Category, SUM(amount) AS total_spent FROM exp_track_db.exp_table GROUP BY Category ORDER BY total_spent DESC LIMIT 5;")
                        result = cursor.fetchall()

                        columns = [desc[0] for desc in cursor.description]

                        data = pd.DataFrame(result,columns=columns)

                        st.dataframe(data) 
elif options == "5.How much was spent on transportation using different payment modes?":
                        cursor.execute("SELECT PaymentMode, SUM(amount) AS total_spent_Transport FROM exp_track_db.exp_table where Category='Transport' group by PaymentMode")
                        result = cursor.fetchall()

                        columns = [desc[0] for desc in cursor.description]

                        data = pd.DataFrame(result,columns=columns)

                        st.dataframe(data) 

elif options == "6. Which transactions resulted in cashback?":
                        cursor.execute("SELECT * FROM exp_track_db.exp_table WHERE  Cashback> 0;")
                        result = cursor.fetchall()

                        columns = [desc[0] for desc in cursor.description]

                        data = pd.DataFrame(result,columns=columns)

                        st.dataframe(data) 

elif options == "7.What is the total spending in each month of the year?":
                        cursor.execute("SELECT MONTHNAME(Date) AS MonthName, SUM(Amount) AS TotalSpending FROM exp_track_db.exp_table WHERE YEAR(Date) = 2024 GROUP BY MONTH(Date), MONTHNAME(Date) ORDER BY MONTH(Date);")
                        result = cursor.fetchall()

                        columns = [desc[0] for desc in cursor.description]

                        data = pd.DataFrame(result,columns=columns)

                        st.dataframe(data) 

elif options == "8.Which months have the highest spending in categories like 'Transport', 'Subscriptions', 'Bills'?":
                        cursor.execute("SELECT MONTHNAME(Date) AS Month, Category, SUM(Amount) AS Total FROM exp_track_db.exp_table WHERE YEAR(Date) = 2024 AND Category IN ('Transport', 'Subscriptions', 'Bills') GROUP BY MONTHNAME(Date), Category")
                        result = cursor.fetchall()

                        columns = [desc[0] for desc in cursor.description]

                        data = pd.DataFrame(result,columns=columns)

                        st.dataframe(data) 

elif options == "9.Are there any recurring expenses that occur during specific months of the year (e.g., insurance premiums, property taxes)?":
                        cursor.execute("SELECT Category, MONTHNAME(Date) AS Month, COUNT(*) AS Count FROM exp_table GROUP BY Category, MONTH(Date), MONTHNAME(Date) HAVING COUNT(*) > 20 ORDER BY COUNT(*) DESC")
                        result = cursor.fetchall()

                        columns = [desc[0] for desc in cursor.description]

                        data = pd.DataFrame(result,columns=columns)

                        st.dataframe(data) 

elif options == "10.How much cashback or rewards were earned in each month?":
                        cursor.execute("SELECT MONTHNAME(Date) AS month, SUM(Cashback) AS CashbackEarned FROM exp_table WHERE Cashback > 0 GROUP BY MONTH(Date),MONTHNAME(Date) ORDER BY MONTH(Date)")
                        result = cursor.fetchall()

                        columns = [desc[0] for desc in cursor.description]

                        data = pd.DataFrame(result,columns=columns)

                        st.dataframe(data) 

elif options == "11.How has your overall spending changed over time (e.g., increasing, decreasing, remaining stable)?":
                        cursor.execute("SELECT DATE_FORMAT(date, '%Y-%m') AS month, SUM(Amount) AS total_spending, ROUND((SUM(Amount) - LAG(SUM(Amount), 1) OVER (ORDER BY DATE_FORMAT(date, '%Y-%m'))) / LAG(SUM(Amount), 1) OVER (ORDER BY DATE_FORMAT(date, '%Y-%m')) * 100, 2) AS monthly_change_percentage, category FROM exp_track_db.exp_table WHERE Category IN ('Groceries', 'Transport', 'Subscriptions', 'Bills', 'Shopping', 'Medicine', 'Entertainment') GROUP BY DATE_FORMAT(date, '%Y-%m'), Category ORDER BY month, total_spending DESC;")
                        result = cursor.fetchall()

                        columns = [desc[0] for desc in cursor.description]

                        data = pd.DataFrame(result,columns=columns)

                        st.dataframe(data) 

elif options == "12.What are the typical costs associated with different types of Transports? (e.g., flights, accommodation, transportation)?":
                        cursor.execute("SELECT CASE WHEN description LIKE '%taxi ride to%' THEN 'Taxi' WHEN description LIKE '%bus fare to%' THEN 'Bus' WHEN description LIKE '%fuel at%' THEN 'Fuel' WHEN description LIKE '%train ticket to%' THEN 'Train' WHEN description LIKE '%ride-sharing to%' THEN 'Ride-Sharing' ELSE 'Other Transport' END AS transport_type, COUNT(*) AS number_of_transactions, AVG(Amount) AS average_cost, MIN(Amount) AS min_cost, MAX(Amount) AS max_cost, SUM(Amount) AS total_spent FROM exp_track_db.exp_table WHERE Category = 'Transport' OR description LIKE '%taxi ride to%'OR description LIKE '%bus fare to%'OR description LIKE '%fuel at%'OR description LIKE '%train ticket to%'OR description LIKE '%ride-sharing to%' GROUP BY transport_type ORDER BY total_spent DESC;")
                        result = cursor.fetchall()

                        columns = [desc[0] for desc in cursor.description]

                        data = pd.DataFrame(result,columns=columns)

                        st.dataframe(data) 

elif options == "13.Are there any patterns in grocery spending (e.g., higher spending on weekends, increased spending during specific seasons)?":
                        cursor.execute("SELECT MONTHNAME(Date) AS month, AVG(Amount) AS avg_spending, SUM(Amount) AS total_spending, COUNT(*) AS transaction_count FROM exp_track_db.exp_table WHERE category = 'Groceries' GROUP BY Date ORDER BY MONTH(date);")
                        result = cursor.fetchall()

                        columns = [desc[0] for desc in cursor.description]

                        data = pd.DataFrame(result,columns=columns)

                        st.dataframe(data) 

elif options == "14.Define High and Low Priority Categories":
                        cursor.execute("WITH category_stats AS (SELECT Category,SUM(Amount) AS total_spent,COUNT(*) AS frequency,(SUM(Amount) / (SELECT SUM(Amount) FROM exp_track_db.exp_table)) * 100 AS percentage FROM exp_track_db.exp_table GROUP BY Category)SELECT Category,total_spent,frequency,percentage,CASE WHEN percentage > 14 THEN 'High Priority' WHEN percentage BETWEEN 13 AND 14 THEN 'Medium Priority'ELSE 'Low Priority' END AS spending_priority FROM category_stats ORDER BY total_spent DESC;")
                        result = cursor.fetchall()

                        columns = [desc[0] for desc in cursor.description]

                        data = pd.DataFrame(result,columns=columns)

                        st.dataframe(data) 

elif options == "15.Which category contributes the highest percentage of the total spending?":
                        cursor.execute("SELECT Category,SUM(amount) AS category_total,(SUM(Amount)/(SELECT SUM(Amount) FROM exp_track_db.exp_table))*100 AS percentage FROM exp_track_db.exp_table GROUP BY Category ORDER BY percentage DESC LIMIT 1;")
                        result = cursor.fetchall()

                        columns = [desc[0] for desc in cursor.description]

                        data = pd.DataFrame(result,columns=columns)

                        st.dataframe(data) 


