#!/usr/bin/python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import GdkPixbuf

class Image() :
	
	def __init__(self, frameFile, width = None, height = None) :
		self.frameObject = 1
		self.pixbuf = GdkPixbuf.Pixbuf.new_from_file(frameFile)
		
		if height is None:
			if width is not None:
				self.scale_by_width(width)
		else:
			self.scale_fit_limits(width, height)
			
		
	
	def resize(self, width, height) :
		self.pixbuf = self.pixbuf.scale_simple(width, height, GdkPixbuf.InterpType.BILINEAR)
	
	
	def scale_by_factor(self, factor) :
		self.resize(width * factor, height * factor)
		
	
	def scale_by_width(self, width) : 
		w = self.pixbuf.get_width()
		h = self.pixbuf.get_height()
		ratio = w / h;
		
		w = width
		h = w / ratio
		self.resize(w, h)
		
	
	def scale_by_height(self, height) :
		w = self.pixbuf.get_width()
		h = self.pixbuf.get_height()
		ratio = w / h;
		
		h = height
		w = h * ratio
		self.resize(w, h)

			
	def scale_fit_limits(self, max_width, max_height) : 
		w = self.pixbuf.get_width()
		h = self.pixbuf.get_height()
		
		ratio = w / h
		
		if(max_width < max_height) : 
			w = max_width
			h = w / ratio
		else :
			h = max_height
			w = h * ratio
			
			if(w > max_width) :
				w = max_width
				h = w / ratio

		self.resize(w, h)

	def update(self, frameFile, width, height) :
		self.pixbuf = GdkPixbuf.Pixbuf.new_from_file(frameFile)
		self.resize(width, height)
		
		
	def set_image(self,image) :
		w = self.pixbuf.get_width()
		h = self.pixbuf.get_height()
		self.pixbuf = image.get_pixbuf()
		self.scale_fit_limits(w, h)
	
	
	def get_pixbuf(self) :
		return self.pixbuf
		
		
	def get_size(self) :
		return self.pixbuf.get_width(), self.pixbuf.get_height()
		
		
class AppendImage(Image) : 
	
	def __init__ (self, frameFile, x_position = 0, y_position = 0, target_width = None, target_height = None) :
	
		Image.__init__(self, frameFile, target_width, target_height)

