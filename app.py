from flask import Flask, render_template, request, session, redirect, url_for, flash
import os
from datetime import datetime, UTC
import json
import collections # Import collections for defaultdict
from flask_session import Session  # Import Flask-Session

# Import from our modules
from app_logic.constants import (
    BALANCE_SHEET_STRUCTURE, 
    ALL_POSITIONS, 
    KPI_REQUIREMENTS, 
    AVAILABLE_KPIS,
    POSITION_NAMES, 
    SECTION_TITLES, 
    CEE_TO_AUTOMOTIVE_CODES, 
    AVAILABLE_MAPPINGS,
    get_all_positions
)
from app_logic.calculator import calculate_selected_kpis, validate_balance_sheet
from app_logic.validators import validate_financial_data, validate_kpi_selection

app = Flask(__name__)
# Secret key for session management. Replace with a strong, random key in production.
app.secret_key = os.environ.get('SECRET_KEY', os.urandom(24))

# Configure server-side session
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'flask_session')
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
Session(app)

# Context Processor to make datetime available in templates
@app.context_processor
def inject_now():
    return {'now': datetime.now(UTC)}  # Use timezone-aware UTC time instead of utcnow

@app.context_processor
def inject_globals():
    """Inject global variables into templates."""
    return {'app_version': "0.3.4 Beta"} # Inject app version

@app.after_request
def add_security_headers(response):
    """Add basic security headers to all responses."""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    return response

@app.route('/', methods=['GET'])
def index():
    """Displays the KPI selection page."""
    session.pop('balance_sheet_data', None)
    session.pop('required_positions', None)
    session.pop('selected_kpis', None)
    session.pop('calculated_kpis', None)

    # Group KPIs by category
    grouped_kpis = collections.defaultdict(dict)
    for key, kpi_details in AVAILABLE_KPIS.items():
        category = kpi_details.get('category_display', 'Altro') # Default category if not specified
        grouped_kpis[category][key] = kpi_details
    
    # Sort categories if desired (e.g., by a predefined order or alphabetically)
    # For now, using the order they appear based on AVAILABLE_KPIS iteration and defaultdict behavior.
    # If a specific order is needed, we can define an order list and sort by it.
    # Example: desired_order = ["Indici di Liquidità", "Capitale Circolante", ...]
    # sorted_grouped_kpis = {cat: grouped_kpis[cat] for cat in desired_order if cat in grouped_kpis}
    # # Add any categories not in desired_order at the end
    # for cat in grouped_kpis:
    #     if cat not in sorted_grouped_kpis:
    #         sorted_grouped_kpis[cat] = grouped_kpis[cat]

    return render_template('select_kpi.html', grouped_kpis=grouped_kpis)

