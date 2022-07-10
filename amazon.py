import requests
from bs4 import BeautifulSoup
import smtplib
import time

# set the headers and user string
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36"
}

# send a request to fetch HTML of the page
response = requests.get('https://www.amazon.in/dp/B09MQSCJQ1/ref=s9_acsd_al_bw_c2_x_3_i?pf_rd_m=A1K21FY43GMZF8&pf_rd_s=merchandised-search-3&pf_rd_r=107ZTS596WH34ECHE0CP&pf_rd_t=101&pf_rd_p=2c3d77ca-ce38-48ee-bef0-e562de6e5a3e&pf_rd_i=11599648031', headers=headers)

# create the soup object
soup = BeautifulSoup(response.content, 'html.parser')

# change the encoding to utf-8
soup.encode('utf-8')

# print(soup.prettify())

# function to check if the price has dropped below 20,000


def check_price():
    title = soup.find(class_="a-offscreen").get_text()
    price = soup.find(class_="a-offscreen").get_text().replace(
        ',', '').replace('₹', '').replace(' ', '').strip()
    # print(price)

    # converting the string amount to float
    converted_price = float(price[0:5])
    print(converted_price)
    if(converted_price < 20000):
        send_mail()

    # using strip to remove extra spaces in the title
    print(title.strip())


# function that sends an email if the prices fell down
def send_mail():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login('email@gmail.com', 'password')

    subject = 'Price Fell Down'
    body = "Check the amazon link https://www.amazon.in/Bose-SoundLink-Wireless-Around-Ear-Headphones/dp/B0117RGG8E/ref=sr_1_11?qid=1562395272&refinements=p_89%3ABose&s=electronics&sr=1-11 "

    msg = f"Subject: {subject}\n\n{body}"

    server.sendmail(
        'sender@gmail.com',
        'receiver@gmail.com',
        msg
    )
    # print a message to check if the email has been sent
    print('Hey Email has been sent')
    # quit the server
    server.quit()


# loop that allows the program to regularly check for prices
while(True):
    check_price()
    time.sleep(60 * 60)
