import tkinter as tk
from bs4 import BeautifulSoup
import requests

def scrapeWebPage():
    # Code to scrape web page
    url = urlEntry.get()
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.title.string
        resultLabel.config(text=f"Title: {title}")
    else:
        resultLabel.config(text="Error accessing web page")

# Code to create GUI
root = tk.Tk()
root.title("Web Page Scraper")

urlLabel = tk.Label(root, text="Enter URL:")
urlLabel.grid(row=0, column=0)

urlEntry = tk.Entry(root, width=50)
urlEntry.grid(row=0, column=1)

scrapeButton = tk.Button(root, text="Scrape", command=scrapeWebPage)
scrapeButton.grid(row=0, column=2)

resultLabel = tk.Label(root, text="")
resultLabel.grid(row=1, column=0, columnspan=3)

root.mainloop()