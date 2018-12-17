class Utils:
    def removeDuplicateInList(collection):
        newList = []
        for item in collection:
            if item not in newList:
                newList.append(item)
        return newList
