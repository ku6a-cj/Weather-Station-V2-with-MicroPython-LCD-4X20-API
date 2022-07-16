import sys
import lcddriver
from time import *
import RPi.GPIO as GPIO
from threading import Thread
import time
from datetime import datetime
from datetime import date
import w1thermsensor
import requests
from gpiozero import CPUTemperature
import socket

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
Akcept=19
Back=26
Next=21
Previous=20


menu_selector=[" "," "," "," "]
menu_selection=0
menu_level=0

GPIO.setup(Akcept, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(Back, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(Next, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(Previous, GPIO.IN, pull_up_down=GPIO.PUD_UP)

current_date=date.today()

#weather api
api_key = "e3c44dc8b4dda873c34a2103267ed3fe"
base_url = "http://api.openweathermap.org/data/2.5/weather?"
city_name="Warsaw"
complete_url=base_url+"appid="+api_key + "&q=" + city_name
response=requests.get(complete_url)
p=response.json()
if p["cod"] != "404":
    y=p["main"]
    
    current_temperature=round(y["temp"] -273, 2)
    z=p["weather"]
    m=p["wind"]
    current_pressure=y["pressure"]
    current_wind_speed=m["speed"]
    weather_description= z[0]["description"]
    
    
    print(current_date)
    print("Temperature="+ str(current_temperature) + "\n description= "+ str(weather_description) + " pressure= "+ str(current_pressure))
    
else:
    print("City not found")



#currency 
url = 'https://v6.exchangerate-api.com/v6/186cf925469ad9afadf3abe8/latest/USD'
response2 = requests.get(url)
data2 = response2.json()
conversion_rates=data2["conversion_rates"]
PLN=conversion_rates["PLN"]
EUR=conversion_rates["EUR"]
RUB=conversion_rates["RUB"]
print("Kurs pln="+str(PLN))

# initialization
lcd = lcddriver.lcd()

# clearing
lcd.lcd_clear()



# usage
def show_menu():
        global menu_level
        print("Menu level="+str(menu_level))
        if menu_level==0:
            lcd.lcd_display_string(menu_selector[0]+"Data i Godzina      ", 1)
            lcd.lcd_display_string(menu_selector[1]+"Pogoda w Warszawie  ", 2)
            lcd.lcd_display_string(menu_selector[2]+"Kursy walutowe      ", 3)
            lcd.lcd_display_string(menu_selector[3]+"Informacje o RPI    ", 4)
        if menu_level==1:
            now=datetime.now()
            lcd.lcd_display_string("Godzina:            ",1)
            lcd.lcd_display_string(str(now.strftime("%H:%M:%S            ")),2)
            lcd.lcd_display_string("Data:               ",3)
            lcd.lcd_display_string(str(current_date)+"          ",4)
        if menu_level==2:
            lcd.lcd_display_string("Temperatura= " + str(current_temperature) + "C ",1)
            lcd.lcd_display_string("Cisnienie=" + str(current_pressure) + "hPa   ",2)
            lcd.lcd_display_string("Opis: "+str(weather_description)+"     ",3)
            lcd.lcd_display_string("V wiatru=" + str(current_wind_speed) + "m/s   ",4)
        if menu_level==3:
            lcd.lcd_display_string("Cena 1 USD"+"          ",1)
            lcd.lcd_display_string("PLN= "+str(PLN)+"          ",2)
            lcd.lcd_display_string("EUR= "+str(EUR)+"          ",3)
            lcd.lcd_display_string("RUB= "+str(RUB)+"          ",4)
        if menu_level==4:
            cpu = CPUTemperature()
            lcd.lcd_display_string("Temp CPU:           " ,1)
            lcd.lcd_display_string(str(cpu.temperature) + "C                 ",2)
            lcd.lcd_display_string("Lokalny adres IP    ",3)
            lcd.lcd_display_string(socket.gethostbyname(socket.gethostname())+"               ",4)



def menu_selector_representation(i):
    global menu_selector
    menu_selector=[" "," "," "," "]
    menu_selector[i]="*"


def menu_selector_usage():
     while True:
         show_menu()
         next_state=GPIO.input(Next)
         Previous_state=GPIO.input(Previous)
         global menu_selection
         global menu_level
         level_next_state=GPIO.input(Akcept)
         level_previous_state=GPIO.input(Back)
         
         if level_previous_state == False:
             menu_level=0
             time.sleep(0.3)

         if level_next_state == False and menu_selection == 0:
             menu_level=1
             time.sleep(0.3)

         if level_next_state == False and menu_selection == 1:
             menu_level=2
             time.sleep(0.3)

         if level_next_state == False and menu_selection == 2:
             menu_level=3
             time.sleep(0.3)
         if level_next_state == False and menu_selection == 3:
             menu_level=4
             time.sleep(0.3)

         if next_state == False:
             menu_selection+=1
             time.sleep(0.3)
         if Previous_state == False:
            menu_selection-=1
            time.sleep(0.3)
        
         if menu_selection>3:
             menu_selection=0
         if menu_selection<0:
             menu_selection=3
         menu_selector_representation(menu_selection) 
         print("Menu selection="+str(menu_selection))
         
    
         



menu_selector_usage()



