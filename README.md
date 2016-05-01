# singularity
singularity hackathon



Topic - 
Smart List
Develop a system which would intelligently generate a shopping list for retailers. You can use the historical order data and the customer profiles to generate the list.
We have built a web-app which will be showing recommendation to each of the retailer on the basis of the items ordered by the retailer in the past.
Data source - Randomly Generated db.
      https://www.google.com/url?q=https%3A%2F%2Fwww.dropbox.com%2Fs%2Ftsd5zd8a7afmzs7%2FD11-02.ZIP%3Fdl%3D0&sa=D&sntz=1&usg=AFQjCNGsv94GAly73vwAtqvuNQ2Rg3sJow
Input - Historical data of retailers
Output - Recommendation of items and their quantity by the wholesaler for retailer

Approach - 
We have provided recommendation on following factors-
Time-interval between ordering of an item.
Item quantity ordered.

We tried to implement ARIMA model for predicting the quantity and date on which the item will be recommended.
Faced some issues at the end, so used average of the time-intervals and quantity

Used Flask for front-end and python for implementing logic.



