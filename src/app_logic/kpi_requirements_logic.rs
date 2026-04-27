use std::collections::BTreeMap;

#[allow(dead_code)]
pub fn get_kpi_requirements() -> BTreeMap<String, Vec<String>> {
    let mut requirements = BTreeMap::new();
    
    // Current Ratio
    requirements.insert("current_ratio".to_string(), 
        vec!["31", "32", "33", "34", "35", "39", "40", "41", "42", "43", "44", "45", "46", "47", "48", "49", "50",
             "79", "80", "81", "82", "83", "84", "85", "86", "87", "88"]
            .iter().map(|s| s.to_string()).collect());
    
    // Quick Ratio  
    requirements.insert("quick_ratio".to_string(),
        vec!["39", "40", "41", "42", "43", "45", "46", "47", "48",
             "79", "80", "81", "82", "83", "84", "85", "86", "87", "88"]
            .iter().map(|s| s.to_string()).collect());
            
    // Cash Ratio
    requirements.insert("cash_ratio".to_string(),
        vec!["49", "50", "79", "80", "81", "82", "83", "84", "85", "86", "87", "88"]
            .iter().map(|s| s.to_string()).collect());
            
    // Debt to Equity
    requirements.insert("debt_to_equity".to_string(),
        vec!["67", "68", "69", "100", "70", "71", "72", "73", "74", "75", "76", "77", "78", "79", "80", "81", "82", "83", "84", "85", "86", "87", "88",
             "52", "53", "54", "55", "56", "57", "58", "59", "64", "65", "66"]
            .iter().map(|s| s.to_string()).collect());
    
    // Debt Ratio
    requirements.insert("debt_ratio".to_string(),
        vec!["67", "68", "69", "100", "70", "71", "72", "73", "74", "75", "76", "77", "78", "79", "80", "81", "82", "83", "84", "85", "86", "87", "88",
             "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30",
             "31", "32", "33", "34", "35", "36", "37", "38", "39", "40", "41", "42", "43", "44", "45", "46", "47", "48", "49", "50"]
            .iter().map(|s| s.to_string()).collect());
    
    // Working Capital
    requirements.insert("working_capital".to_string(),
        vec!["31", "32", "33", "34", "35", "39", "40", "41", "42", "43", "44", "45", "46", "47", "48", "49", "50",
             "79", "80", "81", "82", "83", "84", "85", "86", "87", "88"]
            .iter().map(|s| s.to_string()).collect());
    
    // Asset Rigidity Index
    requirements.insert("asset_rigidity_index".to_string(),
        vec!["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30",
             "31", "32", "33", "34", "35", "36", "37", "38", "39", "40", "41", "42", "43", "44", "45", "46", "47", "48", "49", "50"]
            .iter().map(|s| s.to_string()).collect());
    
    // Asset Elasticity Index
    requirements.insert("asset_elasticity_index".to_string(),
        vec!["31", "32", "33", "34", "35", "39", "40", "41", "42", "43", "44", "45", "46", "47", "48", "49", "50",
             "31", "32", "33", "34", "35", "36", "37", "38", "39", "40", "41", "42", "43", "44", "45", "46", "47", "48", "49", "50"]
            .iter().map(|s| s.to_string()).collect());
    
    // Fixed Asset Coverage Ratio
    requirements.insert("fixed_asset_coverage_ratio".to_string(),
        vec!["52", "53", "54", "55", "56", "57", "58", "59", "64", "65", "66",
             "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30"]
            .iter().map(|s| s.to_string()).collect());
    
    // Tax/Social Debt on Assets Ratio
    requirements.insert("tax_social_debt_on_assets_ratio".to_string(),
        vec!["85", "86",
             "31", "32", "33", "34", "35", "36", "37", "38", "39", "40", "41", "42", "43", "44", "45", "46", "47", "48", "49", "50"]
            .iter().map(|s| s.to_string()).collect());
    
    // Tangible Net Worth
    requirements.insert("tangible_net_worth".to_string(),
        vec!["52", "53", "54", "55", "56", "57", "58", "59", "64", "65", "66",
             "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
            .iter().map(|s| s.to_string()).collect());
    
    // Equity Multiplier
    requirements.insert("equity_multiplier".to_string(),
        vec!["31", "32", "33", "34", "35", "36", "37", "38", "39", "40", "41", "42", "43", "44", "45", "46", "47", "48", "49", "50",
             "52", "53", "54", "55", "56", "57", "58", "59", "64", "65", "66"]
            .iter().map(|s| s.to_string()).collect());
    
    // Long-term Debt to Equity
    requirements.insert("long_term_debt_to_equity".to_string(),
        vec!["70", "71", "72", "73", "74", "75", "76", "77", "78",
             "52", "53", "54", "55", "56", "57", "58", "59", "64", "65", "66"]
            .iter().map(|s| s.to_string()).collect());
    
    // Intangible Assets Ratio
    requirements.insert("intangible_assets_ratio".to_string(),
        vec!["1", "2", "3", "4", "5", "6", "7", "8", "9", "10",
             "31", "32", "33", "34", "35", "36", "37", "38", "39", "40", "41", "42", "43", "44", "45", "46", "47", "48", "49", "50"]
            .iter().map(|s| s.to_string()).collect());
    
    // Financial Assets Ratio
    requirements.insert("financial_assets_ratio".to_string(),
        vec!["46", "47", "48",
             "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30",
             "31", "32", "33", "34", "35", "36", "37", "38", "39", "40", "41", "42", "43", "44", "45", "46", "47", "48", "49", "50"]
            .iter().map(|s| s.to_string()).collect());
    
    // Non-current Assets Coverage
    requirements.insert("non_current_assets_coverage".to_string(),
        vec!["52", "53", "54", "55", "56", "57", "58", "59", "64", "65", "66",
             "70", "71", "72", "73", "74", "75", "76", "77", "78",
             "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30"]
            .iter().map(|s| s.to_string()).collect());
    
    // Net Working Capital Ratio
    requirements.insert("net_working_capital_ratio".to_string(),
        vec!["31", "32", "33", "34", "35", "39", "40", "41", "42", "43", "44", "45", "46", "47", "48", "49", "50",
             "79", "80", "81", "82", "83", "84", "85", "86", "87", "88",
             "31", "32", "33", "34", "35", "36", "37", "38", "39", "40", "41", "42", "43", "44", "45", "46", "47", "48", "49", "50"]
            .iter().map(|s| s.to_string()).collect());
    
    // Debt to Equity Excl TFR
    requirements.insert("debt_to_equity_excl_tfr".to_string(),
        vec!["67", "68", "69", "70", "71", "72", "73", "74", "75", "76", "77", "78", "79", "80", "81", "82", "83", "84", "85", "86", "87", "88",
             "52", "53", "54", "55", "56", "57", "58", "59", "64", "65", "66"]
            .iter().map(|s| s.to_string()).collect());
    
    // Debt Ratio Excl TFR
    requirements.insert("debt_ratio_excl_tfr".to_string(),
        vec!["67", "68", "69", "70", "71", "72", "73", "74", "75", "76", "77", "78", "79", "80", "81", "82", "83", "84", "85", "86", "87", "88",
             "31", "32", "33", "34", "35", "36", "37", "38", "39", "40", "41", "42", "43", "44", "45", "46", "47", "48", "49", "50"]
            .iter().map(|s| s.to_string()).collect());
    
    requirements
}

#[allow(dead_code)]
pub fn get_pos_current_assets() -> Vec<String> {
    (31..51).map(|x| x.to_string()).collect()
}

#[allow(dead_code)]
pub fn get_pos_liquid_assets() -> Vec<String> {
    vec!["39", "40", "41", "42", "43", "45", "46", "47", "48"]
        .iter().map(|s| s.to_string()).collect()
}

#[allow(dead_code)]
pub fn get_pos_cash() -> Vec<String> {
    vec!["49", "50"].iter().map(|s| s.to_string()).collect()
}

#[allow(dead_code)]
pub fn get_pos_current_liabilities() -> Vec<String> {
    vec!["79", "80", "81", "82", "83", "84", "85", "86", "87", "88"]
        .iter().map(|s| s.to_string()).collect()
}

#[allow(dead_code)]
pub fn get_pos_total_liabilities() -> Vec<String> {
    vec!["67", "68", "69", "100", "70", "71", "72", "73", "74", "75", "76", "77", "78", 
         "79", "80", "81", "82", "83", "84", "85", "86", "87", "88"]
        .iter().map(|s| s.to_string()).collect()
}

#[allow(dead_code)]
pub fn get_pos_total_equity() -> Vec<String> {
    vec!["52", "53", "54", "55", "56", "57", "58", "59", "64", "65", "66"]
        .iter().map(|s| s.to_string()).collect()
}
