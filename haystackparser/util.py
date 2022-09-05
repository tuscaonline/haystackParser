

from typing import List


def populateListWithNone(listToAppend:List, length):
    for i in range(len(listToAppend), length):
        listToAppend.append(None)
    return listToAppend
