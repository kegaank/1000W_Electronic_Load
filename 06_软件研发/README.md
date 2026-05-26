# 06 软件研发

## 子目录
```
06_软件研发/
├── README.md
├── firmware/        # 固件（C/FreeRTOS）
├── web_ui/          # Web控制面板（React）
├── app/             # 移动App（React Native）
├── cloud/           # 云端平台（MQTT/InfluxDB/Grafana）
├── cli/             # Python CLI 工具
└── docs/            # 软件架构文档
```

## 关键交付物

| 交付物 | 状态 | 负责人 |
|---|---|---|
| 固件骨架（FreeRTOS） | ⏳ | AI |
| PID控制环路代码 | ⏳ | AI |
| 通信协议实现（Modbus/SCPI） | ⏳ | AI |
| 数据采集驱动 | ⏳ | AI |
| Web UI 控制面板 | ⏳ | AI |
| 移动App（iOS/Android） | ⏳ | AI |
| 云端数据平台 | ⏳ | AI |
| Python CLI 工具 | ⏳ | AI |
| OTA 更新机制 | ⏳ | AI |

## 对应周次
W9起持续（固件每2-4周OTA迭代）

## 联动维度
- ← 03 系统设计（控制算法参数）
- ← 05 硬件研发（联调）
- → 07 测试验证
- → 11 客户成功（OTA推送）
