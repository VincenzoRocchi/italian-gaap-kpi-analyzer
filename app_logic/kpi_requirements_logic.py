from .balance_sheet_config import BALANCE_SHEET_STRUCTURE, POSITION_NAMES

# Helper to get all position numbers - needs adjustment for nested structure
def get_all_positions(structure_part):
    positions = []
    if isinstance(structure_part, dict):
        for key, value in structure_part.items():
            positions.extend(get_all_positions(value)) # Recurse for dictionaries
    elif isinstance(structure_part, list):
        # Expecting list of strings now
        if all(isinstance(item, str) for item in structure_part):
             positions.extend(structure_part) # Extend if it's a list of positions
    return sorted(list(set(positions))) # Return unique sorted positions

ALL_POSITIONS = get_all_positions(BALANCE_SHEET_STRUCTURE)

# Map KPIs to the positions they require (UPDATED for new structure)
KPI_REQUIREMENTS = {
    # These will be repopulated after POS_ lists are updated with string keys
}

# Define _kpi_req_total_assets before it's used by POS_TOTAL_ASSETS
_kpi_req_total_assets_constituents = (
    [str(x) for x in get_all_positions(BALANCE_SHEET_STRUCTURE['assets']['non_current_assets']) if "(Placeholder" not in POSITION_NAMES.get(str(x), "")] +
    [str(x) for x in get_all_positions(BALANCE_SHEET_STRUCTURE['assets']['current_assets']) if "(Placeholder" not in POSITION_NAMES.get(str(x), "")] +
    [str(x) for x in get_all_positions(BALANCE_SHEET_STRUCTURE['assets']['prepaid_expenses_and_accrued_income']) if "(Placeholder" not in POSITION_NAMES.get(str(x), "")]
)
_kpi_req_total_assets = sorted(list(set(_kpi_req_total_assets_constituents)))

# KPI position lists for calculation (already in constants.py but ensuring they are here)
POS_CURRENT_ASSETS = [31, 32, 33, 34, 35, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50]
POS_LIQUID_ASSETS = [39, 40, 41, 42, 43, 45]
POS_CASH = [49, 50]
POS_CURRENT_LIABILITIES = [79, 80, 81, 82, 83, 84, 85, 86, 87, 88]
POS_TOTAL_LIABILITIES = [67, 68, 69, 100, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88]
POS_TOTAL_EQUITY = [52, 53, 54, 55, 56, 57, 58, 59, 64, 65, 66]
POS_TOTAL_ASSETS = _kpi_req_total_assets # Use the dynamically generated list

# Dynamically define POS_ lists based on BALANCE_SHEET_STRUCTURE for clarity and maintainability
_temp_imm_immat = get_all_positions(BALANCE_SHEET_STRUCTURE['assets']['non_current_assets']['intangible_assets'])
POS_IMMOBILIZZAZIONI_IMMATERIALI = sorted([str(x) for x in _temp_imm_immat if "(Placeholder" not in POSITION_NAMES.get(str(x), "")])

_temp_imm_mat = get_all_positions(BALANCE_SHEET_STRUCTURE['assets']['non_current_assets']['tangible_assets'])
POS_IMMOBILIZZAZIONI_MATERIALI = sorted([str(x) for x in _temp_imm_mat if "(Placeholder" not in POSITION_NAMES.get(str(x), "")])

# POS_IMMOBILIZZAZIONI_FINANZIARIE does not have placeholders in its typical range 26-30, so no filter needed here, but ensure it's stringified
POS_IMMOBILIZZAZIONI_FINANZIARIE = [str(x) for x in get_all_positions(BALANCE_SHEET_STRUCTURE['assets']['non_current_assets']['financial_investments_non_current'])]

POS_IMMOBILIZZAZIONI_NETTE = sorted(list(set(
    POS_IMMOBILIZZAZIONI_IMMATERIALI + # Already filtered and stringified
    POS_IMMOBILIZZAZIONI_MATERIALI +   # Already filtered and stringified
    POS_IMMOBILIZZAZIONI_FINANZIARIE # Already stringified
)))

POS_DEBITI_TRIBUTARI = [str(x) for x in BALANCE_SHEET_STRUCTURE['equity_liabilities']['liabilities']['tax_payables']]
POS_DEBITI_PREVIDENZIALI = [str(x) for x in BALANCE_SHEET_STRUCTURE['equity_liabilities']['liabilities']['social_security_payables']]

# New POS list for Long-term Debt
POS_DEBITI_OLTRE_12_MESI = sorted(list(set(
    BALANCE_SHEET_STRUCTURE['equity_liabilities']['liabilities']['bonds_issued'] + 
    BALANCE_SHEET_STRUCTURE['equity_liabilities']['liabilities']['convertible_bonds_issued'] + 
    BALANCE_SHEET_STRUCTURE['equity_liabilities']['liabilities']['amounts_owed_to_shareholders_for_loans'] + 
    [BALANCE_SHEET_STRUCTURE['equity_liabilities']['liabilities']['amounts_owed_to_banks'][0]] + # Index 0 for long-term part
    [BALANCE_SHEET_STRUCTURE['equity_liabilities']['liabilities']['amounts_owed_to_other_lenders'][0]] + # Index 0 for long-term part
    [BALANCE_SHEET_STRUCTURE['equity_liabilities']['liabilities']['debt_represented_by_credit_instruments'][0]] + # Index 0 for long-term part
    [BALANCE_SHEET_STRUCTURE['equity_liabilities']['liabilities']['amounts_owed_to_group_companies'][0]] # Index 0 for long-term part
)))

