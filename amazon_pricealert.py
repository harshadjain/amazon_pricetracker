#///////////////////////////////////////////IMPORTING MODULES ////////////////////////////////////////////////////////////////////
import requests
from bs4 import BeautifulSoup
import smtplib
import os 
from dotenv import load_dotenv
load_dotenv()
#///////////////////////////////////////////DEFINING VARIABLES////////////////////////////////////////////////////////////////////

MY_EMAIL=os.getenv("MY_EMAIL")
TO_EMAIL=os.getenv("TO_EMAIL")
MY_PASS=os.getenv("MY_PASS") # this is not the password of the gmail account this is the APP password created by google specifically for mail.
BUDGET_PRICE=20500
PRODUCT_URL = "https://www.amazon.in/dp/B09TWH8YHM/ref=sspa_dk_detail_2?pd_rd_i=B09TWHTBKQ&pd_rd_w=Yv0LX&content-id=amzn1.sym.93cf4d99-e9b9-496a-8c11-b758e79d2b72&pf_rd_p=93cf4d99-e9b9-496a-8c11-b758e79d2b72&pf_rd_r=J3X9618AQDQ2JSSST0TY&pd_rd_wg=InkYO&pd_rd_r=3baa966e-538d-40d7-a3ff-f3b3ba8a0cd7&s=electronics&sp_csd=d2lkZ2V0TmFtZT1zcF9kZXRhaWw&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUFMRkVHU1BSUjlUWlgmZW5jcnlwdGVkSWQ9QTA1MzA5MTUyODYzQjk4QVNTVFNQJmVuY3J5cHRlZEFkSWQ9QTA5Mjc2MTIyMUVOSFRMVzFGNUhPJndpZGdldE5hbWU9c3BfZGV0YWlsJmFjdGlvbj1jbGlja1JlZGlyZWN0JmRvTm90TG9nQ2xpY2s9dHJ1ZQ&th=1"

#///////////////////////////////////////////BUIDLING SOUP ////////////////////////////////////////////////////////////////////
header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
       "Accept-Encoding": "gzip, deflate", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
       "DNT": "1", "Connection": "close", "Upgrade-Insecure-Requests": "1"}
response = requests.get(PRODUCT_URL, headers=header)
soup=BeautifulSoup(response.text,"lxml")

#///////////////////////////////////////////EXTRACTING THE CURRENT PRICE ////////////////////////////////////////////////////////////////////

CURRENT_PRICE=((soup.find('span',{'class':'a-offscreen'})).get_text().strip().split('₹')[1])
CURRENT_PRICE=int(float((''.join(map(str,CURRENT_PRICE))).replace(',','')))

#///////////////////////////////////////////COMPARING THE  CURRENT PRICE WITH BUDGET PRICE ////////////////////////////////////////////////////////////////////

if CURRENT_PRICE<BUDGET_PRICE:
    with smtplib.SMTP("smtp.gmail.com",port=587) as connection:
        connection.ehlo()
        connection.starttls()
        connection.ehlo()
        connection.login(user=MY_EMAIL,password=MY_PASS)
        connection.sendmail(from_addr=MY_EMAIL,
        to_addrs=TO_EMAIL,
        msg=f'Subject:AMAZON PRICE DROP ALERT!!\n\nYOUR SELECTED PRODUCT JUST GOT CHEAPER THAN YOUR PRICE @{CURRENT_PRICE}\n CLICK ON THE BEOW LINK TO PLACE YOUR ORDER \n {PRODUCT_URL}'
        )
        connection.quit()
