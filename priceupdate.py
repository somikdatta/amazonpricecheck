import requests
from bs4 import BeautifulSoup
import smtplib
import time

# Declarations
URL = ''
fromEmail = ''
# Generate App password (mail) for 2FA enabled accounts, for others disable secure login from Account Settings->Security
fromEmailPwd = ''
toEmail = ''
updateAfter = 0
price = 0.0
title = ''
headers = {
    "User Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"}


def main():
    # Product URL
    global URL
    URL = input()
    global fromEmail
    fromEmail = input()
    global fromEmailPwd
    fromEmailPwd = input()
    global toEmail
    toEmail = input()
    global updateAfter
    updateAfter = int(input())
    global price
    page = requests.get(URL, headers=headers)
    print(page)
    soup = BeautifulSoup(page.content, 'html.parser')
    global title
    title = soup.find(id="productTitle").get_text().strip()
    global price
    # Get the price when the program runs for the first time
    price = float(soup.find(id="priceblock_ourprice").get_text().strip()[
                  2:7].replace(',', '.'))
    time.sleep(10)
    # Start monitoring
    while(True):
        priceVariationCheck()
        time.sleep(60*60*updateAfter)


def priceVariationCheck():
    newPrice = updateprice()
    global price
    if(newPrice < price):
        price = newPrice
        mailer(newPrice)


def updateprice():
    page = requests.get(URL, headers=headers)
    print(page)
    # If response is 200 then:
    # Parse HTML as page.content is still nascent
    soup = BeautifulSoup(page.content, 'html.parser')
    # Get necessary HTML items
    priceNow = soup.find(id="priceblock_ourprice").get_text().strip()
    # Since we need to compare prices, we need the price in integer or float
    # I chose float since it was easiet to just replace ',' with '.' and make it float
    priceNum = float(priceNow[2:7].replace(',', '.'))
    return priceNum

# mailer() method uses Gmail's SMTP


def mailer(currentPrice):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(fromEmail, fromEmailPwd)
    subject = f'Prices Down for {title}'
    body = f'Check the Amazon link: {URL}\nPrice Reduced By: Rs.{price-currentPrice}\nCurrent Price: Rs.{currentPrice}'
    message = f'Subject: {subject}\n\n{body}'
    server.sendmail(fromEmail,
                    toEmail, message)
    server.quit()


if __name__ == "__main__":
    main()
