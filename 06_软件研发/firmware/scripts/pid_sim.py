#!/usr/bin/env python3
"""
pid_sim.py — PID control loop simulation for EL-1000 electronic load.

Simulates the current control loop (CC mode) with:
  - Plant model: M90N20 transconductance + RC output load
  - PI controller with anti-windup (as implemented in pid.c)
  - Step response test: setpoint step 0→30A
  - Bode plot analysis: phase margin, gain margin, crossover frequency

Usage:
  source ~/.venv-power/bin/activate
  python pid_sim.py

Output:
  Plots saved to 06_软件研发/docs/pid_sim_results/
"""

import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import EngFormatter
import control as ct

# ─── Output directory ──────────────────────────────────────────────────
OUT_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    'docs', 'pid_sim_results'
)
os.makedirs(OUT_DIR, exist_ok=True)
print(f"Output directory: {OUT_DIR}")

# ─── System constants ──────────────────────────────────────────────────
FS = 860.0          # PID loop rate (Hz)
TS = 1.0 / FS       # Sample period (s) ≈ 1.163 ms

# Power stage — 12 × M90N20 MOSFETs
N_MOSFET = 12
GM_PER_MOSFET = 20.0       # Transconductance per MOSFET (S)
GM_TOTAL = N_MOSFET * GM_PER_MOSFET  # 240 S
VTH = 2.5                   # MOSFET threshold voltage (V), typical for M90N20

# Sense resistors — 12 × 0.050Ω in parallel
R_SENSE = 0.050                      # per resistor (Ω)
R_SENSE_TOTAL = R_SENSE / N_MOSFET   # 0.004167 Ω

# Current sense amplifier gain (RS6332 differential amp)
A_SENSE = 10.0                       # V/V
H_CURRENT = R_SENSE_TOTAL * A_SENSE  # V/A → 0.04167 V/A

# HRPWM → Gate drive (D882/B772 push-pull + RC filter)
PWM_VOLTAGE = 3.3           # PWM logic high (V)
DRIVE_GAIN = 0.95           # Emitter follower voltage gain
K_PWM = PWM_VOLTAGE * DRIVE_GAIN  # 3.135 V/duty

# Load parameters (simulated DUT)
R_LOAD = 1.0                # Load resistance (Ω) — 1Ω for 30A at 30V
C_LOAD = 100e-6             # Load capacitance (F) — 100 µF typical

# ─── PI controller parameters (from pid.c) ─────────────────────────────
KP = 0.5
KI = 10.0                  # Discrete KI (accumulates Ki * error * dt)
KD = 0.001
MAX_OUTPUT = 0.95
MIN_OUTPUT = 0.0
MAX_INTEGRAL = 0.95
MIN_INTEGRAL = -0.5

# ─── Simulation parameters ─────────────────────────────────────────────
T_SIM = 0.5                 # Simulation time (s)
N_STEPS = int(T_SIM / TS)   # Number of simulation steps
T = np.arange(N_STEPS) * TS  # Time vector

# Step: 0 -> 30A at t=50ms with soft-start ramp (~100 iterations = 116ms)
T_STEP = 0.05
SETPOINT_BEFORE = 0.0
SETPOINT_AFTER = 30.0      # Amps
SOFT_START_ITERS = 100      # Ramp iterations (matches firmware soft_start_iters)


# ═══════════════════════════════════════════════════════════════════════
# 1. CONTINUOUS-TIME PLANT MODEL
# ═══════════════════════════════════════════════════════════════════════
def build_plant_continuous():
    """
    Build continuous-time plant model.

    Includes Vgs threshold voltage (Vth) and source resistance (Rs)
    limiting. Small-signal model linearized around operating point.

    Transfer function from duty (0~1) to sensed voltage (V):
      Gp(s) = Vgs/Vth * gm * R_LOAD / (1 + s*R_LOAD*C_LOAD)

    where Vgs = K_PWM * (duty) - Vth (effective gate drive above threshold)
    """
    # Effective transconductance including source degeneration
    # gm_eff = gm / (1 + gm * Rs)
    # Rs per MOSFET = 0.050 Ohm, 12 in parallel → 0.00417 Ohm
    # But current divides among all MOSFETs
    gm_eff = GM_TOTAL / (1 + GM_TOTAL * R_SENSE_TOTAL)  # ~72.4 S

    # DC gain from effective Vgs to sensed voltage
    # Id = gm_eff * (Vgs - Vth)
    # Vsense = Id * Rsense_total * Asense
    K_dc = gm_eff * R_SENSE_TOTAL * A_SENSE * K_PWM

    # Pole due to load RC
    tau_load = R_LOAD * C_LOAD     # 100 us

    num = [K_dc]
    den = [tau_load, 1.0]          # 1st order lag
    G_plant = ct.TransferFunction(num, den)

    # Add a small parasitic pole at 50 kHz (MOSFET switching)
    tau_par = 1.0 / (2 * np.pi * 50000)
    G_para = ct.TransferFunction([1], [tau_par, 1.0])
    G_plant = G_plant * G_para

    return G_plant, gm_eff


