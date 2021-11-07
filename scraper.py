from bs4 import BeautifulSoup
import requests

def scrape_objects(obj_type,link):
        ''' This function retrieves all of the instances of a certain object type. '''
        page = requests.get(link)
        soup = BeautifulSoup(page.content,"lxml")
        results = soup.find_all(obj_type)
        for i in range(len(results)):
                results[i] = results[i].text
        return results




        


