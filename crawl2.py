from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import csv

# instagram login ID and Password
login_ID = "gimamugae1765"
login_pass = "alfkzmfak50"

# write in the user name who you want to get comments and hashtags #
user_ID = input('user_ID: ') 

# download chrome driver and move location to same default folder
driver = webdriver.Chrome()  # download chrome driver and move location to same default folder
driver.implicitly_wait(5)

front_url = 'https://www.instagram.com/'
driver.get(front_url)
# to input ID
driver.find_element_by_name('username').send_keys(login_ID)

# to input password
driver.find_element_by_name('password').send_keys(login_pass)

# login button click
driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button').click()
sleep(2)

# click the button in the page after login page
driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/div/div/button').click()
sleep(2)


# go into selected account page
page_url = front_url + user_ID
driver.get(page_url)
# all posting count
posting_count = int(driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[1]/span/span').text)
                            

# print(posting_count)

# count the number of pictures in one account
# we are going to gather the back part of the each picture's url

videos = 0
carousels = 0
pictures = 0

picture_urls = []
while (True):
    try:
        body = driver.find_element_by_css_selector('body')

        # press PageDown button 5times
        body.send_keys(Keys.PAGE_DOWN)
        sleep(3)

        test = driver.find_element_by_css_selector("._2z6nI")
        table_html = test.get_attribute('innerHTML')
        soup = BeautifulSoup(table_html, 'html.parser')
        pictures_html = soup.select('.Nnq7C .v1Nh3 a[href]')

        for content in pictures_html:
            picture_url = "https://www.instagram.com" + content['href']

            if picture_url in picture_urls:
                continue
            else:
                picture_urls.append(picture_url)
                check = content.select('.u7YqG span')
                print("check:", check)

                if check == []:
                    print("picture")
                    pictures += 1
                else:
                    media = check[0]['aria-label'] 
                    if media == "슬라이드":
                        print("슬라이드")
                        carousels += 1
                    elif media == "동영상":
                        print("동영상")
                        videos += 1
            print()

        if len(picture_urls) == posting_count:
            break
    except:
        pass
print(f"인플루언서 {user_ID}의 Live Post 유형 분석")
print()
print("사진게시물:", pictures)
print()
print("영상게시물:", videos)
print()
print("슬라이드게시물:", carousels)
print()
print("전체 게시물: ", len(picture_urls))
driver.close()