G_plant_ct, gm_eff = build_plant_continuous()
dc_gain = float(abs(ct.evalfr(G_plant_ct, 0)))
print(f"\nPlant DC gain: {dc_gain:.4f} V/V (duty->Vsense)")
print(f"   gm_eff (with source degeneration): {gm_eff:.1f} S")
print(f"   gm_raw (total): {GM_TOTAL:.0f} S")


# ═══════════════════════════════════════════════════════════════════════
# 2. DISCRETE-TIME PI CONTROLLER
# ═══════════════════════════════════════════════════════════════════════
class PIController:
    """
    Discrete-time PI controller matching pid.c implementation.

    integral[n] = integral[n-1] + Ki * error[n] * dt
    i_term = integral[n] (clamped)
    p_term = Kp * error[n]
    output = p_term + i_term (clamped)
    """

    def __init__(self, kp, ki, dt, max_out=0.95, min_out=0.0,
                 max_int=0.5, min_int=-0.5):
        self.kp = kp
        self.ki = ki
        self.dt = dt
        self.max_out = max_out
        self.min_out = min_out
        self.max_int = max_int
        self.min_int = min_int

        self.integral = 0.0
        self.prev_error = 0.0
        self.prev_output = 0.0

    def update(self, setpoint, measurement):
        error = setpoint - measurement

        # Proportional
        p_term = self.kp * error

        # Integral (forward Euler, with clamping)
        self.integral += self.ki * error * self.dt
        if self.integral > self.max_int:
            self.integral = self.max_int
        if self.integral < self.min_int:
            self.integral = self.min_int

        # Sum
        output = p_term + self.integral

        # Output clamp
        if output > self.max_out:
            output = self.max_out
        if output < self.min_out:
            output = self.min_out

        self.prev_error = error
        self.prev_output = output
        return output

    def reset(self):
        self.integral = 0.0
        self.prev_error = 0.0
        self.prev_output = 0.0


# ═══════════════════════════════════════════════════════════════════════
# 3. DISCRETE-TIME PLANT SIMULATION
# ═══════════════════════════════════════════════════════════════════════
def plant_step_discrete(duty, i_load_prev, v_load_prev):
    """
    One simulation step of the plant with realistic MOSFET model.

    Vgs = K_PWM * duty (gate drive voltage)
    Id = gm_eff * (Vgs - Vth)   when Vgs > Vth, else 0
    V_load[n] = V_load[n-1] + dt * (Id - V_load[n-1]/R_load) / C_load
    Vsense = Id * R_sense_total * A_sense
    """
    vgs = K_PWM * duty
    if vgs > VTH:
        # Effective gm includes source degeneration
        i_load = gm_eff * (vgs - VTH)
    else:
        i_load = 0.0
    i_load = max(i_load, 0.0)

    # Load dynamics (RC circuit)
    v_load = v_load_prev + TS * (i_load - v_load_prev / R_LOAD) / C_LOAD
    v_load = max(v_load, 0.0)

    # Sensed voltage
    v_sense = i_load * H_CURRENT

    return i_load, v_load, v_sense


