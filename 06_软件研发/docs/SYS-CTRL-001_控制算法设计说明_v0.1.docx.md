# SYS-CTRL-001 控制算法设计说明 v0.1

> **项目**: EL-1000 1000W 可编程电子负载
> **日期**: 2026-05-31
> **状态**: Draft
> **负责人**: 固件团队

---

## 1. 文档概述

### 1.1 目的
本文档描述 EL-1000 电子负载的控制算法架构、PID 算法实现、环路参数推导、模式切换逻辑、保护集成及校准策略。

### 1.2 参考文档
| 文档编号 | 名称 |
|---------|------|
| SYS-SCH-001 | 功率级原理图设计说明 v0.4 |
| SYS-SCH-002 | 控制电路原理图设计说明 v0.1 |
| — | firmware/docs/arch.md (固件架构) |
| — | pid.h / pid.c (PID实现) |
| — | current_loop.h/.c (电流环路) |
| — | voltage_loop.h/.c (电压环路) |

### 1.3 缩写
| 缩写 | 说明 |
|------|------|
| CC | Constant Current (恒流模式) |
| CV | Constant Voltage (恒压模式) |
| CR | Constant Resistance (恒阻模式) |
| CW | Constant Power (恒功率模式) |
| HRPWM | High-Resolution PWM (高分辨率PWM) |
| CMPSS | Comparator Subsystem (比较器子系统) |
| MEP | Micro-Edge Positioner (微边沿定位器) |
| OCP | Over-Current Protection |
| OVP | Over-Voltage Protection |
| OTP | Over-Temperature Protection |
| OPP | Over-Power Protection |

---

## 2. 控制环路架构

### 2.1 总体框图

```
                    ┌─────────────────────────────────────────────┐
                    │              EL-1000 Control System          │
                    │                                              │
  Setpoint ────────►│  ┌─────────┐  ┌──────────┐  ┌───────────┐  │
  (I/V/R/P)         │  │  Mode   │  │  Outer   │  │  Inner    │  │
                    │  │ Select  │──►│  Loop    │──►│  Current  │──► PWM ──► MOSFETs
                    │  │         │  │  (V/R/P) │  │  Loop     │  │
                    │  └─────────┘  └──────────┘  └─────┬─────┘  │
                    │        ▲                           │        │
                    │        │  Voltage / Power FB       │ Current│
                    │        └───────────────────────────┤ FB    │
                    │                                    │        │
                    │  ┌──────────┐  ┌──────────┐        │        │
                    │  │ CMPSS    │  │ SW       │        │        │
                    │  │ HW Trip  │  │ Protection│        │        │
                    │  └──────────┘  └──────────┘        │        │
                    └────────────────────────────────────┴────────┘
```

### 2.2 环路层次

| 环路 | 类型 | 更新率 | 输出 | 应用模式 |
|------|------|--------|------|---------|
| 内环 — 电流环 | PI (并联式) | 860 Hz | 占空比 → HRPWM | CC, CV, CR, CW |
| 外环 — 电压环 | PI (并联式) | 860 Hz | 电流给定 → 内环 | CV |
| 外环 — 功率环 | PI (并联式) | 860 Hz | 电流给定 → 内环 | CW (规划中) |
| 外环 — 电阻环 | PI (并联式) | 860 Hz | 电流给定 → 内环 | CR (规划中) |

### 2.3 级联控制策略

CV/CR/CW 模式使用 **级联控制** 结构：
- **外环** (电压/功率/电阻) 输出电流给定值 (I_demand)
- **内环** (电流) 快速跟踪该给定值
- 内环带宽 ≫ 外环带宽 (典型比值为 5:1 至 10:1)

优势：
- 内环快速响应电流扰动，保护 MOSFET
- 外环可独立设计，无需担心电流环稳定性
- 自然实现限流保护 (外环输出限幅)

---

## 3. PID 算法实现

