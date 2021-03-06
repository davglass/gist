#!/usr/bin/env python3.0
import sys
import urllib.parse
import urllib.request
import urllib.error
import optparse
import subprocess
import json
import os
import re

GIST_SERVER = "gist.github.com"

HTTP_GIST_PUBLIC = "http://{server}/{id}".format(server=GIST_SERVER, id="{id}")
HTTP_GIST_PUBLIC_TXT = "http://{server}/{id}.txt".format(server=GIST_SERVER, id="{id}")
HTTP_GIST_POST = "http://{server}/gists".format(server=GIST_SERVER)

GIST_API_NEW = "http://{server}/api/v1/{format}/new".format(server=GIST_SERVER, format="json")

GIT_GIST_PUBLIC = "git://{server}/{id}.git".format(server=GIST_SERVER, id="{id}")
GIT_GIST_PRIVATE = "git@{server}:{id}.git".format(server=GIST_SERVER, id="{id}")

RE_GIST_URL = re.compile("^https?://{server}/([0-9A-Fa-f]+)$".format(server=re.escape(GIST_SERVER)))

class GistError(Exception):
	"""A parent of all exceptions raised by this module."""

class NotFileError(GistError, IOError):
	"""Raised when a filename is specified that is invalid."""

class AuthenticationError(GistError, urllib.error.HTTPError):
	"""Raised when the server rejects a user's authentication."""

def load_authentication():
	"""
		Loads GitHub/Gist authentication information from the git config,
		
		The authentication information is returned as a tuple (user, token).
		If authentication information is unavailable or incomplete, None
		is returned.
	"""
	
	user = subprocess.Popen(["git", "config", "github.user"], stdout=subprocess.PIPE).communicate()[0].decode("UTF-8").strip()
	token = subprocess.Popen(["git", "config", "github.token"], stdout=subprocess.PIPE).communicate()[0].decode("UTF-8").strip()
	
	if user and token:
		return(user, token)
	else:
		return(None)

def clip(text):
	"""
		Attempts to copy the specified text to the clipboard, returning
		a boolean indicating success.
	"""
	
	text_bytes = text.encode()
	
	try:
		pbcopy = subprocess.Popen("pbcopy", stdin=subprocess.PIPE, stdout=subprocess.PIPE)
		pbcopy.communicate(text_bytes)
		return(not pbcopy.returncode)
	except OSError:
		try:
			xclip = subprocess.Popen("xclip", stdin=subprocess.PIPE, stdout=subprocess.PIPE)
			xclip.communicate(text_bytes)
			return(not xclip.returncode)
		except OSError:
			pass
	
	return(False)

class GistUser(object):
	"""
		Represents a Gist user, including authentication information.
	"""
	
	def __init__(self, authentication=None):
		"""
			Iniitalizes a GistUser()
			
			Authentication information may be provided in the form of a tuple
			(user, token), otherwise it will be attempted to be loaded from
			the git config variables github.user and github.token.
		"""
		
		if authentication:
			if len(authentication) == 2:
				self.authentication = tuple(authentication)
			else:
				raise ValueError("Authenication tuple must be of length 2.")
		else:
			self.authentication = load_authentication()
	
	def __repr__(self):
		if self.authentication:
			return("GistUser({0})".format(self.authentication))
		else:
			return("GistUser(authentication=None)")
	
	def read(self, id):
		"""
			Retrives and returns the text-only representation of a specified Gist.
		"""
		
		url = HTTP_GIST_PUBLIC_TXT.format(id=id)
		
		return(urllib.request.urlopen(url).read().decode())
	
	def clone(self, id, private=None):
		"""
			Clones the specified Gist.
		"""
		
		if private is None:
			private = False # TODO: Determine if the user owns this repo.
		
		if private:
			url = GIT_GIST_PRIVATE.format(id=id)
		else:
			url = GIT_GIST_PUBLIC.format(id=id)
		
		command = ["git", "clone", url, "gist-{id}".format(id=id)]
		
		return(0 == subprocess.Popen(command).wait())
	
	def write(self, files, private=False):
		"""
			Creates a new Gist from the specified files.
			
			files should be provided as a list of tuples(contents, filename, extension)
			
			Returns the id of the newly-created Gist.
		"""
		
		if not files:
			raise(ValueError("Cannot create a Gist without data."))
		
		post_data = {}
		
		if private:
			post_data["private"] = "on"
		
		for n, c_f_e in enumerate(files, start=1):
			content, filename, extension = c_f_e
			
			if not extension:
				if filename:
					extension = os.path.splitext(filename)[1]
				else:
					extension = ".txt"
			
			if not filename:
				filename = ""
			
			form_key = "gistfile{n}".format(n=n)
			
			post_data["file_ext[{key}]".format(key=form_key)] =  extension
			post_data["file_name[{key}]".format(key=form_key)] = filename
			post_data["file_contents[{key}]".format(key=form_key)] = content
		
		if self.authentication:
			post_data["login"], post_data["token"] = self.authentication
			
			sys.stderr.write("Uploading files as user {username}...\n".format(username=self.authentication[0]))
		else:
			sys.stderr.write("Uploading files anonymously...\n")
		
		post_data = urllib.parse.urlencode(post_data)
		
		reqest = urllib.request.Request(HTTP_GIST_POST, post_data)
		
		try:
			response = urllib.request.urlopen(reqest)
		except urllib.error.HTTPError as e:
			if e.code == 401:
				raise(AuthenticationError("Authentication failed, please ensure that your athentication configuration is correct."))
			else:
				raise
		
		url = response.geturl()
		
		id = RE_GIST_URL.match(url).groups()[0]
		
		return(id)