# ═══════════════════════════════════════════════════════════════════════
# 4. TIME-DOMAIN SIMULATION
# ═══════════════════════════════════════════════════════════════════════
def run_step_response(kp=KP, ki=KI):
    """Run step response simulation."""
    pid = PIController(kp, ki, TS, MAX_OUTPUT, MIN_OUTPUT,
                       MAX_INTEGRAL, MIN_INTEGRAL)

    # Storage
    i_load_arr = np.zeros(N_STEPS)
    v_load_arr = np.zeros(N_STEPS)
    v_sense_arr = np.zeros(N_STEPS)
    duty_arr = np.zeros(N_STEPS)
    setpoint_arr = np.zeros(N_STEPS)
    error_arr = np.zeros(N_STEPS)
    integral_arr = np.zeros(N_STEPS)

    # State
    i_load = 0.0
    v_load = 0.0
    soft_start_active = False
    soft_start_current = 0.0
    soft_start_step = 0.0

    for n in range(N_STEPS):
        t_n = T[n]

        # Setpoint with optional soft-start ramp
        if t_n < T_STEP:
            sp = SETPOINT_BEFORE
            soft_start_active = False
        elif not soft_start_active:
            # Initiate soft-start at step
            soft_start_active = True
            soft_start_current = 0.0
            soft_start_step = SETPOINT_AFTER / SOFT_START_ITERS
            sp = soft_start_current
        else:
            if soft_start_current < SETPOINT_AFTER:
                soft_start_current += soft_start_step
                if soft_start_current >= SETPOINT_AFTER:
                    soft_start_current = SETPOINT_AFTER
                    soft_start_active = False
            sp = soft_start_current
        setpoint_arr[n] = sp

        # Current measurement in sensed voltage
        v_sense = i_load * H_CURRENT
        measured_current = v_sense / H_CURRENT  # Back to Amps for PID

        # PID update
        duty = pid.update(sp, measured_current)
        duty_arr[n] = duty
        error_arr[n] = sp - measured_current
        integral_arr[n] = pid.integral

        # Plant step
        i_load, v_load, v_sense_out = plant_step_discrete(duty, i_load, v_load)
        i_load_arr[n] = i_load
        v_load_arr[n] = v_load
        v_sense_arr[n] = v_sense_out

    return {
        't': T,
        'i_load': i_load_arr,
        'v_load': v_load_arr,
        'v_sense': v_sense_arr,
        'duty': duty_arr,
        'setpoint': setpoint_arr,
        'error': error_arr,
        'integral': integral_arr,
    }


# ─── Run simulation ────────────────────────────────────────────────────
print("\n--- Step Response Simulation ---")
sim_data = run_step_response()
t = sim_data['t']

# Find step index
step_idx = np.searchsorted(t, T_STEP)

# Find settling metrics
i_final = np.mean(sim_data['i_load'][-int(0.1/TS):])  # avg last 100ms
i_overshoot = (np.max(sim_data['i_load'][step_idx:]) - i_final) / i_final * 100

# Find rise time (10% -> 90%)
i_min = sim_data['i_load'][step_idx]
i_max = np.max(sim_data['i_load'][step_idx:])
i_10 = i_min + 0.1 * (i_final - i_min)
i_90 = i_min + 0.9 * (i_final - i_min)
idx_10 = np.where(sim_data['i_load'][step_idx:] >= i_10)[0]
idx_90 = np.where(sim_data['i_load'][step_idx:] >= i_90)[0]
rise_time = 0
if len(idx_10) and len(idx_90):
    rise_time = (t[step_idx + idx_90[0]] - t[step_idx + idx_10[0]]) * 1000

# Find settling time (within +/-2% of final)
i_2p = 0.02 * i_final
settle_mask = np.abs(sim_data['i_load'][step_idx:] - i_final) < i_2p
settle_time_ms = None
if np.any(settle_mask):
    settle_idx = np.where(settle_mask)[0][0]
    settle_time_ms = (t[step_idx + settle_idx] - t[step_idx]) * 1000

print(f"   Setpoint: 0 -> {SETPOINT_AFTER}A at t={T_STEP*1000:.0f}ms (soft-start: {SOFT_START_ITERS} iters)")
print(f"   Final current: {i_final:.2f} A")
print(f"   Overshoot (from setpoint): {i_overshoot:.2f}%")
print(f"   Rise time (10-90%, dominant: soft-start ramp): {rise_time:.2f} ms")
if settle_time_ms:
    print(f"   Settling time (+/-2%): {settle_time_ms:.2f} ms")
else:
    print("   Settling: N/A")


