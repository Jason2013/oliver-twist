# coding=utf-8

import os
import re
import shutil

def f1():
    for f in os.listdir():
        pattern = r"^\d{2}\.rst$"
        m = re.match(pattern, f)
        if m:
            print(f)
            os.remove(f)


def f2():
    for f in os.listdir():
        pattern = r"^\d{3}\.rst$"
        m = re.match(pattern, f)
        if m:
            print(f)
            # os.remove(f)

            with open(f, encoding='utf-8') as fi:
                s1 = fi.read()

            s2 = s1.replace('*', '')
            if s2 != s1:
                with open(f, 'w', encoding='utf-8') as fo:
                    fo.write(s2)
                print("fixed: %s" % f)



def f3():
    for f in os.listdir():
        pattern = r"^\d{3}\.rst$"
        m = re.match(pattern, f)
        if m:
            print(f)
            footnote(f)


def footnote(filename):
    pattern = '[①②③④⑤⑥⑦⑧⑨]'
    with open(filename, encoding='utf-8') as f:
        for s in f.readlines():
            m = re.search(pattern, s)
            if m:
                print(s)

    


if __name__ == '__main__':
    f3()
