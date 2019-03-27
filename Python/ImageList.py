#!/usr/bin/python3

# Classe Model é um gerenciador de lista específico para a classe Image.Control

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import GdkPixbuf
import Image as Img

class Model() :
	
	def __init__ (self) :
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
		if self.images[index].widget is not None :
			self.images[index].widget.destroy()
		self.images.pop(index)
			
	
	def clear(self) :
		for i in range(len(self.images)):
			self.rm(i)
		self.sorting = "ini_crescent"
	
