#!/usr/bin/env python3

"""
邮箱推送脚本 - Python版本
用法: python3 send_email.py <内容文件> <主题>
"""

import sys
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from pathlib import Path
import subprocess

def load_config():
    """加载配置文件"""
    config_file = Path.home() / ".openclaw/skills/stock-wechat/config.json"
    
    if not config_file.exists():
        print(f"❌ 配置文件不存在: {config_file}")
        sys.exit(1)
    
    with open(config_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def markdown_to_html(markdown_text):
    """将Markdown转换为HTML"""
    try:
        # 尝试使用pandoc
        result = subprocess.run(
            ['pandoc', '-f', 'markdown', '-t', 'html'],
            input=markdown_text,
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            return result.stdout
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    
    # 如果pandoc不可用，使用简单HTML包装
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }}
        h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }}
        h2 {{ color: #2c3e50; border-left: 4px solid #3498db; padding-left: 10px; }}
        h3 {{ color: #34495e; }}
        table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #3498db; color: white; }}
        tr:nth-child(even) {{ background-color: #f2f2f2; }}
        strong {{ color: #e74c3c; }}
        code {{ background-color: #f4f4f4; padding: 2px 6px; border-radius: 3px; }}
        pre {{ background-color: #f4f4f4; padding: 10px; border-radius: 5px; overflow-x: auto; }}
    </style>
</head>
<body>
<pre style="white-space: pre-wrap; font-family: inherit;">{markdown_text}</pre>
</body>
</html>"""
    return html

def send_email(config, content_file, subject):
    """发送邮件"""
    # 检查是否启用
    if not config.get('push', {}).get('email', {}).get('enabled', False):
        print("❌ 邮箱推送未启用")
        return False
    
    email_config = config['push']['email']
    email_address = email_config['address']
    smtp_config = email_config['smtp']
    
    # 检查必要配置
    if not all([email_address, smtp_config.get('server'), smtp_config.get('authCode')]):
        print("❌ 邮箱配置不完整")
        return False
    
    # 读取内容文件
    content_path = Path(content_file)
    if not content_path.exists():
        print(f"❌ 内容文件不存在: {content_file}")
        return False
    
    with open(content_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"📧 正在发送邮件...")
    print(f"  收件人: {email_address}")
    print(f"  主题: {subject}")
    
    # 创建邮件
    msg = MIMEMultipart('alternative')
    msg['From'] = email_address  # QQ邮箱要求From必须与登录邮箱一致
    msg['To'] = email_address
    msg['Subject'] = Header(subject, 'utf-8')
    
    # 添加纯文本版本
    text_part = MIMEText(content, 'plain', 'utf-8')
    msg.attach(text_part)
    
    # 添加HTML版本（如果配置为html格式）
    if email_config.get('format') == 'html':
        html_content = markdown_to_html(content)
        html_part = MIMEText(html_content, 'html', 'utf-8')
        msg.attach(html_part)
    
    try:
        # 连接SMTP服务器
        server = smtplib.SMTP(smtp_config['server'], smtp_config['port'])
        server.starttls()
        server.login(email_address, smtp_config['authCode'])
        
        # 发送邮件
        server.sendmail(email_address, [email_address], msg.as_string())
        server.quit()
        
        print(f"✅ 邮件发送成功！")
        print(f"  时间: {Path(content_file).stat().st_mtime}")
        return True
        
    except Exception as e:
        print(f"❌ 邮件发送失败: {e}")
        return False

def main():
    if len(sys.argv) < 3:
        print("用法: python3 send_email.py <内容文件> <主题>")
        sys.exit(1)
    
    content_file = sys.argv[1]
    subject = sys.argv[2]
    
    config = load_config()
    success = send_email(config, content_file, subject)
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
