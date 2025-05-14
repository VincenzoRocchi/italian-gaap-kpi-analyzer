import pytest
from app_logic.calculator import calculate_selected_kpis, validate_balance_sheet
from app_logic.constants import (
    AVAILABLE_KPIS,
    POS_CURRENT_ASSETS, POS_LIQUID_ASSETS, POS_CASH,
    POS_CURRENT_LIABILITIES, POS_TOTAL_LIABILITIES, POS_TOTAL_EQUITY,
    POS_TOTAL_ASSETS,
    POS_IMMOBILIZZAZIONI_IMMATERIALI, POS_IMMOBILIZZAZIONI_MATERIALI,
    POS_IMMOBILIZZAZIONI_FINANZIARIE, POS_IMMOBILIZZAZIONI_NETTE,
    POS_DEBITI_TRIBUTARI, POS_DEBITI_PREVIDENZIALI,
    POS_DEBITI_OLTRE_12_MESI,
    POS_ATTIVITA_FINANZIARIE_CORRENTI,
    KPI_REQUIREMENTS
)

@pytest.fixture
def kpi_test_setup():
    """Provides initial zeroed data and available KPIs for tests."""
    initial_data = {str(i): 0.0 for i in range(1, 101)}
    return {"data": initial_data, "available_kpis": AVAILABLE_KPIS}

# --- Test Functions (converted from unittest methods) ---

def test_current_ratio_calculation(kpi_test_setup):
    data = kpi_test_setup["data"].copy()
    available_kpis = kpi_test_setup["available_kpis"]
    
    for k in POS_CURRENT_ASSETS[:5]: data[str(k)] = 10 # Current Assets = 50
    for k in POS_CURRENT_LIABILITIES[:4]: data[str(k)] = 5  # Current Liabilities = 20
    
    selected_kpis = ['current_ratio']
    results = calculate_selected_kpis(data, selected_kpis)
    
    assert 'current_ratio' in results
    assert results['current_ratio']['value'] == pytest.approx(50 / 20)
    assert results['current_ratio']['details'] == available_kpis['current_ratio']

def test_current_ratio_division_by_zero(kpi_test_setup):
    data = kpi_test_setup["data"].copy()
    available_kpis = kpi_test_setup["available_kpis"]

    for k in POS_CURRENT_ASSETS[:5]: data[str(k)] = 10 # Current Assets = 50
    # Current Liabilities = 0 (all positions in POS_CURRENT_LIABILITIES are 0 by default setup)
    selected_kpis = ['current_ratio']
    results = calculate_selected_kpis(data, selected_kpis)
    assert 'current_ratio' in results
    assert results['current_ratio']['value'] is None
    assert results['current_ratio']['details'] == available_kpis['current_ratio']

def test_working_capital_calculation(kpi_test_setup):
    data = kpi_test_setup["data"].copy()
    # available_kpis = kpi_test_setup["available_kpis"] # Not needed for this specific assertion

    for k in POS_CURRENT_ASSETS[:5]: data[str(k)] = 10  # Current Assets = 50
    for k in POS_CURRENT_LIABILITIES[:4]: data[str(k)] = 5 # Current Liabilities = 20
    results = calculate_selected_kpis(data, ['working_capital'])
    assert 'working_capital' in results
    assert results['working_capital']['value' ] == pytest.approx(50 - 20)

# Note: The balance sheet validation test setup was complex and might need more careful POS_ list selection
# For pytest conversion, I'll simplify its data setup slightly if the original was too broad or specific
# to unittest structure, ensuring it still tests balanced and unbalanced scenarios effectively.

def test_balance_sheet_validation_balanced(kpi_test_setup):
    data = kpi_test_setup["data"].copy()
    # Create a simple balanced scenario
    # Assets
    data[str(POS_TOTAL_ASSETS[0])] = 1000.0 # e.g., some cash or other asset
    # Equity & Liabilities Side
    data[str(POS_TOTAL_EQUITY[0])] = 600.0
    data[str(POS_TOTAL_LIABILITIES[0])] = 400.0
    # (Assuming provisions, TFR, accrued_expenses are 0 for simplicity here)

    result = validate_balance_sheet(data)
    assert result['valid'] == True, f"Assets: {result['assets']}, L&E: {result['liabilities_equity']}"
    # Need to recalculate sums based on *all* items in POS_TOTAL_ASSETS etc. for accurate comparison
    # For simplicity, this test assumes validate_balance_sheet correctly sums all items
    # and here we primarily test the balanced logic. More granular sum checks could be added.

