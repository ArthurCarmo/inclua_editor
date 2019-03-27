#!/usr/bin/python3

# Esse arquivo faz a conexão dos sinais dos widgets às funções callback,
# atribui os widgets aos objetos de controle e inicializa a janela principal do programa

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import sys
import file_counter as fc

import Player
import Image as Img


#def append_image (widget, event, player, new_image) :
#	print ("(%d, %d)" % (event.x, event.y))
	
#	if new_image is None :
#		print("Selecione uma imagem")
#		return True


# Objeto que recupera os widgets do arquivo xml
builder = Gtk.Builder()	
try:
	builder.add_from_file("../ui_file2.ui")
except:			
	print("File not found")
	sys.exit()

frames_dir = "../img/demo_screenshots/"

# Widgets do player principal e do player de edição
player = Player.Control(builder.get_object("main_window"), builder.get_object("player_fixed_image_grid"), builder.get_object("player_frame"), builder.get_object("player_progress_bar"), builder.get_object("player_progress_label"), frames_dir, 400, 300)
merger = Player.Control(builder.get_object("merger_window"), builder.get_object("merger_fixed_image_grid"), builder.get_object("merger_frame"), builder.get_object("merger_progress_bar"), builder.get_object("merger_progress_label"), frames_dir, 400, 300)

# Atribuição das 
builder.get_object("main_window").connect("destroy", Gtk.main_quit)
builder.get_object("main_quit_button").connect("clicked", Gtk.main_quit)
builder.get_object("main_play_button").connect("clicked", player.toggle)
#builder.get_object("main_file_chooser_box").connect("file_set", Img.Control.init_from_file_chooser_box)
builder.get_object("main_open_merger_button").connect("clicked", merger.capture_state, player)

builder.get_object("merger_window").connect("delete-event", merger.hide)
# builder.get_object("merger_frame_event_box").connect("button_press_event", append_image, merger, new_image)
builder.get_object("merger_cancel_button").connect("clicked", merger.hide)

# Imagem teste para aparecer entre os frames 20 e 45
t_img = "../img/test_img_1.jpg"
player.append_image(t_img, 0, 0, 20, 45, 0.34, 0.5, builder.get_object("player_new_image"))

#print(player.appended_images.images[0].show())

Gtk.main()
sys.exit()
