import tkinter as tk
from bs4 import BeautifulSoup
import requests
import webbrowser

def onclickLink(url):
    # Open the link in the default web browser
    webbrowser.open_new(url)

def scrapeWebPage():
    # Code to scrape web page
    url = urlEntry.get()
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.title.string
        # all links that start with https://
        links = soup.find_all('a', href=True)
        resultLabel.config(text=f"Title: {title}")
        #show all links that start with https:// and make them clickable
        linksResultLabel.config(text="Links:")
        for link in links:
            if link.get('href').startswith('https'):
                link_text = link.get('href')
                link_label = tk.Label(root, text=link_text, fg="blue", cursor="hand2")
                link_label.grid(sticky="w")
                link_label.bind("<Button-1>", lambda url=link_text: onclickLink(url))
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

linksLabel = tk.Label(root, text="")
linksLabel.grid(row=2, column=0, columnspan=3)

linksResultLabel = tk.Label(root, text="")
linksResultLabel.grid(row=3, column=0, columnspan=3)

root.mainloop()