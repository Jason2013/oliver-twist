# coding=utf-8

import os
import re
import shutil
import argparse

def f1():
    for f in os.listdir():
        pattern = r"^\d{2}\.rst$"
        m = re.match(pattern, f)
        if m:
            print(f)
            os.remove(f)


def fix_chars(filename):
    with open(filename, encoding='utf-8') as fi:
        s1 = fi.read()

    s2 = s1.replace('*', '')
    s2 = s2.replace('��', '阳')
    # 只有当空格前后都是中文字符时，才将空格替换为无
    s2 = re.sub(r'([\u4e00-\u9fff]) ([\u4e00-\u9fff])', r'\1\2', s2)
    # ��
    if s2 != s1:
        with open(filename, 'w', encoding='utf-8') as fo:
            fo.write(s2)
    print("fixed: %s" % filename)



def f3(func):
    for f in os.listdir():
        pattern = r"^\d{3}\.rst$"
        m = re.match(pattern, f)
        if m:
            print(f)
            func(f)


def check_footnote(filename):
    pattern = '[①②③④⑤⑥⑦⑧⑨]'
    # pattern = '[②]'
    with open(filename, encoding='utf-8') as f:
        for s in f.readlines():
            m = re.search(pattern, s)
            if m:
                print(s)


def fix_footnote(filename):
    pattern = '[①②③④⑤⑥⑦⑧⑨]'

    sentences = []
    footnotes = []
    
    # 添加计数器
    not_at_start_count = 0  # 不在行首的匹配数量
    at_start_count = 0      # 在行首的匹配数量
    
    with open(filename, encoding='utf-8') as f:
        for s in f.readlines():
            m = re.search(pattern, s)
            if m:
                # 检查匹配的pattern是否在行首
                if m.start() == 0:
                    # 在行首，替换为 .. [#] 并追加到footnotes
                    new_line = re.sub(pattern, '.. [#] ', s)
                    footnotes.append(new_line)
                    at_start_count += 1
                else:
                    # 不在行首，替换为 [#]_ 并追加到sentences
                    new_line = re.sub(pattern, ' [#]_ ', s)
                    sentences.append(new_line)
                    not_at_start_count += 1
            else:
                # 没有匹配到pattern，追加到sentences
                sentences.append(s)
    
    # 添加断言：确保不在行首的匹配和在行首的匹配数量相同
    assert not_at_start_count == at_start_count, f"匹配数量不相等：不在行首 {not_at_start_count} vs 在行首 {at_start_count}"

    if not_at_start_count == 0:
        return
    
    # 合并sentences和footnotes
    all_lines = sentences +  (['\n'] if sentences[-1] != '\n' else []) + footnotes
    
    # 回写到文件
    with open(filename, 'w', encoding='utf-8') as f:
        f.writelines(all_lines)


if __name__ == '__main__':
    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(description='处理 RST 文件的工具')
    parser.add_argument('action', choices=['check_footnote', 'fix_footnote', 'fix_chars'], 
                       help='要执行的操作: check_footnote(检查脚注), fix_footnote(修复脚注), fix_chars(修复字符)')
    
    # 解析命令行参数
    args = parser.parse_args()
    
    # 打印 action 的值
    print(f"执行操作: {args.action}")
    
    # 根据 action 参数执行相应的操作
    if args.action == 'check_footnote':
        f3(check_footnote)  # 调用 check_footnote 相关的函数
    elif args.action == 'fix_footnote':
        # 处理脚注修复
        f3(fix_footnote)
    elif args.action == 'fix_chars':
        f3(fix_chars)  # 调用修复字符的函数
