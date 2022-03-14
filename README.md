# OpenWeatherData

## OpenWeather API background 
The program uses the OpenWeatherData api to make a request to the weather data and store 
the data into a text file called rawdata. As of now the data will be in JSON string format
until further update. The maximum number of requests for now is 3 per day afterward the program
will print to terminal when the limit was reached. (There is no particular reasoning for selecting 3
. However the maximum number of calls per minute is 6 while per month is 100,000 for free usage of the API. 
For more details, visit OpenWeatherData for the api documenation). 

## Program Description 
Make a request to the api every time the script is ran, based on a predefined limit per
day do not go pass that limit; Store the data from the request into a mysql database. 
