#!/usr/bin/python3

import file_counter as fc
import Image as Img
import ImageList as ImgList

from gi.repository import GObject as gobject

class Model () :

	def __init__(self, framesDir, width = 533, height = 300, width_margin_ratio  = 0.95, height_margin_ratio = 0.95) :
	
		self.framesDir			= framesDir
	
		self.width			= width
		self.height			= height

		self.width_margin_ratio		= width_margin_ratio
		self.height_margin_ratio	= height_margin_ratio
	
		self.win_width			= self.width * self.width_margin_ratio
		self.win_height 		= self.height * self.height_margin_ratio
	
		self.curr_frame 		= 0
		self.last_frame 		= fc.frame_counter(framesDir) - 1

		self.playing			= 0
		self.playing_thread		= 0
		
		self.progress_label_width	= 2 * fc.ndigits(self.last_frame) + 2
		self.progress_label_text	= "%d/%d" % (self.curr_frame+1, self.last_frame+1)
		
		self.appended_images 		= ImgList.Model()
		
				
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



	def append_image(self, image, x_global_coord, y_global_coord, ini_frame, end_frame, target_width = 0.34, target_height = 0.5, widget = None) : 
		self.appended_images.add(Img.Control(image, x_global_coord / self.win_width, y_global_coord / self.win_height, max(ini_frame, 0), min(end_frame, self.last_frame), max(min(1, target_width), 0.1), max(min(1, target_height), 0.1), widget))


	def width_margin (self) :
		return (self.width - self.win_width) / 2
	
	
	def height_margin (self) :
		return (self.height - self.win_height) / 2


import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class Control(Model): 

	def __init__ (self, window, canvasFixed, frameWidget, progress_bar, progress_label, framesDir, width = 533, height = 300, width_margin_ratio  = 0.95, height_margin_ratio = 0.95) :
	
		Model.__init__(self, framesDir, width, height, width_margin_ratio, height_margin_ratio )
		
		
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
		
		if self.window.is_visible():
			allocation = canvasFixed.get_allocation()
			self.width  = allocation.width
			self.height = allocation.height
			
			self.win_width	= self.width * self.width_margin_ratio
			self.win_height = self.height * self.height_margin_ratio
			self.frameWidget.set_from_pixbuf(Img.Model(self.framesDir + "frame_%d.png" % self.curr_frame, self.win_width, self.win_height).pixbuf)
			
			self.win_width = self.frameWidget.get_pixbuf().get_width()
			self.win_height = self.frameWidget.get_pixbuf().get_height()
			
			self.center_frame()
			self.refresh()
	
	
	def get_new_frame(self, widget) :
		self.move_to_frame(round(widget.get_value()))
		
	
	def center_frame(self) :
		
		if self.window.is_visible() :
			c = self.canvasFixed.get_allocation()
			self.win_width = self.frameWidget.get_pixbuf().get_width()
			self.win_height = self.frameWidget.get_pixbuf().get_height()
		
			self.canvasFixed.move(self.frameWidget.get_parent(), (c.width - self.win_width) / 2, (c.height - self.win_height) / 2)
		
		
	def resize_and_center(self, widget, allocation) :
		if self.window.is_visible() :

			self.width  = allocation.width
			self.height = allocation.height
			
			self.win_width	= self.width * self.width_margin_ratio
			self.win_height = self.height * self.height_margin_ratio
			
			self.frameWidget.set_from_pixbuf(Img.Model(self.framesDir + "frame_%d.png" % self.curr_frame, self.win_width, self.win_height).pixbuf)
			
			self.win_width = self.frameWidget.get_pixbuf().get_width()
			self.win_height = self.frameWidget.get_pixbuf().get_height()
			
			for img in self.appended_images.images :
				if img.widget is not None:
					img.reload()
					
			self.center_frame()
		
	def refresh(self) :
		if self.window.is_visible() :
			self.progress_bar.set_value(self.curr_frame)
			self.progress_label.set_text("%d/%d" % (self.curr_frame+1, self.last_frame+1))
			self.frameWidget.set_from_pixbuf(Img.Model(self.framesDir + "frame_%d.png" % self.curr_frame, self.win_width, self.win_height).pixbuf)
			
			for img in self.appended_images.images :
				if img.widget is not None :
					if not img.shows_in_frame(self.curr_frame) :
						img.hide()
					else :
						self.canvasFixed.move(img.widget, self.win_width * img.normal_x + self.width_margin(), self.win_height * img.normal_y + self.height_margin())
						img.scale_fit_limits(img.relative_width * self.win_width, img.relative_height * self.win_height)
						img.show()

	
	def show(self, width = 350, height = 500) :
		self.window.set_default_size(width, height)
		self.window.set_visible(True)
		self.refresh()
		return True
		
		
	def hide(self, widget, event = None) :
		self.window.set_visible(False)
		return True
		
	
	def copy_appended_images(self, pHandler) :
		self.appended_images.clear()
		for img in pHandler.appended_images.images :
			new_img = Img.Control()
			new_img.state_copy(img)
			if img.widget is not None :
				new_img.bind_widget(self.add_image_widget())
			self.appended_images.add(new_img)
		
		
	def copy_state(self, pHandler) :
		
		self.stop()
		
		self.framesDir			= pHandler.framesDir

		self.curr_frame 		= pHandler.curr_frame
		self.last_frame 		= pHandler.last_frame

		self.playing			= 0
		self.playing_thread		= 0
		
		self.progress_label_width	= pHandler.progress_label_width
		self.progress_label_text	= pHandler.progress_label_text
		
		self.copy_appended_images(pHandler)
		
	
	def capture_state(self, widget, player) :
		player.pause()
		self.copy_state(player)
		self.show()
	
		
	def add_image_widget(self) :
			new_widget = Gtk.Image()
			new_widget.set_visible(False)
			self.canvasFixed.put(new_widget, 0, 0)
			return new_widget
			
		
	def bind_image_widget(self, imgWidget, index) :
		self.appended_images[index].bind_widget(imgWidget)
		
	
