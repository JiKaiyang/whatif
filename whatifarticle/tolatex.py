#!/usr/bin/python
from HTMLParser import HTMLParser
from re import sub
from sys import stderr
from traceback import print_exc

class ToLatex(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.text = []

    def handle_data(self, data):
        text = data.strip()
        if len(text) > 0:
            text = sub('[ \t\r\n]+', ' ', text)
            self.text.append(text)

    def handle_starttag(self, tag, attrs):
        if tag == 'p':
            self.text.append('\n')
            d = dict(attrs)
            if 'id' in d.keys():
                if d['id'] == 'question':
                    self.text.append('\\question\n')
                if d['id'] == 'attribute':
                    self.text.append('\\attribute\n')
        if tag == 'br':
            self.text.append('\n')
        if tag == 'h1':
            self.text.append('\n\\chapter{')
        if tag == 'img':
            d = dict(attrs)
            self.text.append('\n\\begin{{figure}}\n\\caption{{{0}}}\n\\centering\n\\includegraphics{{{1}}}\n\\end{{figure}}\n'.format(d['title'], d['src'][1:]))

    def handle_startendtag(self, tag, attrs):
        if tag == 'img':
            d = dict(attrs)
            self.text.append('\n\\begin{{figure}}\n\\caption{{{0}}}\n\\centering\n\\includegraphics{{{1}}}\n\\end{{figure}}\n'.format(d['title'], d['src'][1:]))
        

    def handle_endtag(self, tag):
        if tag == 'h1':
            self.text.append('}\n')
        if tag == 'p':
            self.text.append('\n')

    def totext(self):
        return ''.join(self.text).strip()

def html2latex(text):
    try:
        p = ToLatex()
        p.feed(text)
        p.close()
        return p.totext()
    except:
        print_exc(file=stderr)
        return text

def main(filename):
    text = ""
    with open(filename, 'r') as f:
        text = "".join(f.readlines())
    return html2latex(text)

if __name__=="__main__":
    import sys
    text = main(sys.argv[1])
    print text
