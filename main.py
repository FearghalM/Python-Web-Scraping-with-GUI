import tkinter as tk
from bs4 import BeautifulSoup
import requests
import webbrowser


def onclick_link(url):
    """Open the link in the default web browser."""
    webbrowser.open_new(url)


def get_random_wiki_url():
    """Get a random Wikipedia article URL and update the entry."""
    api_url = "https://en.wikipedia.org/api/rest_v1/page/random/summary"
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            random_url = data["content_urls"]["desktop"]["page"]
            url_entry.delete(0, tk.END)
            url_entry.insert(0, random_url)
        else:
            update_result_label("Error fetching random Wikipedia article")
    except requests.RequestException as e:
        update_result_label(f"Error: {e}")


def scrape_web_page():
    """Scrape the web page and display results."""
    url = url_entry.get()
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise exception for HTTP errors
        soup = BeautifulSoup(response.content, "html.parser")
        title = soup.title.string
        links = soup.find_all("a", href=True)
        update_result_label(f"Title: {title}")
        
        unique_links = set(link.get("href") for link in links if link.get("href").startswith("https"))
        update_links_labels(unique_links)
    except requests.RequestException as e:
        update_result_label(f"Error accessing web page: {e}")
    except Exception as e:
        update_result_label(f"An unexpected error occurred: {e}")


def update_links_labels(links):
    """Update link labels with the provided links."""
    links_result_label.config(text="Links:")
    clear_links_labels()
    for idx, link_text in enumerate(links, start=4):
        link_label = tk.Label(root, text=link_text, fg="blue", cursor="hand2")
        link_label.grid(row=idx, column=0, sticky="w")
        link_label.bind("<Button-1>", lambda event, url=link_text: onclick_link(url))
        link_labels.append(link_label)


def clear_links_labels():
    """Clear existing link labels."""
    for label in link_labels:
        label.grid_forget()


def update_result_label(message):
    """Update the result label with the provided message."""
    result_label.config(text=message)


# Create GUI
root = tk.Tk()

# Create a title
root.title("Web Page Scraper")

url_label = tk.Label(root, text="Enter URL:")
url_label.grid(row=0, column=0, padx=5, pady=5)

url_entry = tk.Entry(root, width=50)
url_entry.grid(row=0, column=1, padx=5, pady=5)

scrape_button = tk.Button(root, text="Scrape", command=scrape_web_page)
scrape_button.grid(row=0, column=2, padx=5, pady=5)

random_wiki_button = tk.Button(root, text="Random Wiki Article", command=get_random_wiki_url)
random_wiki_button.grid(row=0, column=3, padx=5, pady=5)

result_label = tk.Label(root, text="")
result_label.grid(row=1, column=0, columnspan=4, padx=5, pady=5)

links_result_label = tk.Label(root, text="")
links_result_label.grid(row=3, column=0, columnspan=4, padx=5, pady=5)

link_labels = []  # Store references to link labels dynamically

root.mainloop()
