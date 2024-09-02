# baltimore-city-employee-salaries
 This process queries the Open Baltimore Data API for city employee salaries. It then stores the salaries as a `csv` file in a google cloud bucket where I upload it into a BigQuery
 table for further analysis.

 In a future update, I may change this processe to write records directly to a bigquery table instead of first creating a CSV. I'll likely continue this process until Baltimore releases these datasets on a more regular schedule.

You can find the final write up for this project on my website [here](https://citysalaries.johnwmathena.com).
