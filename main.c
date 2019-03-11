#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#include <gtk/gtk.h>

extern int count_files(const char *);
extern int ndigits(int);

// Controle do player
guint thread_Id;
GObject *scrollbar; 
GObject *progress_label;
GObject *fixed;

char progress_label_text[400];
int progress_label_width = 0;
int playing;

// Frame que será mostrado
GObject *frame;
GObject *event_box;
GObject *added_img;

char pic_filename[5000];
char added_img_path[5000] = "/home/arthur/Documentos/inclua_editor/teste_img_2.jpg";
const char *frames_dir="/home/arthur/.config/unity3d/LAViD/VLibrasVideoMaker/t_beta_01/";
int curr_frame = 0;
int last_frame;

#define ORIGINAL_PNG_WIDTH  800
#define ORIGINAL_PNG_HEIGHT 600

gint frame_winW  = 800 * 2 / 3 * 0.95;
gint frame_winH  = 600 / 2     * 0.95;
gint canvas_winW = 800 * 2 / 3;
gint canvas_winH = 600 / 2;
gint added_imgW = 0;
gint added_imgH = 0;

gdouble frameW_margin = 0.95;
gdouble frameH_margin = 0.95;

static void update_progress_label() {

	sprintf(progress_label_text, "%d/%d", curr_frame+1, last_frame+1);
	gtk_label_set_text( GTK_LABEL(progress_label), progress_label_text );
	
}

static void update_frame() { 
	
	GError *error = NULL;
	GdkPixbuf *pixbuf;
	GdkPixbuf *new_pixbuf;

	sprintf(pic_filename, "%sframe_%d.png", frames_dir, curr_frame);
	
	pixbuf = gdk_pixbuf_new_from_file(pic_filename, &error);
	if(pixbuf == NULL) {
		g_printerr("%s\n", error->message);
		g_clear_error( &error );
		exit(EXIT_FAILURE);
	}
	
	new_pixbuf = gdk_pixbuf_scale_simple(pixbuf, frame_winW, frame_winH, GDK_INTERP_BILINEAR);
	gtk_image_set_from_pixbuf(GTK_IMAGE(frame), new_pixbuf);
	
}

static int next_frame() {

	if(++curr_frame > last_frame) {
		curr_frame = 0;
		update_frame();
		return 0;
	}
	
	update_frame();
	return 1;
	
}

static int prev_frame() {

	if(--curr_frame < 0) {
		curr_frame = last_frame;
		update_frame();
		return 0;
	}
	
	update_frame();
	return 1;
	
}

static gboolean handle_player( ) {
	
	if (playing == 0) {
		g_source_remove(thread_Id);
		thread_Id = 0;
		return FALSE;
	}
	
	playing = next_frame();
	gtk_range_set_value(GTK_RANGE(scrollbar), curr_frame);
	
	return playing?TRUE:FALSE;
	
}

static void play_function (GtkWidget *widget, gpointer user_data) {

	playing = 1 - playing;
	thread_Id = g_timeout_add(33, handle_player, NULL);

}

static void move_to_frame(GtkWidget *widget, gpointer user_data) { 

	curr_frame = (int) (gtk_range_get_value(GTK_RANGE(widget)) + 0.5);
	update_frame();
	update_progress_label();

}

void set_4by3_ratio() {

	gint w, h;
	
	if(frame_winW < frame_winH) {
		h = 3 * frame_winW / 4;
		w = frame_winW;
	} else {
		h = frame_winH;
		w = 4 * frame_winH / 3;
		if(w > frame_winW) {
			h = 3 * frame_winW / 4;
			w = frame_winW;
		}
	}

	frame_winW = w;
	frame_winH = h;
	
}

void center_image() {

	gtk_fixed_move(GTK_FIXED(fixed), GTK_WIDGET(event_box), (canvas_winW - frame_winW) / 2, (canvas_winH - frame_winH) / 2);

}

static void set_fixed_children_dim(GtkWidget *widget, GdkRectangle *allocate, gpointer user_data) { 

	canvas_winW = allocate->width;
	canvas_winH = allocate->height;

	frame_winW = allocate->width * frameW_margin;
	frame_winH = allocate->height * frameH_margin;
	
	set_4by3_ratio();
	center_image();
	update_frame(); 
	
}

