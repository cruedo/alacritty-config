from bs4 import BeautifulSoup as bs
import requests as req
import sys


def m_write(name, cols, f):
	bad = ['!','.','@','#','$']
	name = ''.join(filter(lambda x: x not in bad, name))
	cols = "\n"+cols
	cols = cols.replace("\n","\n  ")
	N = f"{name}: &{name}"
	cols = cols.replace("colors:", N)
	f.write(cols)


if __name__ == "__main__":

	output_file = "themes.yml"
	if(len(sys.argv) > 1):
		output_file = sys.argv[1]

	url = "https://github.com/alacritty/alacritty/wiki/Color-schemes"
	res = req.get(url)
	html_doc = res.content

	soup = bs(html_doc, 'html.parser')

	attr = {
		"class" : "markdown-body"
	}

	x = soup.find(attrs=attr).find_all('details')

	cnt = 0
	themes = list(x)
	f = open(output_file, "w")
	f.write("schemes:\n\n")

	for i in themes:
		cnt += 1
		variants = list(i.find_all('div'))
		name = i.summary.string.replace(" ","")

		sz = len(variants)
		rname = name

		for k,v in enumerate(variants):
			if(sz == 2):
				if(k == 0): rname = name + '-light'
				else: rname = name + '-dark'
			cols = v['data-snippet-clipboard-copy-content']
			m_write(rname, cols, f)


	f.close()
