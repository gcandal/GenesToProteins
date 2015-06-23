BIN_DIR=bin
clean:
	rm -f -r $(BIN_DIR)
make: clean
	mkdir $(BIN_DIR)
	gcc -o transform main.c -l sqlite3.0
	mv transform $(BIN_DIR)/transform

run:
	$(BIN_DIR)/transform