from .constants import (
    AVAILABLE_KPIS, POS_CURRENT_ASSETS, POS_LIQUID_ASSETS, POS_CASH, 
    POS_CURRENT_LIABILITIES, POS_TOTAL_LIABILITIES, POS_TOTAL_EQUITY, 
    POS_TOTAL_ASSETS, BALANCE_SHEET_STRUCTURE, get_all_positions,
    # New POS lists for CEE/Italian CCII KPIs
    POS_IMMOBILIZZAZIONI_IMMATERIALI, POS_IMMOBILIZZAZIONI_MATERIALI, 
    POS_IMMOBILIZZAZIONI_FINANZIARIE, POS_IMMOBILIZZAZIONI_NETTE,
    POS_DEBITI_TRIBUTARI, POS_DEBITI_PREVIDENZIALI,
    POS_DEBITI_OLTRE_12_MESI,
    POS_ATTIVITA_FINANZIARIE_CORRENTI, # Import new POS list
    KPI_REQUIREMENTS,
    POS_TOTAL_LIABILITIES_EXCL_TFR
)

def calculate_selected_kpis(data, selected_kpi_keys):
    """Calculates Selected KPIs based on the provided data dictionary and keys.
    
    Args:
        data (dict): Financial data with position numbers as keys (string format)
        selected_kpi_keys (list): List of KPI keys to calculate
    
    Returns:
        dict: Dictionary with KPI results where keys are KPI keys.
              Each value is a dict: {'value': ..., 'status': 'ok'/'error', 'message': '...', 'details': ...}.
    """
    results = {}

    for kpi_key in selected_kpi_keys:
        kpi_details = AVAILABLE_KPIS.get(kpi_key)
        if not kpi_details:
            results[kpi_key] = {
                'value': None,
                'status': 'error',
                'message': 'KPI non definito.',
                'details': {'name_display': f'Unknown KPI: {kpi_key}', 'description_short': 'N/A'}
            }
            continue

        result_entry = {'value': None, 'status': 'error', 'message': 'Errore sconosciuto', 'details': kpi_details}

        try:
            # Existing KPI Calculations
            if kpi_key == 'current_ratio':
                current_assets_sum = get_sum(data, POS_CURRENT_ASSETS)
                current_liabilities_sum = get_sum(data, POS_CURRENT_LIABILITIES)
                if current_liabilities_sum != 0:
                    result_entry['value'] = current_assets_sum / current_liabilities_sum
                    result_entry['status'] = 'ok'
                    result_entry['message'] = ''
                else:
                    result_entry['message'] = "Divisione per zero (Passività Correnti nulle)."

            elif kpi_key == 'quick_ratio':
                liquid_assets_sum = get_sum(data, POS_LIQUID_ASSETS)
                current_liabilities_sum = get_sum(data, POS_CURRENT_LIABILITIES)
                if current_liabilities_sum != 0:
                    result_entry['value'] = liquid_assets_sum / current_liabilities_sum
                    result_entry['status'] = 'ok'
                    result_entry['message'] = ''
                else:
                    result_entry['message'] = "Divisione per zero (Passività Correnti nulle)."

            elif kpi_key == 'cash_ratio':
                cash_sum = get_sum(data, POS_CASH)
                current_liabilities_sum = get_sum(data, POS_CURRENT_LIABILITIES)
                if current_liabilities_sum != 0:
                    result_entry['value'] = cash_sum / current_liabilities_sum
                    result_entry['status'] = 'ok'
                    result_entry['message'] = ''
                else:
                    result_entry['message'] = "Divisione per zero (Passività Correnti nulle)."

            elif kpi_key == 'debt_to_equity':
                total_liabilities_sum = get_sum(data, POS_TOTAL_LIABILITIES)
                total_equity_sum = get_sum(data, POS_TOTAL_EQUITY)
                if total_equity_sum != 0:
                    result_entry['value'] = total_liabilities_sum / total_equity_sum
                    result_entry['status'] = 'ok'
                    result_entry['message'] = ''
                else:
                    result_entry['message'] = "Divisione per zero (Patrimonio Netto nullo)."
            
            elif kpi_key == 'debt_to_equity_excl_tfr':
                total_liabilities_excl_tfr_sum = get_sum(data, POS_TOTAL_LIABILITIES_EXCL_TFR)
                total_equity_sum = get_sum(data, POS_TOTAL_EQUITY)
                if total_equity_sum != 0:
                    result_entry['value'] = total_liabilities_excl_tfr_sum / total_equity_sum
                    result_entry['status'] = 'ok'
                    result_entry['message'] = ''
                else:
                    result_entry['message'] = "Divisione per zero (Patrimonio Netto nullo)."

            elif kpi_key == 'debt_ratio':
                total_liabilities_sum = get_sum(data, POS_TOTAL_LIABILITIES)
                total_assets_sum = get_sum(data, POS_TOTAL_ASSETS)
                if total_assets_sum != 0:
                    result_entry['value'] = total_liabilities_sum / total_assets_sum
                    result_entry['status'] = 'ok'
                    result_entry['message'] = ''
                else:
                    result_entry['message'] = "Divisione per zero (Totale Attivo nullo)."

            elif kpi_key == 'working_capital':
                current_assets_sum = get_sum(data, POS_CURRENT_ASSETS)
                current_liabilities_sum = get_sum(data, POS_CURRENT_LIABILITIES)
                result_entry['value'] = current_assets_sum - current_liabilities_sum
                result_entry['status'] = 'ok'
                result_entry['message'] = ''
                
            # New KPIs (Italian Standard / CCII Inspired)
            elif kpi_key == 'asset_rigidity_index':
                immobilizzazioni_nette_sum = get_sum(data, POS_IMMOBILIZZAZIONI_NETTE)
                total_assets_sum = get_sum(data, POS_TOTAL_ASSETS)
                if total_assets_sum != 0:
                    result_entry['value'] = immobilizzazioni_nette_sum / total_assets_sum
                    result_entry['status'] = 'ok'
                    result_entry['message'] = ''
                else:
                    result_entry['message'] = "Divisione per zero (Totale Attivo nullo)."

            elif kpi_key == 'asset_elasticity_index':
                current_assets_sum = get_sum(data, POS_CURRENT_ASSETS)
                total_assets_sum = get_sum(data, POS_TOTAL_ASSETS)
                if total_assets_sum != 0:
                    result_entry['value'] = current_assets_sum / total_assets_sum
                    result_entry['status'] = 'ok'
                    result_entry['message'] = ''
                else:
                    result_entry['message'] = "Divisione per zero (Totale Attivo nullo)."

            elif kpi_key == 'fixed_asset_coverage_ratio':
                total_equity_sum = get_sum(data, POS_TOTAL_EQUITY)
                immobilizzazioni_nette_sum = get_sum(data, POS_IMMOBILIZZAZIONI_NETTE)
                if immobilizzazioni_nette_sum != 0:
                    result_entry['value'] = total_equity_sum / immobilizzazioni_nette_sum
                    result_entry['status'] = 'ok'
                    result_entry['message'] = ''
                else:
                    result_entry['message'] = "Divisione per zero (Immobilizzazioni Nette nulle)."

            elif kpi_key == 'tax_social_debt_on_assets_ratio':
                debiti_tributari_sum = get_sum(data, POS_DEBITI_TRIBUTARI)
                debiti_previdenziali_sum = get_sum(data, POS_DEBITI_PREVIDENZIALI)
                total_assets_sum = get_sum(data, POS_TOTAL_ASSETS)
                if total_assets_sum != 0:
                    result_entry['value'] = (debiti_tributari_sum + debiti_previdenziali_sum) / total_assets_sum
                    result_entry['status'] = 'ok'
                    result_entry['message'] = ''
                else:
                    result_entry['message'] = "Divisione per zero (Totale Attivo nullo)."

            elif kpi_key == 'tangible_net_worth':
                total_equity_sum = get_sum(data, POS_TOTAL_EQUITY)
                immobilizzazioni_immateriali_sum = get_sum(data, POS_IMMOBILIZZAZIONI_IMMATERIALI)
                result_entry['value'] = total_equity_sum - immobilizzazioni_immateriali_sum
                result_entry['status'] = 'ok'
                result_entry['message'] = ''
            
            elif kpi_key == 'equity_multiplier':
                total_assets_sum = get_sum(data, POS_TOTAL_ASSETS)
                total_equity_sum = get_sum(data, POS_TOTAL_EQUITY)
                if total_equity_sum != 0:
                    result_entry['value'] = total_assets_sum / total_equity_sum
                    result_entry['status'] = 'ok'
                    result_entry['message'] = ''
                else:
                    result_entry['message'] = "Divisione per zero (Patrimonio Netto nullo)."

            elif kpi_key == 'long_term_debt_to_equity':
                debiti_oltre_12_mesi_sum = get_sum(data, POS_DEBITI_OLTRE_12_MESI)
                total_equity_sum = get_sum(data, POS_TOTAL_EQUITY)
                if total_equity_sum != 0:
                    result_entry['value'] = debiti_oltre_12_mesi_sum / total_equity_sum
                    result_entry['status'] = 'ok'
                    result_entry['message'] = ''
                else:
                    result_entry['message'] = "Divisione per zero (Patrimonio Netto nullo)."

            elif kpi_key == 'intangible_assets_ratio':
                immobilizzazioni_immateriali_sum = get_sum(data, POS_IMMOBILIZZAZIONI_IMMATERIALI)
                total_assets_sum = get_sum(data, POS_TOTAL_ASSETS)
                if total_assets_sum != 0:
                    result_entry['value'] = immobilizzazioni_immateriali_sum / total_assets_sum
                    result_entry['status'] = 'ok'
                    result_entry['message'] = ''
                else:
                    result_entry['message'] = "Divisione per zero (Totale Attivo nullo)."

            elif kpi_key == 'financial_assets_ratio':
                immobilizzazioni_finanziarie_sum = get_sum(data, POS_IMMOBILIZZAZIONI_FINANZIARIE)
                attivita_finanziarie_correnti_sum = get_sum(data, POS_ATTIVITA_FINANZIARIE_CORRENTI)
                total_assets_sum = get_sum(data, POS_TOTAL_ASSETS)
                if total_assets_sum != 0:
                    result_entry['value'] = (immobilizzazioni_finanziarie_sum + attivita_finanziarie_correnti_sum) / total_assets_sum
                    result_entry['status'] = 'ok'
                    result_entry['message'] = ''
                else:
                    result_entry['message'] = "Divisione per zero (Totale Attivo nullo)."

            elif kpi_key == 'non_current_assets_coverage':
                total_equity = get_sum(data, POS_TOTAL_EQUITY)
                long_term_debt = get_sum(data, POS_DEBITI_OLTRE_12_MESI)
                net_fixed_assets = get_sum(data, POS_IMMOBILIZZAZIONI_NETTE)
                if net_fixed_assets != 0:
                    result_entry['value'] = (total_equity + long_term_debt) / net_fixed_assets
                    result_entry['status'] = 'ok'
                    result_entry['message'] = ''
                else:
                    result_entry['message'] = "Divisione per zero (Immobilizzazioni Nette nulle)."

            elif kpi_key == 'net_working_capital_ratio':
                current_assets = get_sum(data, POS_CURRENT_ASSETS)
                current_liabilities = get_sum(data, POS_CURRENT_LIABILITIES)
                total_assets = get_sum(data, POS_TOTAL_ASSETS)
                net_working_capital = current_assets - current_liabilities
                if total_assets != 0:
                    result_entry['value'] = net_working_capital / total_assets
                    result_entry['status'] = 'ok'
                    result_entry['message'] = ''
                else:
                    result_entry['message'] = "Divisione per zero (Totale Attivo nullo)."
            
            elif kpi_key == 'debt_ratio_excl_tfr':
                total_liabilities_excl_tfr_sum = get_sum(data, POS_TOTAL_LIABILITIES_EXCL_TFR)
                total_assets_sum = get_sum(data, POS_TOTAL_ASSETS)
                if total_assets_sum != 0:
                    result_entry['value'] = total_liabilities_excl_tfr_sum / total_assets_sum
                    result_entry['status'] = 'ok'
                    result_entry['message'] = ''
                else:
                    result_entry['message'] = "Divisione per zero (Totale Attivo nullo)."

            else: # Should not happen if kpi_key is in AVAILABLE_KPIS
                result_entry['message'] = "Logica di calcolo non implementata."

        except Exception as e:
            # General error catch for unexpected issues during calculation
            result_entry['status'] = 'error'
            result_entry['message'] = f"Errore di calcolo: {str(e)}" # Basic error message
        
        results[kpi_key] = result_entry
    return results

def get_sum(data_dict, position_keys):
    """Helper to sum values from data_dict for a list of position_keys."""
    total = 0
    for key in position_keys:
        total += data_dict.get(str(key), 0)  # Ensure keys are strings and default to 0 if not found
    return total

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