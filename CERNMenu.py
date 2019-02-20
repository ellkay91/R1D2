import MenuTools as MT
import sys
import datetime
# pip install googletrans
#from googletrans import Translator
#translator = Translator()

Week = ["Mon", "Tue", "Wed", "Thu", "Fri"]
today = Week[datetime.date.today().weekday()]
weeknumber = datetime.date.today().isocalendar()[1]



restaurant = "R1"
dish = "vegetarian"
if len(sys.argv) > 1:
    restaurant = sys.argv[1]
if len(sys.argv) > 2:
    dish = sys.argv[2]
    
if restaurant != "R1" and restaurant != "R2":
    print "undefined Restaurant", restaurant, " - using R1"
    restaurant = "R1"




if len(sys.argv) == 3:
    splittable, DishType = MT.getTable(restaurant)
    MT.checkDish(DishType, dish)
    MT.printWeekDish(restaurant, dish, splittable, DishType)

if len(sys.argv) > 3:
    day = sys.argv[3]
    doNext=None
    if "next" in day:
        doNext=1
        splittable, DishType = MT.getTable(restaurant, 1)
        day=day.replace("next","")
    else:
        splittable, DishType = MT.getTable(restaurant)
    MT.checkDish(DishType, dish)
    MT.printWeekDish(restaurant, dish, splittable, DishType, doNext)
    if day in Week:
        print "\n"
        MT.printDay(restaurant, day, splittable, DishType, doNext)
    if day == "today":
        print "\n"
        MT.printDay(restaurant, today, splittable, DishType)

