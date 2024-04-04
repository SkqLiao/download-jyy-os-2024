import subprocess
import os
import requests
import argparse
from tqdm import tqdm

def runScripts(scripts, lectures, forced_run, logging):
    scripts = [os.path.join(os.path.dirname(__file__), script) for script in scripts]
    root_dir = 'os_lectures'
    
    if not os.path.exists(root_dir):
        os.mkdir(root_dir)
    
    for i in tqdm(lectures, desc='Processing lectures'):
        dir_path = os.path.join(root_dir, f'lec{i}')
        if os.path.exists(dir_path) and not forced_run:
            tqdm.write(f"lec{i} 已存在，跳过")
            continue
        
        if os.path.exists(dir_path):
            # remove existing directory and its subdirectories
            subprocess.run(['rm', '-rf', dir_path])
        
        os.mkdir(dir_path)
        for script in scripts:
            tqdm.write(f"Running {script.split('/')[-1]} on Lecture {i}")
            subprocess.run(['python', script], cwd=dir_path, capture_output=logging)


def getLectureNumber():
    url = 'https://jyywiki.cn/OS/2024/lect{}.md'
    i = 1
    while True:
        response = requests.get(url.format(i))
        if response.status_code == 404:
            return i - 1
        i += 1


parser = argparse.ArgumentParser(description="下载jyy OS 2024 讲义与代码")
parser.add_argument('--force', action='store_true', help="强制下载（否则若文件夹存在则不下载）")
parser.add_argument('--lectures', nargs='+', type=int, help="指定要下载的课程序号")
parser.add_argument('--logging', action='store_true', help="输出日志信息")

args = parser.parse_args()
lecture_number = getLectureNumber()
lectures = [i for i in range(1, lecture_number + 1)]
if args.lectures:
    lectures = args.lectures
    for lecture in lectures:
        if lecture > lecture_number:
            print(f"Lecture {lecture}不存在，合法范围：[1, {lecture_number}]")
            exit()
            
forced_run = True if args.force else False
logging = False if args.logging else True

scripts = ['convert.py', 'get.py']
runScripts(scripts, lectures, forced_run, logging)