#!/usr/bin/python
# -*- coding: utf-8 -*-
from HTMLParser import HTMLParser
from re import sub
from sys import stderr
from traceback import print_exc

def replacemark(string):
    if len(string) == 0:
        return ""
    mark = ["$", "%", "^", "_", "#", "~"]
    s = "\\"+string[0] if string[0] in mark else string[0]
    for i in range(len(string)-1):
        if string[i] == "\\" and ( string[i+1] == '[' or string[i+1] == '('):
            for j in range(i+1, len(string)):
                if string[j-1] != "\\" and string[j] in mark[:2]:
                    s += '\\'
                s += string[j]
            return s
        if string[i] != "\\" and string[i+1] in mark:
            s += '\\'
        s += string[i+1]
    return s

class ToLatex(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.text = []

    def handle_data(self, data):
        text = data.strip()
        if len(text) > 0:
            text = sub('[ \t\r\n]+', ' ', text)
            self.text.append(replacemark(text))

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == 'p':
            self.text.append('\n')
            if 'id' in d.keys():
                if d['id'] == 'question':
                    self.text.append('\\question')
                elif d['id'] == 'attribute':
                    self.text.append('\\hfill')
                    self.text.append('\\attribute')
            self.text.append('{')
        if tag == 'br':
            self.text.append('\n')
        if tag == 'em':
            self.text.append(' \\emph{')
        if tag == 'h1':
            if 'href' in self.text[-1]:
                self.text[-1] = '{'
            self.text.append('\n\\chapter{')
        if tag == 'img':
            src = d['src'][1:] if not d['src'].startswith('http://what-if.xkcd.com/') else d['src'][len('http://what-if.xkcd.com/'):]
            self.text.append(u'\n\\begin{{figure}}\n\\centering\n\\includegraphics[scale=0.8, max width=\\textwidth]{{{1}}}\n\\caption{{{0}}}\n\\end{{figure}}\n'.format(replacemark(d['title']), src))
        if tag == 'a':
            link = replacemark(d['href'])
            self.text.append(u' \\href{' + link + '}{')
        if tag == 'span':
            if 'class' in d.keys() and d['class'] == 'refbody':
                self.text.append(' \\footnote{')
            elif 'class' in d.keys() and d['class'] == 'refnum':
                self.text.append('__del__')
            else:
                self.text.append('{')

    def handle_startendtag(self, tag, attrs):
        if tag == 'img':
            d = dict(attrs)
            src = d['src'][1:] if not d['src'].startswith('http://what-if.xkcd.com/') else d['src'][len('http://what-if.xkcd.com/'):]
            self.text.append(u'\n\\begin{{figure}}\n\\centering\n\\includegraphics[max width=\\textwidth]{{{1}}}\n\\caption{{{0}}}\n\\end{{figure}}\n'.format(replacemark(d['title']), src))
        
    def handle_endtag(self, tag):
        if tag == 'h1':
            self.text.append('}\n')
        if tag == 'p':
            self.text.append('}\n')
        if tag == 'span' or tag == 'em':
            if '__del__' in self.text:
                self.text = self.text[:self.text.index('__del__')]
            else:
                self.text.append('} ')
        if tag == 'a':
            if self.text[-1].endswith('{'):
                self.text[-1] = ""
            else:
                self.text.append('}')

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
    import codecs
    text = ""
    with codecs.open(filename, 'r', 'utf8') as f:
        text = "".join(f.readlines())
    return html2latex(text)

if __name__=="__main__":
    import sys
    import codecs
    text = main(sys.argv[1])
    if len(sys.argv) > 2:
        filename = sys.argv[2]
        with codecs.open(filename, 'a+', 'utf8') as f:
            f.write(text)
            f.write('\n\n')
    else:
        print text
