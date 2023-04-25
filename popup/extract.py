# Extract links and images from website 
import re
from bs4 import BeautifulSoup
from urllib.request import urlopen
from pyscript import Element
from js import main, pageHtml, pageURL

# parse current pages html with beautifulsoup
soup = BeautifulSoup(pageHtml, 'html.parser')
products = soup.find_all(class_=re.compile("product|item"))

# store all the images on the page
images = []
d = {}

# search for ".com" or ".co.uk" in URL to get substring 
if pageURL.find('.co.uk') != -1:
	substring = pageURL[:pageURL.find('.co.uk')+6]
else:
	substring = pageURL[:pageURL.find('.com')+4]

def makeAbsolute(link):
	# if link is relative, add the substring to the link
	if link.startswith('https:') == False:
		link = substring + link
	return link

def makeAbsoluteImg(link):
	if link.startswith('https:')==False:
		link = 'https:' + link 
	return link
     
# Hashmap where key: link and value:image
for product in products:
	link_element = product.find('a')
	if link_element and 'href' in link_element.attrs:
		link = link_element['href']
		# if link is relative, add the substring to the link
		link = makeAbsolute(link)
		# If link not already in dictionary, add it
		if link not in d:
			d[link] = ""
		image_element = product.find('img')
		if image_element and 'src' in image_element.attrs:
			image = image_element['src']
			image = makeAbsoluteImg(image) 
			d[link] = image


image_width = '200px'
image_height = '200px'

# generate html to inject
new_code = ""
for key in d:
	#print("Link: ",key)
	#print("Img: ", d[key])   
	string = "\t"+ "<li><a href='" + key+"'target='_blank'><img width='" + image_width + "' height='" + image_height + "' src='"+d[key]+"'></a></li>" + "\n" +"\t" + "\t" + "\t"
	new_code += string

# create the storefront!
main(new_code, 0.2)