# ═══════════════════════════════════════════════════════════════════════
# 5. PLOT - Step Response
# ═══════════════════════════════════════════════════════════════════════
def plot_step_response(data, filename='step_response.png'):
    fig, axes = plt.subplots(4, 1, figsize=(12, 10), sharex=True)

    ax = axes[0]
    ax.plot(data['t'] * 1000, data['setpoint'], 'k--', label='Setpoint', linewidth=1.5)
    ax.plot(data['t'] * 1000, data['i_load'], 'b-', label='Load Current', linewidth=1.5)
    ax.axvline(x=T_STEP * 1000, color='gray', linestyle=':', alpha=0.5)
    ax.set_ylabel('Current (A)')
    ax.set_title('Current Step Response - CC Mode 0->30A')
    ax.legend(loc='lower right')
    ax.grid(True, alpha=0.3)

    ax = axes[1]
    ax.plot(data['t'] * 1000, data['duty'] * 100, 'g-', linewidth=1.5)
    ax.set_ylabel('Duty Cycle (%)')
    ax.set_title('PID Output (Duty Cycle)')
    ax.grid(True, alpha=0.3)

    ax = axes[2]
    ax.plot(data['t'] * 1000, data['error'], 'r-', linewidth=1.5)
    ax.set_ylabel('Error (A)')
    ax.set_title('Control Error')
    ax.grid(True, alpha=0.3)

    ax = axes[3]
    ax.plot(data['t'] * 1000, data['integral'], 'm-', linewidth=1.5)
    ax.set_xlabel('Time (ms)')
    ax.set_ylabel('Integral Term')
    ax.set_title('Integral (Anti-windup clamped)')
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    path = os.path.join(OUT_DIR, filename)
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"   Saved: {path}")


plot_step_response(sim_data)


# ═══════════════════════════════════════════════════════════════════════
# 6. PLOT - Step Response Detail Zoom
# ═══════════════════════════════════════════════════════════════════════
def plot_detail_zoom(data, filename='step_detail_zoom.png'):
    """Zoomed view of the first 200 ms after step."""
    t_zoom_start = 0
    t_zoom_end = 0.2  # 200 ms
    mask = (data['t'] >= t_zoom_start) & (data['t'] <= t_zoom_end)

    fig, axes = plt.subplots(3, 1, figsize=(12, 8), sharex=True)

    ax = axes[0]
    ax.plot(data['t'][mask] * 1000, data['setpoint'][mask], 'k--', label='Setpoint')
    ax.plot(data['t'][mask] * 1000, data['i_load'][mask], 'b-', label='Current')
    ax.axvline(x=T_STEP * 1000, color='gray', linestyle=':')
    ax.set_ylabel('Current (A)')
    ax.set_title('Step Response Detail (Zoomed)')
    ax.legend(loc='lower right')
    ax.grid(True, alpha=0.3)

    ax = axes[1]
    ax.plot(data['t'][mask] * 1000, data['duty'][mask] * 100, 'g-')
    ax.set_ylabel('Duty (%)')
    ax.grid(True, alpha=0.3)

    ax = axes[2]
    ax.plot(data['t'][mask] * 1000, data['v_load'][mask], 'orange', linewidth=1.5)
    ax.set_xlabel('Time (ms)')
    ax.set_ylabel('V_load (V)')
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    path = os.path.join(OUT_DIR, filename)
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"   Saved: {path}")


plot_detail_zoom(sim_data)


# ═══════════════════════════════════════════════════════════════════════
# 7. BODE PLOT ANALYSIS
# ═══════════════════════════════════════════════════════════════════════

# Continuous-time PI: C(s) = Kp + Ki/s = (Kp*s + Ki) / s
# Reason: pid.c accumulates integral += Ki * error * dt
# So the continuous equivalent is: C(s) = Kp + Ki/s
G_pi_s = ct.TransferFunction([KP, KI], [1, 0])  # (Kp*s + Ki) / s

# Plant continuous
Gp_s = G_plant_ct
H_s = ct.TransferFunction([H_CURRENT], [1.0])

# Open-loop continuous: L(s) = C(s) * Gp(s) * H(s)
L_s = G_pi_s * Gp_s * H_s
print(f"\n--- Bode Analysis (Continuous) ---")
print(f"   Open-loop poles: {ct.poles(L_s)}")
print(f"   Open-loop zeros: {ct.zeros(L_s)}")

# Compute stability margins
gm = None
pm = None
w_gm = None
w_pm = None
w_gm_hz = 0
w_pm_hz = 0

try:
    margins = ct.stability_margins(L_s)
    gm = float(margins[0]) if np.isfinite(margins[0]) else float('inf')
    pm = float(margins[1]) if np.isfinite(margins[1]) else 0.0
    w_gm = float(margins[2]) if np.isfinite(margins[2]) else 0.0
    w_pm = float(margins[4]) if np.isfinite(margins[4]) else 0.0
    w_gm_hz = w_gm / (2 * np.pi) if w_gm > 0 else 0
    w_pm_hz = w_pm / (2 * np.pi) if w_pm > 0 else 0

    gm_db = 20 * np.log10(gm) if np.isfinite(gm) and gm > 0 else float('inf')
    if np.isfinite(gm_db):
        print(f"   Gain Margin: {gm_db:.1f} dB  (at {w_gm_hz:.1f} Hz)")
    else:
        print(f"   Gain Margin: inf dB  (phase never crosses -180 deg)")
    print(f"   Phase Margin: {pm:.1f} deg  (at {w_pm_hz:.1f} Hz)")
