"""
AD-HTC FUEL-ENHANCED GAS CYCLE
Thermodynamic Analysis Module
MEG 315 Applied Thermodynamics 2 - University of Lagos

This module performs thermodynamic calculations and generates
h-s and T-H charts for system monitoring and analysis.
"""

# ============================================
# IMPORT REQUIRED LIBRARIES
# ============================================

import matplotlib.pyplot as plt
import numpy as np
import os
from datetime import datetime

# ============================================
# GLOBAL CONSTANTS
# ============================================

# Air properties (constant for our temperature range)
GAMMA = 1.4      # Specific heat ratio for air (C_p/C_v)
CP_AIR = 1.005   # kJ/kgK - Specific heat of air at constant pressure

# Default design parameters (from project schematic)
DEFAULT_T1 = 288      # K - Inlet air temperature (ambient)
DEFAULT_R = 15        # - Compression ratio
DEFAULT_T3 = 2691.50  # K - Turbine inlet temperature (after combustion)

# ============================================
# THERMODYNAMIC CALCULATION FUNCTIONS
# ============================================

def calculate_compressor_exit(T1, r, gamma=GAMMA):
    """
    Calculate compressor exit temperature using isentropic compression formula.
    
    Formula: T2 = T1 * (r)^((gamma-1)/gamma)
    
    Parameters:
    T1 (float): Inlet temperature (K)
    r (float): Compression ratio
    gamma (float): Specific heat ratio (default=1.4 for air)
    
    Returns:
    float: Compressor exit temperature (K)
    """
    exponent = (gamma - 1) / gamma
    T2 = T1 * (r ** exponent)
    return T2


def calculate_heat_input(m_dot, Cp, T3, T2):
    """
    Calculate heat input in combustion chamber.
    
    Formula: Q_in = m_dot * Cp * (T3 - T2)
    
    Parameters:
    m_dot (float): Mass flow rate (kg/s)
    Cp (float): Specific heat at constant pressure (kJ/kgK)
    T3 (float): Turbine inlet temperature (K)
    T2 (float): Compressor exit temperature (K)
    
    Returns:
    float: Heat input rate (kW)
    """
    return m_dot * Cp * (T3 - T2)


def calculate_ideal_efficiency(r, gamma=GAMMA):
    """
    Calculate ideal thermal efficiency of Brayton cycle.
    
    Formula: eta = 1 - r^((1-gamma)/gamma)
    
    Parameters:
    r (float): Compression ratio
    gamma (float): Specific heat ratio
    
    Returns:
    float: Ideal thermal efficiency (0-1)
    """
    return 1 - (r ** ((1 - gamma) / gamma))


def generate_th_diagram_data(T3, T_stack=850, num_points=100):
    """
    Generate data for T-H diagram.
    
    Parameters:
    T3 (float): Turbine inlet temperature (K)
    T_stack (float): Stack exhaust temperature (K)
    num_points (int): Number of points for smooth curve
    
    Returns:
    tuple: (heat_steps, T_gas)
    """
    heat_steps = np.linspace(0, 100, num_points)  # 0% to 100% heat transfer
    T_gas = np.linspace(T3, T_stack, num_points)  # Gas cooling profile
    return heat_steps, T_gas


def generate_hs_diagram_data():
    """
    Generate representative data for h-s diagram.
    
    In a full implementation, this would use steam tables.
    Here we use simplified representative values for visualization.
    
    Returns:
    tuple: (s_steam, h_steam) - entropy and enthalpy arrays
    """
    # Entropy values [kJ/kg·K] at key state points
    s_steam = [1.5, 6.5, 6.8, 2.0, 1.5]
    
    # Enthalpy values [kJ/kg] at key state points
    h_steam = [500, 3200, 2400, 500, 500]
    
    return s_steam, h_steam


def check_steam_quality(h4, h_f, h_g):
    """
    Check steam quality at turbine exit.
    
    Quality = (h4 - h_f) / (h_g - h_f)
    
    Parameters:
    h4 (float): Enthalpy at turbine exit (kJ/kg)
    h_f (float): Enthalpy of saturated liquid (kJ/kg)
    h_g (float): Enthalpy of saturated vapor (kJ/kg)
    
    Returns:
    float: Steam quality (0-1)
    str: Warning message if quality too low
    """
    quality = (h4 - h_f) / (h_g - h_f)
    
    warning = None
    if quality < 0.88:
        warning = f"WARNING: Steam quality {quality:.3f} below 0.88! Risk of blade erosion!"
    elif quality < 0.95:
        warning = f"CAUTION: Steam quality {quality:.3f} - monitor closely"
    
    return quality, warning

