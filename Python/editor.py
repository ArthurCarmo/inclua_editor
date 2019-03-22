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


player = Player.FramePlayer(builder.get_object("fixed_image_grid"), builder.get_object("player_frame"), builder.get_object("player_scrollbar"), builder.get_object("player_progress_label"), frames_dir, 400, 300)

builder.get_object("main_window").connect("destroy", Gtk.main_quit)
builder.get_object("quit").connect("clicked", Gtk.main_quit)
builder.get_object("play").connect("clicked", player.toggle)
# builder.get_object("frame_event_box").connect("button_press_event", player.add_image)
# builder.get_object("file_chooser_box").connect("file_set", new_image_select)

Gtk.main()
sys.exit()
