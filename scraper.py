
from bs4 import BeautifulSoup
import requests
import re

def find_obj_by_type(obj_type, link=None, tree=None):
        ''' This function retrieves all instances of a certain object type.'''
        if (tree != None and link != None) or (tree == None and link == None):
                return "Error!"
        elif tree != None:
                soup = BeautifulSoup(tree,"lxml")
        elif link != None:
                page = requests.get(link)
                soup = BeautifulSoup(page.content,"lxml")
        if obj_type[0] == ">":
                try:
                    return soup.find_all(re.compile(obj_type[1::]))
                except:
                    return soup.find_all(obj_type)
        else:
                return soup.find_all(obj_type)

def scr_obj_by_type(obj_type, attr_to_scrape, link=None, tree=None):
        '''This function retrieves requested data from all instances of a certain object type.'''
        results = find_obj_by_type(obj_type, link, tree)
        if attr_to_scrape == "text":
                for i in range(len(results)):
                        results[i] = results[i].text
        else:
                for i in range(len(results)):
                        results[i] = results[i].get(attr_to_scrape)
        return results

def find_obj_by_attr(attr_type, attr_val, link=None, tree=None):
        ''' This function retrieves all instances of an object that has a certain attribute value. '''
        if (tree != None and link != None) or (tree == None and link == None):
                return "Error!"
        elif tree != None:
                soup = BeautifulSoup(tree, "lxml")
        elif link != None:
                page = requests.get(link)
                soup = BeautifulSoup(page.content,"lxml")
        if attr_val[0] == ">":
                try:
                    return soup.find_all(attrs={attr_type:re.compile(attr_val[1::])})
                except:
                    return soup.find_all(attrs={attr_type:attr_val})
        else:
                return soup.find_all(attrs={attr_type:attr_val})

def scr_obj_by_attr(attr_type, attr_val, attr_to_scrape, link=None, tree=None):
        '''This function retrieves requested data from all instances of an object that has a certain attribute value.'''
        results = find_obj_by_attr(attr_type, attr_val, link, tree)
        if attr_to_scrape == "text":
                for i in range(len(results)):
                        results[i] = results[i].text
        else:
                for i in range(len(results)):
                        results[i] = results[i].get(attr_to_scrape)
        return results







