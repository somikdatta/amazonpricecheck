import requests
from bs4 import BeautifulSoup
import smtplib
import time

# Declarations
URL = ''
fromEmail = ''
fromEmailPwd = ''
toEmail = ''
headers = {
    "User Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"}


def main():
    # Product URL
    global URL
    URL = input()
    global fromEmail
    fromEmail = input()
    # Generate App password (mail) for 2FA enabled accounts, for others disable secure login from Account Settings->Security
    global fromEmailPwd
    fromEmailPwd = input()
    global toEmail
    toEmail = input()
    updateprice()


def updateprice():
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
    if(priceNum >= 1.0):
        mailer(title, priceNum)

# mailer() method uses Gmail's SMTP


def mailer(title, currentPrice):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(fromEmail, fromEmailPwd)
    subject = f'Prices Down for {title}'
    body = f'Check the Amazon link: {URL}\nCurrent Price: Rs.{currentPrice}'
    message = f'Subject: {subject}\n\n{body}'
    server.sendmail(fromEmail,
                    toEmail, message)
    server.quit()


if __name__ == "__main__":
    main()