# ============================================
# PLOTTING FUNCTIONS
# ============================================

def plot_hs_diagram(ax, s_steam, h_steam):
    """
    Plot h-s diagram on given axes.
    
    Parameters:
    ax: matplotlib axes object
    s_steam (list): Entropy values
    h_steam (list): Enthalpy values
    """
    # Plot Rankine cycle loop
    ax.plot(s_steam, h_steam, 'b-o', linewidth=2, markersize=8, 
            label='HTC Rankine Loop')
    
    # Add saturation dome (simplified representation)
    ax.fill_between([1.5, 7], 400, 1000, color='gray', alpha=0.1, 
                    label='Saturation Dome')
    
    # Label state points
    points = [(1.5, 500, '1'), (6.5, 3200, '3'), 
              (6.8, 2400, '4'), (2.0, 500, '2')]
    for x, y, label in points:
        ax.annotate(label, (x, y), xytext=(5, 5), 
                   textcoords='offset points', fontsize=12, fontweight='bold')
    
    # Formatting
    ax.set_title('HTC Steam Cycle: h-s Chart', fontsize=14, fontweight='bold')
    ax.set_xlabel('Specific Entropy (s) [kJ/kg·K]', fontsize=12)
    ax.set_ylabel('Specific Enthalpy (h) [kJ/kg]', fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend(loc='best')
    ax.set_xlim([1, 8])
    ax.set_ylim([0, 3500])


def plot_th_diagram(ax, heat_steps, T_gas, T3, T2):
    """
    Plot T-H diagram on given axes.
    
    Parameters:
    ax: matplotlib axes object
    heat_steps (array): Heat transfer percentages
    T_gas (array): Gas temperatures
    T3 (float): Turbine inlet temperature
    T2 (float): Compressor exit temperature
    """
    # Plot hot gas cooling line
    ax.plot(heat_steps, T_gas, 'r-', linewidth=3, label='Gas Exhaust Cooling')
    
    # Create simplified cold stream heating curve
    cold_steps = np.linspace(0, 100, 100)
    T_cold = np.zeros_like(cold_steps)
    
    # Sensible heating (liquid)
    T_cold[0:30] = np.linspace(300, 450, 30)
    # Boiling plateau (phase change)
    T_cold[30:50] = 450
    # Superheating
    T_cold[50:100] = np.linspace(450, 650, 50)
    
    ax.plot(cold_steps, T_cold, 'g-', linewidth=3, label='HTC Feedstock Heating')
    
    # Find and mark pinch point
    # (Simplified - in real code, find actual minimum difference)
    pinch_x = 45
    pinch_y_gas = np.interp(pinch_x, heat_steps, T_gas)
    pinch_y_cold = np.interp(pinch_x, cold_steps, T_cold)
    pinch_delta = pinch_y_gas - pinch_y_cold
    
    ax.plot([pinch_x, pinch_x], [pinch_y_cold, pinch_y_gas], 
            'k--', linewidth=2, label=f'Pinch Point ΔT={pinch_delta:.1f}K')
    
    # Add horizontal line showing critical temperatures
    ax.axhline(y=T2, color='orange', linestyle=':', alpha=0.5, 
               label=f'Compressor Exit (T₂={T2:.1f}K)')
    
    # Formatting
    ax.set_title('Process Gas: T-H Chart', fontsize=14, fontweight='bold')
    ax.set_xlabel('Heat Transfer (Q) [Cumulative %]', fontsize=12)
    ax.set_ylabel('Temperature (T) [K]', fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend(loc='upper right')
    ax.set_xlim([0, 100])
    ax.set_ylim([0, 3000])
    
    # Add annotation explaining pinch point
    ax.annotate(f'Pinch Point: {pinch_delta:.1f}K\nMinimum ΔT for heat transfer', 
                xy=(pinch_x, pinch_y_gas-200), 
                xytext=(60, 1500),
                arrowprops=dict(arrowstyle='->', color='black', linewidth=1.5),
                fontsize=10,
                bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.7))


def plot_analysis(T1, r, T3, save=False, filename=None):
    """
    Main plotting function - creates both charts.
    
    Parameters:
    T1 (float): Inlet temperature (K)
    r (float): Compression ratio
    T3 (float): Turbine inlet temperature (K)
    save (bool): Whether to save figure to file
    filename (str): Output filename (if None, auto-generated)
    
    Returns:
    matplotlib.figure.Figure: The generated figure
    """
    # Calculate T2
    T2 = calculate_compressor_exit(T1, r)
    
    # Generate data
    heat_steps, T_gas = generate_th_diagram_data(T3)
    s_steam, h_steam = generate_hs_diagram_data()
    
    # Create figure with two subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
    
    # Plot both diagrams
    plot_hs_diagram(ax1, s_steam, h_steam)
    plot_th_diagram(ax2, heat_steps, T_gas, T3, T2)
    
    # Add overall title with parameters
    fig.suptitle(f'AD-HTC Fuel-Enhanced Gas Cycle Analysis\n'
                 f'T₁={T1}K, r={r}, T₂={T2:.2f}K, T₃={T3}K', 
                 fontsize=16, fontweight='bold')
    
    plt.tight_layout()
    
    # Save if requested
    if save:
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"AD_HTC_Analysis_{timestamp}.png"
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"Figure saved as: {filename}")
    
    return fig


