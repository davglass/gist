#!/usr/bin/env python3.0
import sys
import urllib.parse
import urllib.request
import urllib.error
import optparse
import subprocess
import os

URL_HTTP_GIST = "http://gist.github.com/"
URL_HTTP_GIST_VIEW = URL_HTTP_GIST + "{id}"
URL_HTTP_GIST_TXT = URL_HTTP_GIST_VIEW + ".txt"
URL_HTTP_GIST_POST = URL_HTTP_GIST + "gists"
URL_GIT_GIST = "git://gist.github.com/{id}.git"

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
		
		url = URL_HTTP_GIST_TXT.format(id=id)
		
		return(urllib.request.urlopen(url).read().decode())
	
	def clone(self, id):
		"""
			Clones (unauthenticatedly) the specified gist.
		"""
		
		command = ["git", "clone", URL_GIT_GIST.format(id=id), "gist-{id}".format(id=id)]
		
		return(0 == subprocess.Popen(command).wait())
	
	def write(self, contents=None, files=None, private=False):
		"""
			Creates a new Gist from the specified strings and/or files.
			
			Returns the id of the newly-created Gist.
		"""
		
		raise(NotImplementedError("This will be fixed before too long."))

def main(*args):
	import gist
	
	optparser = optparse.OptionParser("usage: %prog\n\nBy default, specified files are posted uploaded to a new gist.")
	optparser.set_defaults(mode="post")
	optparser.add_option("-p", "--private", dest="private",
		action="store_true",
		help="Makes the newly created gist private.")
	optparser.add_option("-c", "--clone", dest="mode", const="clone",
		action="store_const",
		help="Provided with one or more IDs, clones the repository of the associated gist(s).")
	optparser.add_option("-r", "--read", dest="mode", const="read",
		action="store_const",
		help="Provided with an ID, displays and copies the text contents of that gist.")
	
	(opts, files) = optparser.parse_args(list(args))
	
	user = gist.GistUser()
	
	if opts.mode == "post":
		if files:
			for filename in files:
				if not os.path.isfile(filename):
					sys.stderr.write("Error: \"{filename}\" is not a real file.".format(filename=filename))
					return(1)
			
			post_data = {}
			
			if user.authentication:
				post_data["login"], post_data["token"] = user.authentication
				
				sys.stderr.write("Uploading files as user {username}...\n".format(username=user.authentication[0]))
			else:
				sys.stderr.write("Uploading files anonymously...\n")
			
			if opts.private:
				post_data["private"] = "on"
			
			for n, filename in enumerate(files, start=1):
				form_key = "gistfile{n}".format(n=n)
				
				post_data["file_ext[{key}]".format(key=form_key)] = os.path.splitext(filename)[1] or ".txt"
				post_data["file_name[{key}]".format(key=form_key)] = os.path.basename(filename)
				post_data["file_contents[{key}]".format(key=form_key)] = open(filename).read().encode("UTF-8")	
			
			post_data = urllib.parse.urlencode(post_data)
			
			reqest = urllib.request.Request(URL_HTTP_GIST_POST, post_data)
			
			try:
				response = urllib.request.urlopen(reqest)
			except urllib.error.HTTPError as e:
				if e.code == 401:
					sys.stderr.write("Error: Authentication failed, please ensure that your athentication configuration is correct.\n")
				else:
					sys.stderr.write("Error: Upload failed with HTTP error {code} {message}.\n".format(code=e.code, message=e.msg))
				
				return(1)
			
			url = response.geturl()
			
			if not clip(url):
				sys.stderr.writeln("Warning: Unable to copy URL to clipboard.")
			
			print(url)
		else:
			sys.stderr.write("No files specified.\n")
			return(1)
	elif opts.mode == "clone":
		if files:
			for id in files:
				print("Cloning gist id {id}".format(id=id))
				
				if user.clone(id):
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
			
			data = user.read(files[0])
			
			if not clip(data):
				sys.stderr.write("Warning: Unable to copy data to clipboard.\n")
			
			# BUGGY: FORMATS AS THOUGH USING REPR ON BYTES, NOT WHAT I MEAN TO BE DOING
			sys.stdout.write(data)
			sys.stderr.write("\n")
			
		else:
			sys.stderr.write("No gist ID specified.\n")
			return(1)

if __name__ == "__main__": sys.exit(main(*sys.argv[1:]))
