use std::collections::BTreeMap;
use serde::{Serialize, Deserialize};

pub fn calculate_selected_kpis(
    data: &BTreeMap<String, f64>,
    selected_kpi_keys: &[String],
) -> BTreeMap<String, KpiResult> {
    let mut results = BTreeMap::new();

    for kpi_key in selected_kpi_keys {
        let result = match kpi_key.as_str() {
            "current_ratio" => calculate_current_ratio(data),
            "quick_ratio" => calculate_quick_ratio(data),
            "cash_ratio" => calculate_cash_ratio(data),
            "debt_to_equity" => calculate_debt_to_equity(data),
            "debt_ratio" => calculate_debt_ratio(data),
            "working_capital" => calculate_working_capital(data),
            _ => KpiResult {
                value: None,
                status: "error".to_string(),
                message: "KPI non definito.".to_string(),
                details: None,
            },
        };
        results.insert(kpi_key.clone(), result);
    }

    results
}

fn get_sum(data: &BTreeMap<String, f64>, positions: &[&str]) -> f64 {
    positions.iter().map(|p| *data.get(*p).unwrap_or(&0.0)).sum()
}

fn calculate_current_ratio(data: &BTreeMap<String, f64>) -> KpiResult {
    let current_assets = get_sum(data, &["31", "32", "33", "34", "35", "39", "40", "41", "42", "43", "44", "45", "46", "47", "48", "49", "50"]);
    let current_liabilities = get_sum(data, &["79", "80", "81", "82", "83", "84", "85", "86", "87", "88"]);

    if current_liabilities != 0.0 {
        KpiResult {
            value: Some(current_assets / current_liabilities),
            status: "ok".to_string(),
            message: "".to_string(),
            details: None,
        }
    } else {
        KpiResult {
            value: None,
            status: "error".to_string(),
            message: "Divisione per zero (Passività Correnti nulle).".to_string(),
            details: None,
        }
    }
}

fn calculate_quick_ratio(data: &BTreeMap<String, f64>) -> KpiResult {
    let liquid_assets = get_sum(data, &["39", "40", "41", "42", "43", "45"]);
    let current_liabilities = get_sum(data, &["79", "80", "81", "82", "83", "84", "85", "86", "87", "88"]);

    if current_liabilities != 0.0 {
        KpiResult {
            value: Some(liquid_assets / current_liabilities),
            status: "ok".to_string(),
            message: "".to_string(),
            details: None,
        }
    } else {
        KpiResult {
            value: None,
            status: "error".to_string(),
            message: "Divisione per zero (Passività Correnti nulle).".to_string(),
            details: None,
        }
    }
}

fn calculate_cash_ratio(data: &BTreeMap<String, f64>) -> KpiResult {
    let cash = get_sum(data, &["49", "50"]);
    let current_liabilities = get_sum(data, &["79", "80", "81", "82", "83", "84", "85", "86", "87", "88"]);

    if current_liabilities != 0.0 {
        KpiResult {
            value: Some(cash / current_liabilities),
            status: "ok".to_string(),
            message: "".to_string(),
            details: None,
        }
    } else {
        KpiResult {
            value: None,
            status: "error".to_string(),
            message: "Divisione per zero (Passività Correnti nulle).".to_string(),
            details: None,
        }
    }
}

fn calculate_debt_to_equity(data: &BTreeMap<String, f64>) -> KpiResult {
    let total_liabilities = get_sum(data, &["67", "68", "69", "100", "70", "71", "72", "73", "74", "75", "76", "77", "78", "79", "80", "81", "82", "83", "84", "85", "86", "87", "88"]);
    let total_equity = get_sum(data, &["52", "53", "54", "55", "56", "57", "58", "59", "64", "65", "66"]);

    if total_equity != 0.0 {
        KpiResult {
            value: Some(total_liabilities / total_equity),
            status: "ok".to_string(),
            message: "".to_string(),
            details: None,
        }
    } else {
        KpiResult {
            value: None,
            status: "error".to_string(),
            message: "Divisione per zero (Patrimonio Netto nullo).".to_string(),
            details: None,
        }
    }
}

fn calculate_debt_ratio(data: &BTreeMap<String, f64>) -> KpiResult {
    let total_liabilities = get_sum(data, &["67", "68", "69", "100", "70", "71", "72", "73", "74", "75", "76", "77", "78", "79", "80", "81", "82", "83", "84", "85", "86", "87", "88"]);
    let total_assets = get_total_assets(data);

    if total_assets != 0.0 {
        KpiResult {
            value: Some(total_liabilities / total_assets),
            status: "ok".to_string(),
            message: "".to_string(),
            details: None,
        }
    } else {
        KpiResult {
            value: None,
            status: "error".to_string(),
            message: "Divisione per zero (Totale Attivo nullo).".to_string(),
            details: None,
        }
    }
}

fn calculate_working_capital(data: &BTreeMap<String, f64>) -> KpiResult {
    let current_assets = get_sum(data, &["31", "32", "33", "34", "35", "39", "40", "41", "42", "43", "44", "45", "46", "47", "48", "49", "50"]);
    let current_liabilities = get_sum(data, &["79", "80", "81", "82", "83", "84", "85", "86", "87", "88"]);

    KpiResult {
        value: Some(current_assets - current_liabilities),
        status: "ok".to_string(),
        message: "".to_string(),
        details: None,
    }
}

fn get_total_assets(data: &BTreeMap<String, f64>) -> f64 {
    let asset_positions: Vec<String> = (1..51).map(|x| x.to_string()).filter(|s| s != "51").collect();
    let asset_refs: Vec<&str> = asset_positions.iter().map(|s| s.as_str()).collect();
    get_sum(data, &asset_refs)
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct KpiResult {
    pub value: Option<f64>,
    pub status: String,
    pub message: String,
    pub details: Option<String>,
}
