#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import os
import re
import sys
import urllib

"""Logpuzzle exercise
Given an apache logfile, find the puzzle urls and download the images.

Here's what a puzzle url looks like:
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""

def read_urls(filename):
  """Returns a list of the puzzle urls from the given log file,
  extracting the hostname from the filename itself.
  Screens out duplicate urls and returns the urls sorted into
  increasing order."""
  # +++your code here+++
  url_list = []
  matches = []
  pattern = r'\S+puzzle\S+'
  hostname = r'http://code.google.com'

  with open(filename, 'r') as f:
    matches = re.findall(pattern, f.read())
    for m in matches:
      if m not in url_list:
        url_list.append(hostname + m)
  url_list = sorted(set(url_list))  
  return url_list
  
def smartsort(url_list):
  places_back = []
  for i in url_list:
    r = re.sub(r'(\w\w\w\w)-(\w\w\w\w).jpg', r'\2-\1.jpg', i)
    places_back.append(r)

  places_back = sorted(places_back)
  places_front = []
  for i in places_back:
    r = re.sub(r'(\w\w\w\w)-(\w\w\w\w).jpg', r'\2-\1.jpg', i)
    places_front.append(r)
  
  return places_front

def download_images(img_urls, dest_dir):
  """Given the urls already in the correct order, downloads
  each image into the given directory.
  Gives the images local filenames img0, img1, and so on.
  Creates an index.html in the directory
  with an img tag to show each local image file.
  Creates the directory if necessary.
  """
  # +++your code here+++
  if not os.path.isdir(dest_dir):
    os.mkdir(dest_dir)

  html = '''
  <verbatim>
  <html>
  <body>
'''

  for i,v in enumerate(img_urls):
    mydir = dest_dir + "/img%i.jpg" % i
    print "Retrieving img %i of %i..." % (i, len(img_urls) - 1)
    urllib.urlretrieve(v, mydir)
    html += "<img src='%s'/>" % (mydir)
 
  html += '''
</body>
</html>
'''

  with open('index.html', 'a') as f:
    f.write(html)      

def main():
  args = sys.argv[1:]

  if not args:
    print 'usage: [--todir dir] logfile '
    sys.exit(1)

  todir = ''
  if args[0] == '--todir':
    todir = args[1]
    del args[0:2]

  img_urls = smartsort(read_urls(args[0]))

  if todir:
    download_images(img_urls, todir)
  else:
    print '\n'.join(img_urls)

if __name__ == '__main__':
  main()
