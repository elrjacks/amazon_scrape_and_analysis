import sqlite3
import pandas as pd


# read from database
def get_data():
    con = sqlite3.connect("Data/amazon_search.db")
    global df
    # Read sqlite query results into a pandas DataFrame
    df = pd.read_sql_query("SELECT DISTINCT ASIN, name, cast(price as float) as price, ratings, cast(ratings_num as integer) as ratings_count, details_link FROM search_result", con)
    # Verify that result of SQL query is stored in the dataframe
    print(df.head())
    con.close()
    return df


# retrieve products in the specified price range
def price_range(lower, upper):
    global price_range_df
    price_range_df = df[(df.price >= lower) & (df.price <= upper)]
    print(price_range_df.head())
    return price_range_df


def ratings(min_rating):
    global rating_df
    df['rating_num'] = df.ratings.str[:3]
    df['rating_num'] = df['rating_num'].astype(float)
    print(df)
    rating_df = df[(df.rating_num >= min_rating)]
    print(rating_df.head())
    return rating_df


def reviews(min_reviews):
    global review_df
    review_df = df[(df.ratings_count >= min_reviews)]
    print(review_df)
    print(review_df.head())
    return review_df


def matches():
    match_df = pd.merge(price_range_df, rating_df, on='ASIN', how='inner')
    print(match_df.head())


if __name__ == '__main__':

    # gather all data from web scrape into data frame
    get_data()
    # get data in new data frame that is in specified price range
    price_range(100, 350)
    # find data within your desired out of 5-star rating
    ratings(4.5)
    # find products with a specified number of reviews
    reviews(500)
    # find products that match all your requirements
    matches()
    # find the average rating for your matches

    # find the rating above the average for your matches - sort my number of reviews

    #

