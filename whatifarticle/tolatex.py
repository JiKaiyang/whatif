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
            if len(self.text) > 1 and self.text[-2] == "":
                self.text[-2] = text.replace('%', '\\%')
                return
            self.text.append(text.replace('%', '\\%'))

    def appendbrace(self, string):
        if len(self.text) > 2 and self.text[-2] == '':
            self.text[-3] += string
            self.text[-1] += "}"
        else:
            self.text.append(string)
            self.text.append('')
            self.text.append('}')

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == 'p':
            self.text.append('\n')
            if 'id' in d.keys():
                if d['id'] == 'question':
                    self.appendbrace('\\question{')
                if d['id'] == 'attribute':
                    self.appendbrace('\\attribute{')
        if tag == 'br':
            self.text.append('\n')
        if tag == 'em':
            self.appendbrace(' \\emph{')
        if tag == 'h1':
            self.appendbrace('\n\\chapter{')
        if tag == 'img':
            self.text.append('\n\\begin{{figure}}\n\\caption{{{0}}}\n\\centering\n\\includegraphics{{{1}}}\n\\end{{figure}}\n'.format(d['title'], d['src'][1:]))
        if tag == 'a':
            if len(self.text) < 3:
                return
            link = d['href'].replace('%','\\%')
            self.appendbrace(' \\href{' + link + '}{')
        if tag == 'span':
            if d['class'] == 'refnum':
                self.text.append("__del__")
            if d['class'] == 'refbody':
                self.appendbrace(' \\footnote{')

    def handle_startendtag(self, tag, attrs):
        if tag == 'img':
            d = dict(attrs)
            self.text.append('\n\\begin{{figure}}\n\\caption{{{0}}}\n\\centering\n\\includegraphics{{{1}}}\n\\end{{figure}}\n'.format(d['title'], d['src'][1:]))
        
    def handle_endtag(self, tag):
        if tag == 'h1':
            self.text.append('\n')
        if tag == 'p':
            self.text.append('\n')
        if tag == 'span':
            if self.text[-2] == '__del__':
                self.text.pop()
                self.text.pop()

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
    print text.encode('utf-8')
