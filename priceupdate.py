import requests
from bs4 import BeautifulSoup
import smtplib
import time

URL = 'https://www.amazon.in/Sennheiser-CX-213-CX213-Earphones/dp/B00SQWD8Z8'

headers = {
    "User Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"}


def updateprice():
    URL = input()
    page = requests.get(URL, headers=headers)
    # If response is 200 then:
    # Parse HTML as page.content is still nascent
    soup = BeautifulSoup(page.content, 'html.parser')
    # Get necessary HTML items
    title = soup.find(id="productTitle").get_text().strip()
    price = soup.find(id="priceblock_ourprice").get_text().strip()
    # Since we need to compare prices, we need the price in integer or float
    # I chose float since it was easiet to just replace ',' with '.' and make it float
    priceNum = float(price[2:7].replace(',', '.'))
    # Email update if price falls
    if(priceNum <= 1.0):
        mailer(title, priceNum)

# mailer() method uses Gmail's SMTP


def mailer(title, currentPrice):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    # Generate App password (mail) for 2FA enabled accounts, for others disable secure login from Account Settings->Security
    server.login('from-emailid@example.com', 'examplepassword')
    subject = f'Prices Down for {title}'
    body = f'Check the Amazon link: {URL}\nCurrent Price: Rs.{currentPrice}'
    message = f'Subject: {subject}\n\n{body}'
    server.sendmail('from-emailid@example.com',
                    'to-emailid@example.com', message)
    server.quit()


while(True):
    updateprice()
    time.sleep(60*60*12)