### 3.1 算法形式：并联式 (Parallel Form)

采用 **测量值微分 (Derivative on Measurement)** 的并联式 PID：

```
error[n]     = setpoint - measurement[n]
p_term[n]    = Kp × error[n]
i_term[n]    = i_term[n-1] + Ki × error[n] × dt
d_term[n]    = -Kd × (measurement[n] - measurement[n-1]) / dt
output[n]    = p_term[n] + i_term[n] + d_term[n]
output[n]    = clamp(output[n], min_output, max_output)
```

**传递函数 (连续域)**:

```
            ┌         1             s·Td ┐
Gc(s) = Kp ·│ 1 + ──────── + ──────────── │
            └       s·Ti       1 + s·Td/N ┘
```

离散化采用 **前向欧拉法** (Forward Euler):
- s → (z-1)/Ts

### 3.2 抗饱和 (Anti-Windup)

采用 **积分钳位 (Integral Clamping)** 策略：

```
if output[n] >= max_output AND error[n] > 0:
    # 输出饱和且误差同向 — 冻结积分
    i_term[n] = i_term[n-1]  # 不累加
elif output[n] <= min_output AND error[n] < 0:
    # 输出饱和且误差反向 — 冻结积分
    i_term[n] = i_term[n-1]
else:
    i_term[n] = i_term[n-1] + Ki × error[n] × dt

# 辅助限幅：对积分项单独限幅
i_term[n] = clamp(i_term[n], max_integral, min_integral)
```

当前实现使用简化版：仅对积分项单独限幅 (±max_integral)，可防止大部分 windup 问题。待进一步调优。

### 3.3 输出限幅

| 环路 | min_output | max_output | 说明 |
|------|-----------|-----------|------|
| 电流环 | 0.0 | 0.95 | 占空比 (HRPWM 0-95%) |
| 电压环 | 0.0 | 110.0 | 电流给定 (A) |

### 3.4 微分项说明

当前电流环 Kd = 0.001 (接近零)，实际表现为 **PI 控制器**。
- 电流环：PI (Kd 接近零，测量值微分形式防止微分冲激)
- 电压环：PI (Kd = 0，纯 PI)

---

## 4. 采样策略

### 4.1 PID 时序 (860 Hz)

```
周期 T = 1/860 ≈ 1.163 ms

┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│ ADC     │    │ PID     │    │ HRPWM   │    │ Sleep   │
│ Sample  │───►│ Compute │───►│ Update  │───►│ (剩余)  │
│ ~20 µs  │    │ ~10 µs  │    │ ~5 µs   │    │~1.13 ms │
└─────────┘    └─────────┘    └─────────┘    └─────────┘
```

### 4.2 ADC 交错采样 (ADC Interleaving)

C2000 F28E12x ADC 支持 13 通道采样。采样策略：
1. **SOC 触发**: ePWM1 时基触发 ADC SOC (860 Hz)
2. **通道序列**: Vload → Iload → Vref → Iref → Temp1..Temp4 → PSU → 保留
3. **交错模式**: 使用两个 ADC 内核 (A + B) 交错采样，等效采样率 1.72 kHz
4. **结果读取**: PID 任务等待所有通道转换完成 (EOC 中断)

### 4.3 HRPWM 同步

- HRPWM 频率: **25 kHz** (周期 40 µs)
- HRPWM 分辨率: **~150 ps** (MEP 步进)
- **同步策略**: PID 更新在 ePWM1 时基零交叉时写入新占空比，保证每个 PWM 周期占空比一致
- **RC 滤波器**: 10 kΩ + 1 µF (f_c ≈ 15.9 Hz)，将 PWM 转换为模拟参考电压 (等效 ~15.2 bit DAC)

---

## 5. PI 参数推导

### 5.1 电流环参数推导

#### 5.1.1 被控对象模型

**功率级**: 12 × M90N20 MOSFET + 12 × 0.050Ω 源极电阻

