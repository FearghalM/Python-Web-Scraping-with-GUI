import tkinter as tk
from bs4 import BeautifulSoup
import requests
import webbrowser
import wikipedia


def onclickLink(url):
    # Open the link in the default web browser
    webbrowser.open_new(url)


# def openRandomWikiArticle():
#     # Get a random Wikipedia article title
#     article_title = wikipedia.random()
#     # Construct the URL for the article
#     article_url = wikipedia.page(article_title).url
#     # Open the article in the default web browser
#     webbrowser.open_new(article_url)

def get_random_wiki_url():
    # API endpoint for fetching a random Wikipedia article
    api_url = "https://en.wikipedia.org/api/rest_v1/page/random/summary"
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            # Extract the URL of the random Wikipedia article
            data = response.json()
            random_url = data["content_urls"]["desktop"]["page"]
            # Update the urlEntry with the random URL
            urlEntry.delete(0, tk.END)
            urlEntry.insert(0, random_url)
        else:
            resultLabel.config(text="Error fetching random Wikipedia article")
    except requests.RequestException as e:
        resultLabel.config(text=f"Error: {e}")


def scrapeWebPage():
    # Code to scrape web page
    url = urlEntry.get()
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        title = soup.title.string
        # all links that start with https://
        links = soup.find_all("a", href=True)
        resultLabel.config(text=f"Title: {title}")
        # show all links that start with https:// and make them clickable
        linksResultLabel.config(text="Links:")
        
        # Use a set to store unique URLs
        unique_links = set()
        for link in links:
            if link.get("href").startswith("https"):
                unique_links.add(link.get("href"))
        
        # Remove existing link labels
        for label in link_labels:
            label.grid_forget()
        
        # Display unique links
        row_num = 4
        for link_text in unique_links:
            link_label = tk.Label(root, text=link_text, fg="blue", cursor="hand2")
            link_label.grid(row=row_num, column=0, sticky="w")
            link_label.bind("<Button-1>", lambda event, url=link_text: onclickLink(url))
            link_labels.append(link_label)
            row_num += 1
    else:
        resultLabel.config(text="Error accessing web page")


# Code to create GUI
root = tk.Tk()
root.title("Web Page Scraper")

urlLabel = tk.Label(root, text="Enter URL:")
urlLabel.grid(row=0, column=0, padx=5, pady=5)

urlEntry = tk.Entry(root, width=50)
urlEntry.grid(row=0, column=1, padx=5, pady=5)

scrapeButton = tk.Button(root, text="Scrape", command=scrapeWebPage)
scrapeButton.grid(row=0, column=2, padx=5, pady=5)

randomWikiButton = tk.Button(root, text="Random Wiki Article", command=get_random_wiki_url)
randomWikiButton.grid(row=0, column=3, padx=5, pady=5)

resultLabel = tk.Label(root, text="")
resultLabel.grid(row=1, column=0, columnspan=4, padx=5, pady=5)

linksResultLabel = tk.Label(root, text="")
linksResultLabel.grid(row=3, column=0, columnspan=4, padx=5, pady=5)

link_labels = []  # to store references to link labels dynamically

root.mainloop()
