from .constants import (
    AVAILABLE_KPIS, POS_CURRENT_ASSETS, POS_LIQUID_ASSETS, POS_CASH, 
    POS_CURRENT_LIABILITIES, POS_TOTAL_LIABILITIES, POS_TOTAL_EQUITY, 
    POS_TOTAL_ASSETS, BALANCE_SHEET_STRUCTURE, get_all_positions
)

def calculate_selected_kpis(data, selected_kpi_keys):
    """Calculates Selected KPIs based on the provided data dictionary and keys.
    
    Args:
        data (dict): Financial data with position numbers as keys (string format)
        selected_kpi_keys (list): List of KPI keys to calculate
    
    Returns:
        dict: Dictionary with KPI results where keys are KPI keys, and values are dicts
              containing 'value' and 'details' (from AVAILABLE_KPIS).
    """
    kpis_results = {}

    # Helper to safely get sum of positions from the input data dict
    def get_sum(positions):
        return sum(data.get(str(p), 0.0) for p in positions)  # data keys are strings

    # Calculate only requested KPIs using the defined position lists
    if 'current_ratio' in selected_kpi_keys and 'current_ratio' in AVAILABLE_KPIS:
        current_assets = get_sum(POS_CURRENT_ASSETS)
        current_liabilities = get_sum(POS_CURRENT_LIABILITIES)
        value = current_assets / current_liabilities if current_liabilities else 0
        kpis_results['current_ratio'] = {'value': value, 'details': AVAILABLE_KPIS['current_ratio']}

    if 'quick_ratio' in selected_kpi_keys and 'quick_ratio' in AVAILABLE_KPIS:
        liquid_assets = get_sum(POS_LIQUID_ASSETS)
        current_liabilities = get_sum(POS_CURRENT_LIABILITIES)
        value = liquid_assets / current_liabilities if current_liabilities else 0
        kpis_results['quick_ratio'] = {'value': value, 'details': AVAILABLE_KPIS['quick_ratio']}

    if 'cash_ratio' in selected_kpi_keys and 'cash_ratio' in AVAILABLE_KPIS:
        cash_equivalents = get_sum(POS_CASH)
        current_liabilities = get_sum(POS_CURRENT_LIABILITIES)
        value = cash_equivalents / current_liabilities if current_liabilities else 0
        kpis_results['cash_ratio'] = {'value': value, 'details': AVAILABLE_KPIS['cash_ratio']}

    if 'debt_to_equity' in selected_kpi_keys and 'debt_to_equity' in AVAILABLE_KPIS:
        total_liabilities = get_sum(POS_TOTAL_LIABILITIES)
        total_equity = get_sum(POS_TOTAL_EQUITY)
        value = total_liabilities / total_equity if total_equity else 0
        kpis_results['debt_to_equity'] = {'value': value, 'details': AVAILABLE_KPIS['debt_to_equity']}

    if 'debt_ratio' in selected_kpi_keys and 'debt_ratio' in AVAILABLE_KPIS:
        total_liabilities = get_sum(POS_TOTAL_LIABILITIES)
        total_assets = get_sum(POS_TOTAL_ASSETS)
        value = total_liabilities / total_assets if total_assets else 0
        kpis_results['debt_ratio'] = {'value': value, 'details': AVAILABLE_KPIS['debt_ratio']}

    if 'working_capital' in selected_kpi_keys and 'working_capital' in AVAILABLE_KPIS:
        current_assets = get_sum(POS_CURRENT_ASSETS)
        current_liabilities = get_sum(POS_CURRENT_LIABILITIES)
        value = current_assets - current_liabilities
        kpis_results['working_capital'] = {'value': value, 'details': AVAILABLE_KPIS['working_capital']}

    return kpis_results

def validate_balance_sheet(data):
    """Validates balance sheet by checking if assets equals liabilities + equity.
    
    Args:
        data (dict): Financial data with position numbers as keys (string format)
    
    Returns:
        dict: Dictionary with validation result
    """
    # Helper to safely get sum of positions from the input data dict
    def get_sum(positions):
        return sum(data.get(str(p), 0.0) for p in positions)  # data keys are strings
        
    # Calculate totals for balance sheet validation
    # from .constants import get_all_positions # Already imported at the top
    total_assets = get_sum(get_all_positions(BALANCE_SHEET_STRUCTURE['assets']))
    total_liabilities = get_sum(get_all_positions(BALANCE_SHEET_STRUCTURE['equity_liabilities']['liabilities']))
    total_equity = get_sum(get_all_positions(BALANCE_SHEET_STRUCTURE['equity_liabilities']['equity']))
    total_provisions = get_sum(get_all_positions(BALANCE_SHEET_STRUCTURE['equity_liabilities']['provisions_for_risks_and_charges']))
    total_accrued = get_sum(get_all_positions(BALANCE_SHEET_STRUCTURE['equity_liabilities']['accrued_expenses_and_deferred_income']))
    total_tfr = float(data.get('100', 0.0))  # TFR is a single value, key is '100'

    total_liabilities_equity_side = total_liabilities + total_equity + total_provisions + total_accrued + total_tfr

    # Use tolerance for float comparison
    is_valid = abs(total_assets - total_liabilities_equity_side) < 0.01
    
    return {
        "valid": is_valid, 
        "assets": total_assets, 
        "liabilities_equity": total_liabilities_equity_side
    } 