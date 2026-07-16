import html.parser

class SimpleHTMLParser(html.parser.HTMLParser):
    def handle_starttag(self, tag, attrs):
        pass
    def handle_endtag(self, tag):
        pass

files = [
    "/Users/mac/Desktop/Websites /GITkaizoku/pages/aesthetic-nerds.html",
    "/Users/mac/Desktop/Websites /GITkaizoku/pages/alloy-collection.html",
    "/Users/mac/Desktop/Websites /GITkaizoku/pages/fandom.html"
]

for fpath in files:
    with open(fpath) as f:
        html_content = f.read()
    try:
        parser = SimpleHTMLParser()
        parser.feed(html_content)
        print(f"Parsed successfully: {fpath}")
    except Exception as e:
        print(f"Error parsing: {fpath} - {e}")
