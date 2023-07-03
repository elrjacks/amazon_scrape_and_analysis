# amazon_scrape_and_analysis
## BeautifulSoup web scraping and Analysis
---
### Why?
Having coding skills is truly amazing, especially when faced with everyday problems. 
One such problem I encountered was finding the perfect espresso machine to purchase from Amazon. 
It seems like a common issue I've come across frequently, trying to assess which product will fit my needs. To tackle it efficiently, 
I started creating spreadsheets to keep track of various items, including their prices, ratings, features, and links, among other details. 
However, this process became time-consuming, and I wanted to find the best option without spending months on the decision-making process. 
Consequently, I developed a program that automates the entire process, providing me with the crème de la crème choices. ☕
---

### Basic Program Structure 
This program consists of two main parts, at least for now. The first part involves **web scraping**, where I utilize *Selenium* and *Python* to effectively scrape data from Amazon. Using the "find element" feature, I iterate through the elements to identify the specific data I want to analyze later. Once the data is collected, I store it in a sqlite3 database for convenient access. To ensure data cleanliness and optimize performance when querying the database, each product is assigned a primary key based on its ASIN on Amazon, eliminating any duplicate items.

Several aspects of the scraping process contribute to its modularity, such as the search box feature and pagination. Users of the scraper can input any desired search term, simulating a search on Amazon's website itself. Additionally, they have the flexibility to define the number of pages they want to scrape. For instance, if they only want to retrieve data from the initial page or two, they can set the maximum number of pages to 1 or 2. Conversely, if they wish to gather as much data as possible, they can specify a higher value, such as 25 or 30 pages. Rest assured, I have accounted for situations where you may want to search more pages than are available for the specified search on Amazon's site.


The second part of the program focuses on **data analysis**, where I utilize *Python's pandas package*. I take the gathered data through multiple steps, generating various files and datasets as output. One of these files is specifically tailored to include products within your specified price range. Another file includes products that meet or exceed your desired rating. Furthermore, I create an inner join of these two datasets, resulting in a "matches" file that combines both criteria.

From the matches data, I calculate the average rating and identify your "perfect" matches. These perfect matches refer to products that surpass the specified average rating. This way, you can easily find and prioritize products with ratings higher than your desired average, ensuring you get the best options based on your preferences.

---
### Example Invocation 
During the initial **scraper.py** run, we get an amazon_search.db. If I head over to https://sqliteonline.com/, I can pull up the database file that is generated after the run. 
![Amazon scraped product database](/Images/database.png "Amazon scraped product database")
