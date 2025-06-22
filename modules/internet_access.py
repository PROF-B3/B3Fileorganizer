import requests
import urllib.parse
try:
    from bs4 import BeautifulSoup
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False
    print("Note: BeautifulSoup not available, basic search only")

class InternetAccess:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'Mozilla/5.0 Academic Research Bot'})
    
    def search_scholar(self, query, max_results=5):
        """Search Google Scholar"""
        print(f"Searching Scholar for: {query}")
        try:
            url = f"https://scholar.google.com/scholar?q={urllib.parse.quote(query)}"
            response = self.session.get(url, timeout=10)
            
            if BS4_AVAILABLE:
                soup = BeautifulSoup(response.content, 'html.parser')
                results = []
                for i, result in enumerate(soup.find_all('div', class_='gs_ri')[:max_results]):
                    title_elem = result.find('h3')
                    title = title_elem.get_text() if title_elem else f"Paper {i+1}"
                    results.append({'title': title[:100], 'source': 'Google Scholar'})
                return results
            else:
                return [{'title': f'Search result for: {query}', 'source': 'Scholar (basic)'}]
                
        except Exception as e:
            print(f"Search error: {e}")
            return [{'title': f'Search unavailable for: {query}', 'source': 'Error'}]
    
    def search_multiple_topics(self, topics):
        """Search multiple academic topics"""
        all_results = []
        for topic in topics:
            results = self.search_scholar(topic)
            all_results.extend(results)
        return all_results
