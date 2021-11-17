from bs4 import BeautifulSoup
import requests

def scrape_objects_text(obj_type,link):
        ''' This function retrieves all instances of a certain object type. '''
        page = requests.get(link)
        soup = BeautifulSoup(page.content,"lxml")
        results = soup.find_all(obj_type)
        for i in range(len(results)):
                results[i] = results[i].text
        return results

def scrape_objects_attr(obj_type,link,attr):
        ''' This function retrieves the value of an attribute of all instances of a certain object type. '''
        page = requests.get(link)
        soup = BeautifulSoup(page.content,"lxml")
        results = soup.find_all(obj_type)
        for i in range(len(results)):
                results[i] = results[i].get(attr)
        return results




        


