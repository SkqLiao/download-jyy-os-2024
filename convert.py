from bs4 import BeautifulSoup
import os
import requests
import re
import base64
from urllib.parse import urljoin
import asyncio
from pyppeteer import launch

async def html_to_pdf(html_path, pdf_path):
    abs_html_path = f'file:///{os.path.abspath(html_path)}'
    
    browser = await launch(args=['--no-sandbox'])
    page = await browser.newPage()
    await page.goto(abs_html_path, {'waitUntil': 'networkidle0'})
    
    # 设置页边距为0
    await page.pdf({
        'path': pdf_path,
        'printBackground': True,
        'margin': {'top': '0mm', 'right': '0mm', 'bottom': '0mm', 'left': '0mm'}, # margin still exists
    })
    
    await browser.close()

def download_html(lecture_id):
    files_list = []
    
    for i in range(100):
        url = f'https://jyywiki.cn/OS/2024/slides/{lecture_id}.{i}.html'
        response = requests.get(url)

        if response.status_code == 200:
            file_name = f'{lecture_id}.{i}.html'
            with open(file_name, 'w', encoding='utf-8') as file:
                file.write(response.text)
            
            print(f'Downloaded: {file_name}')
            files_list.append(file_name)
    print('下载完成！共下载', len(files_list), '个文件')
    return files_list

def merge(files, html_file):
    all_svgs = []

    for file_path in files[1:]:
        with open(file_path, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'html.parser')
            svgs = soup.find_all('svg', {'data-marpit-svg': True})
            all_svgs.extend(svgs)
    
    first_file_path = files[0]
    with open(first_file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
    
    target_div = soup.body.find('div')
    if not target_div:
        print("在第一个文件的<body>内没有找到<div>元素")
        return
    
    for svg in all_svgs:
        target_div.append(svg)
    
    with open(html_file, 'w', encoding='utf-8') as file:
        file.write(str(soup))
    print(f"合并成功，已保存到{html_file}")


def encode_image_to_base64(image_path):
    with open(image_path, 'rb') as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_string

def download_and_replace(file_path, base_url):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    pattern = r'"(\.\./\.\./[^/]+/[^/]+\.\w+)"'
    matches = re.findall(pattern, content)
    image_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg']
    for match in set(matches):
        full_url = urljoin(base_url, match)
        file_name = os.path.basename(match)
        
        if not any(match.endswith(ext) for ext in image_extensions):
            content = content.replace(match, full_url)
            print('替换', match, '为', full_url)
        else:
            response = requests.get(full_url)
            encoded_content = base64.b64encode(response.content).decode('utf-8')
            mime_type = 'image/webp' if match.endswith('.webp') else 'image/png'
            data_url = f'data:{mime_type};base64,{encoded_content}'
            content = content.replace(match, data_url)
            print('将', match, '替换为Base64编码的数据URL')

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)


pwd = os.getcwd()
lecture_id = int(pwd.split('/')[-1].split('lec')[-1])
html_file = f'lec{lecture_id}.html'
pdf_file = f'lec{lecture_id}.pdf'

files = download_html(lecture_id)
merge(files, html_file)
base_url = 'https://jyywiki.cn/OS/2024/slides/'
download_and_replace(html_file, base_url)
print('合并完成！')
html_path = os.path.join(pwd, html_file)
asyncio.get_event_loop().run_until_complete(html_to_pdf(html_path, pdf_file))
