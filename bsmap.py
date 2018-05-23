from utils import *
from clipmode import clipmode
import os

class Bsmap()

	def check(self):
		if not toolcheck('bsmap -h'):
			return False,'BSMAP not found!'
		if os.path.exists('BAM_FILE'):
			return False,'"BAM_FILE" exists! Please delete "BAM_FILE"'
		os.mkdir("BAM_FILE")
		return True,''

	def clipping(self,filenames,param={}):
		result = clipmode(filenames,param)
