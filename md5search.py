#!/usr/bin/env python
import os,sys, argparse, hashlib

def parseArguments():
	parser = argparse.ArgumentParser(description = 'md5search.py: search using md5 hash.')
	# Path to start searching
	parser.add_argument('-p', '--path',
						help = '-p/--path: path to start searching',
						type  = str,
						default = '/',
						required = False)
	# File to search
	parser.add_argument('-f', '--file',
						help = '-f/--file: file to use its md5 to search',
						type  = str,
						required = True)
						
	return vars(parser.parse_args())

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def fileExists(fname):
	if os.path.isfile(fname) and os.access(fname, os.R_OK):
		return True
	else:
		return False

def md5search(startPath,md5src,sizesrc):
	# Start searching from startPath directory
	for dirpath, dirs, files in os.walk(startPath):
		# for each file in directory
		for f in files:
			fileName = '%s/%s'%(dirpath,f)
			try:
				if not os.path.islink(fileName):
					sizetmp = os.path.getsize(fileName)
					if sizetmp == sizesrc:
						md5temp = md5(fileName)
						if md5temp == md5src:
							print fileName
			except:
				pass
		  

if __name__ == '__main__':
	args = parseArguments()
	
	# Exit if file does not exist
	if not fileExists(args['file']):
		print '%s does not exists or is not readable'%(args['file'])
		sys.exit()
	
	# Get the md5 hash of the file to search
	md5src = md5(args['file'])
	sizesrc = os.path.getsize(args['file'])
	md5search(args['path'],md5src,sizesrc)
