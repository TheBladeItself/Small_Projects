import urllib.request
import re

def get_props(s):
	props = {}
	parse = re.compile('^<li><strong>.+:</strong>.+</li>$',re.M)
	lines = parse.findall(s)
	for line in lines:
		line = line[12:-5]
		#print(line)
		line = line.split(':</strong> ')
		props[line[0]]=line[1]
		#print(line)
	if 'Formula' in props.keys():
		props['Formula'] =props['Formula'].replace('<sub>','')
		props['Formula'] =props['Formula'].replace('</sub>','')
	parse = re.compile('<title>.+</title>')
	text = parse.search(s).group()
	props['Name']=text[7:-8].lower().replace(' ','-')
    
	parse = re.compile('<td align=\"left\">T<sub>boil</sub></td><td class=\"right-nowrap\">[\.\d]+')
	text = parse.findall(s)
	if text:
		props['Boiling Point']=text[0][63:]
    
	parse = re.compile('<td align="left">T<sub>c</sub></td><td class="right-nowrap">[\.\d]+')
	text = parse.findall(s)
	if text:
		props['Critical Temperature']=text[0][60:]
    
	parse = re.compile('<td align="left">P<sub>c</sub></td><td class="right-nowrap">[\.\d]+')
	text = parse.findall(s)
	if text:
		props['Critical Preassure']=float(text[0][60:])*10e5
    
	parse = re.compile('<li><strong>Other names:</strong>[^<>]+</li>')
	text = parse.findall(s)
	if text:
		props['Other Names']= text[0][33:-5].replace('&amp;','&')
	return props

def lookup(chemical):
	# Get a file-like object for the Python Web site's home page.
	chemical = chemical.replace(' ', '-')
	site = "http://webbook.nist.gov"
	search = "/cgi/cbook.cgi?Units=SI&cTP=on&Name="
	f = urllib.request.urlopen(site+search+str(chemical))
	# Read from the object, storing the page's contents in 's'.
	s = f.read().decode('utf-8')
	f.close()
	parse = re.compile('<title>.+</title>')
	title = parse.search(s).group()
	if title[7:-8] == "Name Not Found":
		return "Name not found"
	if title[7:-8] == "Search Results":
		parse = re.compile('<a href=\".+\">.+</a>')
		links = parse.findall(s)
		for link in links:
			link = link[9:-4]
			link = link.split("\">")
			if link[1].lower().replace(' ', '-') == chemical.lower():
				#print(site+link[0])
				f = urllib.urlopen(site+link[0])
				s = f.read()
				f.close()
				return get_props(s)
		return "Multiple species were found"
    
	return get_props(s)

chem = input("Enter a chemical: ")
props = lookup(chem)
if props =="Name not found":
	print("Chemical not found")
elif props =="Search Results":
	print("Multiple components with that name were found")
else:
	print
	for prop in props.keys():
		print(prop,": ", props[prop])
	print
