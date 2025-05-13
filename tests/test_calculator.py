import unittest
from app_logic.calculator import calculate_selected_kpis, validate_balance_sheet
# validate_balance_sheet uses constants, so they must be accessible in its new context.
# If calculator.py correctly imports from .constants, this test file might not need direct constant imports
# unless it sets up data that relies on them directly for test construction.
# For now, let's assume calculator.py handles its constant needs via its own relative imports.

class TestCalculator(unittest.TestCase):
    def test_current_ratio_calculation(self):
        """Test current ratio calculation with sample data."""
        # Sample data with current assets = 1000 and current liabilities = 500
        # These position keys must match those used in app_logic.constants for POS_CURRENT_ASSETS etc.
        test_data = {
            # Current assets - Example based on POS_CURRENT_ASSETS from constants
            '31': 200.0,  # Example: Inventory
            '39': 300.0,  # Example: Receivables
            '46': 200.0,  # Example: Current Financial Assets
            '49': 300.0,  # Example: Cash
            
            # Current liabilities - Example based on POS_CURRENT_LIABILITIES
            '79': 200.0,  # Example: Trade Payables (short term)
            '80': 300.0,  # Example: Amounts owed to banks (short term)
        }
        # We need AVAILABLE_KPIS for the calculate_selected_kpis to work as it populates details
        # This implies calculator.py must correctly get AVAILABLE_KPIS from .constants
        results = calculate_selected_kpis(test_data, ['current_ratio'])
        self.assertIn('current_ratio', results)
        self.assertAlmostEqual(results['current_ratio']['value'], 2.0)
    
    def test_working_capital_calculation(self):
        """Test working capital calculation with sample data."""
        test_data = {
            '31': 200.0, 
            '39': 300.0, 
            '46': 200.0, 
            '49': 300.0, 
            '79': 200.0,
            '80': 200.0, 
        }
        results = calculate_selected_kpis(test_data, ['working_capital'])
        self.assertIn('working_capital', results)
        self.assertAlmostEqual(results['working_capital']['value'], 600.0)
    
    def test_balance_sheet_validation(self):
        """Test balance sheet validation with balanced and unbalanced data."""
        # Balanced data - keys must match what BALANCE_SHEET_STRUCTURE and get_all_positions expect
        balanced_data = {
            # Assets
            '1': 100.0,   
            '11': 200.0,  
            '31': 300.0,  
            '49': 400.0,  
            # Equity & Liabilities
            '52': 500.0,  # Capital
            '70': 200.0,  # Bonds
            '79': 200.0,  # Trade payables (short)
            '100': 100.0 # TFR
            # total assets = 1000
            # total equity_liabilities_side = 500(E) + 200(L) + 200(L) + 100(TFR) = 1000
        }
        
        result = validate_balance_sheet(balanced_data)
        self.assertTrue(result['valid'], f"Assets: {result['assets']}, L&E: {result['liabilities_equity']}")
        self.assertAlmostEqual(result['assets'], 1000.0)
        self.assertAlmostEqual(result['liabilities_equity'], 1000.0)
        
        unbalanced_data = {
            '1': 100.0,   
            '11': 200.0,  
            '31': 300.0,  
            '49': 400.0,  
            '52': 400.0,  # Equity (changed from 500)
            '70': 200.0,  
            '79': 200.0,
            '100': 100.0 
            # total assets = 1000
            # total equity_liabilities_side = 400(E) + 200(L) + 200(L) + 100(TFR) = 900
        }
        
        result = validate_balance_sheet(unbalanced_data)
        self.assertFalse(result['valid'])
        self.assertAlmostEqual(result['assets'], 1000.0)
        self.assertAlmostEqual(result['liabilities_equity'], 900.0)

if __name__ == '__main__':
    unittest.main() 