def test_balance_sheet_validation_unbalanced(kpi_test_setup):
    data = kpi_test_setup["data"].copy()
    # Create a simple unbalanced scenario
    data[str(POS_TOTAL_ASSETS[0])] = 1000.0
    data[str(POS_TOTAL_EQUITY[0])] = 500.0 # Equity is 100 less than needed for balance
    data[str(POS_TOTAL_LIABILITIES[0])] = 400.0

    result = validate_balance_sheet(data)
    assert result['valid'] == False


def test_asset_rigidity_index(kpi_test_setup):
    data = kpi_test_setup["data"].copy()
    available_kpis = kpi_test_setup["available_kpis"]

    # Setup data for a non-zero numerator and denominator
    # Immobilizzazioni Nette (Numerator parts)
    data[str(POS_IMMOBILIZZAZIONI_IMMATERIALI[0])] = 10.0
    data[str(POS_IMMOBILIZZAZIONI_MATERIALI[0])] = 20.0
    data[str(POS_IMMOBILIZZAZIONI_FINANZIARIE[0])] = 5.0
    sum_immobilizzazioni_nette = 10.0 + 20.0 + 5.0 # = 35.0

    # Other assets to make Total Assets (Denominator) different from numerator sum
    data[str(POS_CURRENT_ASSETS[0])] = 15.0 # e.g. Inventories
    sum_current_assets_for_total = 15.0
    
    # Expected total assets: sum_immobilizzazioni_nette + sum_current_assets_for_total = 35 + 15 = 50
    # The calculator will sum all items in POS_TOTAL_ASSETS from the data dict.
    # Ensure no other asset items are accidentally non-zero from kpi_test_setup if POS_TOTAL_ASSETS is broad.
    # kpi_test_setup provides all 0.0, so only items we set here are non-zero.
    expected_total_assets = sum_immobilizzazioni_nette + sum_current_assets_for_total

    results = calculate_selected_kpis(data, ['asset_rigidity_index'])
    assert 'asset_rigidity_index' in results
    if expected_total_assets != 0:
        assert results['asset_rigidity_index']['value'] == pytest.approx(sum_immobilizzazioni_nette / expected_total_assets)
    else:
        assert results['asset_rigidity_index']['value'] is None # Should not happen with this test data setup
    assert results['asset_rigidity_index']['details'] == available_kpis['asset_rigidity_index']

def test_asset_rigidity_index_div_by_zero(kpi_test_setup):
    data = kpi_test_setup["data"].copy() # Starts with all 0.0
    available_kpis = kpi_test_setup["available_kpis"]
    # To ensure total_assets_sum is 0, all components of POS_TOTAL_ASSETS must be 0.
    # This also means immobilizzazioni_nette_sum will be 0.
    # The calculator should return None for 0/0 scenario.
    results = calculate_selected_kpis(data, ['asset_rigidity_index'])
    assert 'asset_rigidity_index' in results
    assert results['asset_rigidity_index']['value'] is None
    assert results['asset_rigidity_index']['details'] == available_kpis['asset_rigidity_index'] 

def test_asset_elasticity_index(kpi_test_setup):
    data = kpi_test_setup["data"].copy()
    available_kpis = kpi_test_setup["available_kpis"]

    # Current Assets (Numerator)
    data[str(POS_CURRENT_ASSETS[0])] = 15.0 
    data[str(POS_CURRENT_ASSETS[1])] = 25.0 
    sum_current_assets = 15.0 + 25.0 # = 40.0

    # Other assets for Total Assets (Denominator)
    data[str(POS_IMMOBILIZZAZIONI_IMMATERIALI[0])] = 60.0
    # Expected total assets = sum_current_assets + 60.0 = 40 + 60 = 100
    expected_total_assets = sum_current_assets + 60.0

    results = calculate_selected_kpis(data, ['asset_elasticity_index'])
    assert 'asset_elasticity_index' in results
    if expected_total_assets != 0:
        assert results['asset_elasticity_index']['value'] == pytest.approx(sum_current_assets / expected_total_assets)
    else:
        assert results['asset_elasticity_index']['value'] is None # Should not happen here
    assert results['asset_elasticity_index']['details'] == available_kpis['asset_elasticity_index']

