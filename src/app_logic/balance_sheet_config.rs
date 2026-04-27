use std::collections::BTreeMap;
use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct BalanceSheetStructure {
    pub assets: Assets,
    pub equity_liabilities: EquityLiabilities,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Assets {
    pub due_from_shareholders: Vec<String>,
    pub non_current_assets: NonCurrentAssets,
    pub current_assets: CurrentAssets,
    pub prepaid_expenses_and_accrued_income: Vec<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct NonCurrentAssets {
    pub intangible_assets: Vec<String>,
    pub tangible_assets: Vec<String>,
    pub financial_investments_non_current: Vec<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CurrentAssets {
    pub inventories: Vec<String>,
    pub trade_and_other_receivables: TradeReceivables,
    pub current_financial_assets: Vec<String>,
    pub cash_and_cash_equivalents: Vec<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct TradeReceivables {
    pub due_from_customers_current: Vec<String>,
    pub due_from_customers_non_current: Vec<String>,
    pub due_from_subsidiaries_current: Vec<String>,
    pub due_from_subsidiaries_non_current: Vec<String>,
    pub due_from_associates_current: Vec<String>,
    pub due_from_associates_non_current: Vec<String>,
    pub due_from_parent_companies_current: Vec<String>,
    pub due_from_parent_companies_non_current: Vec<String>,
    pub tax_receivables_current: Vec<String>,
    pub tax_receivables_non_current: Vec<String>,
    pub deferred_tax_assets_current: Vec<String>,
    pub deferred_tax_assets_non_current: Vec<String>,
    pub other_receivables_current: Vec<String>,
    pub other_receivables_non_current: Vec<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct EquityLiabilities {
    pub equity: Equity,
    pub provisions_for_risks_and_charges: Vec<String>,
    pub employee_severance_indemnity_tfr: Vec<String>,
    pub liabilities: Liabilities,
    pub accrued_expenses_and_deferred_income: Vec<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Equity {
    pub capital_social: Vec<String>,
    pub fondo_di_dotazione: Vec<String>,
    pub share_premium_reserve: Vec<String>,
    pub revaluation_reserve: Vec<String>,
    pub legal_reserve: Vec<String>,
    pub statutory_reserves: Vec<String>,
    pub other_reserves: Vec<String>,
    pub retained_earnings_or_accumulated_loss_bf: Vec<String>,
    pub profit_or_loss_for_the_year: Vec<String>,
    pub negative_reserve_for_treasury_shares: Vec<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Liabilities {
    pub bonds_issued: Vec<String>,
    pub convertible_bonds_issued: Vec<String>,
    pub amounts_owed_to_shareholders_for_loans: Vec<String>,
    pub amounts_owed_to_banks: Vec<String>,
    pub amounts_owed_to_other_lenders: Vec<String>,
    pub advances_received_from_customers: Vec<String>,
    pub trade_payables: Vec<String>,
    pub debt_represented_by_credit_instruments: Vec<String>,
    pub amounts_owed_to_group_companies: Vec<String>,
    pub tax_payables: Vec<String>,
    pub social_security_payables: Vec<String>,
    pub other_payables: Vec<String>,
}

pub fn get_balance_sheet_structure() -> BalanceSheetStructure {
    BalanceSheetStructure {
        assets: Assets {
            due_from_shareholders: vec![],
            non_current_assets: NonCurrentAssets {
                intangible_assets: (1..11).map(|x| x.to_string()).collect(),
                tangible_assets: (11..26).map(|x| x.to_string()).collect(),
                financial_investments_non_current: (26..31).map(|x| x.to_string()).collect(),
            },
            current_assets: CurrentAssets {
                inventories: (31..39).map(|x| x.to_string()).collect(),
                trade_and_other_receivables: TradeReceivables {
                    due_from_customers_current: vec!["39".to_string()],
                    due_from_customers_non_current: vec!["39.NCA".to_string()],
                    due_from_subsidiaries_current: vec!["40".to_string()],
                    due_from_subsidiaries_non_current: vec!["40.NCA".to_string()],
                    due_from_associates_current: vec!["41".to_string()],
                    due_from_associates_non_current: vec!["41.NCA".to_string()],
                    due_from_parent_companies_current: vec!["42".to_string()],
                    due_from_parent_companies_non_current: vec!["42.NCA".to_string()],
                    tax_receivables_current: vec!["43".to_string()],
                    tax_receivables_non_current: vec!["43.NCA".to_string()],
                    deferred_tax_assets_current: vec!["44".to_string()],
                    deferred_tax_assets_non_current: vec!["44.NCA".to_string()],
                    other_receivables_current: vec!["45".to_string()],
                    other_receivables_non_current: vec!["45.NCA".to_string()],
                },
                current_financial_assets: (46..49).map(|x| x.to_string()).collect(),
                cash_and_cash_equivalents: (49..51).map(|x| x.to_string()).collect(),
            },
            prepaid_expenses_and_accrued_income: vec!["51".to_string()],
        },
        equity_liabilities: EquityLiabilities {
            equity: Equity {
                capital_social: vec!["52".to_string()],
                fondo_di_dotazione: vec!["53".to_string()],
                share_premium_reserve: vec!["54".to_string()],
                revaluation_reserve: vec!["55".to_string()],
                legal_reserve: vec!["56".to_string()],
                statutory_reserves: vec!["57".to_string()],
                other_reserves: vec!["58".to_string()],
                retained_earnings_or_accumulated_loss_bf: vec!["64".to_string()],
                profit_or_loss_for_the_year: vec!["65".to_string()],
                negative_reserve_for_treasury_shares: vec!["66".to_string()],
            },
            provisions_for_risks_and_charges: (67..70).map(|x| x.to_string()).collect(),
            employee_severance_indemnity_tfr: vec!["100".to_string()],
            liabilities: Liabilities {
                bonds_issued: vec!["70".to_string()],
                convertible_bonds_issued: vec!["71".to_string()],
                amounts_owed_to_shareholders_for_loans: vec!["72".to_string()],
                amounts_owed_to_banks: vec!["73".to_string(), "80".to_string()],
                amounts_owed_to_other_lenders: vec!["74".to_string(), "81".to_string()],
                advances_received_from_customers: vec!["75".to_string(), "82".to_string()],
                trade_payables: vec!["76".to_string(), "79".to_string()],
                debt_represented_by_credit_instruments: vec!["77".to_string(), "83".to_string()],
                amounts_owed_to_group_companies: vec!["78".to_string(), "84".to_string()],
                tax_payables: vec!["85".to_string()],
                social_security_payables: vec!["86".to_string()],
                other_payables: vec!["87".to_string()],
            },
            accrued_expenses_and_deferred_income: vec!["88".to_string()],
        },
    }
}

pub fn get_position_names() -> BTreeMap<String, String> {
    let mut names = BTreeMap::new();
    names.insert("1".to_string(), "Costi di impianto e di ampliamento".to_string());
    names.insert("2".to_string(), "Costi di sviluppo".to_string());
    names.insert("3".to_string(), "Diritti di brevetto industriale e diritti di utilizzazione delle opere dell'ingegno".to_string());
    names.insert("4".to_string(), "Concessioni, licenze, marchi e diritti simili".to_string());
    names.insert("5".to_string(), "Avviamento".to_string());
    names.insert("6".to_string(), "Immobilizzazioni in corso e acconti (Immateriali)".to_string());
    names.insert("7".to_string(), "Altre immobilizzazioni immateriali".to_string());
    for i in 8..11 {
        names.insert(i.to_string(), format!("(Placeholder {} - Immateriali)", i));
    }
    names.insert("11".to_string(), "Terreni e fabbricati".to_string());
    names.insert("12".to_string(), "Impianti e macchinario".to_string());
    names.insert("13".to_string(), "Attrezzature industriali e commerciali".to_string());
    names.insert("14".to_string(), "Altri beni (Materiali)".to_string());
    names.insert("15".to_string(), "Immobilizzazioni in corso e acconti (Materiali)".to_string());
    for i in 16..26 {
        names.insert(i.to_string(), format!("(Placeholder {} - Materiali)", i));
    }
    names.insert("26".to_string(), "Partecipazioni in imprese controllate (Immobilizzate)".to_string());
    names.insert("27".to_string(), "Partecipazioni in imprese collegate (Immobilizzate)".to_string());
    names.insert("28".to_string(), "Partecipazioni in imprese controllanti (Immobilizzate)".to_string());
    names.insert("29".to_string(), "Altre partecipazioni (Immobilizzate)".to_string());
    names.insert("30".to_string(), "Altri titoli immobilizzati".to_string());
    for i in 31..39 {
        names.insert(i.to_string(), format!("Rimanenze {}", i));
    }
    names.insert("39".to_string(), "Crediti verso clienti (entro 12 mesi)".to_string());
    names.insert("39.NCA".to_string(), "Crediti verso clienti (oltre 12 mesi)".to_string());
    names.insert("40".to_string(), "Crediti verso imprese controllate (entro 12 mesi)".to_string());
    names.insert("40.NCA".to_string(), "Crediti verso imprese controllate (oltre 12 mesi)".to_string());
    names.insert("41".to_string(), "Crediti verso imprese collegate (entro 12 mesi)".to_string());
    names.insert("41.NCA".to_string(), "Crediti verso imprese collegate (oltre 12 mesi)".to_string());
    names.insert("42".to_string(), "Crediti verso imprese controllanti (entro 12 mesi)".to_string());
    names.insert("42.NCA".to_string(), "Crediti verso imprese controllanti (oltre 12 mesi)".to_string());
    names.insert("43".to_string(), "Crediti tributari (entro 12 mesi)".to_string());
    names.insert("43.NCA".to_string(), "Crediti tributari (oltre 12 mesi)".to_string());
    names.insert("44".to_string(), "Imposte anticipate (considerate correnti)".to_string());
    names.insert("44.NCA".to_string(), "Imposte anticipate (considerate non correnti)".to_string());
    names.insert("45".to_string(), "Crediti verso altri (entro 12 mesi)".to_string());
    names.insert("45.NCA".to_string(), "Crediti verso altri (oltre 12 mesi)".to_string());
    names.insert("46".to_string(), "Partecipazioni in altre imprese (Attivo Circolante)".to_string());
    names.insert("47".to_string(), "Altri titoli (Attivo Circolante)".to_string());
    names.insert("48".to_string(), "Strumenti finanziari derivati attivi (Attivo Circolante)".to_string());
    names.insert("49".to_string(), "Depositi bancari e postali".to_string());
    names.insert("50".to_string(), "Assegni e denaro in cassa".to_string());
    names.insert("51".to_string(), "Ratei e Risconti attivi".to_string());
    names.insert("52".to_string(), "Capitale sociale".to_string());
    names.insert("53".to_string(), "Fondo di dotazione".to_string());
    names.insert("54".to_string(), "Riserva da sovrapprezzo delle azioni".to_string());
    names.insert("55".to_string(), "Riserve di rivalutazione".to_string());
    names.insert("56".to_string(), "Riserva legale".to_string());
    names.insert("57".to_string(), "Riserve statutarie".to_string());
    names.insert("58".to_string(), "Altre riserve, distintamente indicate".to_string());
    names.insert("64".to_string(), "Utili (perdite) portati a nuovo".to_string());
    names.insert("65".to_string(), "Utile (perdita) dell'esercizio".to_string());
    names.insert("66".to_string(), "Riserva negativa per azioni proprie in portafoglio".to_string());
    names.insert("67".to_string(), "Fondi per imposte, anche differite".to_string());
    names.insert("68".to_string(), "Fondi per quiescenza e obblighi simili".to_string());
    names.insert("69".to_string(), "Altri fondi (Rischi e Oneri)".to_string());
    names.insert("70".to_string(), "Obbligazioni".to_string());
    names.insert("71".to_string(), "Obbligazioni convertibili".to_string());
    names.insert("72".to_string(), "Debiti verso soci per finanziamenti".to_string());
    names.insert("73".to_string(), "Debiti verso banche (oltre 12 mesi)".to_string());
    names.insert("74".to_string(), "Debiti verso altri finanziatori (oltre 12 mesi)".to_string());
    names.insert("75".to_string(), "Acconti da clienti (oltre 12 mesi)".to_string());
    names.insert("76".to_string(), "Debiti verso fornitori (oltre 12 mesi)".to_string());
    names.insert("77".to_string(), "Debiti rappresentati da titoli di credito (oltre 12 mesi)".to_string());
    names.insert("78".to_string(), "Debiti verso imprese del gruppo (oltre 12 mesi aggregate)".to_string());
    names.insert("79".to_string(), "Debiti verso fornitori (entro 12 mesi)".to_string());
    names.insert("80".to_string(), "Debiti verso banche (entro 12 mesi)".to_string());
    names.insert("81".to_string(), "Debiti verso altri finanziatori (entro 12 mesi)".to_string());
    names.insert("82".to_string(), "Acconti da clienti (entro 12 mesi)".to_string());
    names.insert("83".to_string(), "Debiti rappresentati da titoli di credito (entro 12 mesi)".to_string());
    names.insert("84".to_string(), "Debiti verso imprese del gruppo (entro 12 mesi aggregate)".to_string());
    names.insert("85".to_string(), "Debiti tributari".to_string());
    names.insert("86".to_string(), "Debiti verso istituti di previdenza e sicurezza sociale".to_string());
    names.insert("87".to_string(), "Altri debiti (entro 12 mesi)".to_string());
    names.insert("88".to_string(), "Ratei e Risconti passivi".to_string());
    names.insert("100".to_string(), "Trattamento di fine rapporto di lavoro subordinato".to_string());
    names
}
