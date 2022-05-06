def encrypt(key: str, text: str):
        '''This function takes a key and a ext to encrypt and retuns the text encrypted.'''
        toRet = ""
        for i in range(len(text)):
                toRet += chr((ord(text[i])+1)^(ord(key[i%len(key)])))
        return toRet

def only_dups(lstoflsts: list):
        '''This function takes a nested list (such as [[],[]]) and returns a list which contains the values that are found in all lists of the nested list.'''
        toRet = []
        samplelst = lstoflsts.pop()
        for lst in lstoflsts:
                for i,item in enumerate(samplelst):
                        if not item in lst:
                                samplelst[i] = False
        for item in samplelst:
                if item != False:
                        toRet.append(item)
        return toRet

def format_lst(lst: list):
        '''This function takes a list of single key dictionaries and returns a dictionary such that every key will lead to a list which contains all of the values that had the same key at the beginning. (for example format_lst([{"a":1},{"a":2},{"b":3}])->{"a":[1,2],"b":[3]}).'''
        toRet = {}
        for pair in (lst):
                for key in pair:
                        if key in toRet:
                                toRet[key].append(pair[key])
                        else:
                                toRet[key] = [pair[key]]
        return toRet