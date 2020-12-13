# manga-raw-downloader
Python script to automatically download untranslated manga from rawdevart.com. The purpose for writing this was simply for me to more conveniently practice my Japanese, but others may find this utility useful as well. 
# Getting Started
Python3 is needed to run this program. Download the program and place it in a directory you want to store the downloaded manga. Run the program. It will ask you to enter two inputs, the first being the URL of the manga you want to download, ex. https://rawdevart.com/comic/grand-blue/, and the second being the folder name the manga will be stored in, which should usually be the name of the manga itself. It will then proceed to download each page of each chapter of the given manga. The output will be stored, separated by chapter, in the new folder created in the same directory as the script.
# Dependencies
Besides Python3 being installed, some additional libraries will be required for the script to run. Those being requests, BeautifulSoup4, and progress. Simply run:
```
pip install BeautifulSoup4 requests progress
```
in the command prompt to install the libraries, then run the main python script.

