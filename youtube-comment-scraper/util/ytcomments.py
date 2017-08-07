import os
import time

import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

COMMENTS_FILE = "youtube_comments.csv"
SHOW_MORE_XPATH = "//*[@id=\"comment-section-renderer\"]/button"
SHOW_MORE_CLASS_NAME = "comment-section-renderer-paginator"

class YouTubeComments(object):
    def __init__(self):
        print "Initialized!"
        self.driver = webdriver.Chrome()

    def get_beautiful_soup_object(self, url):
        return BeautifulSoup(url, "lxml")

    def parsedata(self, soup):
        comments = soup.find_all("section", {"class": "comment-thread-renderer"})
        username = comment_str = replies = "NA"
        for comment in comments:
            print comment
            print "*****************************************"
            username = self.get_user_name(comment)
            comment_str = self.get_comment(comment)
            replies = self.get_replies(comment)
            comment_details = {"username": username, "comment": comment_str, "replies": replies}
            comment_df = pd.DataFrame(comment_details, index=[0])
            if not os.path.isfile(COMMENTS_FILE):
                comment_df.to_csv(COMMENTS_FILE, header=True, encoding='utf-8')
            else:  # else it exists so append without writing the header
                comment_df.to_csv(COMMENTS_FILE, mode='a', header=False, encoding='utf-8')




                # if file does not exist write header

    def get_user_name(self, comment):
        # TODO
        user_soup = comment.find("div", {"class": "comment-renderer-header"})
        user_name = user_soup.find("a").text
        return user_name

    def get_comment(self, comment):
        comment_soup = comment.find("div", {"class": "comment-renderer-text-content"})
        comment_text = comment_soup.text
        return comment_text

    def get_replies(self, comment):
        comment_replies_soup = comment.find("div", {"class": "comment-replies-renderer"})
        return

    def get_comments(self, link):
        # try:
        #    self.driver = webself.driver.PhantomJS()
        # except Exception as exp:
        #    raise exp
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        print last_height

        self.driver.get(link)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        print last_height
        r = requests.get(link)
        if r.status_code != 200:
            raise Exception("Exiting!")
        html = self.driver.page_source
        soup = self.get_beautiful_soup_object(html)
        while (1):
            self.parsedata(soup)
            time.sleep(2)
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            # element = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, SHOW_MORE_XPATH)));
            # element = self.driver.find_element_by_link_text("Show More")
            # element.click()
            last_height = self.driver.execute_script("return document.body.scrollHeight")
            print last_height
            element = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, SHOW_MORE_XPATH)))
            #element = self.driver.find_element_by_xpath(SHOW_MORE_XPATH)
            element.click()
            time.sleep(3)
