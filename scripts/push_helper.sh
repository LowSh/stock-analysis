#!/bin/bash

# 推送助手脚本 - 自动推送公众号版本到iMessage和邮箱
# 用法: ./push_helper.sh <公众号版本文件>

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="$HOME/.openclaw/skills/stock-wechat/config.json"
CONTENT_FILE="$1"

# 检查参数
if [ -z "$CONTENT_FILE" ]; then
    echo "用法: $0 <公众号版本文件>"
    exit 1
fi

if [ ! -f "$CONTENT_FILE" ]; then
    echo "❌ 内容文件不存在: $CONTENT_FILE"
    exit 1
fi

if [ ! -f "$CONFIG_FILE" ]; then
    echo "❌ 配置文件不存在: $CONFIG_FILE"
    exit 1
fi

# 读取配置
IMESSAGE_ENABLED=$(jq -r '.push.imessage.enabled // false' "$CONFIG_FILE")
IMESSAGE_AUTO_PUSH=$(jq -r '.push.imessage.autoPush.enabled // false' "$CONFIG_FILE")
EMAIL_ENABLED=$(jq -r '.push.email.enabled // false' "$CONFIG_FILE")

echo "📤 推送助手启动..."
echo "  内容文件: $CONTENT_FILE"

# 推送到iMessage
push_imessage() {
    if [ "$IMESSAGE_ENABLED" == "true" ] && [ "$IMESSAGE_AUTO_PUSH" == "true" ]; then
        echo ""
        echo "📱 推送到iMessage..."
        
        PHONE_NUMBER=$(jq -r '.push.imessage.phoneNumber' "$CONFIG_FILE")
        FORMAT=$(jq -r '.push.imessage.format' "$CONFIG_FILE")
        
        if [ -z "$PHONE_NUMBER" ]; then
            echo "❌ iMessage号码未配置"
            return 1
        fi
        
        # 读取内容
        CONTENT=$(cat "$CONTENT_FILE")
        
        # 压缩内容（如果配置为compressed）
        if [ "$FORMAT" == "compressed" ]; then
            # 生成压缩版（保留关键信息）
            CONTENT=$(echo "$CONTENT" | \
                sed 's/^# //g' | \
                sed 's/^## /→ /g' | \
                sed 's/^### /• /g' | \
                sed 's/\*\*//g' | \
                sed '/^---$/d' | \
                sed '/^|/d' | \
                head -100)
        fi
        
        # 发送iMessage
        osascript <<EOF
tell application "Messages"
    send "$CONTENT" to buddy "$PHONE_NUMBER" of (service 1 whose service type is iMessage)
end tell
EOF
        
        if [ $? -eq 0 ]; then
            echo "✅ iMessage推送成功"
        else
            echo "❌ iMessage推送失败"
        fi
    fi
}

# 推送到邮箱
push_email() {
    if [ "$EMAIL_ENABLED" == "true" ]; then
        echo ""
        echo "📧 推送到邮箱..."
        
        # 提取标题（第一行）
        TITLE=$(head -1 "$CONTENT_FILE" | sed 's/^# //g')
        
        # 调用Python邮件发送脚本
        python3 "$SCRIPT_DIR/send_email.py" "$CONTENT_FILE" "$TITLE"
        
        if [ $? -eq 0 ]; then
            echo "✅ 邮箱推送成功"
        else
            echo "❌ 邮箱推送失败"
        fi
    fi
}

# 执行推送
push_imessage
push_email

echo ""
echo "✅ 推送完成！"
