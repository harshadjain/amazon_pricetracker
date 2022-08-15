import requests
import pandas as pd
from bs4 import BeautifulSoup
Title=[]
Date=[]
Rating=[]
Comment=[]

Review_URL=input("Enter the review URL here.")
resp=requests.get(Review_URL)
soup=BeautifulSoup(resp.text,"html.parser")

def total_ratings(soup):
    total_review=soup.findAll('div',{'class':"reviewNumericalSummary"})
    for x in total_review:
        num_=x.find('div',{'data-hook':'total-review-count'}).getText().strip().split(' ')[0]
    return num_
total_review_count=total_ratings(soup)
print("Total_Review_Count: " + total_review_count)

review=soup.findAll('div',{'data-hook':"review"})
for x in review:
    Title.append(x.find('a',{'data-hook':'review-title'}).getText().strip())
    Date.append(x.find('span',{'data-hook':'review-date'}).getText().strip().split('on')[1])
    Rating.append(x.find('i',{'data-hook':'review-star-rating'}).getText().strip().split(' ')[0])
    Comment.append(x.find('span',{'data-hook':'review-body'}).getText().strip())
    


excel_file={
    "Title":Title,
    "Date":Date,
    "Rating":Rating,
    "Comment":Comment
}

df=pd.DataFrame(excel_file)
df.to_csv("/Users/oneroot/Desktop/harshad/myenv/output/data.csv",index=False)