from util.ytcomments import YouTubeComments

if __name__ == '__main__':
    scraper = YouTubeComments()
    scraper.get_comments("https://www.youtube.com/watch?v=JGhoLcsr8GA")
