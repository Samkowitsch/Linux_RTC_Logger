import os 
import socket
import struct
import sys
import time
import datetime
import sched
import csv

csvFile = "time.csv"
csvHeader = ["NTP" , "RTC" , "SYS"]


def RequestTimefromNtp(addr='0.de.pool.ntp.org'):
	REF_TIME_1970 = 2208988800  # Reference time
	client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	data = b'\x1b' + 47 * b'\0'
	client.sendto(data, (addr, 123))
	data, address = client.recvfrom(1024)
	if data:
        	t = struct.unpack('!12I', data)[10]
        	t -= REF_TIME_1970
	
	ct = time.ctime(t)
	forTime = datetime.datetime.strptime(ct , '%a %b %d %H:%M:%S %Y')
	return forTime.strftime('%H:%M:%S')


def getHwclock():
	hwclock = os.popen('hwclock -r').read()
	ts = hwclock.split()[1]
	ts = ts.split('.')[0]
	return ts



def getSystemTime():
	t = time.localtime()
	current_time = time.strftime("%H:%M:%S" , t)
	return current_time

	
def getTimeStamps(timeScheduler):
	timeScheduler.enter(60 , 1 , getTimeStamps , (timeScheduler ,))
	print("Get Timestamp from NTP , RTC and System")
	start = time.time()
	ntpTime = RequestTimefromNtp()
	rtcTime = getHwclock()
	sysTime = getSystemTime()
	end = time.time()
	print("NTP : " , ntpTime , " RTC : " , rtcTime , " SYS : " , sysTime , " Runtime : " , end - start)

	data = [ntpTime , rtcTime , sysTime]
	
	if not (os.path.isfile(csvFile)):
		print("Create new file with header")
		with open(csvFile , 'w') as f:
			writer = csv.writer(f)
			writer.writerow(csvHeader)
 

	with open(csvFile , 'a') as f:
		writer = csv.writer(f)
		writer.writerow(data)


if __name__ == "__main__":
	print("RTC Test script")
	timeScheduler = sched.scheduler(time.time , time.sleep)
	timeScheduler.enter(0 , 1 , getTimeStamps , (timeScheduler,))
	timeScheduler.run() 

