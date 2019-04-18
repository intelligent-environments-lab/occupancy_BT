#!/usr/bin/python3.4

#TESTING AUTOUPDATER

import subprocess
import os
import datetime
import operator
import schedule
import csv
import time
import smtplib
import mimetypes
import sys
import json

#Making modifications to the script location

class Scanner:
    running_list = {}
    occupancy = []
    #day = datetime.date.today();f_day = str(day.year)+"-"+str(day.month)+"-"+str(day.day)
    day = datetime.date.today()
    f_day = str(datetime.date.today().year)+"-"+str(datetime.date.today().month)+"-"+str(datetime.date.today().day)
    reboot = False
    full_list = []

    def name(self):
        return open("/home/pi/name",'r').read().rstrip()
    def reset(self): #Really shouldn't be used, as the program will terminate in the morning
        self.running_list.clear()
    def sort(self):
        print 'Sorting...'
        return sorted(self.running_list, key=operator.itemgetter(1))
    def clean(self):
        print 'Cleaning...'
        off = subprocess.Popen('sudo hciconfig hci0 reset',stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
        out,err = off.communicate()
        return None
    def run(self):
        print 'Running...'
        timer = 15
        command = "sudo timeout "+str(timer)+" stdbuf -oL hcitool lescan"
        current = subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
        out,err = current.communicate()
	rawMacs = out.split('\n')
	macs = []
	for a in rawMacs:
    	    macs.append(hash(a))
	return macs

#        return out.split('\n')
    def filt(self,macs):
        print 'Filtering...'
        self.full_list = []
        #This builds a dictionary list of every device in question to avoid duplicates
        temp = {}
        for i in macs[1:len(macs)]:
        #    if i != '':
        #        temp[i[0:17]] = 1
	    if i != 0:
		temp[i] = 1
        #Adds data for histogram approach at volumetric measurement
        timeit = datetime.datetime.now()
        #This line is the full list of mac addresses
        self.full_list = [k for k,v in temp.items()]
        self.full_list.insert(0,str(timeit))

        t = str(timeit),len(temp)
        self.occupancy = t #This adds the tuple containing time and occupancy volume to occupancy list
        #Adds to the running counter of the day
        for k,v in temp.items():
            if k in self.running_list:
                self.running_list[k]+=1
            else:
                self.running_list[k]=1
        return None
    def update(self):
        print "Updating..."
        self.clean()
        self.filt(self.run())
        self.reboot = False
    def write(self,BTD,MAC,RAW):
        print 'Saving...'
        #The following two lines append the current office profile volumetric data to the file
        with open(BTD,'a+') as f:
            writer_1 = csv.writer(f)
            writer_1.writerow(self.occupancy)
        #The following writes a new file every time the system is called, maintaining the most current data format in case of file disruption. Consider adding a file reading mechanism at startup to recover the data in case of power outage
        with open(MAC,'w+') as f:
            writer_2 = csv.writer(f)
            for key, value in self.running_list.items():
                writer_2.writerow([key,value])
        with open(RAW,'a+') as f:
            json.dump(self.full_list,f)
        self.reboot = True #Resets the process of filling data points

if __name__=="__main__":
    #/home/pi/IEL_OCC/Data_Collection/
    script_dir = os.path.expanduser("~")
    dest_dir = os.path.join(script_dir,'/home/pi/DATA')
    print(dest_dir)
    try:
        os.makedirs(dest_dir)
    except OSError:
        pass # already exists
    my_scan = Scanner()
    BTD = os.path.join(dest_dir,'BTD_'+my_scan.name()+'_'+my_scan.f_day+'.csv')
    MAC = os.path.join(dest_dir,'MAC_'+my_scan.name()+'_'+my_scan.f_day+'.csv')
    RAW = os.path.join(dest_dir,'RAW_'+my_scan.name()+'_'+my_scan.f_day+'.csv')

    my_scan.reset() #Cleans the bluetooth ports
    schedule.every(1).minute.do(my_scan.write,BTD,MAC,RAW) #Builds a system scheduler to run every minute
    while True:
        timer = datetime.datetime.now()
        if timer.hour == 23 and timer.minute == 59: #Email everything at midnight
            sys.exit()
        if my_scan.reboot:
            my_scan.update()
        schedule.run_pending()
