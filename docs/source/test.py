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
            check_footnote(f)


def check_footnote(filename):
    pattern = '[①②③④⑤⑥⑦⑧⑨]'
    # pattern = '[②]'
    with open(filename, encoding='utf-8') as f:
        for s in f.readlines():
            m = re.search(pattern, s)
            if m:
                print(s)


def footnote(filename):
    pattern = '[①②③④⑤⑥⑦⑧⑨]'

    sentences = []
    footnotes = []
    
    with open(filename, encoding='utf-8') as f:
        for s in f.readlines():
            m = re.search(pattern, s)
            if m:
                # 检查匹配的pattern是否在行首
                if m.start() == 0:
                    # 在行首，替换为 .. [#] 并追加到footnotes
                    new_line = re.sub(pattern, ' .. [#] ', s)
                    footnotes.append(new_line)
                else:
                    # 不在行首，替换为 [#]_ 并追加到sentences
                    new_line = re.sub(pattern, ' [#]_ ', s)
                    sentences.append(new_line)
            else:
                # 没有匹配到pattern，追加到sentences
                sentences.append(s)
    
    # 合并sentences和footnotes
    all_lines = sentences + footnotes
    
    # 回写到文件
    with open(filename, 'w', encoding='utf-8') as f:
        f.writelines(all_lines)


if __name__ == '__main__':
    f3()