```
等效源极电阻: R_sense = 0.050Ω / 12 = 0.004167 Ω
MOSFET 转移特性: Id ≈ gm × Vgs (饱和区)
M90N20 典型 gm ≈ 20 S (在 Id ≈ 8A 时)
12 管并联等效: gm_total ≈ 12 × 20 = 240 S
```

**驱动级** (D882 + B772 推挽):
```
从 HRPWM 滤波输出 (Vdac) 到 MOSFET Vgs 的增益:
- HRPWM RC 滤波器: Vdac = D × 3.3V (D: 占空比 0~1)
- 推挽射极跟随器: Av ≈ 0.95 (压降约 0.15V)
- Vgs = 0.95 × D × 3.3V
```

**电流检测** (RS6332 差分放大器):
```
假设电流检测差分放大增益: A_i_sense = 10
Vsense = I_load × R_sense × A_i_sense = I_load × 0.004167 × 10 = I_load × 0.04167
ADC 读数: Vadc = Vsense (ADC 输入范围 0~3.3V)
```

#### 5.1.2 电流环开环传递函数

```
被控对象 (从占空比到电流):
  Gp(s) = gm_total × (3.3V × 0.95) / (1 + s/ωp)
  其中 ωp ≈ 1/(R_load × C_load) — 负载极点
  在 CC 模式下，负载可视为短路 (低阻抗)，ωp 较高

电流检测:
  H(s) = R_sense × A_i_sense = 0.04167

环路增益:
  L(s) = Gc(s) × Gp(s) × H(s)
```

#### 5.1.3 当前 PI 参数

| 参数 | 值 | 单位 |
|------|-----|------|
| Kp | 0.5 | — |
| Ki | 10.0 | — |
| Kd | 0.001 | — |
| dt | 0.001163 | s |

**连续域等效**:
```
Ki_continuous = Ki × dt = 10.0 × 0.001163 = 0.01163
Ti = Kp / Ki_continuous = 0.5 / 0.01163 ≈ 43 s
```

**穿越频率估算**:
```
在零点频率 fz = 1/(2π×Ti) ≈ 0.0037 Hz 之后，
增益以 -20 dB/dec 滚降。
假设电流环闭环带宽 ≈ 30~50 Hz (受 860 Hz 采样率限制)
```

> **注意**: 以上参数为初始值，需通过仿真 (pid_sim.py) 和实际测试进一步调优。

### 5.2 电压环参数推导

#### 5.2.1 被控对象模型

**电压检测分压器**: 1/13.2
```
Vadc = Vin × (1/13.2)
ADC 满量程 3.3V 对应输入电压: 3.3 × 13.2 = 43.56V (使用分压)
实际输入可达 150V，需附加衰减或 ADC 支持更高范围
```

**电压环被控对象 = 电流环闭环**:
```
电压环输出 → 电流给定 → 电流环闭环 → 负载电流 → 负载电容充电 → 电压
```

#### 5.2.2 当前 PI 参数

| 参数 | 值 | 单位 |
|------|-----|------|
| Kp | 0.2 | — |
| Ki | 2.0 | — |
| Kd | 0.0 | — |
| 输出限幅 | 0 ~ 110.0 | A |

**连续域等效**:
```
Ki_continuous = Ki × dt = 2.0 × 0.001163 = 0.002326
Ti = Kp / Ki_continuous = 0.2 / 0.002326 ≈ 86 s
```

电压环带宽应远低于电流环 (约 1/5 ~ 1/10)。

### 5.3 调优策略

建议调试流程:
1. **电流环调试**: 断开外环，纯 CC 模式，阶跃响应测试
2. **电压环调试**: CV 模式下，逐步增加 Kp 直到出现振铃，然后回调 50%
3. **功率环调试**: CW 模式下，采用与电压环类似的 PI 参数 (预期 Kp ≈ 0.1, Ki ≈ 1.0)

