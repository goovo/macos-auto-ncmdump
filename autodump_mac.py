from ncmdump import dump
import os
import fnmatch

print("软件仅供学习交流，请勿用于商业及非法用途，如产生法律纠纷与本人无关。")
print("------")
print("请在下方输入网易云音乐下载路径，请确保输入正确，否则无法正常转换。")
print("如果您不知道路径在哪里，默认路径为：~/Library/Application Support/NeteaseMusicMac/CloudMusic/")
print("如留空，使用默认路径")
default_path = os.path.expanduser("/Users/zen/Music/网易云音乐/")
download_folder = input("下载路径：") or default_path
os.system('clear')
waiting = True
print("当前下载路径：" + download_folder)
print("您现在可以在网易云音乐客户端中直接下载歌曲，本工具会自动将ncm转换成mp3格式。")
print("等待转换...")

def all_files(root, patterns='*', single_level=False, yield_folder=False):
    patterns = patterns.split(';')
    for path, subdirs, files in os.walk(root):
        if yield_folder:
            files.extend(subdirs)
        files.sort()
        for fname in files:
            for pt in patterns:
                if fnmatch.fnmatch(fname, pt):
                    yield os.path.join(path, fname)
                    break
        if single_level:
            break

try:
    while True:
        thefile = list(all_files(download_folder, '*.ncm'))
        for item in thefile:
            if waiting == True:
                waiting = False
                os.system('clear')
            print(dump(item), "转换成功！")
            os.remove(item)
except KeyboardInterrupt:
    print("\n程序已退出")