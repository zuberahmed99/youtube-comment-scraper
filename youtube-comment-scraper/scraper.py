from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import os
import requests
import time

COMMENTS_FILE = "youtube_comments.csv"
SHOW_MORE_XPATH =  "//*[@id=\"comment-section-renderer\"]/button/span/span[2]"


driver = webdriver.PhantomJS()
def get_beautiful_soup_object(url):
    return BeautifulSoup(url)

def parsedata(soup):
    comments = soup.find_all("section",{"class": "comment-thread-renderer"})
    username = comment_str = replies = "NA"
    for comment in comments:
        print comment
        print "*****************************************"
        username = get_user_name(comment)
        comment_str = get_comment(comment)
        replies = get_replies(comment)
        comment_details = {"username": username, "comment": comment_str, "replies": replies}
        comment_df = pd.DataFrame(comment_details, index=[0])
        if not os.path.isfile(COMMENTS_FILE):
            comment_df.to_csv(COMMENTS_FILE, header=True, encoding='utf-8')
        else:  # else it exists so append without writing the header
            comment_df.to_csv(COMMENTS_FILE, mode='a', header=False, encoding='utf-8')




    # if file does not exist write header



def get_user_name(comment):
    #TODO
    user_soup = comment.find("div", {"class": "comment-renderer-header"})
    user_name = user_soup.find("a").text
    return user_name

def get_comment(comment):
    comment_soup = comment.find("div", {"class": "comment-renderer-text-content"})
    comment_text = comment_soup.text
    return comment_text

def get_replies(comment):
    comment_replies_soup = comment.find("div", {"class": "comment-replies-renderer"})
    return

def get_comments(link):
   # try:
    #    driver = webdriver.PhantomJS()
   # except Exception as exp:
    #    raise exp

    driver.get(link)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)
    r = requests.get(link)
    if r.status_code != 200:
        raise Exception("Exiting!")
    html = driver.page_source
    soup = get_beautiful_soup_object(html)
    while(1):
        parsedata(soup)
        time.sleep(5)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        #element = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, SHOW_MORE_XPATH)));
        #element = driver.find_element_by_link_text("Show More")
        #element.click()
        element = driver.find_element_by_xpath(SHOW_MORE_XPATH)
        element.click()
        time.sleep(3)





get_comments("https://www.youtube.com/watch?v=JGhoLcsr8GA")
