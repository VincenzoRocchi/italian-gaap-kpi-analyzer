use std::collections::BTreeMap;
use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct KpiTooltipInfo {
    pub full_explanation: String,
    pub formula_display: String,
    pub optimal_range_cee: String,
    pub interpretation_notes: String,
    pub required_inputs_display: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct KpiDetails {
    pub name_display: String,
    pub description_short: String,
    pub is_ratio: bool,
    pub category_display: String,
    pub is_crisis_law_kpi: bool,
    pub tooltip_info: KpiTooltipInfo,
}

pub fn get_available_kpis() -> BTreeMap<String, KpiDetails> {
    let mut kpis = BTreeMap::new();
    
    kpis.insert("current_ratio".to_string(), KpiDetails {
        name_display: "Indice di Liquidità Corrente".to_string(),
        description_short: "Misura la capacità di coprire le passività a breve termine con le attività correnti.".to_string(),
        is_ratio: true,
        category_display: "Indici di Liquidità".to_string(),
        is_crisis_law_kpi: false,
        tooltip_info: KpiTooltipInfo {
            full_explanation: "Il Current Ratio confronta le attività che possono essere convertite in cassa entro un anno con le passività che devono essere pagate entro un anno. È un indicatore chiave della solvibilità a breve termine di un'azienda.".to_string(),
            formula_display: "Attività Correnti / Passività Correnti".to_string(),
            optimal_range_cee: "1.2 - 2.0 (manifatturiero), 0.8 - 1.5 (servizi). Varia per settore.".to_string(),
            interpretation_notes: "Un valore > 1 indica che l'azienda ha più attività correnti che passività correnti. Un valore troppo alto potrebbe indicare un uso inefficiente degli asset.".to_string(),
            required_inputs_display: "Attività Correnti (Rimanenze, Crediti, Titoli, Liquidità), Passività Correnti (Debiti a breve termine)".to_string(),
        },
    });

    kpis.insert("quick_ratio".to_string(), KpiDetails {
        name_display: "Indice di Liquidità Immediata (Acid Test)".to_string(),
        description_short: "Misura la capacità di coprire le passività a breve termine con le attività più liquide.".to_string(),
        is_ratio: true,
        category_display: "Indici di Liquidità".to_string(),
        is_crisis_law_kpi: false,
        tooltip_info: KpiTooltipInfo {
            full_explanation: "Simile al Current Ratio, ma esclude le rimanenze (considerate meno liquide) e i risconti attivi. Fornisce una misura più stringente della liquidità.".to_string(),
            formula_display: "(Crediti + Titoli + Liquidità) / Passività Correnti".to_string(),
            optimal_range_cee: "0.8 - 1.2. Soglia critica < 0.5 indica alto rischio.".to_string(),
            interpretation_notes: "Un valore > 0.5-1.0 è generalmente considerato sano. Indica la capacità di far fronte agli obblighi a breve senza vendere le scorte.".to_string(),
            required_inputs_display: "Crediti, Titoli, Liquidità, Passività Correnti".to_string(),
        },
    });

    kpis.insert("cash_ratio".to_string(), KpiDetails {
        name_display: "Indice di Liquidità Ciclica (Cash Ratio)".to_string(),
        description_short: "Misura la capacità di coprire le passività a breve termine con la liquidità immediata.".to_string(),
        is_ratio: true,
        category_display: "Indici di Liquidità".to_string(),
        is_crisis_law_kpi: false,
        tooltip_info: KpiTooltipInfo {
            full_explanation: "Il Cash Ratio considera solo il denaro immediatamente disponibile (cassa e depositi bancari) per coprire le passività a breve. È l'indicatore più conservativo di liquidità.".to_string(),
            formula_display: "(Disponibilità Liquide + Depositi Bancari) / Passività Correnti".to_string(),
            optimal_range_cee: "0.2 - 0.5. Valori > 1 potrebbero indicare capitale inutilizzato.".to_string(),
            interpretation_notes: "Un valore troppo basso indica rischio di illiquidità. Un valore troppo alto potrebbe indicare inefficiente gestione della cassa.".to_string(),
            required_inputs_display: "Disponibilità Liquide, Depositi Bancari, Passività Correnti".to_string(),
        },
    });

    kpis.insert("debt_to_equity".to_string(), KpiDetails {
        name_display: "Indice di Indebitamento Netto (Debt to Equity)".to_string(),
        description_short: "Misura il rapporto tra debiti totali e patrimonio netto.".to_string(),
        is_ratio: true,
        category_display: "Indici di Indebitamento".to_string(),
        is_crisis_law_kpi: true,
        tooltip_info: KpiTooltipInfo {
            full_explanation: "Il Debt to Equity Ratio misura quanto l'azienda si finanzia attraverso il debito rispetto al patrimonio netto. Un valore alto indica maggiore dipendenza dal debito.".to_string(),
            formula_display: "Debiti Totali / Patrimonio Netto".to_string(),
            optimal_range_cee: "< 1.0 (conservativo), < 2.0 (accettabile). Varia per settore.".to_string(),
            interpretation_notes: "Valore > 2 indica alto rischio finanziario. Valore < 1 indica struttura finanziaria solida.".to_string(),
            required_inputs_display: "Debiti Totali (a breve + a lungo), Patrimonio Netto".to_string(),
        },
    });

    kpis.insert("debt_ratio".to_string(), KpiDetails {
        name_display: "Indice di Indebitamento sul Totale Attivo (Debt Ratio)".to_string(),
        description_short: "Misura la percentuale di attività finanziate tramite debito.".to_string(),
        is_ratio: true,
        category_display: "Indici di Indebitamento".to_string(),
        is_crisis_law_kpi: false,
        tooltip_info: KpiTooltipInfo {
            full_explanation: "Il Debt Ratio indica quale percentuale delle attività totali è finanziata da debiti. Mostra il livello di leva finanziaria dell'azienda.".to_string(),
            formula_display: "Debiti Totali / Attività Totali".to_string(),
            optimal_range_cee: "< 0.5 (conservativo), < 0.7 (accettabile).".to_string(),
            interpretation_notes: "Valore > 0.7 indica alta leva finanziaria e maggior rischio. Investitori preferiscono valori bassi.".to_string(),
            required_inputs_display: "Debiti Totali, Attività Totali".to_string(),
        },
    });

    kpis.insert("working_capital".to_string(), KpiDetails {
        name_display: "Capitale Circolante Netto (Working Capital)".to_string(),
        description_short: "Misura la differenza tra attività correnti e passività correnti.".to_string(),
        is_ratio: false,
        category_display: "Indici di Liquidità".to_string(),
        is_crisis_law_kpi: false,
        tooltip_info: KpiTooltipInfo {
            full_explanation: "Il Capitale Circolante Netto rappresenta la liquidità che l'azienda ha a disposizione per finanziare le operazioni quotidiane. È la differenza tra attività a breve e passività a breve.".to_string(),
            formula_display: "Attività Correnti - Passività Correnti".to_string(),
            optimal_range_cee: "Positivo e stabile. Valore ottimale dipende dal ciclo operativo.".to_string(),
            interpretation_notes: "Valore positivo indica liquidità sufficiente. Valore negativo può indicare dipendenza dal credito a breve termine.".to_string(),
            required_inputs_display: "Attività Correnti, Passività Correnti".to_string(),
        },
    });

    kpis
}
