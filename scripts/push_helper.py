#!/usr/bin/env python3

"""
推送助手 - 自动推送公众号版本到iMessage和邮箱
用法: python3 push_helper.py <公众号版本文件>
"""

import sys
import json
import subprocess
from pathlib import Path

def load_config():
    """加载配置文件"""
    config_file = Path.home() / ".openclaw/skills/stock-wechat/config.json"
    
    if not config_file.exists():
        print(f"❌ 配置文件不存在: {config_file}")
        return None
    
    with open(config_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def push_imessage(content_file, config):
    """推送到iMessage"""
    imessage_config = config.get('push', {}).get('imessage', {})
    
    if not imessage_config.get('enabled', False):
        print("ℹ️  iMessage推送未启用")
        return
    
    if not imessage_config.get('autoPush', {}).get('enabled', False):
        print("ℹ️  iMessage自动推送未启用")
        return
    
    phone_number = imessage_config.get('phoneNumber')
    if not phone_number:
        print("❌ iMessage号码未配置")
        return
    
    print("\n📱 推送到iMessage...")
    
    # 读取内容
    with open(content_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 压缩内容（如果配置为compressed）
    if imessage_config.get('format') == 'compressed':
        lines = content.split('\n')
        compressed_lines = []
        for line in lines[:100]:  # 只取前100行
            line = line.replace('# ', '').replace('## ', '→ ').replace('### ', '• ')
            line = line.replace('**', '')
            if line.strip() and not line.startswith('---') and not line.startswith('|'):
                compressed_lines.append(line)
        content = '\n'.join(compressed_lines)
    
    # 转义双引号
    content_escaped = content.replace('"', '\\"').replace("'", "'\\''")
    
    # 发送iMessage
    applescript = f'''
tell application "Messages"
    send "{content_escaped}" to buddy "{phone_number}" of (service 1 whose service type is iMessage)
end tell
'''
    
    try:
        result = subprocess.run(
            ['osascript', '-e', applescript],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print("✅ iMessage推送成功")
        else:
            print(f"❌ iMessage推送失败: {result.stderr}")
    except Exception as e:
        print(f"❌ iMessage推送失败: {e}")

def push_email(content_file, config):
    """推送到邮箱"""
    email_config = config.get('push', {}).get('email', {})
    
    if not email_config.get('enabled', False):
        print("ℹ️  邮箱推送未启用")
        return
    
    print("\n📧 推送到邮箱...")
    
    # 提取标题（第一行）
    with open(content_file, 'r', encoding='utf-8') as f:
        first_line = f.readline().strip()
        title = first_line.replace('# ', '')
    
    # 调用邮件发送脚本
    script_dir = Path(__file__).parent
    send_email_script = script_dir / "send_email.py"
    
    if not send_email_script.exists():
        print(f"❌ 邮件发送脚本不存在: {send_email_script}")
        return
    
    try:
        result = subprocess.run(
            ['python3', str(send_email_script), str(content_file), title],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        print(result.stdout)
        if result.returncode != 0:
            print(f"❌ 邮箱推送失败: {result.stderr}")
    except Exception as e:
        print(f"❌ 邮箱推送失败: {e}")

def main():
    if len(sys.argv) < 2:
        print("用法: python3 push_helper.py <公众号版本文件>")
        sys.exit(1)
    
    content_file = Path(sys.argv[1])
    
    if not content_file.exists():
        print(f"❌ 内容文件不存在: {content_file}")
        sys.exit(1)
    
    print(f"📤 推送助手启动...")
    print(f"  内容文件: {content_file}")
    
    config = load_config()
    if not config:
        sys.exit(1)
    
    # 执行推送
    push_imessage(content_file, config)
    push_email(content_file, config)
    
    print("\n✅ 推送完成！")

if __name__ == "__main__":
    main()
