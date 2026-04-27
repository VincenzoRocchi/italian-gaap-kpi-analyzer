use std::collections::BTreeMap;

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
    
    requirements
}

pub fn get_pos_current_assets() -> Vec<String> {
    (31..51).map(|x| x.to_string()).collect()
}

pub fn get_pos_liquid_assets() -> Vec<String> {
    vec!["39", "40", "41", "42", "43", "45", "46", "47", "48"]
        .iter().map(|s| s.to_string()).collect()
}

pub fn get_pos_cash() -> Vec<String> {
    vec!["49", "50"].iter().map(|s| s.to_string()).collect()
}

pub fn get_pos_current_liabilities() -> Vec<String> {
    vec!["79", "80", "81", "82", "83", "84", "85", "86", "87", "88"]
        .iter().map(|s| s.to_string()).collect()
}

pub fn get_pos_total_liabilities() -> Vec<String> {
    vec!["67", "68", "69", "100", "70", "71", "72", "73", "74", "75", "76", "77", "78", 
         "79", "80", "81", "82", "83", "84", "85", "86", "87", "88"]
        .iter().map(|s| s.to_string()).collect()
}

pub fn get_pos_total_equity() -> Vec<String> {
    vec!["52", "53", "54", "55", "56", "57", "58", "59", "64", "65", "66"]
        .iter().map(|s| s.to_string()).collect()
}
