#!/usr/bin/python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import sys
import file_counter as fc


frames_dir = "../img/demo_screenshots/"

curr_frame = 0
last_frame = fc.frame_counter(frames_dir)
progress_label_width = 2 * fc.ndigits(last_frame) + 2;

print (last_frame)

# Objeto que recupera os widgets do arquivo xml
builder = Gtk.Builder()	
try:
	builder.add_from_file("../ui_file2.ui")
except:			
	print("File not found")
	sys.exit()

# Window callbacks
def window_resize_correction(window):
	print("%dx%d" % (window.get_size()))
# Picture callbacks

# Player callbacks

main_window = builder.get_object("main_window")
main_window.connect("destroy", Gtk.main_quit)
main_window.connect("check_resize", window_resize_correction)

Gtk.main()
sys.exit()