@app.route('/input', methods=['GET', 'POST'])
def input_required_fields():
    # Define sort_key_func at a scope accessible throughout the function
    def sort_key_func(item_key):
        parts = item_key.split('.')
        if len(parts) == 1 and parts[0].isdigit():
            return (int(parts[0]), '')
        elif len(parts) == 2 and parts[0].isdigit() and parts[1] == 'NCA':
            return (int(parts[0]), parts[1])
        return (float('inf'), item_key) # Fallback for non-standard keys, sorts them last

    if request.method == 'POST':
        selected_kpi_keys = request.form.getlist('kpi_keys')
        valid, error_message = validate_kpi_selection(selected_kpi_keys, AVAILABLE_KPIS)
        if not valid:
            flash(error_message, "warning")
            return redirect(url_for('index'))

        required_positions_set = set()
        for key in selected_kpi_keys:
            if key in KPI_REQUIREMENTS:
                required_positions_set.update(KPI_REQUIREMENTS[key])
        
        sorted_required_positions = sorted(list(required_positions_set), key=sort_key_func)
        
        session['required_positions'] = sorted_required_positions
        session['selected_kpis'] = selected_kpi_keys
        
        # Clear any previous raw input data
        if 'raw_input_data' in session:
            session.pop('raw_input_data', None)
            
        existing_data = session.get('balance_sheet_data', {})
        current_balance_sheet_data = {str(pos): existing_data.get(str(pos), 0.0) for pos in sorted_required_positions}
        session['balance_sheet_data'] = current_balance_sheet_data
        
        return redirect(url_for('input_required_fields'))

    elif request.method == 'GET':
        if 'selected_kpis' not in session or 'required_positions' not in session:
            flash("Sessione non valida o scaduta. Seleziona nuovamente i KPI.", "warning")
            return redirect(url_for('index'))
        
        if 'balance_sheet_data' not in session:
             session['balance_sheet_data'] = {str(pos): 0.0 for pos in session.get('required_positions', [])}
        elif 'raw_input_data' in session:
            # If we have raw_input_data, merge it with balance_sheet_data to preserve user input
            # even for invalid values
            raw_data = session.get('raw_input_data', {})
            for pos in session['required_positions']:
                pos_str = str(pos)
                field_name = f'pos_{pos}'
                if field_name in raw_data:
                    # Try to use the original raw string values for form fields
                    try:
                        # Try to convert to float for the internal representation
                        value_str = raw_data[field_name].replace(',', '.')
                        session['balance_sheet_data'][pos_str] = float(value_str)
                    except ValueError:
                        # If not a valid float, keep the raw value anyway for display purposes
                        session['balance_sheet_data'][f"raw_{pos_str}"] = raw_data[field_name]
            # Clear raw_input_data after using it
            session.pop('raw_input_data', None)

    selected_kpi_keys = session.get('selected_kpis', [])
    sorted_required_positions = session.get('required_positions', [])
    current_data = session.get('balance_sheet_data', {})

    if not selected_kpi_keys or not sorted_required_positions:
        flash("Errore di sessione. Si prega di ricominciare.", "danger")
        return redirect(url_for('index'))

    selected_kpi_details = {key: AVAILABLE_KPIS[key] for key in selected_kpi_keys if key in AVAILABLE_KPIS}

    required_structure = collections.defaultdict(lambda: collections.defaultdict(dict))
    # temp_structure_for_ordering was removed as it's not essential for this restored logic.

    for main_cat_key, main_cat_value in BALANCE_SHEET_STRUCTURE.items():
        for sub_cat_key, sub_cat_value in main_cat_value.items():
            if isinstance(sub_cat_value, dict): # e.g., 'non_current_assets', 'current_assets', 'equity', 'liabilities'
                for item_group_key, item_group_value in sub_cat_value.items(): 
                    if isinstance(item_group_value, dict): # Special case for 'trade_and_other_receivables'
                        # Initialize dict for this group if it's not already there
                        if item_group_key not in required_structure[main_cat_key][sub_cat_key]:
                            required_structure[main_cat_key][sub_cat_key][item_group_key] = {}
                        for specific_receivable_key, specific_receivable_list in item_group_value.items():
                            relevant_positions = [p for p in specific_receivable_list if p in sorted_required_positions]
                            if relevant_positions:
                                required_structure[main_cat_key][sub_cat_key][item_group_key][specific_receivable_key] = relevant_positions
                    elif isinstance(item_group_value, list): # Standard case like 'inventories'
                        relevant_positions = [p for p in item_group_value if p in sorted_required_positions]
                        if relevant_positions:
                            # Ensure the order from sorted_required_positions is maintained for the displayed list
                            ordered_relevant_positions = [p for p in sorted_required_positions if p in relevant_positions]
                            required_structure[main_cat_key][sub_cat_key][item_group_key] = ordered_relevant_positions
            elif isinstance(sub_cat_value, list): # Top-level lists like 'due_from_shareholders'
                relevant_positions = [p for p in sub_cat_value if p in sorted_required_positions]
                if relevant_positions:
                    ordered_relevant_positions = [p for p in sorted_required_positions if p in relevant_positions]
                    required_structure[main_cat_key][sub_cat_key] = ordered_relevant_positions
    
    final_required_structure = json.loads(json.dumps(required_structure))

    all_mapping_data = {
        "automotive_dealer": CEE_TO_AUTOMOTIVE_CODES
    }

    return render_template('input.html',
                           structure=final_required_structure, 
                           data=current_data, 
                           position_names=POSITION_NAMES,
                           selected_kpi_details=selected_kpi_details, 
                           section_titles=SECTION_TITLES,
                           available_mappings=AVAILABLE_MAPPINGS, 
                           all_mapping_data_json=json.dumps(all_mapping_data),
                           errors=session.get('validation_errors', {})
                           )

