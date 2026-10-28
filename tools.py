"""The agent's tools: two free public APIs it can search."""
import json
import xml.etree.ElementTree as ET

import httpx

WIKIPEDIA_URL = "https://en.wikipedia.org/w/api.php"
ARXIV_URL = "https://export.arxiv.org/api/query"
# Wikipedia blocks requests that don't say who is calling and where to find the project.
HEADERS = {"User-Agent": "research-assistant-learning-project/1.0 "
                         "(https://github.com/AlmaBetter-School/ai-integrated-app)"}
ATOM = "{http://www.w3.org/2005/Atom}"  # arXiv answers in Atom XML.


def shorten(text, limit=600):
    text = " ".join(text.split())
    return text if len(text) <= limit else text[:limit] + "…"


def search_wikipedia(query):
    """Tool 1: background facts from Wikipedia."""
    response = httpx.get(WIKIPEDIA_URL, headers=HEADERS, timeout=20.0, params={
        "action": "query", "format": "json", "generator": "search", "gsrsearch": query,
        "gsrlimit": 3, "prop": "extracts|info", "exintro": 1, "explaintext": 1, "inprop": "url",
    })
    response.raise_for_status()
    pages = response.json().get("query", {}).get("pages", {}).values()
    pages = sorted(pages, key=lambda page: page.get("index", 0))  # Best match first.
    return [{"title": page["title"], "summary": shorten(page.get("extract", "")),
             "url": page["fullurl"]} for page in pages]


def search_arxiv(query):
    """Tool 2: scientific papers from arXiv."""
    response = httpx.get(ARXIV_URL, headers=HEADERS, timeout=20.0, params={
        "search_query": f"all:{query}", "max_results": 3, "sortBy": "relevance",
    })
    response.raise_for_status()
    papers = []
    for entry in ET.fromstring(response.text).findall(f"{ATOM}entry"):
        papers.append({
            "title": shorten(entry.findtext(f"{ATOM}title", "")),
            "authors": [a.findtext(f"{ATOM}name", "") for a in entry.findall(f"{ATOM}author")][:3],
            "published": entry.findtext(f"{ATOM}published", "")[:10],
            "summary": shorten(entry.findtext(f"{ATOM}summary", "")),
            "url": entry.findtext(f"{ATOM}id", ""),
        })
    return papers


# The model reads these descriptions to decide which tool fits the question.
TOOLS = [
    {"type": "function", "function": {
        "name": "search_wikipedia",
        "description": "Search Wikipedia for background facts, definitions, people, places and history.",
        "parameters": {"type": "object", "required": ["query"], "properties": {
            "query": {"type": "string", "description": "A short search phrase"}}},
    }},
    {"type": "function", "function": {
        "name": "search_arxiv",
        "description": "Search arXiv for scientific research papers, including recent studies.",
        "parameters": {"type": "object", "required": ["query"], "properties": {
            "query": {"type": "string", "description": "A short search phrase"}}},
    }},
]
FUNCTIONS = {"search_wikipedia": search_wikipedia, "search_arxiv": search_arxiv}


def run_tool(name, arguments):
    """Run the tool the model asked for and return the result as text for the model."""
    if name not in FUNCTIONS:
        return f"Error: there is no tool called {name}."
    try:
        results = FUNCTIONS[name](arguments["query"])
    except (httpx.HTTPError, ET.ParseError, KeyError, TypeError) as error:
        return f"Error: {name} failed ({type(error).__name__}). Try the other tool or answer without it."
    return json.dumps(results) if results else "No results found."
