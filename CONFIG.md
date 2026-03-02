# 📱 推送配置说明

_配置文件：config.json_

---

## 📋 配置项说明

### 1️⃣ iMessage推送配置

```json
"push": {
  "imessage": {
    "enabled": true,                    // 是否启用iMessage推送
    "phoneNumber": "+86 YOUR_PHONE_NUMBER",   // 接收手机号
    "autoPush": {
      "enabled": true,                  // 是否自动推送
      "times": ["09:00", "12:30"],      // 自动推送时间
      "afterMarketClose": true          // 收盘后是否推送
    },
    "format": "compressed",             // 推送格式：compressed（压缩版）/ full（完整版）
    "maxMessageLength": 4000,           // 最大消息长度（字符）
    "retryOnFailure": true,             // 失败是否重试
    "retryCount": 3                     // 重试次数
  }
}
```

**配置说明：**

| 配置项 | 类型 | 说明 | 默认值 |
|--------|------|------|--------|
| `enabled` | boolean | 是否启用iMessage推送 | `true` |
| `phoneNumber` | string | 接收手机号（带国家代码） | `+86 YOUR_PHONE_NUMBER` |
| `autoPush.enabled` | boolean | 是否自动推送 | `true` |
| `autoPush.times` | array | 自动推送时间（24小时制） | `["09:00", "12:30"]` |
| `autoPush.afterMarketClose` | boolean | 收盘后是否推送（15:00） | `true` |
| `format` | string | 推送格式：`compressed` 或 `full` | `compressed` |
| `maxMessageLength` | number | 最大消息长度（字符） | `4000` |
| `retryOnFailure` | boolean | 失败是否重试 | `true` |
| `retryCount` | number | 重试次数 | `3` |

---

### 2️⃣ 邮箱推送配置

```json
"push": {
  "email": {
    "enabled": false,                   // 是否启用邮箱推送
    "address": "YOUR_EMAIL@qq.com",      // 接收邮箱
    "smtp": {
      "server": "smtp.qq.com",          // SMTP服务器
      "port": 587,                      // SMTP端口
      "authCode": ""                    // SMTP授权码（需要填写）
    },
    "format": "html"                    // 邮件格式：html / text
  }
}
```

**获取QQ邮箱授权码：**
1. 登录QQ邮箱网页版
2. 设置 → 账户 → POP3/IMAP/SMTP服务
3. 开启SMTP服务，生成授权码
4. 填写到 `authCode` 字段

---

### 3️⃣ 内容配置

```json
"content": {
  "includeHistoricalEvents": true,      // 是否包含历史事件
  "eventBackgroundInfo": true,          // 是否显示事件背景信息
  "hotSectorsCount": 5,                 // 热门板块数量
  "stockRecommendationsPerSector": 3,   // 每个板块推荐股票数量
  "includeMarketData": true,            // 是否包含市场数据
  "includeRiskWarning": true            // 是否包含风险提示
}
```

---

### 4️⃣ 定时任务配置

```json
"schedule": {
  "morning": {
    "enabled": true,                    // 是否启用早上更新
    "time": "09:00",                    // 更新时间
    "includePreviousNightNews": true,   // 是否包含前一晚新闻
    "previousNightTimeRange": ["18:00", "24:00"]  // 前一晚新闻时间范围
  },
  "noon": {
    "enabled": true,                    // 是否启用中午更新
    "time": "12:30"                     // 更新时间
  },
  "custom": []                          // 自定义定时任务
}
```

**添加自定义定时任务：**
```json
"custom": [
  {
    "name": "收盘提醒",
    "time": "15:05",
    "enabled": true
  }
]
```

---

### 5️⃣ 显示配置

```json
"display": {
  "timezone": "Asia/Shanghai",          // 时区
  "dateFormat": "YYYY-MM-DD",           // 日期格式
  "timeFormat": "HH:mm",                // 时间格式
  "emoji": true,                        // 是否使用emoji
  "colorScheme": {                      // 颜色方案（公众号版本）
    "body": "#333333",
    "title": "#2c3e50",
    "highlight": "#e74c3c"
  }
}
```

---

### 6️⃣ 高级配置

```json
"advanced": {
  "enableScreenshot": false,            // 是否启用截图功能
  "screenshotProvider": "openclaw",     // 截图服务提供商
  "dataSources": [                      // 数据源
    "10jqka.com.cn",
    "cls.cn",
    "eastmoney.com"
  ],
  "archiveRetention": {                 // 存档保留时间（天）
    "dailyLogs": 30,
    "coreContent": 90
  },
  "logLevel": "info"                    // 日志级别：debug / info / warn / error
}
```

---

## 🔧 配置修改方式

### 方法1：直接编辑配置文件

**配置文件位置：**
```
~/.openclaw/skills/stock-wechat/config.json
```

**编辑步骤：**
1. 打开配置文件
2. 修改配置项
3. 保存文件
4. 下次运行时生效

### 方法2：通过命令修改（待实现）

```bash
# 启用/禁用iMessage推送
openclaw stock-config --imessage-enable true

# 修改接收号码
openclaw stock-config --imessage-phone "+86 13800000000"

# 修改推送时间
openclaw stock-config --schedule-morning "09:00"
```

---

## 📱 使用示例

### 示例1：关闭自动推送

```json
"push": {
  "imessage": {
    "enabled": true,
    "autoPush": {
      "enabled": false    // 关闭自动推送
    }
  }
}
```

**效果：** 不会自动推送，需要手动触发（"推送到手机"）

---

### 示例2：只推送早上版本

```json
"push": {
  "imessage": {
    "enabled": true,
    "autoPush": {
      "enabled": true,
      "times": ["09:00"]   // 只在早上9点推送
    }
  }
}
```

**效果：** 只在早上9:00自动推送，中午12:30不推送

---

### 示例3：添加收盘后推送

```json
"push": {
  "imessage": {
    "enabled": true,
    "autoPush": {
      "enabled": true,
      "times": ["09:00", "12:30"],
      "afterMarketClose": true   // 15:05推送
    }
  }
}
```

**效果：** 早上9:00、中午12:30、收盘后15:05都会推送

---

### 示例4：修改接收号码

```json
"push": {
  "imessage": {
    "enabled": true,
    "phoneNumber": "+86 13800000000"   // 改为新号码
  }
}
```

**效果：** 推送到新号码

---

### 示例5：启用邮箱推送

```json
"push": {
  "email": {
    "enabled": true,
    "address": "your@email.com",
    "smtp": {
      "server": "smtp.qq.com",
      "port": 587,
      "authCode": "abcdefghijklmnop"   // 填写授权码
    }
  }
}
```

**效果：** 同时推送到iMessage和邮箱

---

## ⚠️ 注意事项

1. **手机号格式：** 必须带国家代码（如：+86）
2. **授权码安全：** 不要泄露SMTP授权码
3. **推送频率：** 避免过于频繁的推送
4. **字符限制：** iMessage单条消息约4000字符
5. **网络要求：** iMessage需要网络连接

---

## 🔄 配置生效

**修改配置后：**
- ✅ 立即生效（下次运行时）
- ❌ 无需重启OpenClaw
- ✅ 自动保存到GitHub

---

## 📞 技术支持

如有问题，请查看：
- 配置文件：`~/.openclaw/skills/stock-wechat/config.json`
- 日志文件：`~/.openclaw/logs/stock-wechat.log`
- GitHub：https://github.com/LowSh/stock-analysis

---

_最后更新：2026-03-02_
