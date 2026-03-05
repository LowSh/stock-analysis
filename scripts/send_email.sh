#!/bin/bash

# 邮箱推送脚本
# 用法: ./send_email.sh <内容文件> <主题>

set -e

CONFIG_FILE="$HOME/.openclaw/skills/stock-wechat/config.json"
CONTENT_FILE="$1"
SUBJECT="$2"

# 检查参数
if [ -z "$CONTENT_FILE" ] || [ -z "$SUBJECT" ]; then
    echo "用法: $0 <内容文件> <主题>"
    exit 1
fi

# 检查配置文件
if [ ! -f "$CONFIG_FILE" ]; then
    echo "❌ 配置文件不存在: $CONFIG_FILE"
    exit 1
fi

# 读取配置
EMAIL_ENABLED=$(jq -r '.push.email.enabled' "$CONFIG_FILE")
EMAIL_ADDRESS=$(jq -r '.push.email.address' "$CONFIG_FILE")
SMTP_SERVER=$(jq -r '.push.email.smtp.server' "$CONFIG_FILE")
SMTP_PORT=$(jq -r '.push.email.smtp.port' "$CONFIG_FILE")
AUTH_CODE=$(jq -r '.push.email.smtp.authCode' "$CONFIG_FILE")
EMAIL_FORMAT=$(jq -r '.push.email.format' "$CONFIG_FILE")

# 检查是否启用
if [ "$EMAIL_ENABLED" != "true" ]; then
    echo "❌ 邮箱推送未启用"
    exit 0
fi

# 检查必要配置
if [ -z "$EMAIL_ADDRESS" ] || [ -z "$SMTP_SERVER" ] || [ -z "$AUTH_CODE" ]; then
    echo "❌ 邮箱配置不完整"
    exit 1
fi

# 检查内容文件
if [ ! -f "$CONTENT_FILE" ]; then
    echo "❌ 内容文件不存在: $CONTENT_FILE"
    exit 1
fi

echo "📧 正在发送邮件..."
echo "  收件人: $EMAIL_ADDRESS"
echo "  主题: $SUBJECT"
echo "  格式: $EMAIL_FORMAT"

# 转换Markdown到HTML（如果需要）
if [ "$EMAIL_FORMAT" == "html" ]; then
    # 使用pandoc转换（如果可用）
    if command -v pandoc &> /dev/null; then
        HTML_CONTENT=$(pandoc -f markdown -t html "$CONTENT_FILE")
        CONTENT_TYPE="text/html; charset=utf-8"
    else
        # 如果没有pandoc，使用简单HTML包装
        HTML_CONTENT="<html><head><meta charset='utf-8'></head><body><pre>$(cat "$CONTENT_FILE")</pre></body></html>"
        CONTENT_TYPE="text/html; charset=utf-8"
    fi
    BODY="$HTML_CONTENT"
else
    BODY=$(cat "$CONTENT_FILE")
    CONTENT_TYPE="text/plain; charset=utf-8"
fi

# 发送邮件（使用curl）
RESPONSE=$(curl -s --url "smtp://$SMTP_SERVER:$SMTP_PORT" \
    --ssl-reqd \
    --mail-from "$EMAIL_ADDRESS" \
    --mail-rcpt "$EMAIL_ADDRESS" \
    --user "$EMAIL_ADDRESS:$AUTH_CODE" \
    -T - <<EOF
From: $EMAIL_ADDRESS
To: $EMAIL_ADDRESS
Subject: $SUBJECT
Content-Type: $CONTENT_TYPE

$BODY
EOF
)

if [ $? -eq 0 ]; then
    echo "✅ 邮件发送成功！"
    echo "  时间: $(date '+%Y-%m-%d %H:%M:%S')"
else
    echo "❌ 邮件发送失败"
    echo "  错误: $RESPONSE"
    exit 1
fi
