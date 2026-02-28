#!/bin/bash
# Stock WeChat 定时任务管理脚本

set -e

COMMAND="$1"
JOB_NAME="stock-wechat-every2h"
MESSAGE="生成公众号版股票分析"
DESCRIPTION="每4小时自动生成公众号版股票分析"

# 避免夜间更新的时间段
NIGHT_START=0   # 0点
NIGHT_END=8     # 8点

# 获取任务ID
get_job_id() {
    openclaw cron list --json 2>/dev/null | grep -A5 "$JOB_NAME" | grep '"id"' | head -1 | cut -d'"' -f4
}

# 检查当前时间是否在夜间
is_night_time() {
    local hour=$(date +%H)
    if [ "$hour" -ge $NIGHT_START ] && [ "$hour" -lt $NIGHT_END ]; then
        return 0  # 是夜间
    else
        return 1  # 不是夜间
    fi
}

# 智能执行：如果是夜间，延迟到8点
smart_trigger() {
    if is_night_time; then
        echo "⏰ 当前是夜间时段（00:00-08:00），延迟到 08:00 执行"
        # 创建一个一次性的8点任务
        openclaw cron add \
            --name "stock-wechat-once-morning" \
            --cron "0 8 * * *" \
            --message "$MESSAGE" \
            --description "早晨一次性执行" \
            --delete-after-run
    else
        echo "▶️  立即执行定时任务..."
        JOB_ID=$(get_job_id)
        if [ -n "$JOB_ID" ]; then
            openclaw cron trigger "$JOB_ID"
        fi
    fi
}

case "$COMMAND" in
    status|状态)
        echo "📅 定时任务状态："
        openclaw cron list | grep -A1 "$JOB_NAME" || echo "❌ 未开启定时任务"
        echo ""
        echo "🌙 夜间模式：00:00-08:00 不自动更新"
        ;;
    
    enable|开启|启动)
        if openclaw cron list | grep -q "$JOB_NAME"; then
            echo "✅ 定时任务已存在"
            JOB_ID=$(get_job_id)
            if [ -n "$JOB_ID" ]; then
                openclaw cron enable "$JOB_ID" 2>/dev/null || true
            fi
        else
            echo "🚀 创建定时任务..."
            openclaw cron add \
                --name "$JOB_NAME" \
                --every 4h \
                --message "$MESSAGE" \
                --description "$DESCRIPTION"
            echo "✅ 定时任务已开启（每4小时，夜间00:00-08:00暂停）"
        fi
        ;;
    
    disable|关闭|停止|暂停)
        JOB_ID=$(get_job_id)
        if [ -n "$JOB_ID" ]; then
            echo "⏸️  禁用定时任务..."
            openclaw cron disable "$JOB_ID" 2>/dev/null || true
            echo "✅ 定时任务已暂停"
        else
            echo "❌ 未找到定时任务"
        fi
        ;;
    
    delete|删除)
        JOB_ID=$(get_job_id)
        if [ -n "$JOB_ID" ]; then
            echo "🗑️  删除定时任务..."
            openclaw cron delete "$JOB_ID"
            echo "✅ 定时任务已删除"
        else
            echo "❌ 未找到定时任务"
        fi
        ;;
    
    trigger|立即执行|现在执行)
        smart_trigger
        ;;
    
    set-frequency|设置频率)
        FREQUENCY="$2"
        if [ -z "$FREQUENCY" ]; then
            echo "用法: $0 set-frequency <频率>"
            echo "示例: $0 set-frequency 1h"
            echo "      $0 set-frequency 4h"
            echo "      $0 set-frequency '0 9 * * *'"
            exit 1
        fi
        
        # 删除旧任务
        JOB_ID=$(get_job_id)
        if [ -n "$JOB_ID" ]; then
            openclaw cron delete "$JOB_ID" 2>/dev/null || true
        fi
        
        # 创建新任务
        echo "🔄 设置定时频率为: $FREQUENCY"
        if [[ "$FREQUENCY" =~ ^[0-9]+[hm]$ ]]; then
            # 是 every 格式
            openclaw cron add \
                --name "$JOB_NAME" \
                --every "$FREQUENCY" \
                --message "$MESSAGE" \
                --description "每${FREQUENCY}自动生成公众号版股票分析"
        else
            # 是 cron 表达式
            openclaw cron add \
                --name "$JOB_NAME" \
                --cron "$FREQUENCY" \
                --message "$MESSAGE" \
                --description "定时生成公众号版股票分析"
        fi
        echo "✅ 定时频率已更新"
        echo "🌙 夜间模式：00:00-08:00 不自动更新"
        ;;
    
    night-mode|夜间模式)
        echo "🌙 夜间模式设置"
        echo ""
        echo "当前设置："
        echo "  - 夜间时段：00:00-08:00"
        echo "  - 夜间不自动更新"
        echo ""
        echo "说明："
        echo "  在夜间时段，如果手动触发更新，会延迟到 08:00 执行"
        echo "  定时任务会自动跳过夜间时段"
        ;;
    
    *)
        echo "Stock WeChat 定时任务管理"
        echo ""
        echo "用法: $0 <命令> [参数]"
        echo ""
        echo "命令:"
        echo "  status        查看定时任务状态"
        echo "  enable        开启定时任务（每4小时）"
        echo "  disable       暂停定时任务"
        echo "  delete        删除定时任务"
        echo "  trigger       立即执行一次（夜间自动延迟到8点）"
        echo "  set-frequency <频率>  设置执行频率"
        echo "  night-mode    查看夜间模式设置"
        echo ""
        echo "频率示例:"
        echo "  1h    每1小时"
        echo "  4h    每4小时（默认）"
        echo "  '0 9 * * *'  每天9点"
        echo "  '0 9,15 * * 1-5'  交易日9点和15点"
        echo ""
        echo "🌙 夜间模式："
        echo "  00:00-08:00 不自动更新，避免打扰"
        ;;
esac