def test_asset_elasticity_index_div_by_zero(kpi_test_setup):
    data = kpi_test_setup["data"].copy() # Starts with all 0.0
    available_kpis = kpi_test_setup["available_kpis"]
    # To ensure total_assets_sum is 0, all components of POS_TOTAL_ASSETS must be 0.
    # This also means current_assets_sum will be 0.
    # The calculator should return None for 0/0 scenario.
    results = calculate_selected_kpis(data, ['asset_elasticity_index'])
    assert 'asset_elasticity_index' in results
    assert results['asset_elasticity_index']['value'] is None
    assert results['asset_elasticity_index']['details'] == available_kpis['asset_elasticity_index']

def test_fixed_asset_coverage_ratio(kpi_test_setup):
    data = kpi_test_setup["data"].copy()
    available_kpis = kpi_test_setup["available_kpis"]

    val_equity = 250
    data[str(POS_TOTAL_EQUITY[0])] = val_equity # Sum total equity = 250
    sum_total_equity = val_equity
    
    val_intang = 100; data[str(POS_IMMOBILIZZAZIONI_IMMATERIALI[0])] = val_intang
    val_tang = 200; data[str(POS_IMMOBILIZZAZIONI_MATERIALI[0])] = val_tang
    val_fin = 50; data[str(POS_IMMOBILIZZAZIONI_FINANZIARIE[0])] = val_fin
    sum_immobilizzazioni_nette = val_intang + val_tang + val_fin # = 350
        
    results = calculate_selected_kpis(data, ['fixed_asset_coverage_ratio'])
    assert 'fixed_asset_coverage_ratio' in results
    if sum_immobilizzazioni_nette != 0:
        assert results['fixed_asset_coverage_ratio']['value'] == pytest.approx(sum_total_equity / sum_immobilizzazioni_nette)
    else:
        assert results['fixed_asset_coverage_ratio']['value'] is None
    assert results['fixed_asset_coverage_ratio']['details'] == available_kpis['fixed_asset_coverage_ratio']

def test_fixed_asset_coverage_ratio_div_by_zero(kpi_test_setup):
    data = kpi_test_setup["data"].copy()
    available_kpis = kpi_test_setup["available_kpis"]
    data[str(POS_TOTAL_EQUITY[0])] = 250 # Numerator non-zero
    results = calculate_selected_kpis(data, ['fixed_asset_coverage_ratio'])
    assert 'fixed_asset_coverage_ratio' in results
    assert results['fixed_asset_coverage_ratio']['value'] is None
    assert results['fixed_asset_coverage_ratio']['details'] == available_kpis['fixed_asset_coverage_ratio']
        
def test_tax_social_debt_on_assets_ratio(kpi_test_setup):
    data = kpi_test_setup["data"].copy()
    available_kpis = kpi_test_setup["available_kpis"]

    val_tax_debt = 20; data[str(POS_DEBITI_TRIBUTARI[0])] = val_tax_debt
    val_social_debt = 10; data[str(POS_DEBITI_PREVIDENZIALI[0])] = val_social_debt
    sum_tax_social_debt = val_tax_debt + val_social_debt # = 30
    
    data[str(POS_IMMOBILIZZAZIONI_NETTE[0])] = 350 # Example fixed asset value
    data[str(POS_CURRENT_ASSETS[0])] = 150       # Example current asset value
    # Total Assets for denominator calculation by get_sum in calculator
    sum_total_assets = 0
    for k in POS_TOTAL_ASSETS: sum_total_assets += data.get(str(k), 0.0)
        
    results = calculate_selected_kpis(data, ['tax_social_debt_on_assets_ratio'])
    assert 'tax_social_debt_on_assets_ratio' in results
    if sum_total_assets != 0:
        assert results['tax_social_debt_on_assets_ratio']['value'] == pytest.approx(sum_tax_social_debt / sum_total_assets)
    else:
        assert results['tax_social_debt_on_assets_ratio']['value'] is None
    assert results['tax_social_debt_on_assets_ratio']['details'] == available_kpis['tax_social_debt_on_assets_ratio']

