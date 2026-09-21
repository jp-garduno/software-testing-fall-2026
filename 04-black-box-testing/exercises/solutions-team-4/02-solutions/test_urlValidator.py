from urlValidator import validateUrl

def test_InNoHttp():
	assert validateUrl("htp://crunchyroll.net/watch") == "Invalid"

def test_VHasHttp():
	assert validateUrl("http://google.com") == "Valid"

def test_VHasHttps():
	assert validateUrl("https://kahoot.com") == "Valid"

def test_VDomain():
	assert validateUrl("http://clo9d_p4ge.com") == "Valid"

def test_InDomain():
	assert validateUrl("http://kahoot^?&.com") == "Invalid"

def test_InBVTLDLessThan2():
	assert validateUrl("http://invalid.g") == "Invalid"

def test_VBVTLDExactly2():
	assert validateUrl("https://youtube.go") == "Valid"

def test_InBVTLDMoreThan6():
	assert validateUrl("http://kahoot.criminalrizz") == "Invalid"

def test_VBVTLDExactly6():
	assert validateUrl("https://slowApi.slowly") == "Valid"

