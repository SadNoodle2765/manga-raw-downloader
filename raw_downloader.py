from collections import namedtuple
import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool
from progress.bar import Bar
import os

BASE_URL = 'https://rawdevart.com'

Chapter = namedtuple('Chapter', ['title', 'url'])
Page = namedtuple('Page', ['number', 'url'])

def run():
    url = input("Enter the manga's base URL from rawdevart.com\n")
    title = input("Enter the name of the manga, which will be the folder name the downloaded chapters will be stored in\n")
    
    soup = get_soup_from_url(url)
    chapters = get_chapters(soup)
    
    try:
        os.mkdir(title)           # Makes a folder named with the title provided by the user
    except FileExistsError:
        print("Folder with that name already exists, will put pictures in that existing folder")

    os.chdir(title)              # Changes directory to created folder
    chapters.reverse()           # Downloads chapters from the first chapter to the last
    
    for chapter in chapters:
        print("Downloading " + chapter.title)
        os.mkdir(chapter.title)       # Makes a folder with current chapter name
        os.chdir(chapter.title)       # Changes directory to chapter folder
        
        download_chapter(chapter)

        os.chdir('..')               # Go back to general directory after downloading the pictures

    print('Downloads completed!')
    

def download_chapter(chapter: Chapter) -> None:
    '''
    Accesses the URL of a given chapter, and downloads the jpg pages from it.
    Uses multiprocessing to parallelize and speed up the download process.
    '''
    
    soup = get_soup_from_url(chapter.url)
    picture_urls = get_picture_urls(soup)

    max_page = len(picture_urls)
    current_page = 1

    page_list = []
    for url in picture_urls:
        page = Page(current_page, url)               # Creates Page objects which includes both the URL of the page jpg, and the page number it's on.
        page_list.append(page)
        
        current_page += 1

    pool = Pool()

    bar = Bar('Page:', max=max_page)        # Progress bar shenanigans
    for i in pool.imap(download_page, page_list):
        bar.next()
    bar.finish()

    print()

def get_soup_from_url(url: str) -> BeautifulSoup:
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup

def get_chapters(soup: BeautifulSoup) -> [Chapter]:
    '''
    From the main page of the given manga,
    grabs the links that leads to each chapter of the manga
    and returns the links along with the title of the chapter in a list.
    '''
    
    chapters = []
    a_tags = soup.select("div[class='list-group w-100'] > div > a")
    for tag in a_tags:
        destination = tag['href']
        url = BASE_URL + destination
        title = tag['title']
        
        chapter = Chapter(title, url)
        chapters.append(chapter)

    return chapters

def get_picture_urls(soup: BeautifulSoup) -> [str]:
    '''
    From the page of the given chapter,
    grabs the links that leads to each jpg of the pages in the chapter,
    and returns the links in a list.
    '''
    
    picture_urls = []
    img_tags = soup.select("img[class='img-fluid not-lazy']")
    for tag in img_tags:
        url = tag['data-src'] 
        picture_urls.append(url)

    return picture_urls


def download_page(page: Page) -> None:
    filename = str(page.number) + '.jpg'
    url = page.url
    r = requests.get(url)
    f = open(filename, 'wb')
    f.write(r.content)
    f.close()


if __name__ == '__main__':
    run()
    