def test_tax_social_debt_on_assets_ratio_div_by_zero(kpi_test_setup):
    data = kpi_test_setup["data"].copy()
    available_kpis = kpi_test_setup["available_kpis"]
    data[str(POS_DEBITI_TRIBUTARI[0])] = 20 # Numerator non-zero
    results = calculate_selected_kpis(data, ['tax_social_debt_on_assets_ratio'])
    assert 'tax_social_debt_on_assets_ratio' in results
    assert results['tax_social_debt_on_assets_ratio']['value'] is None
    assert results['tax_social_debt_on_assets_ratio']['details'] == available_kpis['tax_social_debt_on_assets_ratio']

def test_tangible_net_worth(kpi_test_setup):
    data = kpi_test_setup["data"].copy()
    available_kpis = kpi_test_setup["available_kpis"]

    val_equity = 250
    data[str(POS_TOTAL_EQUITY[0])] = val_equity # Sum = 250
    sum_total_equity = val_equity
    
    sum_intangibles = 0
    for i_idx, i_pos in enumerate(POS_IMMOBILIZZAZIONI_IMMATERIALI):
        val = 10 + i_idx # Ensure some variation if list is long
        data[str(i_pos)] = val
        sum_intangibles += val
            
    results = calculate_selected_kpis(data, ['tangible_net_worth'])
    assert 'tangible_net_worth' in results
    assert results['tangible_net_worth']['value'] == pytest.approx(sum_total_equity - sum_intangibles)
    assert results['tangible_net_worth']['details'] == available_kpis['tangible_net_worth']

# --- Tests for Priority 1 KPIs ---

def test_equity_multiplier(kpi_test_setup):
    data = kpi_test_setup["data"].copy()
    available_kpis = kpi_test_setup["available_kpis"]

    data[str(POS_TOTAL_ASSETS[0])] = 1000.0 # Total Assets = 1000
    data[str(POS_TOTAL_ASSETS[1])] = 500.0  # Total Assets = 1000 + 500 = 1500
    sum_total_assets = 1500.0

    data[str(POS_TOTAL_EQUITY[0])] = 300.0  # Total Equity = 300
    sum_total_equity = 300.0

    results = calculate_selected_kpis(data, ['equity_multiplier'])
    assert 'equity_multiplier' in results
    assert results['equity_multiplier']['value'] == pytest.approx(sum_total_assets / sum_total_equity)
    assert results['equity_multiplier']['details'] == available_kpis['equity_multiplier']

def test_equity_multiplier_div_by_zero(kpi_test_setup):
    data = kpi_test_setup["data"].copy()
    available_kpis = kpi_test_setup["available_kpis"]

    data[str(POS_TOTAL_ASSETS[0])] = 1000.0 # Total Assets = 1000 (Numerator non-zero)
    # POS_TOTAL_EQUITY remains 0.0 from setup

    results = calculate_selected_kpis(data, ['equity_multiplier'])
    assert 'equity_multiplier' in results
    assert results['equity_multiplier']['value'] is None
    assert results['equity_multiplier']['details'] == available_kpis['equity_multiplier']

def test_long_term_debt_to_equity(kpi_test_setup):
    data = kpi_test_setup["data"].copy()
    available_kpis = kpi_test_setup["available_kpis"]

    # POS_DEBITI_OLTRE_12_MESI is [70, 71, 72, 73, 74, 77, 78]
    data['70'] = 100.0 # Bonds
    data['73'] = 150.0 # Bank debt > 1yr
    sum_long_term_debt = 100.0 + 150.0 # = 250.0

    data[str(POS_TOTAL_EQUITY[0])] = 500.0  # Total Equity = 500
    sum_total_equity = 500.0

    results = calculate_selected_kpis(data, ['long_term_debt_to_equity'])
    assert 'long_term_debt_to_equity' in results
    assert results['long_term_debt_to_equity']['value'] == pytest.approx(sum_long_term_debt / sum_total_equity)
    assert results['long_term_debt_to_equity']['details'] == available_kpis['long_term_debt_to_equity']

def test_long_term_debt_to_equity_div_by_zero(kpi_test_setup):
    data = kpi_test_setup["data"].copy()
    available_kpis = kpi_test_setup["available_kpis"]

    data['70'] = 100.0 # Long term debt = 100 (Numerator non-zero)
    # POS_TOTAL_EQUITY remains 0.0 from setup

    results = calculate_selected_kpis(data, ['long_term_debt_to_equity'])
    assert 'long_term_debt_to_equity' in results
    assert results['long_term_debt_to_equity']['value'] is None
    assert results['long_term_debt_to_equity']['details'] == available_kpis['long_term_debt_to_equity']