except Exception as e:
    print(f"   Margin calculation: {e}")


def plot_bode(filename='bode_analysis.png'):
    fig, axes = plt.subplots(3, 1, figsize=(12, 10))

    # Bode of L(s)
    mag, phase, omega = ct.bode(L_s, plot=False, Hz=True)

    ax = axes[0]
    ax.semilogx(omega, 20 * np.log10(mag.squeeze()), 'b-', linewidth=1.5)
    ax.axhline(y=0, color='gray', linestyle=':', alpha=0.7)
    ax.set_ylabel('Magnitude (dB)')
    ax.set_title('Open-Loop Bode Plot - L(s) = C(s) * Gp(s) * H(s)')
    ax.grid(True, alpha=0.3, which='both')

    # Mark gain crossover
    if w_pm is not None and w_pm > 0:
        ax.axvline(x=w_pm_hz, color='g', linestyle='--', alpha=0.7,
                   label=f'wc = {w_pm_hz:.1f} Hz')
    if w_gm is not None and w_gm > 0:
        ax.axvline(x=w_gm_hz, color='r', linestyle='--', alpha=0.7,
                   label=f'w_pi = {w_gm_hz:.1f} Hz')
    ax.legend(fontsize=9)

    ax = axes[1]
    phase_squeeze = phase.squeeze()
    ax.semilogx(omega, phase_squeeze, 'b-', linewidth=1.5)
    ax.axhline(y=-180, color='gray', linestyle=':', alpha=0.7)
    ax.set_ylabel('Phase (deg)')
    ax.set_ylim(-270, -45)
    ax.grid(True, alpha=0.3, which='both')

    # Closed-loop Bode
    T_s = G_pi_s * Gp_s / (1 + L_s)
    mag_c, phase_c, omega_c = ct.bode(T_s, plot=False, Hz=True)

    ax = axes[2]
    ax.semilogx(omega_c, 20 * np.log10(mag_c.squeeze()), 'r-', linewidth=1.5)
    ax.axhline(y=-3, color='gray', linestyle=':', alpha=0.7, label='-3 dB')
    ax.set_xlabel('Frequency (Hz)')
    ax.set_ylabel('Magnitude (dB)')
    ax.set_title('Closed-Loop Bode Plot - T(s)')
    ax.grid(True, alpha=0.3, which='both')

    # Find bandwidth
    mag_c_db = 20 * np.log10(mag_c.squeeze())
    idx_3db = np.where(mag_c_db < -3)[0]
    if len(idx_3db):
        bw = omega_c[idx_3db[0]]
    else:
        bw = omega_c[-1]
    ax.axvline(x=bw, color='orange', linestyle='--', alpha=0.7,
               label=f'BW = {bw:.1f} Hz')
    ax.legend(fontsize=9)

    plt.tight_layout()
    path = os.path.join(OUT_DIR, filename)
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"   Saved: {path}")
    print(f"   Closed-loop bandwidth (-3dB): {bw:.1f} Hz")


plot_bode()


# ─── Nyquist plot ──────────────────────────────────────────────────────
def plot_nyquist(filename='nyquist_plot.png'):
    fig, ax = plt.subplots(figsize=(8, 8))
    resp = ct.nyquist_response(L_s)
    r = resp.response  # 1D complex array
    real_vals = r.real
    imag_vals = r.imag

    ax.plot(real_vals, imag_vals, 'b-', linewidth=1.2)
    ax.plot(real_vals, -imag_vals, 'b--', linewidth=0.8, alpha=0.5)
    ax.plot([-1], [0], 'rx', markersize=10, markeredgewidth=2, label='-1 point')
    ax.axhline(y=0, color='gray', linestyle='-', alpha=0.3)
    ax.axvline(x=0, color='gray', linestyle='-', alpha=0.3)
    ax.set_xlabel('Real')
    ax.set_ylabel('Imaginary')
    ax.set_title('Nyquist Plot - L(s)')
    ax.grid(True, alpha=0.3)
    ax.axis('equal')
    ax.legend()
    ax.set_xlim(-3, 2)
    ax.set_ylim(-3, 3)

    plt.tight_layout()
    path = os.path.join(OUT_DIR, filename)
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"   Saved: {path}")


