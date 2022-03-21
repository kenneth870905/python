import asyncio
from threading import Thread
from time import sleep

#every time class

loop = asyncio.get_event_loop()
class EveryTime(Thread):
	def __init__(self,seconds,func):
		super().__init__()
		self.delay = seconds
		self.func = func
		self.is_done = False
	def done(self):
		self.is_done = True
	def run(self):
		while(not self.is_done ):
			try:
				loop.create_task(self.func())
				sleep(self.delay)
			except:
				pass
		print("Thread Done")