# --- Tests for Priority 2 KPIs ---

def test_intangible_assets_ratio(kpi_test_setup):
    data = kpi_test_setup["data"].copy()
    available_kpis = kpi_test_setup["available_kpis"]

    # POS_IMMOBILIZZAZIONI_IMMATERIALI are 1-10
    data['1'] = 50.0
    data['5'] = 100.0
    sum_intangible_assets = 50.0 + 100.0 # = 150.0

    # Other assets for total assets
    data[str(POS_CURRENT_ASSETS[0])] = 200.0 
    data[str(POS_IMMOBILIZZAZIONI_MATERIALI[0])] = 150.0
    sum_total_assets = sum_intangible_assets + 200.0 + 150.0 # = 500.0

    results = calculate_selected_kpis(data, ['intangible_assets_ratio'])
    assert 'intangible_assets_ratio' in results
    assert results['intangible_assets_ratio']['value'] == pytest.approx(sum_intangible_assets / sum_total_assets)
    assert results['intangible_assets_ratio']['details'] == available_kpis['intangible_assets_ratio']

def test_intangible_assets_ratio_div_by_zero(kpi_test_setup):
    data = kpi_test_setup["data"].copy()
    available_kpis = kpi_test_setup["available_kpis"]
    # Intangible assets (numerator) can be non-zero, but if total assets is 0, it means intangibles must also be 0.
    # So, this tests 0/0 case.
    # data['1'] = 50.0 # This would make total assets non-zero. So, leave all assets as 0 from setup.
    results = calculate_selected_kpis(data, ['intangible_assets_ratio'])
    assert 'intangible_assets_ratio' in results
    assert results['intangible_assets_ratio']['value'] is None
    assert results['intangible_assets_ratio']['details'] == available_kpis['intangible_assets_ratio']

def test_financial_assets_ratio(kpi_test_setup):
    data = kpi_test_setup["data"].copy()
    available_kpis = kpi_test_setup["available_kpis"]

    # POS_IMMOBILIZZAZIONI_FINANZIARIE are 26-30
    data['26'] = 100.0
    sum_immob_fin = 100.0

    # POS_ATTIVITA_FINANZIARIE_CORRENTI are 46-48
    data['46'] = 50.0
    data['47'] = 25.0
    sum_att_fin_corr = 50.0 + 25.0 # = 75.0

    numerator = sum_immob_fin + sum_att_fin_corr # = 175.0

    # Other assets for total assets
    data[str(POS_CURRENT_ASSETS[0])] = 100.0 # Make sure this is not pos 46 or 47
    data[str(POS_IMMOBILIZZAZIONI_IMMATERIALI[0])] = 125.0
    sum_total_assets = numerator + 100.0 + 125.0 # = 175 + 100 + 125 = 400.0

    results = calculate_selected_kpis(data, ['financial_assets_ratio'])
    assert 'financial_assets_ratio' in results
    assert results['financial_assets_ratio']['value'] == pytest.approx(numerator / sum_total_assets)
    assert results['financial_assets_ratio']['details'] == available_kpis['financial_assets_ratio']

def test_financial_assets_ratio_div_by_zero(kpi_test_setup):
    data = kpi_test_setup["data"].copy()
    # Ensure total assets is zero (which it is by default in the fixture)
    # Numerator will also be zero as its components are part of total assets.
    # data[str(POS_IMMOBILIZZAZIONI_FINANZIARIE[0])] = 100 # This line made total assets non-zero
    result = calculate_selected_kpis(data, ['financial_assets_ratio'])
    assert result['financial_assets_ratio']['value'] is None

# Tests for non_current_assets_coverage
def test_non_current_assets_coverage_calculation(kpi_test_setup):
    data = kpi_test_setup["data"].copy()
    data[str(POS_TOTAL_EQUITY[0])] = 2000  # Equity
    data[str(POS_DEBITI_OLTRE_12_MESI[0])] = 1000  # Long Term Debt
    # POS_IMMOBILIZZAZIONI_NETTE is a list of positions. Set one of its components.
    # For example, if POS_IMMOBILIZZAZIONI_MATERIALI is part of POS_IMMOBILIZZAZIONI_NETTE:
    data[str(POS_IMMOBILIZZAZIONI_MATERIALI[0])] = 1500 # Net Fixed Assets component
    # (2000 + 1000) / 1500 = 3000 / 1500 = 2.0
    result = calculate_selected_kpis(data, ['non_current_assets_coverage'])
    assert result['non_current_assets_coverage']['value'] == pytest.approx(2.0)

