#!/bin/bash
# 股票分析日志更新检查脚本

echo "=== 股票分析日志更新检查 ==="
echo ""

# 获取当前时间
CURRENT_TIME=$(date "+%Y-%m-%d %H:%M:%S")
CURRENT_HOUR=$(date "+%H")
CURRENT_MINUTE=$(date "+%M")

echo "📅 当前时间：$CURRENT_TIME"
echo ""

# 检查非公众号版本
echo "📄 检查：股票分析日志.md（非公众号版本）"
echo "----------------------------------------"

# 获取文件最后更新时间
FILE_UPDATE=$(grep -m 1 "_最后更新：" ~/Desktop/claw实验/股票分析日志.md | sed 's/.*_最后更新：//')
if [ -n "$FILE_UPDATE" ]; then
    echo "✓ 文件最后更新：$FILE_UPDATE"
    
    # 提取时间部分
    FILE_HOUR=$(echo "$FILE_UPDATE" | grep -oE "[0-9]{2}:[0-9]{2}" | cut -d: -f1)
    FILE_MINUTE=$(echo "$FILE_UPDATE" | grep -oE "[0-9]{2}:[0-9]{2}" | cut -d: -f2)
    
    # 检查时间是否合理（不应超过当前时间）
    if [ "$FILE_HOUR" -gt "$CURRENT_HOUR" ] 2>/dev/null; then
        echo "⚠️  警告：文件更新时间（$FILE_UPDATE）超过当前时间（$CURRENT_TIME）！"
    elif [ "$FILE_HOUR" -eq "$CURRENT_HOUR" ] && [ "$FILE_MINUTE" -gt "$CURRENT_MINUTE" ] 2>/dev/null; then
        echo "⚠️  警告：文件更新时间（$FILE_UPDATE）超过当前时间（$CURRENT_TIME）！"
    else
        echo "✓ 时间合理"
    fi
else
    echo "❌ 未找到最后更新时间"
fi

# 检查最新事件时间
echo ""
echo "✓ 最新事件时间（前5个）："
grep -E "^\s*-\s*\*\*[0-9]{1,2}:[0-9]{2}\*\*" ~/Desktop/claw实验/股票分析日志.md | head -5 | while read line; do
    EVENT_TIME=$(echo "$line" | grep -oE "\*\*[0-9]{1,2}:[0-9]{2}\*\*" | tr -d '*')
    EVENT_HOUR=$(echo "$EVENT_TIME" | cut -d: -f1)
    EVENT_MINUTE=$(echo "$EVENT_TIME" | cut -d: -f2)
    
    # 检查事件时间是否超过当前时间
    if [ "$EVENT_HOUR" -gt "$CURRENT_HOUR" ] 2>/dev/null; then
        echo "  ⚠️  $EVENT_TIME - 未来时间！"
    elif [ "$EVENT_HOUR" -eq "$CURRENT_HOUR" ] && [ "$EVENT_MINUTE" -gt "$CURRENT_MINUTE" ] 2>/dev/null; then
        echo "  ⚠️  $EVENT_TIME - 未来时间！"
    else
        echo "  ✓ $EVENT_TIME - $(echo "$line" | sed 's/.*\*\* //' | cut -c1-30)"
    fi
done

echo ""

# 检查公众号版本
echo "📄 检查：股票分析日志_公众号版.md（公众号版本）"
echo "----------------------------------------"

# 获取文件最后更新时间
FILE_UPDATE=$(grep -m 1 "_最后更新：\|最后更新：" ~/Desktop/claw实验/股票分析日志_公众号版.md | sed 's/.*最后更新：//')
if [ -n "$FILE_UPDATE" ]; then
    echo "✓ 文件最后更新：$FILE_UPDATE"
    
    # 提取时间部分
    FILE_HOUR=$(echo "$FILE_UPDATE" | grep -oE "[0-9]{2}:[0-9]{2}" | cut -d: -f1)
    FILE_MINUTE=$(echo "$FILE_UPDATE" | grep -oE "[0-9]{2}:[0-9]{2}" | cut -d: -f2)
    
    # 检查时间是否合理
    if [ "$FILE_HOUR" -gt "$CURRENT_HOUR" ] 2>/dev/null; then
        echo "⚠️  警告：文件更新时间（$FILE_UPDATE）超过当前时间（$CURRENT_TIME）！"
    elif [ "$FILE_HOUR" -eq "$CURRENT_HOUR" ] && [ "$FILE_MINUTE" -gt "$CURRENT_MINUTE" ] 2>/dev/null; then
        echo "⚠️  警告：文件更新时间（$FILE_UPDATE）超过当前时间（$CURRENT_TIME）！"
    else
        echo "✓ 时间合理"
    fi
else
    echo "❌ 未找到最后更新时间"
fi

# 检查最新事件时间
echo ""
echo "✓ 最新事件时间（前5个）："
grep -E "^\s*-\s*\*\*[0-9]{1,2}:[0-9]{2}\*\*" ~/Desktop/claw实验/股票分析日志_公众号版.md | head -5 | while read line; do
    EVENT_TIME=$(echo "$line" | grep -oE "\*\*[0-9]{1,2}:[0-9]{2}\*\*" | tr -d '*')
    EVENT_HOUR=$(echo "$EVENT_TIME" | cut -d: -f1)
    EVENT_MINUTE=$(echo "$EVENT_TIME" | cut -d: -f2)
    
    # 检查事件时间是否超过当前时间
    if [ "$EVENT_HOUR" -gt "$CURRENT_HOUR" ] 2>/dev/null; then
        echo "  ⚠️  $EVENT_TIME - 未来时间！"
    elif [ "$EVENT_HOUR" -eq "$CURRENT_HOUR" ] && [ "$EVENT_MINUTE" -gt "$CURRENT_MINUTE" ] 2>/dev/null; then
        echo "  ⚠️  $EVENT_TIME - 未来时间！"
    else
        echo "  ✓ $EVENT_TIME - $(echo "$line" | sed 's/.*\*\* //' | cut -c1-30)"
    fi
done

echo ""
echo "=== 检查完成 ==="
