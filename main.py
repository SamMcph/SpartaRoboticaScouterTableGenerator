from __future__ import print_function
import csv

import time
import tbaapiv3client
from pprint import pprint
import matplotlib.pyplot as plt 
import json 
from tkinter import *
import customtkinter
from tkinter import StringVar
f = open('key.json')
data = json.load(f)
api_key = data["key"]
customtkinter.set_appearance_mode("dark") 
customtkinter.set_default_color_theme("blue") 
#creates the window 
win = customtkinter.CTk()
win.geometry("300x400")
win.title('Scouting Application')
def get_alliance_color(alliances,team_key):
    for i in range(len(alliances.blue.team_keys)):
        if team_key == alliances.blue.team_keys[i]:
            return "blue"
    return "red"
def get_alliance_numbers(alliances,alliance_color):
    alliance_list =""
    if alliance_color=="blue":
        for i in range(len(alliances.blue.team_keys)):
            team_num= alliances.blue.team_keys[i].split("c")[1]
            alliance_list += team_num+", "
    else:
         for i in range(len(alliances.red.team_keys)):
            team_num= alliances.red.team_keys[i].split("c")[1]
            alliance_list += team_num+", "
    return alliance_list
class window():
    def __init__(self):
        configuration = tbaapiv3client.Configuration(
            host = "https://www.thebluealliance.com/api/v3",
            api_key = {
                'X-TBA-Auth-Key': api_key
            }
        )

        with tbaapiv3client.ApiClient(configuration) as api_client:
            self.api_instance = tbaapiv3client.EventApi(api_client)
        self.game_text= StringVar()
        self.output_text=""
        self.game_text.set(self.output_text)
        self.gameslabel =  customtkinter.CTkLabel(win,textvariable =self.game_text)    
        self.gameslabel.place(x=1100 ,y=5)
        self.choice = customtkinter.StringVar(value="Regional")
        optionmenu = customtkinter.CTkOptionMenu(win, values=["Colorado", "Utah"],variable=self.choice)
        optionmenu.place(x=25,y=75)
        self.colorado = '2023code' 
        self.utah = '2023utwv'
        self.event_key="2023code"
        self.team_num="3648"
    def get_regional(self):
        if self.choice.get() =="Utah":
            self.event_key = self.utah
        elif self.choice.get() =="Colorado":
            self.event_key = self.colorado
    def generate_data(self):
        self.team_num = textbox.get("0.0", "end").rstrip()
        textbox.delete("0.0", "end") 
        team_key = "frc"+self.team_num
        self.get_regional()
        team_key = "frc"+self.team_num
        api_response = self.api_instance.get_team_event_matches(team_key,self.event_key)
        self.fields = ["Team Numer","Match Number","Alliance Teams","Alliance Color","Score","Alliance Winner",]
        self.rows = []
        for i in range(len(api_response)):
            winning= api_response[i].winning_alliance
            match_num = api_response[i].match_number
            alliances = api_response[i].alliances
            alliance_color = get_alliance_color(alliances,team_key)
            alliance_teams = get_alliance_numbers(alliances,alliance_color)
            self.rows.append([self.team_num,match_num,alliance_teams,alliance_color,f"red: {str(alliances.red.score)} - blue: {str(alliances.blue.score)}",
                        winning])
    def generate_text(self):
        self.generate_data()
        fig, ax = plt.subplots() 
        ax.set_axis_off() 
        print(len(self.rows))
        print(len(self.fields))
        table = ax.table( 
            cellText = self.rows,  
            colLabels = self.fields,
            colColours =["palegreen"] * 6,
            cellLoc ='center',  
            loc ='center')
        table.set_fontsize(25)
        table.scale(1.5, 1.5)
        plt.show()

    def generate_csv(self):
        self.generate_data()
        with open("writablecsv.csv", 'w') as csvfile: 
            csvwriter = csv.writer(csvfile) 
            csvwriter.writerow(self.fields) 
            csvwriter.writerows(self.rows)
    

textbox = customtkinter.CTkTextbox(win, width=200, height=10)
textbox.place(x=25,y=25)
window_class = window()
team_num_label = customtkinter.CTkLabel(win, text="Team Number", width=20 ,height=1)
team_num_label.place(x=75,y=3)
generate_button = customtkinter.CTkButton(win,text="Generate",command=window_class.generate_text)
generate_button.place(x=25,y=125)

generate_csv_button = customtkinter.CTkButton(win,text="Generate CSV", command=window_class.generate_csv)
generate_csv_button.place(x=25,y=175)

win.mainloop()
