#!/usr/bin/python3

import file_counter as fc
import Image as Img
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class framePlayer () :

	def __init__(self, framesDir, width = 533, height = 300, width_margin_ratio  = 0.95, height_margin_ratio = 0.95) :
	
		self.curr_frame = 0
		self.last_frame = fc.frame_counter(framesDir)

		self.playing			= 0
		self.playing_thread		= 0
		
		self.progress_label_width	= 2 * fc.ndigits(self.last_frame) + 2
		self.progress_label_text	= "%d/%d" % (self.curr_frame+1, self.last_frame+1)
		
#		self.width			= self.widget.get_width()
#		self.height			= self.widget.get_height()
	
		self.frame = Img.Image(framesDir + "frame_%d.png" % self.curr_frame, self.width * self.width_margin_ratio, self.height * self.height_margin_ratio)
		
	def toggle(self) : 
		if self.playing:
			self.pause()
		else:
			self.play()
			
	def stop(self) :
		self.pause();
		self.move_to_frame(0)
		
	def pause(self) :
		if self.playing == 1:
			gobject.source_remove(self.playing_thread)
			
	def play(self) :
		if self.playing == 0:
			self.playing_thread = gobject.timeout_add(1000.0 / 30, next_frame())
	
	def next_frame(self) :
		self.curr_frame += 1
		if self.curr_frame > self.last_frame :
			self.curr_frame = 0
			return False
		self.refresh()
		return True
	
	def prev_frame(self) :
		self.curr_frame -= 1
		if self.curr_frame < 0 :
			self.curr_frame = self.last_frame
			return False
		self.refresh()
		return True
		
	def move_to_frame(self, frame) :
		curr_frame = min(max(frame, 0), last_frame)
		self.refresh()
		
	def refresh(self) :
		self.progress_label_text = "%d/%d" % (self.curr_frame+1, self.last_frame+1)
		self.frame = Frame.Frame(self.framesDir + "frame_%d.png" % self.curr_frame)

		
