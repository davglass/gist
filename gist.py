#!/usr/bin/env python3.0
import sys
import urllib.request
import optparse
import subprocess

URL_GIST = "http://gist.github.com/"
URL_GIST_VIEW = URL_GIST + "{id}"
URL_GIST_TXT = URL_GIST_VIEW + ".txt"
URL_GIST_POST = URL_GIST + "gists"

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
		
		raise(NotImplementedError("Keep waiting"))
	
	def write(self, content, private=False):
		"""
			Creates a Gist with the specified contents.
			
			Returns the id of the newly-created Gist.
		"""
		
		raise(NotImplementedError("I swear it won't be long"))

def main(*args):
	import gist
	
	user = gist.GistUser()
	print(user)
	
	user.read(1234)

if __name__ == "__main__": sys.exit(main(*sys.argv[1:]))
