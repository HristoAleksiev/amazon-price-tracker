import requests
from bs4 import BeautifulSoup
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

amazon_url = "https://www.amazon.de/-/en/Logitech-Master-Advanced-Mouse-Bluetooth/dp/B07W6JMMNC/"
amazon_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/"
                  "537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9,bg;q=0.8,es;q=0.7",
}
email_smtp = "smtp.gmail.com"
sender_email = os.getenv("SENDER_EMAIL")
sender_password = os.getenv("SENDER_PASSWORD")
receiver_email = os.getenv("RECEIVER_EMAIL")

message = MIMEMultipart("alternative")
message["Subject"] = "Amazon price tracking services!"
message["From"] = sender_email
message["To"] = receiver_email

# Getting the price of the product:
response = requests.get(amazon_url, headers=amazon_headers)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")
price = float(soup.find(id="priceblock_ourprice").text.split("€")[1])
name_of_product = soup.find(id="productTitle").text.strip()

text_to_send = f"""
Oh, hello there!
I heard you like this product in Amazon:
{name_of_product}
Link:{amazon_url}
"""
html_to_send = f"""
<html lang="en" dir="ltr">
  <head>
    <style>
      #main-div {{
        background-color: #f8eded;
        border-top: 1px solid #e4bad4;
        border-left: 1px solid #e4bad4;
        border-bottom: 3px solid #e4bad4;
        border-right: 3px solid #e4bad4;
        border-radius: 25px;
        color: #33a652;
        width: 500px;
        text-align: center;
      }}
    </style>
  </head>
  <body>
    <div id="main-div">
      <p>Oh, hello there!<br>I heard you like this product from Amazon:</p>
      <a href="{amazon_url}">{name_of_product}</a>
      <p>The product is currently at a price of <strong>€{price}</strong>
       and this email is here to recommend that you buy NOW!</p>
    </div>
  </body>
</html>
"""

message.attach(MIMEText(text_to_send, "plain"))
message.attach(MIMEText(html_to_send, "html"))

with smtplib.SMTP(email_smtp) as connection:
    connection.starttls()
    connection.login(user=sender_email, password=sender_password)
    connection.sendmail(from_addr=sender_email,
                        to_addrs=receiver_email,
                        msg=message.as_string())
