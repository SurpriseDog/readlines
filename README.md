### Readlines

Do you have a **GIGANTIC** text file that you want to get an arbitrary series of lines from the start or end of the file? A file so big it doesn't fit into main memory? The read_lines function will handle that. Now you can access a large text file as if it were a list in python.


### Usage:

This is a 100% drop in replacement for file.readlines()[start:end] The start and end variables can be postive, negative or any combination of the two. It will make a large text file work EXACTLY the same as a list without every worrying about memory size. 

For example, if you want to read from the 20th to the 15th to last line you can run read_lines(filename, -20, -15) and it will read the file backwards in chunks of 4096 bytes before reversing and yielding line -20 to line -15, while never keeping more than 2 chunks of data in memory.

To use, `import readlines` into your project and run the code:

```
readlines.read_lines(filename, start, end)
```

Example reading a 950k dictionary: 

```
./readlines.py  /usr/share/dict/words -1223 -1215
```

which will produce:

```
-1223 wing
-1222 wing's
-1221 winged
-1220 winger
-1219 wingers
-1218 winging
-1217 wingless
-1216 wingnut
```



### License:
Getting all of the edge cases to work for this was suprisingly difficult, but I wrote a unit test to try thousands of different variations and now it finally works everytime. That’s why I’m making this freely available to the Internet under the GNU Affero General Public License v3.0 - All I ask if that if you wish to use this in your project, send me a message to let me know how it works for you and if you found any bugs. Thanks!
