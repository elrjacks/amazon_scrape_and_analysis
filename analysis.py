import sqlite3
import pandas as pd
import numpy as np


# read from database
def get_data():
    con = sqlite3.connect("Data/amazon_search.db")
    global df
    # Read sqlite query results into a pandas DataFrame
    df = pd.read_sql_query("SELECT DISTINCT ASIN, name, cast(price as float) as price, ratings, cast(ratings_num as integer) as ratings_count, details_link FROM search_result", con)
    # Verify that result of SQL query is stored in the dataframe
    print("All products...")
    print(df.head())
    con.close()


# retrieve products in the specified price range
def price_range(lower, upper):
    global price_range_df
    price_range_df = df[(df.price >= lower) & (df.price <= upper)]
    print("Products in your price range are as follows: ")
    # print(price_range_df.to_string())


def ratings(min_rating):
    global rating_df
    df['rating_num'] = df.ratings.str[:3]
    df['rating_num'] = df['rating_num'].astype(float)
    rating_df = df[(df.rating_num >= min_rating)]
    print("Products in with your desired rating or higher are as follows: ")
    # print(rating_df.to_string())


def reviews(min_reviews):
    global review_df
    review_df = df[(df.ratings_count >= min_reviews)]
    print("Products with you desired number of reviews or higher are as follows: ")
    # print(review_df.to_string())


def matches(df1, df2, df3, number_of_matches):
    global match_df
    match_df = pd.merge(df1, df2)

    # if you want to merge all three set indicator to Y
    if all_three == 'Y':
        match_df = pd.merge(match_df, df3)
    print("Products that are in your desired match result set are as follows: ")
    print(match_df.to_string())
    # find the average rating for your matches
    avg_rating = average_rating(match_df)
    # find your products that are you best match overall
    best_matches(avg_rating, number_of_matches)


def average_rating(data_frame):
    avg_rating = round(match_df.loc[:, 'rating_num'].mean(),2)
    print(f'Average rating out of five stars for your perfect product is = {avg_rating}')
    return avg_rating


def best_matches(avg_rating, number_of_matches):
    # find the rating above the average for your matches - sort by number of reviews
    best_match_df = match_df[(match_df.rating_num >= avg_rating)]
    best_match_df = best_match_df.sort_values(by="ratings_count", ascending=False)
    best_match_df = best_match_df.head(number_of_matches)
    print(f'Your top {number_of_matches} match(es) is as follows: ')
    print(best_match_df.to_string())


def driver():
    # gather all data from web scrape into data frame
    get_data()
    # get data in new data frame that is in specified price range
    min = int(input('What is your minimum price?\n'))
    max = int(input('What is your maximum price?\n'))
    price_range(min, max)
    # find data within your desired out of 5-star rating
    rating = float(input('What is the least rating out of 5 you wish to see products for?\n'))
    ratings(rating)
    # find products with a specified number of reviews
    rev = int(input('What is the minimum number of reviews you would like to see?\n'))
    reviews(rev)
    # match on price and rating is default
    # match on price rating and reviews may be done
    global all_three
    all_three = input('Would you like to see only matches that macth on all three, price range, ratings, and reviews? This will limit your result set. (Y/N)\n')
    num_of_matches = int(input('What total number of matches would you like to see?\n'))
    # find products that match all your requirements
    matches(price_range_df, rating_df, review_df, num_of_matches)


if __name__ == '__main__':
    driver()

