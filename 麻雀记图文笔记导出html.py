import sqlite3
import os
from datetime import datetime
import re
import html
from bs4 import BeautifulSoup  # 导入BeautifulSoup
import time

# 连接到SQLite数据库
db_path=input('请输入麻雀记db文件路径或拖动db文件至此：')
print(db_path)
db_path=db_path.strip().strip('"').strip("'")
conn = sqlite3.connect(db_path)  # 替换为你的db文件名
cursor = conn.cursor()

# 确认目标文件夹存在，如果不存在则创建
output_dir = r".\麻雀记"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 执行查询语句
query = """
SELECT title, content, create_time, update_time
FROM card
WHERE type = 0 AND IS_INTERNAL = 0 AND CARD_STATUS = 0;
"""
cursor.execute(query)

# 获取所有符合条件的记录
records = cursor.fetchall()

for record in records:
    title, content, create_time_ms, update_time_ms = record
    
    # 将毫秒时间戳转换为正常时间
    if create_time_ms:
        create_time = datetime.fromtimestamp(create_time_ms / 1000).strftime('%Y-%m-%d %H:%M:%S')
    else:
        create_time = ''
    
    if update_time_ms:
        update_time = datetime.fromtimestamp(update_time_ms / 1000).strftime('%Y-%m-%d %H:%M:%S')
    else:
        update_time = ''
    
    # 解码HTML实体并提取纯文本
    if not title and content:
        content_unescaped = html.unescape(content)  # 解码HTML实体
        soup = BeautifulSoup(content_unescaped, 'html.parser')  # 使用BeautifulSoup解析HTML
        text_content = soup.get_text().strip()  # 提取纯文本并去除首尾空白
        first_line = text_content.split('\n', 1)[0]  # 取第一行文本
        file_name_base = re.sub(r'[^\w\-_]', '', first_line)[:10]  # 清理文件名并限制长度
    else:
        title_unescaped = html.unescape(title.strip()) if title else ''
        file_name_base = re.sub(r'[^\w\-_]', '', title_unescaped)[:10]  # 同样清理文件名并限制长度
    
    # 如果文件名为空，提供一个默认值
    if not file_name_base:
        file_name_base = '默认文件名'
    
    # 构建完整的文件路径
    file_path = os.path.join(output_dir, f"{file_name_base}.html")
    
    # 检查文件是否已经存在，如果存在则添加编号以避免覆盖
    counter = 1
    while os.path.exists(file_path):
        file_path = os.path.join(output_dir, f"{file_name_base}_{counter}.html")
        counter += 1
    
    # 构建HTML内容
    html_content = ""
    if title:  # 如果有标题，则添加到HTML内容中
        html_content += f"<h1>{title}</h1>"
    html_content += f"{content}"
    
    # 写入HTML文件
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(html_content)
        
        print(f"Created HTML file: {file_path}")
        
        # 设置文件的修改时间和访问时间
        if create_time_ms and update_time_ms:
            create_time_seconds = int(create_time_ms / 1000)
            update_time_seconds = int(update_time_ms / 1000)
            os.utime(file_path, (update_time_seconds, update_time_seconds))
            
            # Windows不直接支持设置创建时间，但可以通过pywin32库间接实现
            try:
                import win32file
                import pywintypes
                handle = win32file.CreateFile(
                    file_path,
                    win32file.GENERIC_WRITE,
                    0,
                    None,
                    win32file.OPEN_EXISTING,
                    0,
                    None
                )
                create_time_pywintypes = pywintypes.Time(datetime.fromtimestamp(create_time_seconds))
                update_time_pywintypes = pywintypes.Time(datetime.fromtimestamp(update_time_seconds))
                win32file.SetFileTime(handle, create_time_pywintypes, None, update_time_pywintypes)
                handle.close()
                
            except Exception as e:
                print(f"Failed to set file creation time: {e}")
                
    except OSError as e:
        print(f"Failed to create HTML file {file_path}: {e}")

# 关闭数据库连接
conn.close()
input("按任意键退出...")
