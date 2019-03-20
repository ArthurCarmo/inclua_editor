#!/usr/bin/python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import GdkPixbuf

class Image() :
	
	def __init__(self, frame, width, height) :
		self.pixbuf = GdkPixbuf.Pixbuf.new_from_file(frame)
		self.resize(width, height)
		
	
	def resize(self, width, height) :
		new_pixbuf = self.pixbuf.scale_simple(width, height, GdkPixbuf.InterpType.BILINEAR)
		pixbuf = new_pixbuf
	
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

			
	def scale_fit_limits(self, max_width = self.width / 3, max_height = self.height / 3) : 
		
		w = self.pixbuf.get_width()
		h = self.pixbuf.get_height()
		
		ratio = w / h
		
		if ratio < 1: 
			h = max_height
			w = ratio * h
		else :
			w = max_width
			h = w / ratio
		
		self.resize(w, h)

	def update(frame, width, height) :
		self.pixbuf = GdkPixbuf.Pixbuf.new_from_file(frame)
		self.resize(width, height)