---

## 6. 模式切换逻辑

### 6.1 模式类型

| 模式 | 控制策略 | 说明 |
|------|---------|------|
| CC | 电流 PID → Duty | 直接控制电流 |
| CV | 电压 PID → 电流 PID → Duty | 级联: 外环电压 → 内环电流 |
| CR | 电阻 PID → 电流 PID → Duty | 级联: 外环电阻 → 内环电流 |
| CW | 功率 PID → 电流 PID → Duty | 级联: 外环功率 → 内环电流 |

### 6.2 模式切换时序

```
触发条件: UART 命令 (CMD_SET_MODE)

流程:
1. 停止当前模式 (电流环/电压环 → duty = 0)
2. 重置当前模式 PID 状态 (pid_reset)
3. 配置新模式 PID 参数
4. 启用软启动 (soft-start, ~100 次迭代 = 116 ms)
5. 标记切换完成

保护: 切换期间禁止输出 ON 到 OFF 跳变
```

### 6.3 CC↔CV 交叉切换 (Crossover)

当同时设置 CC 和 CV 限制时:
```
if measured_v > cv_setpoint AND mode == CC:
    # 自动切换到 CV 模式
    modes_switch(MODE_CV)
elif measured_a > cc_setpoint AND mode == CV:
    # 自动切换到 CC 模式
    modes_switch(MODE_CC)
```

> **当前暂未实现**: 需要增加自动交叉逻辑 (auto-range crossover)。

### 6.4 瞬态响应规格

| 参数 | 目标 | 测量条件 |
|------|------|---------|
| 上升时间 (tr) | < 1 ms | CC 0→30A, 电阻负载 |
| 过冲 (Overshoot) | < 5% | CC 0→30A, 电阻负载 |
| 稳定时间 (ts ±2%) | < 5 ms | CC 0→30A, 电阻负载 |
| CV 稳定时间 | < 20 ms | CV 0→12V, 电池负载模拟 |

---

## 7. 保护集成

### 7.1 硬件保护 (CMPSS)

C2000 F28E12x 的 CMPSS 子系统提供纳秒级硬件比较器：

| 通道 | 正输入 | 负输入 (DAC) | 触发阈值 | 动作 |
|------|--------|--------------|---------|------|
| CMPSS1 | 电压检测 | DAC1 | OVP: 150V | PWM TZ1 trip |
| CMPSS2 | 电流检测 | DAC2 | OCP: 110A | PWM TZ2 trip |
| CMPSS3 | PSU 监控 | DAC3 | UVLO: 10.8V | 系统关断 |

**硬件保护路径**:
```
               CMPSS
Vin ─┬─► ADC ──► +│
     │           │ │──► TZ (Trip Zone) ──► HRPWM Force Hi-Z
     └─► 分压 ───► -│ (DAC 阈值)
```

**安全特性**:
- TZ 触发后自动闭锁 (latch)，需手动清除故障标志
- 故障清除后通过 CMPSS 数字滤波消抖

### 7.2 软件保护

由 `protection_task` 在 1 kHz 下执行：

| 保护项 | 阈值 | 滞后 | 动作 |
|--------|------|------|------|
| OVP | 150V | 5V | PWM shutdown + 故障标志 |
| OCP | 110A | 2A | PWM shutdown + 故障标志 |
| OPP | 1050W | 20W | PWM shutdown 或功率折返 |
| OTP | 90°C | 10°C | 75°C 折返 → 90°C 关断 |
| 通信超时 | 500ms | — | 保持当前设置 + 警告 LED |

### 7.3 软件限幅 (在 PID 输出端)

```
电流环: duty = clamp(duty, 0.0, 0.95)
电压环: I_demand = clamp(I_demand, 0.0, 110.0)
CC 限幅: soft_start_target = min(setpoint, 110.0)
CV 限幅: target_voltage = min(setpoint, 150.0)
```

