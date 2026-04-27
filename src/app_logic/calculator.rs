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
            "asset_rigidity_index" => calculate_asset_rigidity_index(data),
            "asset_elasticity_index" => calculate_asset_elasticity_index(data),
            "fixed_asset_coverage_ratio" => calculate_fixed_asset_coverage_ratio(data),
            "tax_social_debt_on_assets_ratio" => calculate_tax_social_debt_on_assets_ratio(data),
            "tangible_net_worth" => calculate_tangible_net_worth(data),
            "equity_multiplier" => calculate_equity_multiplier(data),
            "long_term_debt_to_equity" => calculate_long_term_debt_to_equity(data),
            "intangible_assets_ratio" => calculate_intangible_assets_ratio(data),
            "financial_assets_ratio" => calculate_financial_assets_ratio(data),
            "non_current_assets_coverage" => calculate_non_current_assets_coverage(data),
            "net_working_capital_ratio" => calculate_net_working_capital_ratio(data),
            "debt_to_equity_excl_tfr" => calculate_debt_to_equity_excl_tfr(data),
            "debt_ratio_excl_tfr" => calculate_debt_ratio_excl_tfr(data),
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

// Asset Rigidity Index: Non-current assets / Total assets
fn calculate_asset_rigidity_index(data: &BTreeMap<String, f64>) -> KpiResult {
    let total_assets = get_total_assets(data);
    
    if total_assets != 0.0 {
        let non_current_value = get_sum(data, &["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30"]);
        KpiResult {
            value: Some(non_current_value / total_assets),
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

// Asset Elasticity Index: Current assets / Total assets
fn calculate_asset_elasticity_index(data: &BTreeMap<String, f64>) -> KpiResult {
    let total_assets = get_total_assets(data);
    
    if total_assets != 0.0 {
        let current_value = get_sum(data, &["31", "32", "33", "34", "35", "39", "40", "41", "42", "43", "44", "45", "46", "47", "48", "49", "50"]);
        KpiResult {
            value: Some(current_value / total_assets),
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

// Fixed Asset Coverage Ratio: Equity / Non-current assets
fn calculate_fixed_asset_coverage_ratio(data: &BTreeMap<String, f64>) -> KpiResult {
    let equity = get_sum(data, &["52", "53", "54", "55", "56", "57", "58", "59", "64", "65", "66"]);
    
    if equity != 0.0 {
        let non_current_value = get_sum(data, &["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30"]);
        KpiResult {
            value: Some(equity / non_current_value),
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

// Tax/Social Debt on Assets Ratio: (TFR + Social Security) / Total Assets
fn calculate_tax_social_debt_on_assets_ratio(data: &BTreeMap<String, f64>) -> KpiResult {
    let tfr_and_social = get_sum(data, &["100", "86"]);
    let total_assets = get_total_assets(data);

    if total_assets != 0.0 {
        KpiResult {
            value: Some(tfr_and_social / total_assets),
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

// Tangible Net Worth: Equity - Intangible Assets
fn calculate_tangible_net_worth(data: &BTreeMap<String, f64>) -> KpiResult {
    let equity = get_sum(data, &["52", "53", "54", "55", "56", "57", "58", "59", "64", "65", "66"]);
    let intangible_value = get_sum(data, &["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]);
    
    KpiResult {
        value: Some(equity - intangible_value),
        status: "ok".to_string(),
        message: "".to_string(),
        details: None,
    }
}

// Equity Multiplier: Total Assets / Equity
fn calculate_equity_multiplier(data: &BTreeMap<String, f64>) -> KpiResult {
    let total_assets = get_total_assets(data);
    let equity = get_sum(data, &["52", "53", "54", "55", "56", "57", "58", "59", "64", "65", "66"]);

    if equity != 0.0 {
        KpiResult {
            value: Some(total_assets / equity),
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

// Long-term Debt to Equity: Long-term debt / Equity
fn calculate_long_term_debt_to_equity(data: &BTreeMap<String, f64>) -> KpiResult {
    let long_term_debt = get_sum(data, &["70", "71", "72", "73", "74", "75", "76", "77", "78"]);
    let equity = get_sum(data, &["52", "53", "54", "55", "56", "57", "58", "59", "64", "65", "66"]);

    if equity != 0.0 {
        KpiResult {
            value: Some(long_term_debt / equity),
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

// Intangible Assets Ratio: Intangible Assets / Total Assets
fn calculate_intangible_assets_ratio(data: &BTreeMap<String, f64>) -> KpiResult {
    let intangible_value = get_sum(data, &["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]);
    let total_assets = get_total_assets(data);
    
    if total_assets != 0.0 {
        KpiResult {
            value: Some(intangible_value / total_assets),
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

// Financial Assets Ratio: Current financial assets / Total Assets
fn calculate_financial_assets_ratio(data: &BTreeMap<String, f64>) -> KpiResult {
    let financial = get_sum(data, &["46", "47", "48"]);
    let total_assets = get_total_assets(data);

    if total_assets != 0.0 {
        KpiResult {
            value: Some(financial / total_assets),
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

// Non-current Assets Coverage: Equity / Non-current assets (including long-term debt)
fn calculate_non_current_assets_coverage(data: &BTreeMap<String, f64>) -> KpiResult {
    let non_current_value = get_sum(data, &["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30"]);
    let equity = get_sum(data, &["52", "53", "54", "55", "56", "57", "58", "59", "64", "65", "66"]);
    
    if non_current_value != 0.0 {
        KpiResult {
            value: Some(equity / non_current_value),
            status: "ok".to_string(),
            message: "".to_string(),
            details: None,
        }
    } else {
        KpiResult {
            value: None,
            status: "error".to_string(),
            message: "Divisione per zero (Attività non correnti nulle).".to_string(),
            details: None,
        }
    }
}

// Net Working Capital Ratio: Working Capital / Total Assets
fn calculate_net_working_capital_ratio(data: &BTreeMap<String, f64>) -> KpiResult {
    let current_assets = get_sum(data, &["31", "32", "33", "34", "35", "39", "40", "41", "42", "43", "44", "45", "46", "47", "48", "49", "50"]);
    let current_liabilities = get_sum(data, &["79", "80", "81", "82", "83", "84", "85", "86", "87", "88"]);
    let working_capital = current_assets - current_liabilities;
    let total_assets = get_total_assets(data);

    if total_assets != 0.0 {
        KpiResult {
            value: Some(working_capital / total_assets),
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

// Debt to Equity Excluding TFR: (Total Liabilities - TFR) / Equity
fn calculate_debt_to_equity_excl_tfr(data: &BTreeMap<String, f64>) -> KpiResult {
    let total_liabilities = get_sum(data, &["67", "68", "69", "100", "70", "71", "72", "73", "74", "75", "76", "77", "78", "79", "80", "81", "82", "83", "84", "85", "86", "87", "88"]);
    let tfr = get_sum(data, &["100"]);
    let equity = get_sum(data, &["52", "53", "54", "55", "56", "57", "58", "59", "64", "65", "66"]);

    if equity != 0.0 {
        KpiResult {
            value: Some((total_liabilities - tfr) / equity),
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

// Debt Ratio Excluding TFR: (Total Liabilities - TFR) / Total Assets
fn calculate_debt_ratio_excl_tfr(data: &BTreeMap<String, f64>) -> KpiResult {
    let total_liabilities = get_sum(data, &["67", "68", "69", "100", "70", "71", "72", "73", "74", "75", "76", "77", "78", "79", "80", "81", "82", "83", "84", "85", "86", "87", "88"]);
    let tfr = get_sum(data, &["100"]);
    let total_assets = get_total_assets(data);

    if total_assets != 0.0 {
        KpiResult {
            value: Some((total_liabilities - tfr) / total_assets),
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