static void frame_clicked(GtkWidget *widget, GdkEventButton *event, gpointer user_data) {
	
	gdouble x_coord, y_coord;

	x_coord = event->x;
	y_coord = event->y;

	gtk_fixed_move(GTK_FIXED(fixed), GTK_WIDGET(added_img), (canvas_winW - frame_winW + added_imgW) / 2, y_coord);
	gtk_widget_set_visible(GTK_WIDGET(added_img), !gtk_widget_is_visible(GTK_WIDGET(added_img))); 	
	
	g_print("(%lf, %lf)\n", x_coord, y_coord);

}

static void set_added_img(GtkFileChooserButton *chooser_button, gpointer user_data) {

	GError *error = NULL;
	GdkPixbuf *pixbuf;
	GdkPixbuf *new_pixbuf;
	
	gint oldW, oldH;
	gint newW, newH;
	gdouble ratio;

	pixbuf = gdk_pixbuf_new_from_file(gtk_file_chooser_button_get_title(chooser_button), &error);
	if(pixbuf == NULL) {
		g_printerr("%s\n", error->message);
		g_clear_error( &error );
		exit(EXIT_FAILURE);
	}
	
	oldW = gdk_pixbuf_get_width(pixbuf);
	oldH = gdk_pixbuf_get_height(pixbuf);
	
	ratio = oldW / oldH;
	
	if(oldW <= frame_winW / 4 && oldH <= frame_winH / 4) {

		newW = oldW;
		newH = oldH;

	} else { 

		if(ratio < 1) { 

			newW = frame_winW / 4;
			newH = newW * ratio;

		} else {

			newH = frame_winH / 4;
			newW = oldW / ratio;

		}

	}
	
	added_imgW = newW;
	added_imgH = newH;
	
	new_pixbuf = gdk_pixbuf_scale_simple(pixbuf, newW, newH, GDK_INTERP_BILINEAR);
	gtk_image_set_from_pixbuf(GTK_IMAGE(added_img), new_pixbuf);	
	
}


// Inicializadores
int main (int argc, char *argv[]) {
	
	GtkBuilder *builder;
	GObject *window;
	GObject *button;
	GObject *file_chooser_box;
	
	GError *error = NULL;
	
	last_frame = count_files(frames_dir) - 1;
	
	gtk_init (&argc, &argv);
	
	builder = gtk_builder_new();
	
	if(gtk_builder_add_from_file(builder, "ui_file2.ui", &error) == 0) {
		g_printerr("%s\n", error->message);
		g_clear_error( &error );
		return 1;
	}


	// Winwdow
	window = gtk_builder_get_object(builder, "main_window");
	g_signal_connect(window, "destroy", G_CALLBACK(gtk_main_quit), NULL);
		
	
	// Buttons
	button = gtk_builder_get_object(builder, "play");
	g_signal_connect(button, "clicked", G_CALLBACK(play_function), NULL);
	
	
	button = gtk_builder_get_object(builder, "quit");
	g_signal_connect(button, "clicked", G_CALLBACK(gtk_main_quit), NULL);


	// Scroll bar
	scrollbar = gtk_builder_get_object(builder, "player_scrollbar");
	g_signal_connect(scrollbar, "value_changed", G_CALLBACK(move_to_frame), NULL);
		
	gtk_range_set_range(GTK_RANGE(scrollbar), 0.0, (gdouble) last_frame);
	

	// Progress label
	progress_label = gtk_builder_get_object(builder, "player_progress_label");
	
	progress_label_width = 2 * ndigits(last_frame) + 2;
	gtk_label_set_width_chars(GTK_LABEL(progress_label), progress_label_width);
	
	update_progress_label();
	

	// File chooser box
	file_chooser_box = gtk_builder_get_object(builder, "file_chooser_box");
	g_signal_connect(file_chooser_box, "file_set", G_CALLBACK(set_added_img), NULL);
	
	
	// Fixed
	fixed = gtk_builder_get_object(builder, "fixed_image_grid");
	g_signal_connect(fixed, "size_allocate", G_CALLBACK(set_fixed_children_dim), NULL);
	
	
	// Event box
	frame_winW = 400;
	frame_winH = 300;
	
	event_box = gtk_builder_get_object(builder, "frame_event_box");
	g_signal_connect(event_box, "button_press_event", G_CALLBACK(frame_clicked), NULL);
	
	
	// Picture
	frame = gtk_builder_get_object(builder, "player_frame");
	sprintf(pic_filename, "%sframe_%d.png", frames_dir, curr_frame);	
	
	
	// Imagem a adicionar
	added_img = gtk_builder_get_object(builder, "added_img");

	center_image();
	set_4by3_ratio();
	update_frame();
	
	gtk_main();

	return 0;

}