def generate_report(T1, r, T3, m_dot=1.0):
    """
    Generate a text report of all calculations.
    
    Parameters:
    T1 (float): Inlet temperature (K)
    r (float): Compression ratio
    T3 (float): Turbine inlet temperature (K)
    m_dot (float): Mass flow rate (kg/s)
    
    Returns:
    str: Formatted report
    """
    T2 = calculate_compressor_exit(T1, r)
    Q_in = calculate_heat_input(m_dot, CP_AIR, T3, T2)
    eta = calculate_ideal_efficiency(r)
    
    # Steam quality check (simplified)
    quality, warning = check_steam_quality(2400, 500, 2600)
    
    report = []
    report.append("=" * 60)
    report.append("AD-HTC FUEL-ENHANCED GAS CYCLE - ANALYSIS REPORT")
    report.append("=" * 60)
    report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("")
    report.append("INPUT PARAMETERS:")
    report.append(f"  Inlet Temperature (T₁): {T1} K")
    report.append(f"  Compression Ratio (r): {r}")
    report.append(f"  Turbine Inlet (T₃): {T3} K")
    report.append(f"  Mass Flow Rate: {m_dot} kg/s")
    report.append("")
    report.append("CALCULATED RESULTS:")
    report.append(f"  Compressor Exit (T₂): {T2:.2f} K")
    report.append(f"  Temperature Rise (T₂-T₁): {T2-T1:.1f} K")
    report.append(f"  Combustion ΔT (T₃-T₂): {T3-T2:.1f} K")
    report.append(f"  Heat Input (Q_in): {Q_in:.2f} kW")
    report.append(f"  Ideal Cycle Efficiency: {eta*100:.1f}%")
    report.append("")
    report.append("STEAM CYCLE:")
    report.append(f"  Turbine Exit Quality: {quality:.3f}")
    if warning:
        report.append(f"  {warning}")
    report.append("")
    report.append("=" * 60)
    
    return "\n".join(report)

# ============================================
# MAIN EXECUTION
# ============================================

if __name__ == "__main__":
    print("\n" + "="*60)
    print("AD-HTC FUEL-ENHANCED GAS CYCLE")
    print("Thermodynamic Analysis Module")
    print("MEG 315 Applied Thermodynamics 2 - University of Lagos")
    print("="*60 + "\n")
    
    # Use default parameters
    T1 = DEFAULT_T1
    r = DEFAULT_R
    T3 = DEFAULT_T3
    
    # Calculate and display T2
    T2 = calculate_compressor_exit(T1, r)
    print(f"Compressor Exit Temperature (T₂): {T2:.2f} K")
    print(f"Temperature Rise: {T2-T1:.1f} K")
    print(f"Ideal Efficiency: {calculate_ideal_efficiency(r)*100:.1f}%")
    print()
    
    # Generate and display report
    report = generate_report(T1, r, T3)
    print(report)
    
    # Generate plots
    print("\nGenerating analysis charts...")
    fig = plot_analysis(T1, r, T3, save=True)
    
    # Show plots
    plt.show()
    
    print("\n✓ Analysis complete!")
    print("✓ Charts saved to current directory")
    print("="*60)
