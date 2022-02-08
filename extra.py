def encrypt(key,text):
        toRet = ""
        for i in range(len(text)):
                toRet += chr((ord(text[i])+1)^(ord(key[i%len(key)])))
        return toRet

def only_dups(lstoflsts):
        toRet = []
        samplelst = lstoflsts.pop()
        for lst in lstoflsts:
                for i,item in enumerate(samplelst):
                        if not item in samplelst:
                                samplelst[i] = False
        for item in samplelst:
                if item != False:
                        toRet.append(item)
        return toRet

def format_lst(lst):
        toRet = {}
        for i,pair in enumerate(lst):
                for key in pair:
                        if key in toRet:
                                toRet[key].append(pair[key])
                        else:
                                toRet[key] = [pair[key]]
        return toRet