plot_nyquist()


# ═══════════════════════════════════════════════════════════════════════
# 8. PARAMETER SWEEP - KI sensitivity
# ═══════════════════════════════════════════════════════════════════════
def run_sweep():
    """Sweep Ki to show effect on response."""
    ki_values = [5.0, 10.0, 20.0, 50.0]
    colors = ['green', 'blue', 'orange', 'red']
    labels = [f'Ki={k}' for k in ki_values]

    fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

    ax = axes[0]
    ax.plot(t * 1000, sim_data['setpoint'], 'k--', label='Setpoint', linewidth=1.5)

    for ki, color, label in zip(ki_values, colors, labels):
        data = run_step_response(kp=KP, ki=ki)
        ax.plot(t * 1000, data['i_load'], color=color, label=label, linewidth=1.2)

    ax.set_ylabel('Current (A)')
    ax.set_title('PI Parameter Sensitivity - Ki Sweep (Kp=0.5 fixed)')
    ax.legend(loc='lower right')
    ax.grid(True, alpha=0.3)

    ax = axes[1]
    for ki, color, label in zip(ki_values, colors, labels):
        data = run_step_response(kp=KP, ki=ki)
        ax.plot(t * 1000, data['duty'] * 100, color=color, label=label, linewidth=1.2)

    ax.set_xlabel('Time (ms)')
    ax.set_ylabel('Duty (%)')
    ax.grid(True, alpha=0.3)
    ax.legend(loc='lower right')

    plt.tight_layout()
    path = os.path.join(OUT_DIR, 'ki_sweep.png')
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"   Saved: {path}")


run_sweep()


# ═══════════════════════════════════════════════════════════════════════
# 9. SUMMARY
# ═══════════════════════════════════════════════════════════════════════
print(f"\n{'='*60}")
print(f"   SIMULATION SUMMARY")
print(f"{'='*60}")
print(f"   Controller:         Parallel-form PI (match pid.c)")
print(f"   Sample rate:        {FS:.0f} Hz (Ts = {TS*1000:.3f} ms)")
print(f"   Plant:              12xM90N20 (gm={GM_TOTAL}S) + {R_LOAD}Ohm//{C_LOAD*1e6:.0f}uF")
print(f"   Current sense:      {R_SENSE_TOTAL*1000:.2f}mOhm x {A_SENSE}x = {H_CURRENT*1000:.2f} mV/A")
print(f"   PWM gain:           {K_PWM:.3f} V/duty (3.3V x {DRIVE_GAIN})")
print(f"{'-'*60}")
print(f"   Step response:      0 -> {SETPOINT_AFTER}A @ {T_STEP*1000:.0f}ms")
print(f"   Overshoot:          {i_overshoot:.2f}%")
print(f"   Rise time:          {rise_time:.2f} ms")
if settle_time_ms:
    print(f"   Settling time:      {settle_time_ms:.2f} ms")
print(f"   Final error:        {np.abs(sim_data['i_load'][-1] - SETPOINT_AFTER):.4f} A")
# Compute closed-loop BW
try:
    T_s = G_pi_s * Gp_s / (1 + L_s)
    mag_c, _, omega_c = ct.bode(T_s, plot=False, Hz=True)
    mag_c_db = 20 * np.log10(np.array(mag_c).squeeze())
    idx_3db = np.where(mag_c_db < -3)[0]
    bw = omega_c[idx_3db[0]] if len(idx_3db) else omega_c[-1]
except Exception:
    bw = 0

if pm is not None and np.isfinite(pm):
    print(f"{'-'*60}")
    print(f"   Phase margin:       {pm:.1f} deg")
    if gm is not None and np.isfinite(gm) and gm > 0 and gm < float('inf'):
        print(f"   Gain margin:        {20*np.log10(gm):.1f} dB")
    else:
        print(f"   Gain margin:        inf dB")
    print(f"   Crossover freq:     {w_pm_hz:.1f} Hz")
    if bw > 0:
        print(f"   Closed-loop BW:     {bw:.1f} Hz")
print(f"{'='*60}")
print(f"\nAll plots saved to: {OUT_DIR}")
print(f"Files:")
for f in sorted(os.listdir(OUT_DIR)):
    print(f"   {f}")
