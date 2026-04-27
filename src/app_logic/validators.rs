use std::collections::BTreeMap;

pub fn validate_financial_data(
    form_data: &BTreeMap<String, String>,
    required_positions: &[String],
) -> (BTreeMap<String, f64>, BTreeMap<String, String>) {
    let mut validated_data = BTreeMap::new();
    let mut errors = BTreeMap::new();

    for pos in required_positions {
        let pos_str = pos.as_str();
        let field_name = format!("pos_{}", pos_str);

        let zero = "0".to_string();
        let value_str = form_data.get(&field_name).unwrap_or(&zero);

        // Replace comma with dot (European numeric format)
        let value_str_clean = value_str.replace(',', ".");

        match value_str_clean.parse::<f64>() {
            Ok(value) => {
                validated_data.insert(pos_str.to_string(), value);
            }
            Err(_) => {
                validated_data.insert(pos_str.to_string(), 0.0);
                validated_data.insert(format!("raw_{}", pos_str), value_str.parse().unwrap_or(0.0));
                errors.insert(field_name, "Valore non valido. Inserire un numero (es. 1234,56)".to_string());
            }
        }
    }

    (validated_data, errors)
}

#[allow(dead_code)]
pub fn validate_kpi_selection(
    selected_kpi_keys: &[String],
    available_kpis: &BTreeMap<String, super::kpi_config::KpiDetails>,
) -> (bool, Option<String>) {
    if selected_kpi_keys.is_empty() {
        return (false, Some("Selezionare almeno un KPI.".to_string()));
    }

    let valid_kpis: Vec<&String> = selected_kpi_keys
        .iter()
        .filter(|k| available_kpis.contains_key(*k))
        .collect();

    if valid_kpis.is_empty() {
        return (false, Some("Nessun KPI valido selezionato.".to_string()));
    }

    (true, None)
}
