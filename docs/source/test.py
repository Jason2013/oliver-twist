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


def rename_files():
    """
    将所有以3个数字为前缀的文件重命名，使数字连续
    """
    # 获取所有匹配3个数字前缀的文件
    files = []
    pattern = r"^(\d{3})\.rst$"
    
    for filename in os.listdir():
        m = re.match(pattern, filename)
        if m:
            files.append(filename)
    
    if not files:
        print("没有找到以3个数字为前缀的 .rst 文件")
        return
    
    # 按文件名排序
    files.sort()
    
    print(f"找到 {len(files)} 个文件需要重命名:")
    for i, old_filename in enumerate(files):
        print(f"  {old_filename}")
    
    # 创建临时文件名映射，避免重命名冲突
    temp_files = []
    for i, old_filename in enumerate(files):
        temp_filename = f"temp_{i:03d}.rst"
        os.rename(old_filename, temp_filename)
        temp_files.append((temp_filename, f"{i+1:03d}.rst"))
        print(f"临时重命名: {old_filename} -> {temp_filename}")
    
    # 重命名为最终的连续编号
    for temp_filename, new_filename in temp_files:
        os.rename(temp_filename, new_filename)
        print(f"最终重命名: {temp_filename} -> {new_filename}")
    
    print(f"重命名完成！文件编号现在从 001 到 {len(files):03d} 连续。")


if __name__ == '__main__':
    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(description='处理 RST 文件的工具')
    parser.add_argument('action', choices=['check_footnote', 'fix_footnote', 'fix_chars', 'rename_files'], 
                       help='要执行的操作: check_footnote(检查脚注), fix_footnote(修复脚注), fix_chars(修复字符), rename_files(重命名文件)')
    
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
    elif args.action == 'rename_files':
        rename_files()  # 重命名文件为连续编号
