import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import GdkPixbuf
import Image as Img

class ListHandler() :
	
	def __init__ (self, widget = None) :
		self.images = []
		self.sorting = "ini_crescent" 
	
	
	def add(self, image) :
		self.images.append(image)
		if self.sorting == "ini_crescent" :
			self.images.sort(key=lambda img : img.ini_frame)
		elif self.sorting == "ini_decrescent" :
			self.images.sort(key=lambda img : img.ini_frame, reverse=True)
		elif self.sorting == "end_crescent" :
			self.images.sort(key=lambda img : img.end_frame)
		elif self.sorting == "end_decrescent" :
			self.images.sort(key=lambda img : img.end_frame, reverse=True)
			
			
	def rm(self, index) :
		self.images.pop(index)
			