def test_non_current_assets_coverage_div_by_zero(kpi_test_setup):
    data = kpi_test_setup["data"].copy()
    data[str(POS_TOTAL_EQUITY[0])] = 2000
    data[str(POS_DEBITI_OLTRE_12_MESI[0])] = 1000
    # Net Fixed Assets (denominator) remains 0 from kpi_test_setup
    result = calculate_selected_kpis(data, ['non_current_assets_coverage'])
    assert result['non_current_assets_coverage']['value'] is None

# Tests for net_working_capital_ratio
def test_net_working_capital_ratio_calculation(kpi_test_setup):
    data = kpi_test_setup["data"].copy()
    # NWC = Current Assets - Current Liabilities
    # Ratio = NWC / Total Assets

    # Set components for NWC
    data[str(POS_CURRENT_ASSETS[0])] = 1500    # e.g., pos 31 (Inventories) for Current Assets
    data[str(POS_CURRENT_LIABILITIES[0])] = 500 # e.g., pos 79 (Trade Payables) for Current Liabilities
    # NWC = 1500 - 500 = 1000

    # Ensure Total Assets is non-zero.
    # POS_TOTAL_ASSETS sums items 1-60.
    # Current Assets (e.g. pos 31) is already set.
    # Add a non-current asset to make Total Assets = 1500 (CA) + 500 (NCA) = 2000
    # Pick a position for a non-current asset that is part of POS_TOTAL_ASSETS and not in POS_CURRENT_ASSETS
    # For example, an item from POS_IMMOBILIZZAZIONI_MATERIALI if its first element is not also POS_CURRENT_ASSETS[0]
    # A simpler way is to ensure that at least one item in POS_TOTAL_ASSETS that is also in POS_CURRENT_ASSETS is set (done by data[str(POS_CURRENT_ASSETS[0])]),
    # and one item in POS_TOTAL_ASSETS that is a fixed asset is set.
    data[str(POS_IMMOBILIZZAZIONI_MATERIALI[0])] = 500 # e.g. pos 11 (Tangible Assets) for Fixed Assets
    
    # Expected: NWC = 1000. Total Assets will be at least 1500 (from current) + 500 (from fixed) = 2000
    # (assuming POS_CURRENT_ASSETS[0] and POS_IMMOBILIZZAZIONI_MATERIALI[0] are distinct and both part of POS_TOTAL_ASSETS)
    # Ratio = 1000 / 2000 = 0.5
    
    # To be very explicit for Total Assets for this test:
    # Ensure other asset items that might be in POS_TOTAL_ASSETS are zero unless explicitly set.
    # The kpi_test_setup already ensures data is zeroed out, and we made a copy.
    # Our setting data[str(POS_CURRENT_ASSETS[0])] = 1500 and data[str(POS_IMMOBILIZZAZIONI_MATERIALI[0])] = 500
    # will make get_sum(data, POS_TOTAL_ASSETS) = 2000 if these are the only non-zero items in range 1-60.

    result = calculate_selected_kpis(data, ['net_working_capital_ratio'])
    assert result['net_working_capital_ratio']['value'] == pytest.approx(0.5)


def test_net_working_capital_ratio_div_by_zero(kpi_test_setup):
    data = kpi_test_setup["data"].copy()
    # Numerator (NWC = CA - CL):
    # CA will be 0 as no current asset items are set (so Total Assets is also 0).
    # data[str(POS_CURRENT_ASSETS[0])] = 100 # This line made Total Assets non-zero
    data[str(POS_CURRENT_LIABILITIES[0])] = 50 # CL = 50, so NWC = 0 - 50 = -50
    # Total Assets (denominator) remains 0 from kpi_test_setup as no asset items are set.
    result = calculate_selected_kpis(data, ['net_working_capital_ratio'])
    assert result['net_working_capital_ratio']['value'] is None

# Removed SAMPLE_DATA and unittest.main() as they are not idiomatic for pytest 