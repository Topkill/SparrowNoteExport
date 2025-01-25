import os
from bs4 import BeautifulSoup
import html2text
import time

def convert_html_to_md(html_content):
    """
    将HTML内容转换为Markdown文本。
    
    :param html_content: HTML字符串
    :return: Markdown字符串
    """
    h = html2text.HTML2Text()
    h.ignore_links = False  # 根据需要调整这些参数
    h.ignore_images = False
    return h.handle(html_content)

def process_html_file(file_path, output_dir):
    """
    处理单个HTML文件并生成对应的Markdown文件。
    
    :param file_path: HTML文件路径
    :param output_dir: 输出Markdown文件的目录
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
            md_content = convert_html_to_md(html_content)
        
        # 构建输出文件路径
        base_name = os.path.basename(file_path).rsplit('.', 1)[0] + '.md'
        output_path = os.path.join(output_dir, base_name)
        
        # 获取原始文件的时间戳
        stat = os.stat(file_path)
        create_time = stat.st_ctime
        modify_time = stat.st_mtime
        
        with open(output_path, 'w', encoding='utf-8') as md_file:
            md_file.write(md_content)
        
        # 设置新文件的时间戳
        os.utime(output_path, (modify_time, modify_time))
        if os.name == 'nt':  # Windows系统下尝试设置创建时间
            try:
                from win32file import CreateFile, SetFileTime, CloseHandle
                from win32file import GENERIC_WRITE
                from win32file import OPEN_EXISTING
                from win32file import FILE_ATTRIBUTE_NORMAL
                from pywintypes import Time
                
                handle = CreateFile(
                    output_path,
                    GENERIC_WRITE,
                    0,
                    None,
                    OPEN_EXISTING,
                    FILE_ATTRIBUTE_NORMAL,
                    None
                )
                create_time_pywintypes = Time(create_time)
                modify_time_pywintypes = Time(modify_time)
                SetFileTime(handle, create_time_pywintypes, None, modify_time_pywintypes)
                CloseHandle(handle)
            except Exception as e:
                print(f"Failed to set file creation time: {e}")
        
        print(f"Converted {file_path} to {output_path}")
    
    except Exception as e:
        print(f"Failed to process {file_path}: {e}")

def batch_convert_html_to_md(html_dir, output_dir):
    """
    批量转换指定目录下的所有HTML文件为Markdown文件。
    
    :param html_dir: 包含HTML文件的目录
    :param output_dir: 输出Markdown文件的目录
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    html_files = [os.path.join(html_dir, f) for f in os.listdir(html_dir) if f.endswith('.html')]
    
    for html_file in html_files:
        process_html_file(html_file, output_dir)

if __name__ == "__main__":
    html_dir = r".\麻雀记"  # 输入HTML文件所在的目录
    output_dir = r".\麻雀记_md"  # 输出Markdown文件的目录
    batch_convert_html_to_md(html_dir, output_dir)
    input("按任意键退出...")