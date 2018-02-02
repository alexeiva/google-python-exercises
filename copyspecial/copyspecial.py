#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import sys
import re
import os
import shutil
#import commands
import subprocess

"""Copy Special exercise
"""

# +++your code here+++
# Write functions and modify main() to call them
def get_special_paths(dir) :
  filenames = os.listdir(dir)
  list_special = []
  for filename in filenames:
    if not os.path.isdir(filename) and filename != sys.argv[0][2:]:
      list_special.append(os.path.abspath(os.path.join(dir, filename)))    
  return list_special

def copy_to(paths, dir):
  try:
    os.makedirs(dir) # makes all required dirs
  except OSError:
    print "Directory exists"
  finally:
    for path in paths:
      print path
      try:
        shutil.copy(path, dir)
      except shutil.Error, exc:
        for error in errors:
          print error
      
#zip_to(list_special, tozip)

def zip_to(paths, zippath):
  pathstring = ', '.join(paths)
  zipargs = ["zip", "-j", zippath]
  for path in paths:
    zipargs.append(path)
  print "Command I'm going to do: zip -j " + zippath, pathstring
  try:
    subprocess.check_output(zipargs)
  except subprocess.CalledProcessError, e:
    ## Control jumps directly to here if any of the above lines throws IOError.
    print "zip I/O error: No such file or directory", e.output,
    print "Directory does not exist:", zippath

def main():
  # This basic command line argument parsing code is provided.
  # Add code to call your functions below.

  # Make a list of command line arguments, omitting the [0] element
  # which is the script itself.
  args = sys.argv[1:]
  if not args:
    print "usage: [--todir dir][--tozip zipfile] dir [dir ...]";
    sys.exit(1)

  # todir and tozip are either set from command line
  # or left as the empty string.
  # The args array is left just containing the dirs.
  todir = ''
  if args[0] == '--todir':
    todir = args[1]
    del args[0:2]

  tozip = ''
  if args[0] == '--tozip':
    tozip = args[1]
    del args[0:2]

  if len(args) == 0:
    print "error: must specify one or more dirs"
    sys.exit(1)

  # +++your code here+++
  # Call your functions

  for arg in args:
    list_special = get_special_paths(arg)
    if len(tozip) > 0:
      zip_to(list_special, tozip)
    else: 
      for item in list_special:
        if len(todir) > 0:
          print todir
          copy_to(list_special, todir)
          break
        elif len(tozip) > 0:
          zip_to(item, tozip)
        else: 
          print item
          break

  
if __name__ == "__main__":
  main()
