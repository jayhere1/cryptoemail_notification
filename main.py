import time
import requests
from bs4 import BeautifulSoup
from lxml import etree
import schedule
import smtplib
import os


my_email = os.environ.get('mail')
password = os.environ.get('password')
to_email = os.environ.get('to_email')

STOCK_ENDPOINT = "https://finance.yahoo.com/quote/LTC-USD/"


def extract_data():
    soup = BeautifulSoup(requests.get(STOCK_ENDPOINT).text, "html.parser")
    dom = etree.HTML(str(soup))
    current_price = dom.xpath('//*[@id="quote-header-info"]/div[3]/div/div/span[1]')[0].text

    return float(current_price)


def send_email(price=extract_data()):
    if price < 180:
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(
                from_addr=my_email,
                to_addrs=to_email,
                msg="Subject:Current price of Litecoin\n\n "
                    f"{price}")


schedule.every(10).minutes.do(send_email)

while True:
    schedule.run_pending()
    time.sleep(60)
