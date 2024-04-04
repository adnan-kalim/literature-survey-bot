from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

def fetch_arxiv_abstracts(query, max_results=15):
    """
    Fetch abstracts from arXiv for a given query.
    """
    search_url = f"http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results={max_results}"
    
    response = requests.get(search_url)
    
    if response.status_code != 200:
        print("Failed to fetch data")
        return []
    
    soup = BeautifulSoup(response.content, 'xml')  
    
    entries = soup.find_all('entry')
    url = 'http://localhost:3000/'
    
    abstracts = []
    for entry in entries:
        title = entry.title.text.strip()
        abstract = entry.summary.text.strip()

        abstracts.append((title, abstract))
    
    return abstracts
 
app = Flask(__name__, template_folder = 'template')
 
@app.route('/',methods=["GET","POST"])
def hello_world():
    # query = "Cancer treatment using chemotherapy"
    # abstracts = fetch_arxiv_abstracts(query)
    # return render_template("abstracts.html", abstracts=abstracts)

    if request.method == "GET":
        query = "" 
    else:  
        query = request.form["search_query"]  

    if query:
        abstracts = fetch_arxiv_abstracts(query)
    else:
        abstracts = []  

    return render_template("abstracts.html", query=query, abstracts=abstracts)
 
if __name__ == '__main__':
    app.run()