# New POS list for Current Financial Assets
POS_ATTIVITA_FINANZIARIE_CORRENTI = [str(x) for x in get_all_positions(BALANCE_SHEET_STRUCTURE['assets']['current_assets']['current_financial_assets'])]

# Re-populate KPI_REQUIREMENTS with the new POS_ lists for accuracy
# Ensure these lists are flat lists of unique integers.
_kpi_req_current_assets = [31, 32, 33, 34, 35, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50]
_kpi_req_liquid_assets = [39, 40, 41, 42, 43, 45]
_kpi_req_cash = [49, 50]
_kpi_req_current_liabilities = [79, 80, 81, 82, 83, 84, 85, 86, 87, 88]
_kpi_req_total_liabilities = [67, 68, 69, 100, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88]
_kpi_req_total_equity = [52, 53, 54, 55, 56, 57, 58, 59, 64, 65, 66]

KPI_REQUIREMENTS = {
    'current_ratio': sorted(list(set([str(x) for x in POS_CURRENT_ASSETS] + [str(y) for y in POS_CURRENT_LIABILITIES]))),
    'quick_ratio': sorted(list(set( [str(x) for x in POS_LIQUID_ASSETS] + [str(x) for x in POS_CASH] + POS_ATTIVITA_FINANZIARIE_CORRENTI + [str(x) for x in POS_CURRENT_LIABILITIES] ))),
    'cash_ratio': sorted(list(set([str(x) for x in POS_CASH] + [str(y) for y in POS_CURRENT_LIABILITIES]))),
    'debt_to_equity': sorted(list(set([str(x) for x in POS_TOTAL_LIABILITIES] + [str(y) for y in POS_TOTAL_EQUITY]))),
    'debt_ratio': sorted(list(set([str(x) for x in POS_TOTAL_LIABILITIES] + [str(y) for y in POS_TOTAL_ASSETS]))),
    'working_capital': sorted(list(set([str(x) for x in POS_CURRENT_ASSETS] + [str(y) for y in POS_CURRENT_LIABILITIES]))),
    'asset_rigidity_index': sorted(list(set([str(x) for x in POS_IMMOBILIZZAZIONI_NETTE] + [str(y) for y in POS_TOTAL_ASSETS]))),
    'asset_elasticity_index': sorted(list(set([str(x) for x in POS_CURRENT_ASSETS] + [str(y) for y in POS_TOTAL_ASSETS]))),
    'fixed_asset_coverage_ratio': sorted(list(set([str(x) for x in POS_TOTAL_EQUITY] + [str(y) for y in POS_IMMOBILIZZAZIONI_NETTE]))),
    'tax_social_debt_on_assets_ratio': sorted(list(set([str(x) for x in POS_DEBITI_TRIBUTARI] + [str(y) for y in POS_DEBITI_PREVIDENZIALI] + [str(z) for z in POS_TOTAL_ASSETS]))),
    'tangible_net_worth': sorted(list(set([str(x) for x in POS_TOTAL_EQUITY] + [str(y) for y in POS_IMMOBILIZZAZIONI_IMMATERIALI]))),
    'equity_multiplier': sorted(list(set([str(x) for x in POS_TOTAL_ASSETS] + [str(y) for y in POS_TOTAL_EQUITY]))),
    'long_term_debt_to_equity': sorted(list(set([str(x) for x in POS_DEBITI_OLTRE_12_MESI] + [str(y) for y in POS_TOTAL_EQUITY]))),
    'intangible_assets_ratio': sorted(list(set([str(x) for x in POS_IMMOBILIZZAZIONI_IMMATERIALI] + [str(y) for y in POS_TOTAL_ASSETS]))),
    'financial_assets_ratio': sorted(list(set(
        [str(x) for x in POS_IMMOBILIZZAZIONI_FINANZIARIE] +
        [str(x) for x in POS_ATTIVITA_FINANZIARIE_CORRENTI] +
        [str(x) for x in POS_TOTAL_ASSETS]
    ))),
    'non_current_assets_coverage': sorted(list(set(
        [str(x) for x in POS_TOTAL_EQUITY] +
        [str(x) for x in POS_DEBITI_OLTRE_12_MESI] +
        [str(x) for x in POS_IMMOBILIZZAZIONI_NETTE]
    ))),
    'net_working_capital_ratio': sorted(list(set([str(x) for x in POS_CURRENT_ASSETS] + [str(y) for y in POS_CURRENT_LIABILITIES] + [str(z) for z in POS_TOTAL_ASSETS])))
}

# New: Total Liabilities Excluding TFR (pos '100')
POS_TOTAL_LIABILITIES_EXCL_TFR = sorted([str(p) for p in POS_TOTAL_LIABILITIES if str(p) != '100'])

# Update KPIs that exclude TFR
KPI_REQUIREMENTS['debt_to_equity_excl_tfr'] = sorted(list(set([str(x) for x in POS_TOTAL_LIABILITIES_EXCL_TFR] + [str(y) for y in POS_TOTAL_EQUITY])))
KPI_REQUIREMENTS['debt_ratio_excl_tfr'] = sorted(list(set([str(x) for x in POS_TOTAL_LIABILITIES_EXCL_TFR] + [str(y) for y in POS_TOTAL_ASSETS]))) 