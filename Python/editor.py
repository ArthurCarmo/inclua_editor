#!/usr/bin/python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import sys
import file_counter as fc

import Player
import Image as Img

frames_dir = "../img/demo_screenshots/"

curr_frame = 0
last_frame = fc.frame_counter(frames_dir)
progress_label_width = 2 * fc.ndigits(last_frame) + 2;

# Objeto que recupera os widgets do arquivo xml
builder = Gtk.Builder()	
try:
	builder.add_from_file("../ui_file2.ui")
except:			
	print("File not found")
	sys.exit()

def append_image (widget, event, player, new_image) :
	print ("(%d, %d)" % (event.x, event.y))
	
	if new_image is None :
		print("Selecione uma imagem")
		return True
	
def set_merger_window(widget, merger, player) :
	player.pause()
	merger.copy_state(player)
	merger.show()


new_image = Img.AppendImage()

player = Player.FramePlayer(builder.get_object("main_window"), builder.get_object("player_fixed_image_grid"), builder.get_object("player_frame"), builder.get_object("player_progress_bar"), builder.get_object("player_progress_label"), frames_dir, 400, 300)
merger = Player.FramePlayer(builder.get_object("merger_window"), builder.get_object("merger_fixed_image_grid"), builder.get_object("merger_frame"), builder.get_object("merger_progress_bar"), builder.get_object("merger_progress_label"), frames_dir, 400, 300)

builder.get_object("main_window").connect("destroy", Gtk.main_quit)
builder.get_object("main_quit_button").connect("clicked", Gtk.main_quit)
builder.get_object("main_play_button").connect("clicked", player.toggle)
builder.get_object("main_file_chooser_box").connect("file_set", new_image.init_from_file_chooser_box)
builder.get_object("main_open_merger_button").connect("clicked", set_merger_window, merger, player)

builder.get_object("merger_window").connect("delete-event", merger.hide)
builder.get_object("merger_frame_event_box").connect("button_press_event", append_image, merger, new_image)
builder.get_object("merger_cancel_button").connect("clicked", merger.hide)

Gtk.main()
sys.exit()
