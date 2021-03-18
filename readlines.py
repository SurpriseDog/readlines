#!/usr/bin/python3
# Usage ./readlines.py <filename> <start num> <end num> <optional chunk size>
# Example reading a 950k dictionary: ./readlines.py  /usr/share/dict/words -220 -219
# or batch testing with no options given


import os

def read_lines(filename, start=0, end=None, chunk=4096):
	# Return a file one line at a time as if it were a list
	# Unlike, file.readlines() will not cache the entire file in memory
	# 100% drop in replacement for file.readlines[start:end] - slicing is tested to work the same.
	# start = start line
	# end = end line
	# -1 = last line and so on
	inf = float('inf')
	
	#For small files it's faster to just read them into memory
	size = os.path.getsize(filename)
	if size <= chunk * 2:	#must be at least 2x to avoid weird errors
		with open(filename, 'r') as f:
			for line in f.readlines()[start:end]:
				yield line
		return

	#In python slicing [:None] is the same as inf
	if end == None:
		end = inf
	elif end == 0:
		return

	def seek_backwards(target):
		#Seek backwards in file until target newline count is found
		count = 0		#number of newlines counted
		if target == 0:
			return size, 0

		#Read chunks backward in file until we have enough newlines
		reps = size//chunk  if size % chunk else size // chunk - 1
		for c in range(reps):
			if not c:
				#First run at end of file. Read 1 chunk plus whatever remains
				pos = size // chunk * chunk
				if pos == size:
					pos -= chunk
				pos -= chunk
				f.seek(pos)
				data = f.read()
				count -= data.count(b'\n')
				if data[-1] == 10:
					#Ignore trailing '\n'
					count+=1
				f.seek(pos+chunk)
			else:
				f.seek(-chunk*2, os.SEEK_CUR)
				data = f.read(chunk)
				count -= data.count(b'\n')

			if count <= target:
				if not c:
					f.seek(pos+len(data))
				break

		#Now that we have the correct chunk move the pointer to where it should be
		while count < target + 1:
			seek = data.find(b'\n') + 1
			data = data[seek:]
			count += 1
		pos = f.tell() - len(data)
		return pos, count

	with open(filename, 'rb') as f:
		start_pos = 0		#Start reading file here
		end_pos = inf		#Stop here
		min_pos = 0			#The minimum file pos for a line to be yielded in [-x:y] mode


		#Special cases for negative slicing:
		if start < 0 or end < 0:
			if start >= 0 and end < 0:
				#Special case [x:-y]
				end_pos, count = seek_backwards(end)
				end = inf
			elif start < 0 and 0 < end < inf:
				#Special case [-x:y]
				min_pos, count = seek_backwards(start)	
			else:
				#Special case [-x:-y]
				start_pos, count = seek_backwards(start)
				end = end - start - (count - start)	 +  1	#accounting for negatives that exceed file size
				start = 0

		#Read the file forwards
		count = 0			#Number of lines yielded so far
		f.seek(start_pos)

		#Go to the start chunk
		newlines = 0
		data = b''
		while count < start:
			if f.tell() == size:
				return
			if start > 0:
				data = f.read(chunk)
			else:
				data += f.read(chunk)
			newlines = data.count(b'\n')
			count += newlines
		count -= newlines

		#Count up the newlines in the current chunk and maybe get more
		tell = 0
		while count < end:
			seek = data.find(b'\n')
			if seek >= 0:
				seek += 1
				if min_pos and tell - len(data) >= min_pos or not min_pos:
					if count >= start:
						yield data[0:seek].decode()
				count += 1
				data = data[seek:]
			else:
				#No more newlines in current chunk, get a new one
				if tell <= min(end_pos, size-1):
					data += f.read(chunk)
					tell = f.tell()
					if tell > end_pos:
						data = data[:-(tell-end_pos)]
				else:
					break
		if tell <= end_pos and count < end and data:
			yield data.decode()


if __name__ == "__main__":
	import random, sys

	if len(sys.argv) >= 4:
		filename = sys.argv[1]
		start = int(sys.argv[2])
		end = int(sys.argv[3])
		chunk = int(sys.argv[4]) if len(sys.argv) == 5 else 4096
		for num, line in enumerate(read_lines(filename, start, end, chunk=chunk)):
			print(start + num, line.rstrip())
		sys.exit(0)
		


	filename='read.lines.test.file.txt'
	src = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen and so on".split()


	def get_expected():
		#Read back data and process it normally
		with open(filename, 'r') as f:
			data  = f.readlines()
			#print("readlines:", data)
			data = list(map(str.strip, data))
			return data[start:end]

	count= 16 ; start= -10 ; end= 8 ; chunk= 9

	if os.path.exists(filename):
		words = src[:count]
		print('words=', words)
		for line in read_lines(filename, start=start, end=end, chunk=chunk):
			print('line=', repr(line))
		expected = get_expected()
		print("Expected =", expected)

	# Write lines of randomly varying length to file and attempt to call read_lines with random paramaters. 
	# Compare result to normal python slicing with f.readlines() in get_expected function.
	for write_loop in range(50):
		count = random.randint(0,24)	
		words = src[:count]
		words = [w*int(2**random.randrange(0,6)-random.randint(0,8)) for w in words]

		#Write random groupings of words to file
		with open(filename, 'w') as f:
			data = '\n'.join(words)+('\n' if random.random() < 0.5 else '')
			print('\n'*8, 'words = ', words)
			print('file data =', repr(data))
			f.write(data)

		for tested in range(100):

			#Randomize testing values:
			start = random.randint(-9,9)
			end = start + random.randint(-2,7)
			chunk = random.randint(2,22)
			if random.random() < 0.5:
				end = None
			
			#Compare Results
			expected = get_expected()
			print("\nword count=", count, "; start=", start, '; end=', end, '; chunk=', chunk)
			print("Expected =", expected)
			rec = []
			for line in read_lines(filename, start, end, chunk=chunk):		
				rec.append(line.strip())
			print("Recieved =", rec)
			if ' '.join(expected).strip() != ' '.join(rec).strip():
				print("Error on test:", (tested+1) * (write_loop+1))
				sys.exit(1)

		print("Tested:", (tested+1) * (write_loop+1))
	os.remove(filename)
	print('Done!')
