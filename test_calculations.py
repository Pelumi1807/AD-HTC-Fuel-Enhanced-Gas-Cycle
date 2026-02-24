"""
AD-HTC FUEL-ENHANCED GAS CYCLE
Unit Tests
MEG 315 Applied Thermodynamics 2 - University of Lagos

This module tests that all calculations are correct.
"""

import unittest
import numpy as np
from main import (
    calculate_compressor_exit,
    calculate_heat_input,
    calculate_ideal_efficiency,
    check_steam_quality,
    generate_th_diagram_data
)


class TestThermodynamicCalculations(unittest.TestCase):
    """Test all thermodynamic calculation functions."""
    
    def setUp(self):
        """Set up test parameters."""
        self.T1 = 288  # K
        self.r = 15    # 
        self.gamma = 1.4
        self.T3 = 2691.50  # K
        self.Cp = 1.005  # kJ/kgK
        self.m_dot = 1.0  # kg/s
    
    def test_calculate_compressor_exit(self):
        """Test T2 calculation."""
        T2 = calculate_compressor_exit(self.T1, self.r, self.gamma)
        
        # Expected value from document: 850.80 K
        self.assertAlmostEqual(T2, 850.80, places=1)
        
        # Physical check: T2 should be > T1
        self.assertGreater(T2, self.T1)
        
        # Test with different r
        T2_higher_r = calculate_compressor_exit(self.T1, 20, self.gamma)
        self.assertGreater(T2_higher_r, T2)
    
    def test_calculate_heat_input(self):
        """Test Q_in calculation."""
        T2 = calculate_compressor_exit(self.T1, self.r, self.gamma)
        Q_in = calculate_heat_input(self.m_dot, self.Cp, self.T3, T2)
        
        # Heat input should be positive
        self.assertGreater(Q_in, 0)
        
        # Check units: kJ/kgK * K = kJ/kg, times kg/s = kW
        self.assertIsInstance(Q_in, float)
    
    def test_calculate_ideal_efficiency(self):
        """Test cycle efficiency calculation."""
        eta = calculate_ideal_efficiency(self.r, self.gamma)
        
        # Efficiency should be between 0 and 1
        self.assertGreater(eta, 0)
        self.assertLess(eta, 1)
        
        # Higher compression ratio = higher efficiency
        eta_higher_r = calculate_ideal_efficiency(20, self.gamma)
        self.assertGreater(eta_higher_r, eta)
    
    def test_check_steam_quality(self):
        """Test steam quality warning system."""
        # Good quality
        quality, warning = check_steam_quality(2500, 500, 2600)
        self.assertAlmostEqual(quality, 0.952, places=3)
        self.assertIsNone(warning)  # No warning for good quality
        
        # Borderline quality
        quality, warning = check_steam_quality(2400, 500, 2600)
        self.assertAlmostEqual(quality, 0.905, places=3)
        self.assertIsNotNone(warning)  # Should have warning
        self.assertIn("CAUTION", warning)
        
        # Bad quality
        quality, warning = check_steam_quality(2300, 500, 2600)
        self.assertAlmostEqual(quality, 0.857, places=3)
        self.assertIsNotNone(warning)  # Should have warning
        self.assertIn("WARNING", warning)
    
    def test_generate_th_diagram_data(self):
        """Test T-H diagram data generation."""
        heat_steps, T_gas = generate_th_diagram_data(self.T3)
        
        # Check array lengths
        self.assertEqual(len(heat_steps), 100)
        self.assertEqual(len(T_gas), 100)
        
        # Check temperature range
        self.assertAlmostEqual(T_gas[0], self.T3)  # First point = T3
        self.assertAlmostEqual(T_gas[-1], 850)     # Last point = 850K
        
        # Check monotonic decreasing
        self.assertTrue(np.all(np.diff(T_gas) < 0))
    
    def test_extreme_values(self):
        """Test with extreme (but possible) values."""
        # Very high compression
        T2_extreme = calculate_compressor_exit(self.T1, 40, self.gamma)
        self.assertLess(T2_extreme, 2000)  # Should still be reasonable
        
        # Very low inlet (cold day)
        T2_cold = calculate_compressor_exit(250, self.r, self.gamma)
        self.assertLess(T2_cold, 800)
        
        # Very high inlet (hot day)
        T2_hot = calculate_compressor_exit(320, self.r, self.gamma)
        self.assertGreater(T2_hot, 900)
    
    def test_mathematical_consistency(self):
        """Test that formulas are mathematically consistent."""
        T2 = calculate_compressor_exit(self.T1, self.r, self.gamma)
        
        # For isentropic process: T2/T1 = (P2/P1)^((γ-1)/γ)
        # Here, P2/P1 = r
        ratio_actual = T2 / self.T1
        ratio_theoretical = self.r ** ((self.gamma - 1) / self.gamma)
        
        self.assertAlmostEqual(ratio_actual, ratio_theoretical)


if __name__ == '__main__':
    print("\n" + "="*60)
    print("RUNNING UNIT TESTS")
    print("="*60)
    unittest.main(argv=[''], verbosity=2, exit=False)
    print("\n" + "="*60)
