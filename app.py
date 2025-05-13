from flask import Flask, render_template, request, session, redirect, url_for, flash
import os
from datetime import datetime
import json
import collections # Import collections for defaultdict

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

# Context Processor to make datetime available in templates
@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()} # Use utcnow for consistency

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
    if request.method == 'POST':
        selected_kpi_keys = request.form.getlist('kpi_keys')
        valid, error_message = validate_kpi_selection(selected_kpi_keys, AVAILABLE_KPIS)
        if not valid:
            flash(error_message, "warning")
            return redirect(url_for('index'))

        required_positions = set()
        for key in selected_kpi_keys:
            if key in KPI_REQUIREMENTS:
                required_positions.update(KPI_REQUIREMENTS[key])

        sorted_required_positions = sorted(list(required_positions))
        session['required_positions'] = sorted_required_positions
        session['selected_kpis'] = selected_kpi_keys
        existing_data = session.get('balance_sheet_data', {})
        session['balance_sheet_data'] = {str(pos): existing_data.get(str(pos), 0.0) for pos in sorted_required_positions}

    elif request.method == 'GET':
        if 'selected_kpis' not in session or 'required_positions' not in session:
            flash("Sessione non valida o scaduta. Seleziona nuovamente i KPI.", "warning")
            return redirect(url_for('index'))
        if 'balance_sheet_data' not in session:
             session['balance_sheet_data'] = {str(pos): 0.0 for pos in session.get('required_positions', [])}
        flash("Modifica i valori inseriti e ricalcola.", "info")

    else: 
        return redirect(url_for('index'))

    selected_kpi_keys = session.get('selected_kpis', [])
    sorted_required_positions = session.get('required_positions', [])
    current_data = session.get('balance_sheet_data', {})

    if not selected_kpi_keys or not sorted_required_positions:
        flash("Errore di sessione. Si prega di ricominciare.", "danger")
        return redirect(url_for('index'))

    selected_kpi_details = {key: AVAILABLE_KPIS[key] for key in selected_kpi_keys if key in AVAILABLE_KPIS}

    required_structure = {}
    for main_cat, sub_cats in BALANCE_SHEET_STRUCTURE.items():
        req_main_cat = {}
        for sub_cat_name, content in sub_cats.items():
            if isinstance(content, dict):
                req_sub_cat = {}
                for nested_name, nested_positions in content.items():
                    req_nested_pos = [p for p in nested_positions if p in sorted_required_positions]
                    if req_nested_pos:
                        req_sub_cat[nested_name] = req_nested_pos
                if req_sub_cat:
                     req_main_cat[sub_cat_name] = req_sub_cat
            elif isinstance(content, list):
                req_pos = [p for p in content if p in sorted_required_positions]
                if req_pos:
                    req_main_cat[sub_cat_name] = req_pos
        if req_main_cat:
            required_structure[main_cat] = req_main_cat

    all_mapping_data = {
        "automotive_dealer": CEE_TO_AUTOMOTIVE_CODES
    }

    return render_template('input.html',
                           structure=required_structure, 
                           data=current_data, 
                           required_positions=sorted_required_positions,
                           position_names=POSITION_NAMES,
                           selected_kpi_details=selected_kpi_details, 
                           section_titles=SECTION_TITLES,
                           available_mappings=AVAILABLE_MAPPINGS, 
                           all_mapping_data_json=json.dumps(all_mapping_data)
                           )

@app.route('/calculate', methods=['POST'])
def calculate():
    if 'required_positions' not in session or 'selected_kpis' not in session:
         flash("Sessione scaduta o invalida. Si prega di ricominciare.", "danger")
         return redirect(url_for('index'))

    required_positions = session['required_positions']
    selected_kpi_keys = session['selected_kpis']

    try:
        balance_sheet_data, errors = validate_financial_data(request.form, required_positions)
        if errors:
            for field_name, error_message in errors.items():
                flash(f"{error_message}", "warning")
            return redirect(url_for('input_required_fields'))
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

    return render_template(
        "results.html",
        results=kpis_results, 
        input_data=balance_sheet_data, 
        balance_check=balance_check, 
        input_data_by_kpi=input_data_by_kpi_display, 
        available_kpis=AVAILABLE_KPIS, 
        position_names=POSITION_NAMES, 
        selected_kpi_keys=selected_kpi_keys, 
        section_titles=SECTION_TITLES
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