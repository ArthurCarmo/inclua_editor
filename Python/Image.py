#!/usr/bin/python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import GdkPixbuf

class Model() :
	
	def __init__(self, frameFile, width = None, height = None) :
		
		self.frameFile = frameFile
		self.pixbuf = None
		if frameFile is not None:
			self.pixbuf = GdkPixbuf.Pixbuf.new_from_file(frameFile)
		
		if height is None:
			if width is not None:
				self.scale_by_width(width)
		else:
			self.scale_fit_limits(width, height)
		
	
	def resize(self, width, height) :
		if self.frameFile is not None :
			self.pixbuf = self.pixbuf.scale_simple(width, height, GdkPixbuf.InterpType.BILINEAR)
			self.pixbuf.get_width(), self.pixbuf.get_height()
	
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
		self.pixbuf
		
		
	def get_size(self) :
		self.pixbuf.get_width(), self.pixbuf.get_height()
	
	def open (self, frameFile, width = None, height = None) :
		self.pixbuf = GdkPixbuf.Pixbuf.new_from_file(frameFile)
		if height is None:
			if width is not None:
				self.scale_by_width(width)
		else:
			self.scale_fit_limits(width, height)
		
	def init_from_file_chooser_box(self, file_chooser_box) :
		self.open(file_chooser_box.get_uri()[7:])
		

class Control(Model) : 
	
	def __init__ (self, frameFile = None, normal_x = 0, normal_y = 0, ini_frame = 0, end_frame = 0, relative_width = None, relative_height = None, widget = None) :
	
		Model.__init__(self, frameFile)
		
		self.normal_x		= normal_x
		self.normal_y		= normal_y
		self.ini_frame 		= ini_frame
		self.end_frame  	= end_frame
		self.relative_width	= relative_width
		self.relative_height	= relative_height
		self.widget 		= widget
		
	
	def shows_in_frame(self, frame_num) :
		return self.ini_frame <= frame_num and frame_num <= self.end_frame
		
	
	def bind_widget(self, widget) :
		self.widget = widget
		
		
	def show(self) :
		if self.widget is not None :
			self.widget.set_from_pixbuf(self.pixbuf)
			self.widget.set_visible(True)
			
	def hide(self) :
		if self.widget is not None :
			self.widget.set_visible(False)
			
	def reload(self) :
		self.pixbuf = GdkPixbuf.Pixbuf.new_from_file(self.frameFile)
		
	def state_copy(self, ImgM) :
	
		self.frameFile		= ImgM.frameFile
		self.pixbuf		= GdkPixbuf.Pixbuf.new_from_file(self.frameFile)
		self.normal_x		= ImgM.normal_x
		self.normal_y		= ImgM.normal_y
		self.ini_frame 		= ImgM.ini_frame
		self.end_frame  	= ImgM.end_frame
		self.relative_width	= ImgM.relative_width
		self.relative_height	= ImgM.relative_height
		if self.widget is not None :
			self.widget.destroy()
			self.widget = None
		