def main(*args):
	import gist
	
	optparser = optparse.OptionParser("\n".join([
		"",
		"  Create a Gist from one or more files",
		"    %prog [-p] file [file2 file3...]",
		"  Create a Gist from stdin, giving if a filename",
		"    cal | %prog -i cal.txt",
		"  Clone the repositories of one or more Gists",
		"    %prog -c id [id2 id3...]",
		"  Display the text contents of a Gist",
		"    %prog -r id",
	]))
	
	optparser.set_defaults(mode="post", private=None)
	optparser.add_option("-p", "--private", dest="private", const=True,
		action="store_const",
		help="When set private repositories and clones are made using the private URLs.")
	optparser.add_option("-u", "--public", dest="private", const=False,
		action="store_const",
		help="The opposite of -p")
	optparser.add_option("-c", "--clone", dest="mode", const="clone",
		action="store_const",
		help="Provided with one or more IDs, clones the repository of the associated Gist(s).")
	optparser.add_option("-r", "--read", dest="mode", const="read",
		action="store_const",
		help="Provided with an ID, displays and copies the text contents of that Gist.")
	optparser.add_option("-i", "--stdin", dest="mode", const="stdin",
			action="store_const",
			help="Makes a new Gist using a single file from stdin, giving it whatever filename is specified.")
	
	
	(opts, files) = optparser.parse_args(list(args))
	
	user = gist.GistUser()
	
	if opts.mode == "post":
		if files:
			file_data = []
			
			for n, filename in enumerate(files, start=1):
				if not os.path.isfile(filename):
					raise(NotFileError("\"{filename}\" is not a real file.".format(filename=filename)))
				
				file_data.append((open(filename).read(), os.path.basename(filename)))
			
			sys.stderr.write("Creating gist...\n")
			
			id = user.write(file_data, private=opts.private)
			
			url = HTTP_GIST_PUBLIC.format(id=id)
			
			if not clip(url):
				sys.stderr.writeln("Warning: Unable to copy URL to clipboard.")
			
			print(url)
		else:
			sys.stderr.write("No files specified.\n")
			return(1)
	elif opts.mode == "stdin":
		if len(files) > 1:
			sys.stderr.write("Warning: Extra arguments ignored\n         (stdin is named from the first filename specified, others are ignored)\n")
			
		if files:
			filename = files[0]
			extension = None
		else:
			filename = None
			extension = ".txt"
		
		id = user.write([(sys.stdin.read(), filename, extension)], private=opts.private)
		
		url = HTTP_GIST_PUBLIC.format(id=id)
		
		sys.stderr.write("Creating gist...\n")
		
		if not clip(url):
			sys.stderr.writeln("Warning: Unable to copy URL to clipboard.")
		
		print(url)
	elif opts.mode == "clone":
		if files:
			for id in files:
				print("Cloning gist id {id}".format(id=id))
				
				if user.clone(id, private=opts.private):
					print("Sucessful")
				else:
					print("Unsucessful")
		else:
			sys.stderr.write("No gist ID(s) specified.\n")
			return(1)
	elif opts.mode == "read":
		if files:
			if len(files) > 1:
				sys.stderr.write("Warning: Extra arguments ignored\n         (reading more than one Gist at a time is unsupported)\n")
			
			sys.stdout.write(data)
			sys.stderr.write("\n")
			
		else:
			sys.stderr.write("No gist ID specified.\n")
			return(1)

if __name__ == "__main__": sys.exit(main(*sys.argv[1:]))
