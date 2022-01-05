from bs4 import BeautifulSoup
import requests

def scrape_object_by_type(obj_type,link,attr_to_scrape):
        ''' This function retrieves all instances of a certain object type. '''
        page = requests.get(link)
        soup = BeautifulSoup(page.content,"lxml")
        results = soup.find_all(obj_type)
        if attr_to_scrape == "text":
                for i in range(len(results)):
                        results[i] = results[i].text
        else:
                for i in range(len(results)):
                        results[i] = results[i].get(attr_to_scrape)
        return results

def scrape_object_by_attr(attr_type,attrVal,link,attr_to_scrape):
        ''' This function retrieves the value of an attribute of all instances of an object that have a certain attribute value. '''
        page = requests.get(link)
        soup = BeautifulSoup(page.content,"lxml")
        results = soup.find_all(attrs={attr_type:attrVal})
        if attr_to_scrape == "text":
                for i in range(len(results)):
                        results[i] = results[i].text
        else:
                for i in range(len(results)):
                        results[i] = results[i].get(attr_to_scrape)
        return results




