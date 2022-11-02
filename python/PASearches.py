def linSearch(list, product):
    for i in range(len(list)):
        if list[i] == product:
            return True
    return False

def giveLinSearch(list, product):
    for i in range(len(list)):
        if list[i] == product:
            return i
    return -1