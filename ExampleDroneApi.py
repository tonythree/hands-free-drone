from DroneApi import DroneApi
from threading import Thread
from multiprocessing import Process
import time

def runDroneApi():
	droneapi = DroneApi()
	droneapi.run()

def main():
	Process(target=runDroneApi).start()

	while not droneapi.should_stop:
		time.sleep(1)

if __name__ == '__main__':
	main()