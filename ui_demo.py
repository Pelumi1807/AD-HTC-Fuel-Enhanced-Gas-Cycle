"""
AD-HTC FUEL-ENHANCED GAS CYCLE
Simple UI Demonstration
MEG 315 Applied Thermodynamics 2 - University of Lagos

This module demonstrates how the UI would interact with the analysis code.
For teaching purposes - shows the "ANALYZE" button concept.
"""

import matplotlib.pyplot as plt
from main import plot_analysis, calculate_compressor_exit, generate_report

def simple_ui_demo():
    """
    Demonstrate a simple command-line interface.
    This mimics what the web UI would do.
    """
    print("\n" + "="*60)
    print("AD-HTC UI DEMONSTRATION")
    print("="*60)
    print("\nThis simulates the 'ANALYZE' button functionality.")
    print("In the real UI, you would click buttons and see charts.\n")
    
    # Default values from project
    T1 = 288
    r = 15
    T3 = 2691.50
    
    print("Current Parameters:")
    print(f"  T₁ (Inlet Temperature): {T1} K")
    print(f"  r (Compression Ratio): {r}")
    print(f"  T₃ (Turbine Inlet): {T3} K")
    
    # Show what happens when ANALYZE is clicked
    input("\nPress Enter to simulate clicking 'ANALYZE'...")
    
    print("\n⚙ Running thermodynamic calculations...")
    T2 = calculate_compressor_exit(T1, r)
    print(f"✓ Calculated T₂ = {T2:.2f} K")
    
    print("\n⚙ Generating performance charts...")
    fig = plot_analysis(T1, r, T3)
    
    print("\n⚙ Generating text report...")
    report = generate_report(T1, r, T3)
    print("\n" + report)
    
    print("\n✓ Analysis complete!")
    print("✓ Charts displayed")
    print("✓ Report generated")
    
    plt.show()
    
    print("\nIn the real UI, this all happens instantly when you click ANALYZE!")


def demonstrate_parameter_change():
    """
    Show how changing parameters affects results.
    """
    print("\n" + "="*60)
    print("PARAMETER SENSITIVITY DEMONSTRATION")
    print("="*60)
    print("\nThis shows what happens when you change inputs.\n")
    
    # Baseline
    T1_base = 288
    r_base = 15
    T3_base = 2691.50
    
    T2_base = calculate_compressor_exit(T1_base, r_base)
    
    print("Baseline Case:")
    print(f"  T₁={T1_base}K, r={r_base}, T₂={T2_base:.2f}K")
    
    # Scenario 1: Higher compression ratio
    r_high = 20
    T2_high = calculate_compressor_exit(T1_base, r_high)
    print(f"\nScenario 1: Higher Compression Ratio (r={r_high})")
    print(f"  T₂ increases to {T2_high:.2f}K (+{T2_high-T2_base:.1f}K)")
    print(f"  Effect: Higher efficiency but hotter components")
    
    # Scenario 2: Higher inlet temperature
    T1_hot = 308  # 35°C hot day
    T2_hot = calculate_compressor_exit(T1_hot, r_base)
    print(f"\nScenario 2: Hot Day (T₁={T1_hot}K)")
    print(f"  T₂ increases to {T2_hot:.2f}K (+{T2_hot-T2_base:.1f}K)")
    print(f"  Effect: Lower density air, less mass flow")
    
    # Scenario 3: Lower turbine inlet
    T3_low = 2500
    print(f"\nScenario 3: Lower Turbine Inlet (T₃={T3_low}K)")
    print(f"  Combustion ΔT: {T3_low-T2_base:.1f}K vs baseline {T3_base-T2_base:.1f}K")
    print(f"  Effect: Less power output, lower efficiency")


if __name__ == "__main__":
    simple_ui_demo()
    demonstrate_parameter_change()
    
    print("\n" + "="*60)
    print("UI DEMONSTRATION COMPLETE")
    print("="*60)
