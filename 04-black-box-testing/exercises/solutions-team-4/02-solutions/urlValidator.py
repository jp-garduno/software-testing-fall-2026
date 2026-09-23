import re

def validateUrl(url):
	validUrlRegex = "^http(s)?:\/\/(\w|\.)+\.(\w){2,6}((\?|#|\/)[^(\?|#|\/|\.)]+)*$"
	result = re.match(validUrlRegex, url)
	return "Valid" if result != None else "Invalid"


