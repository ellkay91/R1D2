import re
import urllib
import bs4
import sys
import datetime

Week = ["Mon", "Tue", "Wed", "Thu", "Fri"]
today = Week[datetime.date.today().weekday()]
weeknumber = datetime.date.today().isocalendar()[1]


def getDishFromList(menu):
    DishType = []
    for m in menu:
        if ('gril' in m or 'Gril' in m) and '2' not in m:
            DishType.append('grill')
        elif ('gril' in m or 'Gril' in m) and '2' in m:
            DishType.append('grill2')
        elif ('pizza' in m or 'Pizza') in m and 'pizza' not in DishType:
            DishType.append('pizza')
        elif 'pizza' in m or 'Pizza' in m:
            DishType.append('pizza2')
        elif 'ialit' in m:
            DishType.append('specialty')
        elif 'tarien' in m:
            DishType.append('vegetarian')
        elif 'enu 1' in m:
            DishType.append('menu1')
        elif 'enu 2' in m:
            DishType.append('menu2')
        elif 'des Gourmands' in m:
            DishType.append('fancy pasta')
        elif 'pasta' in m:
            DishType.append('pasta')
        elif 'burger' in m:
            DishType.append('burger')
        elif 'te du jour' in m:
            DishType.append('pasta')
        elif 'te du jour no 2' in m:
            DishType.append('pasta2')
        elif 'march' in m:
            DishType.append('march')
        else:
            DishType.append('mystery')
    return DishType

def getLink(restaurant):
    if restaurant == "R1":
        link = "http://www.novae-restauration.ch/menus/menu-week/cern/13?lang=en"
    elif restaurant == "R2":
        link = "http://www.novae-restauration.ch/menus/menu-week/cern/21?lang=en"
    return link


def extract_name(bsitem):
    return bsitem.find('span').text


def extract_price(bsitem):
    reg = re.compile(r'(\d+\.?\d*)')
    mat = reg.findall(bsitem.text)
    if len(mat) > 0:
        return float(mat[0])
    return 0.0



def getTable(restaurant, addweek=None):
    link = getLink(restaurant)
    if addweek is not None:
        link += "&week="+str(weeknumber+addweek)
    f = urllib.urlopen(link)
    myfile = f.read()
    #print myfile
    menus = bs4.BeautifulSoup(myfile, 'lxml').find(
        'table',
        class_='menuRestaurant').findAll('td',
                                         class_='typeMenu')
    menus = [ m.text.encode('utf-8').replace("\n"," ") for m in menus ]
    # print (',').join(menus).decode('utf-8')
    items = bs4.BeautifulSoup(myfile, 'lxml').find(
        'table',
        class_='menuRestaurant').findAll('table',
                                         class_='HauteurMenu')

    table =  [extract_name(i).encode('utf-8').replace("\n"," ") for i in items[1::2]]
    DishTypes = getDishFromList(menus)# getDishType(restaurant)
    n=len(DishTypes)
    splittable = [table[i:i+n] for i in xrange(0,len(table),n)]
    return splittable, DishTypes



def printDay(restaurant, day, splittable, DishType, doNext=None):
    if doNext is not None:
        print restaurant, "Next", day, "Menu:"
    else:
        print restaurant, day, "Menu:"
    #DishType = getDishType(restaurant)
    daylist = splittable[Week.index(day)]
    for d in range(0, len(daylist)):
        print DishType[d] + ": " + daylist[d].decode('utf-8') 
        #print "     ("+translator.translate(daylist[d]).text+")"

def printWeekDish(restaurant, dish, splittable, DishType, doNext=None):
    
    if doNext is not None:
        print restaurant, dish, "Menu for Next Week:"
    else:
        print restaurant, dish, "Menu:"
    # DishType = getDishType(restaurant)
    dishlist =  [ s[DishType.index(dish)] for s in splittable]
    for d in range(0, len(dishlist)):
        print Week[d] +": " + dishlist[d].decode('utf-8') 
        #print "     ("+translator.translate(dishlist[d]).text+")"


def checkDish(DishType, dish):
    if dish not in DishType:
        print "undefined dish", dish, " - using vegetarian"
        dish = "vegetarian"
        sys.exit()

    