---

## 8. 校准策略

### 8.1 校准数据结构

```c
typedef struct {
    float v_offset;     // 电压 ADC 偏置 (V)
    float v_gain;       // 电压 ADC 增益 (V/ADC_count)
    float i_offset;     // 电流 ADC 偏置 (A)
    float i_gain;       // 电流 ADC 增益 (A/ADC_count)
    uint8_t cal_valid;  // 0 = 无效, 1 = 有效
    uint32_t cal_date;  // Unix 时间戳
} el1000_calibration_t;
```

### 8.2 校准流程

#### 电压校准
```
1. 输入已知电压 V1 (如 10V)，记录 ADC 读数 ADC1
2. 输入已知电压 V2 (如 100V)，记录 ADC 读数 ADC2
3. 计算:
   v_gain = (V2 - V1) / (ADC2 - ADC1)
   v_offset = V1 - v_gain × ADC1
```

#### 电流校准
```
1. 设置负载电流 I1 (如 1A)，记录 ADC 读数 ADC1
2. 设置负载电流 I2 (如 50A)，记录 ADC 读数 ADC2
3. 计算:
   i_gain = (I2 - I1) / (ADC2 - ADC1)
   i_offset = I1 - i_gain × ADC1
```

### 8.3 校准模式

通过 UART 命令 `CMD_CAL_MODE` 进入校准模式：
1. 系统进入 STATUS_CAL
2. 禁用保护阈值 (仅硬件 CMPSS 保持)
3. 使用外部精密万用表 (6.5 位) 作为参考
4. 每个通道校准后写入 EEPROM
5. 校准数据上电时校验，无效则使用默认值

### 8.4 精度预算

| 参数 | 目标精度 | 主要误差源 |
|------|---------|-----------|
| 电压测量 | ±0.1% FS | 分压电阻精度 (±1%) → 校准后 |
| 电流测量 | ±0.2% FS | RS6332 Vos (0.8mV), 感测电阻 (±1%) |
| 设定分辨率 | 0.01A / 0.01V | HRPWM 15.2bit + 校准后 |

---

## 9. 待办事项 (TODO)

- [ ] 通过 pid_sim.py 仿真验证 PI 参数
- [ ] 硬件实测后调整 Kp/Ki
- [ ] 实现 CR 模式外环 PID
- [ ] 实现 CW 模式外环 PID
- [ ] 实现 CC↔CV 自动交叉
- [ ] 实现增益调度 (Gain Scheduling) — 根据工作点切换 PI 参数
- [ ] 实现前馈补偿 (Feed-Forward) — 加快瞬态响应
- [ ] 实现继电器反馈自整定 (Relay Feedback Auto-Tune)
- [ ] CMPSS 硬件阈值可通过 UART 配置
- [ ] 故障日志存入 EEPROM
- [ ] 功率折返 (Power Foldback) 的温度曲线

---

## 附录 A: 电流环 Simulink 模型参数

```
采样时间: Ts = 1/860 ≈ 1.163e-3 s
PI 控制器: Kp = 0.5, Ki = 10.0 (离散域, Ki × Ts = 0.01163)
感测增益: H = 0.04167 V/A
MOSFET gm: 240 S
PWM 增益: 3.135 (3.3V × 0.95)
负载极点: f_p = 1/(2π × R_load × C_load)
```

## 附录 B: PI 参数速查表

| 模式 | Kp | Ki | Kd | 输出范围 | 说明 |
|------|----|----|-----|---------|------|
| CC | 0.5 | 10.0 | 0.001 | 0~0.95 | 电流内环 |
| CV | 0.2 | 2.0 | 0.0 | 0~110A | 电压外环 |
| CR | TBD | TBD | 0.0 | 0~110A | 待调试 |
| CW | TBD | TBD | 0.0 | 0~110A | 待调试 |

---

*文档结束 — SYS-CTRL-001 v0.1*
