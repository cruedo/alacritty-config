from bs4 import BeautifulSoup as bs
import requests as req
from pathlib import Path
 
 
if __name__ == "__main__":
 
    HOME = str(Path.home())
    BASE_PATH = HOME + "/.config/alacritty/themes/"
    Path(BASE_PATH).mkdir(parents=True, exist_ok=True)
 
    url = "https://github.com/alacritty/alacritty/wiki/Color-schemes"
    res = req.get(url)
    html_doc = res.content
 
    soup = bs(html_doc, 'html.parser')
 
    attr = {
        "class" : "markdown-body"
    }
 
    x = soup.find(attrs=attr).find_all('details')
 
    themes = list(x)
    print("import:")
 
    for i in themes:
        variants = list(i.find_all('div'))
        name = i.summary.string.replace(" ","")
        sz = len(variants)
        
        for k,v in enumerate(variants):
            variant_type = ""
            if(sz == 2):
                if(k == 0): variant_type = '-Light'
                else: variant_type = '-Dark'
            
            theme_name = name + variant_type
            cols = v['data-snippet-clipboard-copy-content']
 
            bad = ['!','.','@','#','$']
            theme_name = ''.join(filter(lambda x: x not in bad, theme_name))
 
            theme_name = theme_name.title()
            root_yml = f"{theme_name}: &{theme_name}"
            cols = cols.replace("colors:", root_yml)
            
            theme_filename = theme_name + ".yml"
            theme_path = BASE_PATH + theme_filename
            
            with open(theme_path, "w") as f:
                f.write(cols)
                f.write(f"\n\ncolors:\n  *{theme_name}")
 
            print("#  - " + "~/.config/alacritty/themes/" + theme_filename)
 