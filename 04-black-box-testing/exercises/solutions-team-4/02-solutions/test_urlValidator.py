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

def test_VBContainsPath():
	assert validateUrl("http://amazon.net/ec2/create") == "Valid"


def test_InBContainsPath1():
	assert validateUrl("https://netflix.com//") == "Invalid"


def test_InContainsPath2():
	assert validateUrl("https://mail.google.com/mail//0/#inbox") == "Invalid"


def test_VDomain2():
	assert validateUrl("https://various.example.com/substantial/pricey") == "Valid"


def test_InDomain2():
	assert validateUrl("https://slim.exam-ple.org/bottle") == "Invalid"


def test_VContainsQuery():
	assert validateUrl("https://music.youtube.com/watch?v=_qur4p4qV7E&list=RDAMVM_qur4p4qV7E") == "Valid"


def test_InContainsEmptyQuery():
	assert validateUrl("https://netflix.com/watch?") == "Invalid"


def test_VContainsFragment():
	assert validateUrl("https://mail.google.com/mail/u/0#trash") == "Valid"


def test_InContainsEmptyFragment():
	assert validateUrl("https://pomofocus.io/start#") == "Invalid"

