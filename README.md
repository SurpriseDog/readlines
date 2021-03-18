# readlines

Do you have a GIGANTIC text file that you want to get an arbitrary sequence of lines from the start or end of the file? A file so big it doesn't fit into main memory? The read_lines function will handle that. Now you can access a large text file as if it were a list in python. 

This is a 100% drop in replacement for filename.readlines()[start:end] The start and end variables can be postive, negative or any combination of the two. It will make a large text file work EXACTLY the same as a list without every worrying about memory size. Getting all of the edge cases to work for this was suprisingly difficult, but I wrote a unit test to try thousands of different variations and now it finally works everytime.

For example, if you want to read from the 20th to the 15th to last line you can run read_lines(filename, -20, -15) and it will read the file backwards in chunks of 4096 bytes before reversing and yielding line -20 to line -15, while never keeping more than 2 chunks of data in memory.