@app.route('/calculate', methods=['POST'])
def calculate():
    if 'required_positions' not in session or 'selected_kpis' not in session:
         flash("Sessione scaduta o invalida. Si prega di ricominciare.", "danger")
         return redirect(url_for('index'))

    required_positions = session['required_positions']
    selected_kpi_keys = session['selected_kpis']

    try:
        # Store the raw form data first to preserve it in case of validation errors
        raw_form_data = {}
        for pos in required_positions:
            field_name = f'pos_{pos}'
            if field_name in request.form:
                raw_form_data[field_name] = request.form[field_name]
        
        session['raw_input_data'] = raw_form_data
        
        balance_sheet_data, errors = validate_financial_data(request.form, required_positions)
        if errors:
            # We no longer need flash messages for each error as they're displayed inline
            # Save what data was valid to preserve user input
            session['balance_sheet_data'] = {k: v for k, v in balance_sheet_data.items()}
            # Store validation errors in session to highlight fields
            session['validation_errors'] = errors
            return redirect(url_for('input_required_fields'))
        # Clear any validation errors if successful
        if 'validation_errors' in session:
            session.pop('validation_errors', None)
        session['balance_sheet_data'] = balance_sheet_data
        
    except Exception as e:
        flash(f'Errore durante l\'elaborazione dei dati: {e}', 'danger')
        return redirect(url_for('input_required_fields'))

    balance_check = validate_balance_sheet(balance_sheet_data)
    kpis_results = calculate_selected_kpis(balance_sheet_data, selected_kpi_keys)
    session['calculated_kpis'] = kpis_results

    input_data_by_kpi_display = {}
    for kpi_key in selected_kpi_keys:
        input_data_by_kpi_display[kpi_key] = {}
        if kpi_key in KPI_REQUIREMENTS:
            for pos in KPI_REQUIREMENTS[kpi_key]:
                pos_str = str(pos)
                if pos_str in balance_sheet_data:
                    input_data_by_kpi_display[kpi_key][pos_str] = balance_sheet_data[pos_str]
                else:
                    input_data_by_kpi_display[kpi_key][pos_str] = None

    # Prepare details for each KPI's inputs
    kpi_input_details = {}
    for kpi_key in selected_kpi_keys:
        kpi_input_details[kpi_key] = []
        required_positions = KPI_REQUIREMENTS.get(kpi_key, [])
        
        # Create a flat list of all unique positions required by any selected KPI for display
        # This is for the "Dati Inseriti per KPI" section which is separate from individual KPI cards now
        
        for pos in sorted(required_positions, key=lambda x: str(x)):
            pos_str = str(pos)
            value = balance_sheet_data.get(pos_str, 0.0)
            name = POSITION_NAMES.get(pos_str, POSITION_NAMES.get(pos, f"Position {pos}"))
            kpi_input_details[kpi_key].append({
                'position': pos_str,
                'name_display': name,
                'value': value
            })
    
    # Consolidate all unique input data across all calculated KPIs for the "Dati Inseriti" card

    return render_template(
        "results.html",
        results=kpis_results, 
        input_data=balance_sheet_data, 
        balance_check=balance_check, 
        input_data_by_kpi=input_data_by_kpi_display, 
        available_kpis=AVAILABLE_KPIS, 
        position_names=POSITION_NAMES, 
        selected_kpi_keys=selected_kpi_keys, 
        section_titles=SECTION_TITLES,
        kpi_input_details=kpi_input_details
    )

if __name__ == '__main__':
    import webbrowser
    # Try to open the browser only when running as the main script (and thus likely as an executable)
    # This avoids opening the browser during Flask's auto-reloader development cycles.
    if not os.environ.get("WERKZEUG_RUN_MAIN"): # WERKZEUG_RUN_MAIN is set by Flask reloader
        try:
            webbrowser.open_new_tab('http://127.0.0.1:5001')
        except Exception as e:
            print(f"Could not open browser: {e}") # Or log this appropriately
    app.run(debug=False, use_reloader=False, host='0.0.0.0', port=5001) 