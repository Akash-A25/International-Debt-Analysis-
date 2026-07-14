import pandas as pd
import streamlit as st
from sqlalchemy import create_engine,text

#---------- db connection--------------
host = "localhost"
port = "5432"  
database = "inter"
username = "postgres"
password = "123AKA123"

# Create the connection string (URL format) -> postgres
engine = f"postgresql://{username}:{password}@{host}:{port}/{database}"
engine = create_engine(engine)

#--------quer page--------
st.header("International Debit Analysis")
queries ={
    "All Country Names":"SELECT DISTINCT \"Country Name\" FROM \"ALLCountries_Data\";",
    " Total Number of Countries" :"SELECT COUNT(DISTINCT \"Country Name\") FROM \"ALLCountries_Data\";",
     "Total Number of Indicators Present" : "SELECT COUNT(DISTINCT \"Series Name\") FROM \"ALLCountries_Data\" ;",
     " First 10 Records" : "SELECT * FROM \"ALLCountries_Data\" LIMIT 10 ;",
     "The Total Global Debt" :"SELECT SUM(\"Value\") AS total_global_debt From \"ALLCountries_Data\"; ",
     "Unique Indicator Names" :"SELECT DISTINCT \"Series Name\"  FROM \"ALLCountries_Data\" ; ",
     "The Number of Records for Each Country" :"SELECT  \"Country Name\",COUNT(*) record_count  FROM \"ALLCountries_Data\" GROUP BY \"Country Name\";",
     "All Records Where Debt is Greater Than 1 Billion USD" : "SELECT * FROM \"ALLCountries_Data\" WHERE \"Value\" >1000000000;",
     " The Minimum,Maximum,and Average Debt Values " : "SELECT MIN(\"Value\") AS min_debt,MAX(\"Value\") AS max_debt,AVG(\"Value\") AS "
                                                       "avg_debt FROM \"ALLCountries_Data\";",
     " Total Number of Records" :"SELECT COUNT(*) FROM \"ALLCountries_Data\";",
     " The Total Debt for Each Country" :"SELECT \"Country Name\",SUM(\"Value\") AS total_debit FROM"
                                           "\"ALLCountries_Data\" GROUP BY \"Country Name\";",
     " Top 10 Countries With The Highest Total Debt" : "SELECT \"Country Name\", SUM(\"Value\") AS total_debt FROM \"ALLCountries_Data\" "
     "GROUP BY \"Country Name\" ORDER BY total_debt DESC LIMIT 10; ",
     "The Average Debt Per Country" : "SELECT \"Country Name\" ,AVG(\"Value\") AS agv_debt FROM \"ALLCountries_Data\" GROUP BY \"Country Name\" ",
     " Total Debt For Each Indicator" :"SELECT \"Series Name\" AS series_name,SUM(\"Value\") AS total_debit FROM \"ALLCountries_Data\" "
                                        "GROUP BY  \"Series Name\"; ",
     "The Indicator Contributing The Highest Total Debt" :"SELECT \"Series Name\",SUM(\"Value\") AS total_debt FROM \"ALLCountries_Data\""
                                                          " GROUP BY \"Series Name\" ORDER BY total_debt DESC LIMIT 10 ;",
     "Country With The Lowest Total Deb" :"SELECT \"Country Name\",SUM(\"Value\") AS total_debt FROM \"ALLCountries_Data\" GROUP BY \"Country Name\""
                                           " ORDER BY total_debt ASC LIMIT 10; ",
     "Total Debt For Each Country And Indicator Combination":"SELECT \"Country Name\",\"Series Name\",SUM(\"Value\")"
                                                              " AS total_debt FROM \"ALLCountries_Data\" GROUP BY \"Country Name\",\"Series Name\";",
     "How Many Indicators Each Country Has" : "SELECT \"Country Name\",COUNT(DISTINCT \"Series Name\") AS series_count"
                                              " FROM \"ALLCountries_Data\" GROUP BY \"Country Name\"; ",
     "Countries Whose Total Debt is Above The Global Average":"SELECT \"Country Name\",SUM(\"Value\") AS total_debt FROM"
                                                               "  \"ALLCountries_Data\" GROUP BY \"Country Name\" HAVING SUM(\"Value\")>(SELECT AVG(\"Value\") FROM \"ALLCountries_Data\");",
     "Rank countries based on total_debt (highest to lowest)" :"SELECT \"Country Name\",SUM(\"Value\") AS total_debt,RANK() OVER (ORDER BY"
                                                                " SUM(\"Value\") DESC ) AS debt_rank FROM \"ALLCountries_Data\" GROUP BY \"Country Name\" ; ",
     "  The Top 5 Indicators Contributing Most to Global Debt" :"SELECT \"Series Name\",SUM(\"Value\") AS total_debt FROM \"ALLCountries_Data\""
                                                                 " GROUP BY \"Series Name\" ORDER BY total_debt DESC LIMIT 5;",
     "Percentage Contribution of Each Country to Total Global Debt" :"SELECT \"Country Name\", SUM(\"Value\") AS country_debt,"
                                                                     "( SUM(\"Value\")/(SELECT SUM(\"Value\") FROM \"ALLCountries_Data\") * 100) AS percentage_contribution "
                                                                      " FROM \"ALLCountries_Data\" GROUP BY \"Country Name\" ",
     
    "The Top 3 Countries For Each Indicator Based On Debt" :"WITH RankedCountries As (SELECT \"Series Name\",\"Country Name\",\"Value\",ROW_NUMBER () OVER"
                                                              " (PARTITION BY \"Series Name\" ORDER BY \"Value\" DESC) AS rank "
                                                              " FROM \"ALLCountries_Data\") SELECT \"Series Name\",\"Country Name\",\"Value\" "
                                                              " FROM RankedCountries WHERE rank <=3; ",
    "The Difference Between Maximum and Minimum Debt For Each Country":"SELECT \"Country Name\",(MAX(\"Value\")-MIN(\"Value\")) AS debt_difference FROM \"ALLCountries_Data\" GROUP BY \"Country Name\"; ",

   "High Debt,Medium Debt,Low Debt (based on thresholds)" :"SELECT \"Country Name\", SUM(\"Value\") AS total_debt,CASE "
                                                            "WHEN SUM(\"Value\") > 50000000000 THEN 'High Debt' "
                                                            " WHEN SUM(\"Value\") BETWEEN 10000000000 AND 50000000000 THEN 'Medium Debt'"
                                                            " ELSE 'Low Debt'END AS debt_category FROM \"ALLCountries_Data\" GROUP BY \"Country Name\";",

  "Window Functions To Calculate Cumulative Debt Per Country" :"SELECT \"Country Name\" , \"Series Name\",\"Value\","
                                                               " SUM(\"Value\") OVER (PARTITION BY \"Country Name\" ORDER BY \"Value\") AS cumulative_debt"
                                                               " FROM \"ALLCountries_Data\";",
   " indicators where average debt is higher than overall average debt" :"SELECT \"Country Name\" , SUM(\"Value\") AS total_debt "
                                                                         "FROM \"ALLCountries_Data\" GROUP BY \"Country Name\" "
                                                                       " HAVING SUM(\"Value\") > (SELECT SUM(\"Value\") * 0.05 FROM \"ALLCountries_Data\" );",
  "countries contributing more than 5% of global debt" :"SELECT \"Country Name\", SUM(\"Value\") AS total_debt FROM \"ALLCountries_Data\""
                                                        " GROUP BY \"Country Name\" HAVING SUM(\"Value\") > (SELECT SUM(\"Value\") * 0.05 FROM \"ALLCountries_Data\");",
  " the most dominant indicator (highest contribution) for each country" :"WITH CountryIndicatorRank AS (SELECT \"Country Name\", \"Series Name\", SUM(\"Value\") AS total_debt,"
                                                                          " ROW_NUMBER () OVER (PARTITION BY \"Country Name\" ORDER BY SUM(\"Value\") DESC) AS rank"
                                                                          " FROM \"ALLCountries_Data\" GROUP BY \"Country Name\",  \"Series Name\")"
                                                                          " SELECT \"Country Name\", \"Series Name\", total_debt" 
                                                                          " FROM CountryIndicatorRank WHERE rank = 1;"
                                                              
} 

selected = st.selectbox("select Query", list(queries))

if st.button("Run"):
    with engine.connect() as conn:
     df =pd.read_sql(text(queries[selected]), conn)
     
    st.dataframe(df)