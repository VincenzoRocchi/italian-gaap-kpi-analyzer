use std::collections::BTreeMap;

use crate::app_logic::{
    balance_sheet_config::get_position_names,
    kpi_config::get_available_kpis,
};

pub struct AppState {
    pub balance_sheet_structure: BTreeMap<String, String>, // Simplified for now
    pub position_names: BTreeMap<String, String>,
    pub available_kpis: BTreeMap<String, crate::app_logic::kpi_config::KpiDetails>,
}

impl AppState {
    pub fn new() -> Self {
        AppState {
            balance_sheet_structure: BTreeMap::new(),
            position_names: get_position_names(),
            available_kpis: get_available_kpis(),
        }
    }
}
