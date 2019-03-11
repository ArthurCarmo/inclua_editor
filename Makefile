teste_ui : main.c file_counter.o
	gcc -o teste2_ui main.c `pkg-config --cflags --libs gtk+-3.0` file_counter.o
	
file_counter.o : file_counter.c
	gcc -c file_counter.c
	
clean :
	rm *.o
