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

    // Asset Rigidity Index
    kpis.insert("asset_rigidity_index".to_string(), KpiDetails {
        name_display: "Indice di Rigidità degli Attivi".to_string(),
        description_short: "Misura la quota di attività non correnti sul totale attivo.".to_string(),
        is_ratio: true,
        category_display: "Indici di Struttura".to_string(),
        is_crisis_law_kpi: false,
        tooltip_info: KpiTooltipInfo {
            full_explanation: "L'Indice di Rigidità misura quanto del totale attivo è immobilizzato in attività non correnti (lungo termine). Un valore alto indica minore flessibilità.".to_string(),
            formula_display: "Attività Non Correnti / Attività Totali".to_string(),
            optimal_range_cee: "0.3 - 0.6 dipende dal settore.".to_string(),
            interpretation_notes: "Valore > 0.7 indica alta rigidità. Settori manifatturieri tendono ad avere valori più alti.".to_string(),
            required_inputs_display: "Attività Non Correnti, Attività Totali".to_string(),
        },
    });

    // Asset Elasticity Index
    kpis.insert("asset_elasticity_index".to_string(), KpiDetails {
        name_display: "Indice di Elasticità degli Attivi".to_string(),
        description_short: "Misura la quota di attività correnti sul totale attivo.".to_string(),
        is_ratio: true,
        category_display: "Indici di Struttura".to_string(),
        is_crisis_law_kpi: false,
        tooltip_info: KpiTooltipInfo {
            full_explanation: "L'Indice di Elasticità misura quanto del totale attivo è in attività correnti (liquidità a breve). Un valore alto indica maggiore flessibilità.".to_string(),
            formula_display: "Attività Correnti / Attività Totali".to_string(),
            optimal_range_cee: "0.4 - 0.7 dipende dal settore.".to_string(),
            interpretation_notes: "Valore > 0.8 indica possibile inefficienza nell'uso degli asset. Valore < 0.3 indica alta rigidità.".to_string(),
            required_inputs_display: "Attività Correnti, Attività Totali".to_string(),
        },
    });

    // Fixed Asset Coverage Ratio
    kpis.insert("fixed_asset_coverage_ratio".to_string(), KpiDetails {
        name_display: "Indice di Copertura degli Immobilizzi".to_string(),
        description_short: "Misura la copertura degli immobilizzi con il patrimonio netto.".to_string(),
        is_ratio: true,
        category_display: "Indici di Copertura".to_string(),
        is_crisis_law_kpi: false,
        tooltip_info: KpiTooltipInfo {
            full_explanation: "L'Indice di Copertura degli Immobilizzi misura quanto degli immobilizzi è coperto dal patrimonio netto. Un valore < 1 indica dipendenza da debiti per finanziare gli asset fissi.".to_string(),
            formula_display: "Patrimonio Netto / Attività Non Correnti".to_string(),
            optimal_range_cee: "> 0.5 (solido), > 1.0 (eccellente).".to_string(),
            interpretation_notes: "Valore < 0.5 indica rischio. Valore > 2.0 può indicare capitale inutilizzato.".to_string(),
            required_inputs_display: "Patrimonio Netto, Attività Non Correnti".to_string(),
        },
    });

    // Tax/Social Debt on Assets Ratio
    kpis.insert("tax_social_debt_on_assets_ratio".to_string(), KpiDetails {
        name_display: "Indice Debiti Tributari/Previdenziali su Attivo".to_string(),
        description_short: "Rapporto tra debiti tributari/previdenziali e attività totali.".to_string(),
        is_ratio: true,
        category_display: "Indici di Indebitamento".to_string(),
        is_crisis_law_kpi: true,
        tooltip_info: KpiTooltipInfo {
            full_explanation: "Misura quanto delle attività totali è impegnato per coprire debiti tributari e verso l'INPS. Indicatore chiave per legge crisi.".to_string(),
            formula_display: "(TFR + Debiti Previdenziali) / Attività Totali".to_string(),
            optimal_range_cee: "< 0.1 (sano), > 0.2 indica rischio crisi.".to_string(),
            interpretation_notes: "Valore alto indica possibile crisi di liquidità verso il fisco/INPS. Critico per Legge 155/2023.".to_string(),
            required_inputs_display: "TFR, Debiti Previdenziali, Attività Totali".to_string(),
        },
    });

    // Tangible Net Worth
    kpis.insert("tangible_net_worth".to_string(), KpiDetails {
        name_display: "Patrimonio Netto Tangibile".to_string(),
        description_short: "Patrimonio netto meno le attività immateriali.".to_string(),
        is_ratio: false,
        category_display: "Indici di Patrimonio".to_string(),
        is_crisis_law_kpi: false,
        tooltip_info: KpiTooltipInfo {
            full_explanation: "Il Patrimonio Netto Tangibile rappresenta il valore reale del patrimonio netto escludendo le attività immateriali (avviamento, brevetti, etc.).".to_string(),
            formula_display: "Patrimonio Netto - Attività Immateriali".to_string(),
            optimal_range_cee: "Positivo e stabile.".to_string(),
            interpretation_notes: "Valore negativo indica che le attività immateriali superano il patrimonio netto. Critico per valutazioni M&A.".to_string(),
            required_inputs_display: "Patrimonio Netto, Attività Immateriali".to_string(),
        },
    });

    // Equity Multiplier
    kpis.insert("equity_multiplier".to_string(), KpiDetails {
        name_display: "Moltiplicatore di Equità".to_string(),
        description_short: "Rapporto tra attività totali e patrimonio netto.".to_string(),
        is_ratio: true,
        category_display: "Indici di Leva Finanziaria".to_string(),
        is_crisis_law_kpi: false,
        tooltip_info: KpiTooltipInfo {
            full_explanation: "Il Moltiplicatore di Equità misura quanta leva finanziaria viene utilizzata. Indica quante attività sono finanziate da ogni euro di patrimonio netto.".to_string(),
            formula_display: "Attività Totali / Patrimonio Netto".to_string(),
            optimal_range_cee: "1.5 - 3.0 (accettabile).".to_string(),
            interpretation_notes: "Valore > 4 indica alta leva finanziaria e rischio. Valore = 1 indica nessun debito.".to_string(),
            required_inputs_display: "Attività Totali, Patrimonio Netto".to_string(),
        },
    });

    // Long-term Debt to Equity
    kpis.insert("long_term_debt_to_equity".to_string(), KpiDetails {
        name_display: "Indebitamento a Lungo Termine su Equità".to_string(),
        description_short: "Rapporto tra debiti a lungo termine e patrimonio netto.".to_string(),
        is_ratio: true,
        category_display: "Indici di Indebitamento".to_string(),
        is_crisis_law_kpi: false,
        tooltip_info: KpiTooltipInfo {
            full_explanation: "Misura quanto del patrimonio netto è impegnato per coprire debiti a lungo termine. Separato dai debiti a breve per analisi della struttura finanziaria.".to_string(),
            formula_display: "Debiti a Lungo Termine / Patrimonio Netto".to_string(),
            optimal_range_cee: "< 1.0 (conservativo), < 2.0 (accettabile).".to_string(),
            interpretation_notes: "Valore > 2 indica alta dipendenza da debiti a lungo termine. Importante per valutazione stabilità.".to_string(),
            required_inputs_display: "Debiti a Lungo Termine, Patrimonio Netto".to_string(),
        },
    });

    // Intangible Assets Ratio
    kpis.insert("intangible_assets_ratio".to_string(), KpiDetails {
        name_display: "Incidenza delle Attività Immateriali".to_string(),
        description_short: "Quota di attività immateriali sul totale attivo.".to_string(),
        is_ratio: true,
        category_display: "Indici di Struttura".to_string(),
        is_crisis_law_kpi: false,
        tooltip_info: KpiTooltipInfo {
            full_explanation: "Misura quanto del totale attivo è rappresentato da attività immateriali (avviamento, brevetti, concessioni). Alto in aziende tech/brand-intensive.".to_string(),
            formula_display: "Attività Immateriali / Attività Totali".to_string(),
            optimal_range_cee: "< 0.2 (manifatturiero), < 0.5 (servizi/tech).".to_string(),
            interpretation_notes: "Valore > 0.5 indica forte dipendenza da asset intangibili. Rischioso se overvalued.".to_string(),
            required_inputs_display: "Attività Immateriali, Attività Totali".to_string(),
        },
    });

    // Financial Assets Ratio
    kpis.insert("financial_assets_ratio".to_string(), KpiDetails {
        name_display: "Incidenza delle Attività Finanziarie Correnti".to_string(),
        description_short: "Quota di attività finanziarie correnti sul totale attivo.".to_string(),
        is_ratio: true,
        category_display: "Indici di Struttura".to_string(),
        is_crisis_law_kpi: false,
        tooltip_info: KpiTooltipInfo {
            full_explanation: "Misura quanto del totale attivo è in attività finanziarie a breve (partecipazioni, titoli). Indica vocazione finanziaria dell'azienda.".to_string(),
            formula_display: "Attività Finanziarie Correnti / Attività Totali".to_string(),
            optimal_range_cee: "< 0.3 (operativo), > 0.5 indica vocazione finanziaria.".to_string(),
            interpretation_notes: "Valore alto indica che l'azienda è più un veicolo finanziario che operativo. Rischio se mercati volatili.".to_string(),
            required_inputs_display: "Attività Finanziarie Correnti, Attività Totali".to_string(),
        },
    });

    // Non-current Assets Coverage
    kpis.insert("non_current_assets_coverage".to_string(), KpiDetails {
        name_display: "Copertura Attività Non Correnti".to_string(),
        description_short: "Patrimonio netto e debiti a lungo che coprono le attività non correnti.".to_string(),
        is_ratio: true,
        category_display: "Indici di Copertura".to_string(),
        is_crisis_law_kpi: false,
        tooltip_info: KpiTooltipInfo {
            full_explanation: "Misura quanto delle attività non correnti è coperto da fonti stabili (patrimonio + debiti lungo termine). Indica solidità della struttura.".to_string(),
            formula_display: "(Patrimonio Netto + Debiti Lungo Termine) / Attività Non Correnti".to_string(),
            optimal_range_cee: "> 1.0 (solido), < 1.0 indica rischio.".to_string(),
            interpretation_notes: "Valore < 1 indica che le attività non correnti non sono pienamente coperte da fonti stabili. Critico per bancabilità.".to_string(),
            required_inputs_display: "Patrimonio Netto, Debiti Lungo Termine, Attività Non Correnti".to_string(),
        },
    });

    // Net Working Capital Ratio
    kpis.insert("net_working_capital_ratio".to_string(), KpiDetails {
        name_display: "Incidenza del Capitale Circolante Netto".to_string(),
        description_short: "Quota di capitale circolante netto sul totale attivo.".to_string(),
        is_ratio: true,
        category_display: "Indici di Liquidità".to_string(),
        is_crisis_law_kpi: false,
        tooltip_info: KpiTooltipInfo {
            full_explanation: "Misura quanto del totale attivo è investito in capitale circolante netto. Indica efficienza nell'uso dei capitali a breve.".to_string(),
            formula_display: "Capitale Circolante Netto / Attività Totali".to_string(),
            optimal_range_cee: "0.1 - 0.3 (ottimale). Dipende dal ciclo operativo.".to_string(),
            interpretation_notes: "Valore > 0.4 indica possibile inefficienza. Valore negativo indica dipendenza da fornitori/banche.".to_string(),
            required_inputs_display: "Capitale Circolante Netto, Attività Totali".to_string(),
        },
    });

    // Debt to Equity Excluding TFR
    kpis.insert("debt_to_equity_excl_tfr".to_string(), KpiDetails {
        name_display: "Indebitamento Netto (escl. TFR)".to_string(),
        description_short: "Rapporto tra debiti totali (escluso TFR) e patrimonio netto.".to_string(),
        is_ratio: true,
        category_display: "Indici di Indebitamento".to_string(),
        is_crisis_law_kpi: true,
        tooltip_info: KpiTooltipInfo {
            full_explanation: "Il Debt to Equity escludendo il TFR misura l'indebitamento netto reale dell'azienda. TFR è una passività tecnica, non debito verso terzi.".to_string(),
            formula_display: "(Debiti Totali - TFR) / Patrimonio Netto".to_string(),
            optimal_range_cee: "< 1.0 (conservativo), < 2.0 (accettabile).".to_string(),
            interpretation_notes: "Valore > 2 indica alto rischio finanziario. Escludere TFR dà quadro più realistico della leva finanziaria.".to_string(),
            required_inputs_display: "Debiti Totali, TFR, Patrimonio Netto".to_string(),
        },
    });

    // Debt Ratio Excluding TFR
    kpis.insert("debt_ratio_excl_tfr".to_string(), KpiDetails {
        name_display: "Indice di Indebitamento (escl. TFR)".to_string(),
        description_short: "Percentuale di attività finanziate da debiti (escluso TFR).".to_string(),
        is_ratio: true,
        category_display: "Indici di Indebitamento".to_string(),
        is_crisis_law_kpi: true,
        tooltip_info: KpiTooltipInfo {
            full_explanation: "Il Debt Ratio escludendo il TFR misura quanto del totale attivo è finanziato da debiti verso terzi (escludendo TFR). Dà quadro più realistico.".to_string(),
            formula_display: "(Debiti Totali - TFR) / Attività Totali".to_string(),
            optimal_range_cee: "< 0.5 (conservativo), < 0.7 (accettabile).".to_string(),
            interpretation_notes: "Valore > 0.7 indica alta leva finanziaria. Escludere TFR evita sovrastima dell'indebitamento.".to_string(),
            required_inputs_display: "Debiti Totali, TFR, Attività Totali".to_string(),
        },
    });

    kpis
}
