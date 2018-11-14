class data:
    list1 = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9)]
    list2 = [(0, 2), (1, 3), (2, 4), (3, 5), (4, 6), (5, 7), (6, 8), (7, 9), (8, 10)]
    listx = []
    listy = []
    count = 0
    for i in list1:            #x waarden
        if(len(list1) > count):
            listx.append(list1[count][0])
            count+=1
    count2 = 0
    for i in list1:            #y waarden
        if(len(list1) > count2):
            listy.append(list1[count2][1])
            count2+=1

schermstatus = 0
sendData = 0
lijst1 = []
lijst2 = []

