#!/usr/bin/python3

import file_counter as fc
import Image as Img

from gi.repository import GObject as gobject

class PlayerHandler () :

	def __init__(self, framesDir, width = 533, height = 300, width_margin_ratio  = 0.95, height_margin_ratio = 0.95) :
	
		self.framesDir			= framesDir
	
		self.width			= width
		self.height			= height

		self.width_margin_ratio		= width_margin_ratio
		self.height_margin_ratio	= height_margin_ratio
	
		self.curr_frame 		= 0
		self.last_frame 		= fc.frame_counter(framesDir) - 1

		self.playing			= 0
		self.playing_thread		= 0
		
		self.progress_label_width	= 2 * fc.ndigits(self.last_frame) + 2
		self.progress_label_text	= "%d/%d" % (self.curr_frame+1, self.last_frame+1)
		
		self.layered_images = [ ] # Lista que associam imagens a intervalos
		
				
	def toggle(self, button = None) : 
	
		if button is not None :
			if button.get_label() == "Play!" :
				button.set_label("Pause!")
			elif button.get_label() == "Pause!" :
				button.set_label("Play!")
		
		if self.playing:
			self.pause()
		else:
			self.play()
			
			
	def stop(self) :
		self.pause()
		self.playing = 0
		self.move_to_frame(0)
		
		
	def pause(self, button = None) :
		if self.playing == 1:
			gobject.source_remove(self.playing_thread)
			self.playing = 0
			
			
	def play(self) :
		if self.playing == 0:
			self.playing_thread = gobject.timeout_add(1000.0 / 30, self.next_frame)
			self.playing = 1;
			
	
	def next_frame(self) :
		self.curr_frame += 1
		if self.curr_frame > self.last_frame :
			self.stop()
			return False
		self.refresh()
		return True
	
	
	def prev_frame(self) :
		self.curr_frame -= 1
		if self.curr_frame < 0 :
			self.stop()
			return False
		self.refresh()
		return True
		
		
	def move_to_frame(self, frame) :
		self.curr_frame = min(max(frame, 0), self.last_frame)
		self.refresh()
		
		
	def refresh(self) :
		self.progress_label_text = "%d/%d" % (self.curr_frame+1, self.last_frame+1)
		
	def copy_state(self, pHandler) :
		
		self.stop()
		
		self.framesDir			= pHandler.framesDir

		self.curr_frame 		= pHandler.curr_frame
		self.last_frame 		= pHandler.last_frame

		self.playing			= 0
		self.playing_thread		= 0
		
		self.progress_label_width	= pHandler.progress_label_width
		self.progress_label_text	= pHandler.progress_label_text
		
		self.layered_images		= pHandler.layered_images



import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class FramePlayer(PlayerHandler): 

	def __init__ (self, window, canvasFixed, frameWidget, progress_bar, progress_label, framesDir, width = 533, height = 300, width_margin_ratio  = 0.95, height_margin_ratio = 0.95) :
	
		PlayerHandler.__init__(self, framesDir, width, height, width_margin_ratio, height_margin_ratio )
		
		
		self.window		= window
		self.canvasFixed	= canvasFixed		
		self.frameWidget	= frameWidget
		self.progress_bar 	= progress_bar
		self.progress_label	= progress_label
		
		self.canvasFixed.connect("size_allocate", self.resize_and_center)
		self.progress_bar.connect("value_changed", self.get_new_frame)
		
		self.progress_label.set_width_chars(self.progress_label_width)
		self.progress_label.set_text("%d/%d" % (self.curr_frame+1, self.last_frame+1))
		self.progress_bar.set_range (0, self.last_frame)
		
		self.width	= width
		self.height	= height
		
		if self.window.is_visible():
			allocation = canvasFixed.get_allocation()
			self.width  = allocation.width
			self.height = allocation.height
			self.frameWidget.set_from_pixbuf(Img.Image(self.framesDir + "frame_%d.png" % self.curr_frame, self.width * self.width_margin_ratio, self.height * self.height_margin_ratio).pixbuf)
			self.center_frame()
	
	
	def get_new_frame(self, widget) :
		self.move_to_frame(round(widget.get_value()))
		
	
	def center_frame(self) :
		
		if self.window.is_visible() :
		
			c = self.canvasFixed.get_allocation()
			f_width = self.frameWidget.get_pixbuf().get_width()
			f_height = self.frameWidget.get_pixbuf().get_height()
		
			self.canvasFixed.move(self.frameWidget.get_parent(), (c.width - f_width) / 2, (c.height - f_height) / 2)
		
		
	def resize_and_center(self, widget, allocation) :
	
		if self.window.is_visible() :
		
			self.width  = allocation.width
			self.height = allocation.height
			
			self.frameWidget.set_from_pixbuf(Img.Image(self.framesDir + "frame_%d.png" % self.curr_frame, self.width * self.width_margin_ratio, self.height * self.height_margin_ratio).pixbuf)
			
			self.center_frame()
		
		
	def refresh(self) :
		
		if self.window.is_visible() :
			self.progress_label.set_text("%d/%d" % (self.curr_frame+1, self.last_frame+1))
			self.progress_bar.set_value(self.curr_frame)
			self.frameWidget.set_from_pixbuf(Img.Image(self.framesDir + "frame_%d.png" % self.curr_frame, self.width * self.width_margin_ratio, self.height * self.height_margin_ratio).pixbuf)
		
	
	def show(self, width = 350, height = 500) :
		self.window.set_default_size(width, height)
		self.window.set_visible(True)
		self.refresh()
		return True
		
		
	def hide(self, widget, event = None) :
		self.window.set_visible(False)
		return True
		

