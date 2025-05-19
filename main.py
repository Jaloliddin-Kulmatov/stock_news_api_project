import requests
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = ""
NEWS_API_KEY = ""

TWILIO_SID = "AC6ebbc339cd640925ee2b243fe1ad420f"
TWILIO_TOKEN = ""
TWILIO_NUMBER = "+18145593138"

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": STOCK_API_KEY
}

stock_response = requests.get(STOCK_ENDPOINT, params=stock_params)
stock_json = stock_response.json()

if "Time Series (Daily)" not in stock_json:
    print("Error in stock data response:")
    print(stock_json)  # Debug output
else:
    stock_data = stock_json["Time Series (Daily)"]
    data_list = [value for (key, value) in stock_data.items()]
    data_list = [value for (key, value) in stock_data.items()]
    yesterday_data = data_list[0]
    yesterday_close_data = yesterday_data["4. close"]

    day_before_data = data_list[1]
    day_before_close_data = day_before_data["4. close"]

    difference = float(day_before_close_data - yesterday_close_data)
    up_down = None
    if difference > 0:
        up_down = "🔺"
    else:
        up_down = "🔻"

    dif_percent = round(difference / float(yesterday_close_data) * 100)
    if dif_percent > 5:
        news_params = {
            "apiKey": NEWS_API_KEY,
            "q": COMPANY_NAME
        }
        news_response = requests.get(NEWS_ENDPOINT, params=news_params)
        three_articles = news_response.json()["articles"][:3]
        formatted_articles_list  = [f"{STOCK}: {up_down}:{dif_percent}%\nHeadline: {article['title']}. \nBrief: {article['description']}" for article in three_articles]

        client = Client(TWILIO_SID, TWILIO_TOKEN)
        for article in formatted_articles_list:
            message = client.messages.create(
                body = article,
                from_= TWILIO_NUMBER,
                to = "+14155238886"
            )
