import sqlite3
import pandas as pd


# read from database
def get_data():
    con = sqlite3.connect("Data/amazon_search.db")
    global df
    # Read sqlite query results into a pandas DataFrame
    df = pd.read_sql_query("SELECT DISTINCT ASIN, name, cast(price as float) as price, ratings, ratings_num, details_link FROM search_result", con)
    # Verify that result of SQL query is stored in the dataframe
    print(df.head())
    con.close()
    return df

# retrieve products in the specified price range
def price_range(lower, upper):
    price_range_df = df[(df.price >= lower) & (df.price <= upper)]
    print(price_range_df.head())
    return price_range_df


if __name__ == '__main__':

    # gather all data from web scrape into data frame
    get_data()
    # get data in new data frame that is in specified price range
    price_range(100, 350)

