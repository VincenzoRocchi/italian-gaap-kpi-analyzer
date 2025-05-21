def validate_financial_data(form_data, required_positions):
    """
    Validates and processes financial data from form input.
    
    Args:
        form_data (dict): Form data submitted by the user
        required_positions (list): List of position numbers that need to be validated
        
    Returns:
        tuple: (validated_data, errors) where validated_data is a dict of validated values
               and errors is a dict of error messages keyed by field name
    """
    validated_data = {}
    errors = {}
    
    for pos in required_positions:
        pos_str = str(pos)
        field_name = f'pos_{pos}'
        
        # Get value, handling potential missing fields
        value_str = form_data.get(field_name, '0')
        
        # Replace comma with dot (for European numeric format)
        value_str = value_str.replace(',', '.')
        
        try:
            # Convert to float and validate
            value = float(value_str)
            
            # Optional: Add additional validation rules here
            # For example, check if the value is within a reasonable range
            # if abs(value) > 1_000_000_000_000:  # Trillion check
            #     errors[field_name] = "Value is unrealistically large"
            
            validated_data[pos_str] = value
        except ValueError:
            # Default to 0.0 if conversion fails
            validated_data[pos_str] = 0.0
            # Store the original input value for preservation
            validated_data[f"raw_{pos_str}"] = form_data.get(field_name, '0')
            errors[field_name] = f"Valore non valido. Inserire un numero (es. 1234,56)"
    
    return validated_data, errors

def validate_kpi_selection(selected_kpi_keys, available_kpis):
    """
    Validates that at least one valid KPI is selected.
    
    Args:
        selected_kpi_keys (list): List of KPI keys selected by the user
        available_kpis (dict): Dictionary of available KPIs
    
    Returns:
        tuple: (valid, error_message) where valid is a boolean and error_message is a string
    """
    if not selected_kpi_keys:
        return False, "Selezionare almeno un KPI."
    
    # Check if all selected KPIs are valid
    valid_kpis = [key for key in selected_kpi_keys if key in available_kpis]
    
    if not valid_kpis:
        return False, "Nessun KPI valido selezionato."
    
    return True, None 