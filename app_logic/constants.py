# Define the structure based on CEE positions (Art. 2424 Codice Civile)
BALANCE_SHEET_STRUCTURE = {
    'assets': {
        # A) Crediti verso soci per versamenti ancora dovuti
        'due_from_shareholders': [], # Placeholder, e.g. ['A1'] if specific position needed
        # B) Immobilizzazioni
        'non_current_assets': { # B)
            'intangible_assets': list(map(str, range(1, 11))),        # B.I (1-10)
            'tangible_assets': list(map(str, range(11, 26))),          # B.II (11-25)
            'financial_investments_non_current': list(map(str, range(26, 31))) # B.III (26-30)
        },
        # C) Attivo Circolante
        'current_assets': { # C)
            'inventories': list(map(str, range(31, 39))),              # C.I (31-38)
            'trade_and_other_receivables': {                         # C.II
                'due_from_customers_current': ['39'],
                'due_from_customers_non_current': ['39.NCA'],
                'due_from_subsidiaries_current': ['40'],
                'due_from_subsidiaries_non_current': ['40.NCA'],
                'due_from_associates_current': ['41'],
                'due_from_associates_non_current': ['41.NCA'],
                'due_from_parent_companies_current': ['42'],
                'due_from_parent_companies_non_current': ['42.NCA'],
                'tax_receivables_current': ['43'], # Crediti tributari
                'tax_receivables_non_current': ['43.NCA'],
                'deferred_tax_assets_current': ['44'], # Imposte anticipate
                'deferred_tax_assets_non_current': ['44.NCA'],
                'other_receivables_current': ['45'], # Crediti verso altri
                'other_receivables_non_current': ['45.NCA'],
            },
            'current_financial_assets': list(map(str, range(46, 49))), # C.III (46-48)
            'cash_and_cash_equivalents': list(map(str, range(49, 51))) # C.IV (49-50)
        },
        # D) Ratei e Risconti Attivi
        'prepaid_expenses_and_accrued_income': ['51'] # D)
    },
    'equity_liabilities': {
        # A) Patrimonio Netto
        'equity': { # A)
            'capital_social': ['52'],
            'fondo_di_dotazione': ['53'],
            'share_premium_reserve': ['54'],
            'revaluation_reserve': ['55'],
            'legal_reserve': ['56'],
            'statutory_reserves': ['57'],
            'other_reserves': ['58'],
            'retained_earnings_or_accumulated_loss_bf': ['64'],
            'profit_or_loss_for_the_year': ['65'],
            'negative_reserve_for_treasury_shares': ['66']
        },
        # B) Fondi per Rischi e Oneri
        'provisions_for_risks_and_charges': list(map(str, range(67, 70))), # B) (67-69)
        # C) Trattamento di Fine Rapporto di Lavoro Subordinato
        'employee_severance_indemnity_tfr': ['100'], # C) Custom position
        # D) Debiti
        'liabilities': { # D)
            'bonds_issued': ['70'],
            'convertible_bonds_issued': ['71'],
            'amounts_owed_to_shareholders_for_loans': ['72'],
            'amounts_owed_to_banks': ['73', '80'], # 73 > 1yr, 80 <= 1yr
            'amounts_owed_to_other_lenders': ['74', '81'], # 74 > 1yr, 81 <= 1yr
            'advances_received_from_customers': ['75', '82'], # 75 > 1yr, 82 <= 1yr
            'trade_payables': ['76', '79'], # 76 > 1yr, 79 <= 1yr
            'debt_represented_by_credit_instruments': ['77', '83'], # 77 > 1yr, 83 <= 1yr
            'amounts_owed_to_group_companies': ['78', '84'], # 78 > 1yr, 84 <= 1yr
            'tax_payables': ['85'],
            'social_security_payables': ['86'],
            'other_payables': ['87']
        },
        # E) Ratei e Risconti Passivi
        'accrued_expenses_and_deferred_income': ['88'] # E)
    }
}

# Helper to get all position numbers - needs adjustment for nested structure
def get_all_positions(structure_part):
    positions = []
    if isinstance(structure_part, dict):
        for key, value in structure_part.items():
            positions.extend(get_all_positions(value)) # Recurse for dictionaries
    elif isinstance(structure_part, list):
        # Expecting list of strings now
        if all(isinstance(item, str) for item in structure_part):
             positions.extend(structure_part) # Extend if it's a list of positions
    return sorted(list(set(positions))) # Return unique sorted positions

ALL_POSITIONS = get_all_positions(BALANCE_SHEET_STRUCTURE)

# Map KPIs to the positions they require (UPDATED for new structure)
KPI_REQUIREMENTS = {
    # These will be repopulated after POS_ lists are updated with string keys
}

# Temporary static definition of available KPIs (Tier 1 for now)
AVAILABLE_KPIS = {
    'current_ratio': {
        'name_display': "Indice di Liquidità Corrente",
        'description_short': "Misura la capacità di coprire le passività a breve termine con le attività correnti.",
        'is_ratio': True,
        'category_display': "Indici di Liquidità",
        'is_crisis_law_kpi': False,
        'tooltip_info': {
            'full_explanation': "Il Current Ratio confronta le attività che possono essere convertite in cassa entro un anno con le passività che devono essere pagate entro un anno. È un indicatore chiave della solvibilità a breve termine di un'azienda.",
            'formula_display': "Attività Correnti / Passività Correnti",
            'optimal_range_cee': "1.2 - 2.0 (manifatturiero), 0.8 - 1.5 (servizi). Varia per settore.",
            'interpretation_notes': "Un valore > 1 indica che l'azienda ha più attività correnti che passività correnti. Un valore troppo alto potrebbe indicare un uso inefficiente degli asset.",
            'required_inputs_display': "Attività Correnti (Rimanenze, Crediti, Titoli, Liquidità), Passività Correnti (Debiti a breve termine)"
        }
    },
    'quick_ratio': {
        'name_display': "Indice di Liquidità Immediata (Acid Test)",
        'description_short': "Misura la capacità di coprire le passività a breve termine con le attività più liquide.",
        'is_ratio': True,
        'category_display': "Indici di Liquidità",
        'is_crisis_law_kpi': False,
        'tooltip_info': {
            'full_explanation': "Simile al Current Ratio, ma esclude le rimanenze (considerate meno liquide) e i risconti attivi. Fornisce una misura più stringente della liquidità.",
            'formula_display': "(Crediti + Titoli + Liquidità) / Passività Correnti",
            'optimal_range_cee': "0.8 - 1.2. Soglia critica < 0.5 indica alto rischio.",
            'interpretation_notes': "Un valore > 0.5-1.0 è generalmente considerato sano. Indica la capacità di far fronte agli obblighi a breve senza vendere le scorte.",
            'required_inputs_display': "Crediti, Titoli, Liquidità, Passività Correnti"
        }
    },
    'cash_ratio': {
        'name_display': "Indice di Cassa",
        'description_short': "Misura la capacità di coprire le passività a breve termine con la sola liquidità disponibile.",
        'is_ratio': True,
        'category_display': "Indici di Liquidità",
        'is_crisis_law_kpi': False,
        'tooltip_info': {
            'full_explanation': "È l'indicatore di liquidità più conservativo, considera solo cassa e equivalenti di cassa rispetto alle passività correnti.",
            'formula_display': "Liquidità / Passività Correnti",
            'optimal_range_cee': "0.1 - 0.2 (PMI). Valori > 0.5 potrebbero indicare eccesso di liquidità non investita.",
            'interpretation_notes': "Mostra la capacità di pagamento immediato senza ricorrere alla vendita di altri asset.",
            'required_inputs_display': "Liquidità, Passività Correnti"
        }
    },
    'debt_to_equity': {
        'name_display': "Rapporto Debiti/Patrimonio Netto",
        'description_short': "Indica il rapporto tra il finanziamento tramite terzi e il capitale proprio.",
        'is_ratio': True,
        'category_display': "Struttura Finanziaria e Leva",
        'is_crisis_law_kpi': False,
        'tooltip_info': {
            'full_explanation': "Misura la leva finanziaria di un'azienda, confrontando il totale dei debiti con il patrimonio netto. Un rapporto elevato può indicare un maggior rischio.",
            'formula_display': "Totale Passività / Patrimonio Netto",
            'optimal_range_cee': "Banche: 8-12 (regolamentato), Manifatturiero: 0.3-0.8, Servizi: 0.2-0.6. Varia molto per settore.",
            'interpretation_notes': "Un rapporto più basso è generalmente preferibile. Un rapporto > 1 significa che l'azienda è finanziata più da debiti che da capitale proprio.",
            'required_inputs_display': "Fondi rischi e oneri, Debiti (L/T e B/T), Risconti Passivi, Patrimonio Netto (Capitale, Riserve, Risultato)"
        }
    },
    'debt_to_equity_excl_tfr': {
        'name_display': "Rapporto Debiti/Patrimonio Netto (escl. TFR)",
        'description_short': "Indica il rapporto tra il finanziamento tramite terzi (escluso TFR) e il capitale proprio.",
        'is_ratio': True,
        'category_display': "Struttura Finanziaria e Leva",
        'is_crisis_law_kpi': False,
        'tooltip_info': {
            'full_explanation': "Misura la leva finanziaria escludendo il Trattamento di Fine Rapporto (TFR) dai debiti totali. Offre una visione alternativa della struttura del debito.",
            'formula_display': "(Totale Passività - TFR) / Patrimonio Netto",
            'optimal_range_cee': "Simile al D/E standard, ma valori leggermente inferiori. Varia per settore.",
            'interpretation_notes': "Un rapporto più basso è generalmente preferibile. Utile per analisti che considerano il TFR una passività con caratteristiche diverse dal debito finanziario.",
            'required_inputs_display': "Fondi rischi e oneri, Debiti (L/T e B/T escluso TFR), Risconti Passivi, Patrimonio Netto"
        }
    },
    'debt_ratio': {
        'name_display': "Rapporto di Indebitamento Totale",
        'description_short': "Indica la percentuale di attivi finanziati tramite debito.",
        'is_ratio': True,
        'category_display': "Struttura Finanziaria e Leva",
        'is_crisis_law_kpi': False,
        'tooltip_info': {
            'full_explanation': "Mostra quale proporzione degli asset di un'azienda è finanziata attraverso il debito.",
            'formula_display': "Totale Passività / Totale Attivo",
            'optimal_range_cee': "Generalmente < 0.6 per aziende stabili. Dipende dal settore e dalla fase del ciclo di vita dell'azienda.",
            'interpretation_notes': "Un rapporto più basso indica minore dipendenza dal debito. Un rapporto > 1 significa che l'azienda ha più debiti che attivi (improbabile per aziende sane).",
            'required_inputs_display': "Fondi rischi e oneri, Debiti (L/T e B/T), Risconti Passivi, Tutte le categorie di Attivo"
        }
    },
    'debt_ratio_excl_tfr': {
        'name_display': "Rapporto di Indebitamento Totale (escl. TFR)",
        'description_short': "Indica la percentuale di attivi finanziati tramite debito (escluso TFR).",
        'is_ratio': True,
        'category_display': "Struttura Finanziaria e Leva",
        'is_crisis_law_kpi': False,
        'tooltip_info': {
            'full_explanation': "Mostra quale proporzione degli asset di un\'azienda è finanziata attraverso il debito, escludendo il Trattamento di Fine Rapporto (TFR).",
            'formula_display': "(Totale Passività - TFR) / Totale Attivo",
            'optimal_range_cee': "Generalmente < 0.6. Valori leggermente inferiori al Debt Ratio standard.",
            'interpretation_notes': "Un rapporto più basso indica minore dipendenza dal debito. Utile per analisi specifiche del TFR.",
            'required_inputs_display': "Fondi rischi e oneri, Debiti (L/T e B/T escluso TFR), Risconti Passivi, Tutte le categorie di Attivo"
        }
    },
    'working_capital': {
        'name_display': "Capitale Circolante Netto",
        'description_short': "Differenza tra attività correnti e passività correnti.",
        'is_ratio': False,
        'category_display': "Capitale Circolante",
        'is_crisis_law_kpi': False,
        'tooltip_info': {
            'full_explanation': "Rappresenta le risorse finanziarie disponibili per le operazioni quotidiane di un'azienda dopo aver coperto gli obblighi a breve termine.",
            'formula_display': "Attività Correnti - Passività Correnti",
            'optimal_range_cee': "Positivo è generalmente buono. Un valore negativo persistente può indicare problemi di liquidità.",
            'interpretation_notes': "Un capitale circolante positivo indica che l'azienda può finanziare le sue operazioni correnti e investire in attività future. Non è un rapporto, ma un valore assoluto.",
            'required_inputs_display': "Attività Correnti, Passività Correnti"
        }
    },
    'asset_rigidity_index': {
        'name_display': "Indice di Rigidità dell'Attivo",
        'description_short': "Misura la proporzione di attivi immobilizzati sul totale attivo.",
        'is_ratio': True,
        'category_display': "Analisi Strutturale dell'Attivo",
        'is_crisis_law_kpi': True,
        'tooltip_info': {
            'full_explanation': "L'indice di rigidità dell'attivo indica quanto del capitale investito è assorbito da immobilizzazioni (attività a lungo ciclo di utilizzo). Un valore elevato suggerisce una struttura patrimoniale meno flessibile.",
            'formula_display': "Immobilizzazioni Nette / Totale Attivo",
            'optimal_range_cee': "Varia per settore. Settori capital intensive avranno valori più alti.",
            'interpretation_notes': "Un indice crescente può indicare investimenti significativi o difficoltà a smobilizzare asset. Da confrontare con l'indice di elasticità.",
            'required_inputs_display': "Immobilizzazioni Nette (Immateriali, Materiali, Finanziarie), Totale Attivo"
        }
    },
    'asset_elasticity_index': {
        'name_display': "Indice di Elasticità dell'Attivo",
        'description_short': "Misura la proporzione di attivo circolante sul totale attivo.",
        'is_ratio': True,
        'category_display': "Analisi Strutturale dell'Attivo",
        'is_crisis_law_kpi': True,
        'tooltip_info': {
            'full_explanation': "L'indice di elasticità dell'attivo indica quanto del capitale investito è rappresentato da attività a breve ciclo di utilizzo (liquidità, crediti a breve, rimanenze). Un valore elevato suggerisce una struttura patrimoniale più flessibile.",
            'formula_display': "Attivo Circolante / Totale Attivo",
            'optimal_range_cee': "Varia per settore. Solitamente complementare all'indice di rigidità.",
            'interpretation_notes': "Un indice elevato può indicare buona liquidità potenziale ma anche possibile sovrainvestimento in capitale circolante.",
            'required_inputs_display': "Attivo Circolante, Totale Attivo"
        }
    },
    'fixed_asset_coverage_ratio': {
        'name_display': "Grado di Copertura delle Immobilizzazioni",
        'description_short': "Indica in che misura le immobilizzazioni sono finanziate dal patrimonio netto.",
        'is_ratio': True,
        'category_display': "Solidità Patrimoniale e Rischio",
        'is_crisis_law_kpi': True,
        'tooltip_info': {
            'full_explanation': "Questo indice misura la capacità del patrimonio netto di coprire le immobilizzazioni. Un valore superiore a 1 indica che le immobilizzazioni sono interamente finanziate con mezzi propri, segnalando solidità patrimoniale.",
            'formula_display': "Patrimonio Netto / Immobilizzazioni Nette",
            'optimal_range_cee': "Generalmente > 1 è considerato positivo. Valori < 1 indicano che parte delle immobilizzazioni è finanziata con debito.",
            'interpretation_notes': "Cruciale per valutare la struttura finanziaria a lungo termine e l'autonomia da fonti esterne per gli investimenti fissi.",
            'required_inputs_display': "Patrimonio Netto, Immobilizzazioni Nette"
        }
    },
    'tax_social_debt_on_assets_ratio': {
        'name_display': "Incidenza Debiti Tributari e Previdenziali su Attivo",
        'description_short': "Misura il peso dei debiti fiscali e contributivi sul totale attivo.",
        'is_ratio': True,
        'category_display': "Solidità Patrimoniale e Rischio",
        'is_crisis_law_kpi': True,
        'tooltip_info': {
            'full_explanation': "Indica quale percentuale del totale attivo è assorbita da debiti verso l'erario e gli enti previdenziali. Un valore elevato può essere un segnale di tensione finanziaria o di difficoltà nel far fronte agli obblighi correnti.",
            'formula_display': "(Debiti Tributari + Debiti Verso Istituti di Previdenza) / Totale Attivo",
            'optimal_range_cee': "Non esiste un range ottimale fisso; va monitorato nel tempo e confrontato con medie settoriali. Valori in crescita o molto alti richiedono attenzione.",
            'interpretation_notes': "Può segnalare un accumulo di passività che, se non gestito, potrebbe portare a sanzioni o pignoramenti. Utile per il risk assessment.",
            'required_inputs_display': "Debiti Tributari (pos. 85), Debiti Verso Istituti di Previdenza (pos. 86), Totale Attivo"
        }
    },
    'tangible_net_worth': {
        'name_display': "Patrimonio Netto Tangibile",
        'description_short': "Misura il patrimonio netto escludendo le attività immateriali.",
        'is_ratio': False, # It's an absolute value
        'category_display': "Solidità Patrimoniale e Rischio",
        'is_crisis_law_kpi': True,
        'tooltip_info': {
            'full_explanation': "Il Patrimonio Netto Tangibile (o Valore Contabile Tangibile) rappresenta il valore del patrimonio netto dell'azienda dopo aver sottratto il valore delle attività immateriali (come avviamento, brevetti, ecc.). Fornisce una misura più conservativa del valore per gli azionisti.",
            'formula_display': "Patrimonio Netto Totale - Immobilizzazioni Immateriali Totali",
            'optimal_range_cee': "Dipende dal settore. Un valore positivo è generalmente atteso. Confrontare con il Patrimonio Netto.",
            'interpretation_notes': "Un valore significativamente inferiore al Patrimonio Netto totale può indicare una forte dipendenza da asset intangibili. Utile per valutare aziende in settori con molti intangibili (es. tech) o in contesti di liquidazione.",
            'required_inputs_display': "Patrimonio Netto, Immobilizzazioni Immateriali (pos. 1-10)"
        }
    },
    'equity_multiplier': {
        'name_display': "Moltiplicatore dell'Equity",
        'description_short': "Misura la leva finanziaria dell'azienda.",
        'is_ratio': True,
        'category_display': "Struttura Finanziaria e Leva",
        'is_crisis_law_kpi': False,
        'tooltip_info': {
            'full_explanation': "Indica quante attività sono finanziate per ogni unità di patrimonio netto. Un valore più alto suggerisce una maggiore leva finanziaria e potenziale rischio.",
            'formula_display': "Totale Attivo / Patrimonio Netto",
            'optimal_range_cee': "Varia significativamente per settore. Confrontare con medie settoriali.",
            'interpretation_notes': "Un moltiplicatore elevato può amplificare i rendimenti ma anche le perdite.",
            'required_inputs_display': "Totale Attivo, Patrimonio Netto"
        }
    },
    'long_term_debt_to_equity': {
        'name_display': "Rapporto Debiti M/L Termine su Patrimonio Netto",
        'description_short': "Misura l'indebitamento a medio-lungo termine rispetto al capitale proprio.",
        'is_ratio': True,
        'category_display': "Struttura Finanziaria e Leva",
        'is_crisis_law_kpi': False,
        'tooltip_info': {
            'full_explanation': "Focalizza sulla sostenibilità del debito a lungo termine rispetto ai mezzi propri. Esclude i debiti a breve termine.",
            'formula_display': "Debiti oltre 12 mesi / Patrimonio Netto",
            'optimal_range_cee': "Generalmente, valori più bassi sono preferibili. Dipende dal settore e dalla stabilità dei flussi di cassa.",
            'interpretation_notes': "Un rapporto elevato può indicare un eccessivo affidamento sul debito a lungo termine.",
            'required_inputs_display': "Debiti oltre 12 mesi (D.1, D.2, D.3, D.4 >1y, D.5 >1y, D.8 >1y, D.9 >1y), Patrimonio Netto"
        }
    },
    'intangible_assets_ratio': {
        'name_display': "Incidenza Immobilizzazioni Immateriali",
        'description_short': "Percentuale di attività immateriali sul totale attivo.",
        'is_ratio': True,
        'category_display': "Analisi Strutturale dell'Attivo",
        'is_crisis_law_kpi': False,
        'tooltip_info': {
            'full_explanation': "Mostra il peso delle immobilizzazioni immateriali (es. brevetti, avviamento) rispetto al totale degli asset.",
            'formula_display': "Immobilizzazioni Immateriali / Totale Attivo",
            'optimal_range_cee': "Varia per settore. Elevato in settori tech/pharma, basso in manifatturiero tradizionale.",
            'interpretation_notes': "Un'alta incidenza può indicare dipendenza da asset intangibili, la cui valutazione può essere soggettiva.",
            'required_inputs_display': "Immobilizzazioni Immateriali (B.I), Totale Attivo"
        }
    },
    'financial_assets_ratio': {
        'name_display': "Incidenza Attività Finanziarie",
        'description_short': "Peso delle attività finanziarie sul totale attivo.",
        'is_ratio': True,
        'category_display': "Analisi Strutturale dell'Attivo",
        'is_crisis_law_kpi': False,
        'tooltip_info': {
            'full_explanation': "Indica la proporzione del totale attivo investita in attività finanziarie, sia immobilizzate (partecipazioni a lungo termine, titoli) sia correnti (titoli a breve termine).",
            'formula_display': "(Immobilizzazioni Finanziarie + Attività Finanziarie Correnti) / Totale Attivo",
            'optimal_range_cee': "Dipende dalla strategia aziendale (holding vs. operativa).",
            'interpretation_notes': "Un valore elevato può indicare una strategia di investimento o una holding; basso per aziende fortemente operative.",
            'required_inputs_display': "Immobilizzazioni Finanziarie (B.III), Attività Finanziarie Correnti (C.III), Totale Attivo"
        }
    },
    'non_current_assets_coverage': {
        'name_display': "Copertura Immobilizzazioni (Capitale Permanente)",
        'description_short': "Misura come le immobilizzazioni sono coperte da patrimonio netto e debiti a M/L.",
        'is_ratio': True,
        'category_display': "Copertura e Capitale Circolante",
        'is_crisis_law_kpi': False,
        'tooltip_info': {
            'full_explanation': "Indica in che misura le immobilizzazioni nette sono finanziate da fonti di capitale permanente (patrimonio netto + debiti a medio/lungo termine). Un valore > 1 è generalmente positivo.",
            'formula_display': "(Patrimonio Netto + Debiti oltre 12 mesi) / Immobilizzazioni Nette",
            'optimal_range_cee': "Idealmente > 1. Valori inferiori a 1 indicano che parte dell'attivo fisso è finanziato con passività correnti, il che è rischioso.",
            'interpretation_notes': "Valuta la correlazione tra fonti e impieghi a lungo termine. Importante per la stabilità finanziaria.",
            'required_inputs_display': "Patrimonio Netto, Debiti oltre 12 mesi, Immobilizzazioni Nette"
        }
    },
    'net_working_capital_ratio': {
        'name_display': "Indice Capitale Circolante Netto su Attivo",
        'description_short': "Misura l'incidenza del capitale circolante netto sul totale attivo.",
        'is_ratio': True,
        'category_display': "Copertura e Capitale Circolante",
        'is_crisis_law_kpi': False,
        'tooltip_info': {
            'full_explanation': "Rapporto tra il Capitale Circolante Netto (Attivo Circolante - Passivo Corrente) e il Totale Attivo. Indica quanta parte dell'attivo è investita in capitale circolante netto.",
            'formula_display': "(Attivo Circolante - Passivo Corrente) / Totale Attivo",
            'optimal_range_cee': "Varia per settore. Un valore positivo è necessario, ma valori troppo alti possono indicare inefficienze.",
            'interpretation_notes': "Un indicatore della liquidità strutturale e della politica di gestione del circolante. Da non confondere con il valore assoluto del CCN.",
            'required_inputs_display': "Attivo Circolante, Passivo Corrente, Totale Attivo"
        }
    }
}

# Map position numbers to Italian names (Aligned with Art. 2424 C.C. based on analysis)
POSITION_NAMES = {
    '1': "Costi di impianto e di ampliamento",
    '2': "Costi di sviluppo", # Note: Italian schema "Costi di Ricerca e Sviluppo (R&S) e di pubblicità"
    '3': "Diritti di brevetto industriale e diritti di utilizzazione delle opere dell'ingegno",
    '4': "Concessioni, licenze, marchi e diritti simili",
    '5': "Avviamento",
    '6': "Immobilizzazioni in corso e acconti (Immateriali)",
    '7': "Altre immobilizzazioni immateriali",
    '8': "(Placeholder 8 - Immateriali)", # Keep placeholders if structure uses them
    '9': "(Placeholder 9 - Immateriali)",
    '10': "(Placeholder 10 - Immateriali)",
    '11': "Terreni e fabbricati",
    '12': "Impianti e macchinario",
    '13': "Attrezzature industriali e commerciali",
    '14': "Altri beni (Materiali)",
    '15': "Immobilizzazioni in corso e acconti (Materiali)",
    '16': "(Placeholder 16 - Materiali)",
    '17': "(Placeholder 17 - Materiali)",
    '18': "(Placeholder 18 - Materiali)",
    '19': "(Placeholder 19 - Materiali)",
    '20': "(Placeholder 20 - Materiali)",
    '21': "(Placeholder 21 - Materiali)",
    '22': "(Placeholder 22 - Materiali)",
    '23': "(Placeholder 23 - Materiali)",
    '24': "(Placeholder 24 - Materiali)",
    '25': "(Placeholder 25 - Materiali)",
    '26': "Partecipazioni in imprese controllate (Immobilizzate)",
    '27': "Partecipazioni in imprese collegate (Immobilizzate)",
    '28': "Partecipazioni in imprese controllanti (Immobilizzate)", # Schema: B.III.1.c)
    '29': "Altre partecipazioni (Immobilizzate)", # Schema: B.III.1.d) Altre imprese
    '30': "Altri titoli immobilizzati", # Schema: B.III.3
    # Schema B.III.2 Crediti (immobilizzati) and B.III.4 Azioni Proprie are not in current structure range 26-30
    '31': "Materie prime, sussidiarie e di consumo",
    '32': "Prodotti in corso di lavorazione e semilavorati",
    '33': "Lavori in corso su ordinazione",
    '34': "Prodotti finiti e merci",
    '35': "Acconti (a fornitori per rimanenze)",
    '36': "(Placeholder 36 - Rimanenze)",
    '37': "(Placeholder 37 - Rimanenze)",
    '38': "(Placeholder 38 - Rimanenze)",
    '39': "Crediti verso clienti (entro 12 mesi)",
    '39.NCA': "Crediti verso clienti (oltre 12 mesi)",
    '40': "Crediti verso imprese controllate (entro 12 mesi)",
    '40.NCA': "Crediti verso imprese controllate (oltre 12 mesi)",
    '41': "Crediti verso imprese collegate (entro 12 mesi)",
    '41.NCA': "Crediti verso imprese collegate (oltre 12 mesi)",
    '42': "Crediti verso imprese controllanti (entro 12 mesi)",
    '42.NCA': "Crediti verso imprese controllanti (oltre 12 mesi)",
    '43': "Crediti tributari (entro 12 mesi)",
    '43.NCA': "Crediti tributari (oltre 12 mesi)",
    '44': "Imposte anticipate (considerate correnti)", # Deferred Tax Assets - typically current or split based on expected reversal
    '44.NCA': "Imposte anticipate (considerate non correnti)",
    '45': "Crediti verso altri (entro 12 mesi)",
    '45.NCA': "Crediti verso altri (oltre 12 mesi)",
    '46': "Partecipazioni in altre imprese (Attivo Circolante)", # Schema: C.III.1,2,3,4
    '47': "Altri titoli (Attivo Circolante)", # Schema: C.III.6
    '48': "Strumenti finanziari derivati attivi (Attivo Circolante)", # Not in current simple C.III range 46-48. Could be merged or need new pos.
    # Schema C.III.5 Azioni Proprie (Attivo Circolante) not in current range 46-48
    '49': "Depositi bancari e postali",
    '50': "Assegni e denaro in cassa",
    '51': "Ratei e Risconti attivi", # Note: Schema D includes "con separata indicazione del disaggio sui prestiti"
    '52': "Capitale sociale",
    '53': "Fondo di dotazione", # Was commented out, adding as per schema structure often includes it
    '54': "Riserva da sovrapprezzo delle azioni",
    '55': "Riserve di rivalutazione",
    '56': "Riserva legale",
    '57': "Riserve statutarie",
    '58': "Altre riserve, distintamente indicate",
    '59': "Riserva per operazioni di copertura di flussi finanziari attesi", # Was commented out
    '60': "(Placeholder 60 - Riserve)",
    '61': "(Placeholder 61 - Riserve)",
    '62': "(Placeholder 62 - Riserve)",
    '63': "(Placeholder 63 - Riserve)",
    '64': "Utili (perdite) portati a nuovo",
    '65': "Utile (perdita) dell'esercizio",
    '66': "Riserva negativa per azioni proprie in portafoglio", # Schema A.VI "Riserva per azioni proprie in portafoglio" (usually positive here implies negative value if assets)
    '67': "Fondi per imposte, anche differite",
    '68': "Fondi per quiescenza e obblighi simili",
    '69': "Altri fondi (Rischi e Oneri)",
    '70': "Obbligazioni", # Will be split into 70.L / 70.S later
    '71': "Obbligazioni convertibili", # Will be split into 71.L / 71.S later
    '72': "Debiti verso soci per finanziamenti", # Will be split into 72.L / 72.S later
    '73': "Debiti verso banche (oltre 12 mesi)",
    '74': "Debiti verso altri finanziatori (oltre 12 mesi)",
    '75': "Acconti da clienti (oltre 12 mesi)", # Passività
    '76': "Debiti verso fornitori (oltre 12 mesi)",
    '77': "Debiti rappresentati da titoli di credito (oltre 12 mesi)",
    '78': "Debiti verso imprese del gruppo (oltre 12 mesi aggregate)", # Will be disaggregated later
    '79': "Debiti verso fornitori (entro 12 mesi)",
    '80': "Debiti verso banche (entro 12 mesi)",
    '81': "Debiti verso altri finanziatori (entro 12 mesi)",
    '82': "Acconti da clienti (entro 12 mesi)", # Passività
    '83': "Debiti rappresentati da titoli di credito (entro 12 mesi)",
    '84': "Debiti verso imprese del gruppo (entro 12 mesi aggregate)", # Will be disaggregated later
    '85': "Debiti tributari", # Will be split 85.L / 85.S later
    '86': "Debiti verso istituti di previdenza e sicurezza sociale", # Will be split 86.L / 86.S later
    '87': "Altri debiti (entro 12 mesi)", # Or generic Altri Debiti, may need .L/.S split later
    '88': "Ratei e Risconti passivi", # Note: Schema E includes "con separata indicazione dell'aggio sui prestiti"
    '100': "Trattamento di fine rapporto di lavoro subordinato"
}

# Mapping for section titles displayed on input page
SECTION_TITLES = {
    'assets': "ATTIVO",
    'equity_liabilities': "PASSIVO E PATRIMONIO NETTO",
    'due_from_shareholders': "A) Crediti verso soci per versamenti ancora dovuti",
    'non_current_assets': "B) Immobilizzazioni", 
    'intangible_assets': "B.I) Immobilizzazioni Immateriali", 
    'tangible_assets': "B.II) Immobilizzazioni Materiali", 
    'financial_investments_non_current': "B.III) Immobilizzazioni Finanziarie", 
    'current_assets': "C) Attivo Circolante", 
    'inventories': "C.I) Rimanenze", 
    'trade_and_other_receivables': "C.II) Crediti", 
    'current_financial_assets': "C.III) Attività Finanziare che non costituiscono immobilizzazioni", 
    'cash_and_cash_equivalents': "C.IV) Disponibilità Liquide", 
    'prepaid_expenses_and_accrued_income': "D) Ratei e Risconti Attivi", 
    'equity': "A) Patrimonio Netto",
    'capital_social': "A.I) Capitale Sociale",
    'share_premium_reserve': "A.II) Riserva da sovrapprezzo azioni",
    'revaluation_reserve': "A.III) Riserve di rivalutazione",
    'legal_reserve': "A.IV) Riserva legale",
    'statutory_reserves': "A.V) Riserve statutarie",
    'other_reserves': "A.VI) Altre riserve, distintamente indicate",
    'retained_earnings_or_accumulated_loss_bf': "A.VIII) Utili (perdite) portati a nuovo",
    'profit_or_loss_for_the_year': "A.IX) Utile (perdita) dell'esercizio",
    'negative_reserve_for_treasury_shares': "A.X) Riserva negativa per azioni proprie in portafoglio",
    'provisions_for_risks_and_charges': "B) Fondi per Rischi e Oneri", 
    'employee_severance_indemnity_tfr': "C) Trattamento di Fine Rapporto di Lavoro Subordinato", 
    'liabilities': "D) Debiti",
    'bonds_issued': "D.1) Obbligazioni",
    'convertible_bonds_issued': "D.2) Obbligazioni Convertibili",
    'amounts_owed_to_shareholders_for_loans': "D.3) Debiti verso soci per finanziamenti",
    'amounts_owed_to_banks': "D.4) Debiti verso banche",
    'amounts_owed_to_other_lenders': "D.5) Debiti verso altri finanziatori",
    'advances_received_from_customers': "D.6) Acconti da Clienti",
    'trade_payables': "D.7) Debiti verso fornitori",
    'debt_represented_by_credit_instruments': "D.8) Debiti rappresentati da titoli di credito",
    'amounts_owed_to_group_companies': "D.9) Debiti verso imprese del gruppo",
    'tax_payables': "D.12) Debiti tributari", 
    'social_security_payables': "D.13) Debiti verso istituti di previdenza e sicurezza sociale", 
    'other_payables': "D.14) Altri debiti", 
    'accrued_expenses_and_deferred_income': "E) Ratei e Risconti Passivi" 
}

# -- Start Automotive Mapping Data --
CEE_TO_AUTOMOTIVE_CODES = {
    '1': ["0102000001"],
    '2': ["0102000005"],
    '4': ["0102000008"],
    '5': ["0102000010"],
    '7': [
        "0102000030",
        "0102000040",
        "0102000041",
        "0102000042", 
        "0102000043",
        "0102000044",
        "0102000045",
        "0102000050",
        "0102000051",
        "0102000052"
    ],
    '12': [
        "0104000070",
        "0104000090",
        "0104000092",
        "0104000095"
    ],
    '13': [
        "0104000015",
        "0104000020",
        "0104000021",
        "0104000022",
        "0104000023",
        "0104000080",
        "0104000100",
        "0104000140"
    ],
    '14': [
        "0104000050",
        "01040000110", # Typo? 0104000110
        "01040000120", # Typo? 0104000120
        "01040000130"  # Typo? 0104000130
    ],
    '26': ["0106000011"],
    '30': [
        "0106000041",
        "0106000050",
        "0106000051",
        "0106000052",
        "0106000053",
        "0106000055",
        "0106000056"
    ],
    '31': [
        "0109000030",
        "0109000050",
        "0109000060",
        "0109000070",
        "01090000150", # Typo? 0109000150
        "0109000200"
    ],
    '34': [
        "0109000001",
        "0109000003",
        "0109000004",
        "0109000005",
        "0109000006",
        "0109000007",
        "0109000008",
        "0109000009",
        "0109000020",
        "0109000025"
    ],
    '39': [ # This mapping will need to be re-evaluated based on current/non-current split for CEE pos 39
        "0110", # Assuming this maps to current portion of '39'
        "0111",
        "0112",
        "0113",
        "0114000010",
        "0116"
    ],
    # Need to consider '39.NCA' if automotive codes distinguish maturity for CEE 39
    '43': [ # Similarly for CEE pos 43
        "0130000001",
        "0130000002",
        "0130000004",
        "0130000007",
        "0130000035",
        "0130000060",
        "0130000072",
        "0130000100",
        "0130000110",
        "0130000130",
        "0130000131",
        "0130000140",
        "0130000150",
        "0130000161",
        "0130000300",
        "0130000310",
        "0130000315"
    ],
    # Need to consider '43.NCA'
    '45': [ # Similarly for CEE pos 45
        "0130000005",
        "0130000020",
        "0130000021",
        "0130000023",
        "0130000025",
        "0130000205",
        "0130000230",
        "0130000240",
        "0130000241",
        "0130000260",
        "0130000350",
        "0130000512",
        "0130000600",
        "0130000601",
        "0130000602"
    ],
    # Need to consider '45.NCA'
    # Also for 40, 41, 42, 44 if they had mappings
    '49': [
        "0153000001",
        "0153000002",
        "0153000003",
        "0153000007",
        "0153000008",
        "0153000009",
        "0153000011",
        "0153000012",
        "0153000014",
        "0153000015",
        "0153000016",
        "0153000020",
        "0153000030",
        "0153000031",
        "0153000032",
        "0153000033",
        "0153000037",
        "0153000040",
        "0153000051",
        "0153000052",
        "0153000053"
    ],
    '50': [
        "0150000001",
        "0150000002",
        "0151000001",
        "0151000002",
        "0151000031",
        "0152000007"
    ],
    '51': [
        "0160000010",
        "0160000025",
        "0160000030",
        "0160000040",
        "0160000042",
        "0160000045",
        "0160000060",
        "0160000070",
        "0160000075"
    ],
    '52': ["0310000010"],
    '54': ["0320000010"],
    '55': ["0320000041"],
    '56': ["0320000020"],
    '57': ["0320000021"],
    '58': ["0320000060"],
    '68': ["0210000011"], # Fondi per quiescenza e obblighi simili
    '73': [ # Debiti v Banche OLTRE 12m
        "0220000020",
        "0220000030",
        "0220000031",
        "0220000040",
        "0220000044",
        "0220000050",
        "0220000060",
        "0220000065",
        "0220000090"
    ],
    '79': [ # Debiti v Fornitori ENTRO 12m
        "0235",
        "0241"
    ],
    '80': [ # Debiti v Banche ENTRO 12m
        "0270000001",
        "0270000005",
        "0270000006",
        "0270000010",
        "0270000012",
        "0270000013",
        "0270000014",
        "0270000015",
        "0270000016"
    ],
    '81': [ # Debiti v Altri Finanziatori ENTRO 12m
        "0271000001",
        "0271000002",
        "0271000004",
        "0271000005",
        "0271000014",
        "0271000015",
        "0271000016",
        "0271000018",
        "0271000022",
        "0271000025",
        "0271000026"
    ],
    '85': [ # Debiti Tributari (assuming current portion if not split in automotive codes)
        "0230000020",
        "0230000054",
        "0230000060",
        "0230000061",
        "0230000100",
        "0230000130",
        "0230000154",
        "0230000155"
    ],
    '86': [ # Debiti v Istituti Previdenza (assuming current)
        "0230000070",
        "0230000090",
        "0230000160",
        "0230000180",
        "0230000185"
    ],
    '87': [ # Altri Debiti (assuming current)
        "02300000120", # Typo? 0230000120
        "0230000201",
        "0230000202",
        "0230000205",
        "0230000206",
        "0230000210",
        "0230000211",
        "0230000212",
        "0230000214",
        "0230000216",
        "0231"
    ],
    '88': [ # Risconti Passivi
        "0260000020",
        "0260000060",
        "0260000080",
        "0260000085"
    ],
    '100': [ # TFR
        "0210000010",
        "0210000051",
        "0210000053",
        "0210000054",
        "0210000055",
        "0210000056"
    ]
}

AVAILABLE_MAPPINGS = {
    "automotive_dealer": {
        "display_name": "Automotive Dealer (Esempio)",
        "data_variable_name": "CEE_TO_AUTOMOTIVE_CODES" # Points to the dict above
    }
}

# Define _kpi_req_total_assets before it's used by POS_TOTAL_ASSETS
_kpi_req_total_assets_constituents = (
    [str(x) for x in get_all_positions(BALANCE_SHEET_STRUCTURE['assets']['non_current_assets']) if "(Placeholder" not in POSITION_NAMES.get(str(x), "")] +
    [str(x) for x in get_all_positions(BALANCE_SHEET_STRUCTURE['assets']['current_assets']) if "(Placeholder" not in POSITION_NAMES.get(str(x), "")] +
    [str(x) for x in get_all_positions(BALANCE_SHEET_STRUCTURE['assets']['prepaid_expenses_and_accrued_income']) if "(Placeholder" not in POSITION_NAMES.get(str(x), "")]
)
_kpi_req_total_assets = sorted(list(set(_kpi_req_total_assets_constituents)))

# KPI position lists for calculation (already in constants.py but ensuring they are here)
POS_CURRENT_ASSETS = [31, 32, 33, 34, 35, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50]
POS_LIQUID_ASSETS = [39, 40, 41, 42, 43, 45]
POS_CASH = [49, 50]
POS_CURRENT_LIABILITIES = [79, 80, 81, 82, 83, 84, 85, 86, 87, 88]
POS_TOTAL_LIABILITIES = [67, 68, 69, 100, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88]
POS_TOTAL_EQUITY = [52, 53, 54, 55, 56, 57, 58, 59, 64, 65, 66]
POS_TOTAL_ASSETS = _kpi_req_total_assets # Use the dynamically generated list

# Dynamically define POS_ lists based on BALANCE_SHEET_STRUCTURE for clarity and maintainability
_temp_imm_immat = get_all_positions(BALANCE_SHEET_STRUCTURE['assets']['non_current_assets']['intangible_assets'])
POS_IMMOBILIZZAZIONI_IMMATERIALI = sorted([str(x) for x in _temp_imm_immat if "(Placeholder" not in POSITION_NAMES.get(str(x), "")])

_temp_imm_mat = get_all_positions(BALANCE_SHEET_STRUCTURE['assets']['non_current_assets']['tangible_assets'])
POS_IMMOBILIZZAZIONI_MATERIALI = sorted([str(x) for x in _temp_imm_mat if "(Placeholder" not in POSITION_NAMES.get(str(x), "")])

# POS_IMMOBILIZZAZIONI_FINANZIARIE does not have placeholders in its typical range 26-30, so no filter needed here, but ensure it's stringified
POS_IMMOBILIZZAZIONI_FINANZIARIE = [str(x) for x in get_all_positions(BALANCE_SHEET_STRUCTURE['assets']['non_current_assets']['financial_investments_non_current'])]

POS_IMMOBILIZZAZIONI_NETTE = sorted(list(set(
    POS_IMMOBILIZZAZIONI_IMMATERIALI + # Already filtered and stringified
    POS_IMMOBILIZZAZIONI_MATERIALI +   # Already filtered and stringified
    POS_IMMOBILIZZAZIONI_FINANZIARIE # Already stringified
)))

POS_DEBITI_TRIBUTARI = [str(x) for x in BALANCE_SHEET_STRUCTURE['equity_liabilities']['liabilities']['tax_payables']]
POS_DEBITI_PREVIDENZIALI = [str(x) for x in BALANCE_SHEET_STRUCTURE['equity_liabilities']['liabilities']['social_security_payables']]

# New POS list for Long-term Debt
POS_DEBITI_OLTRE_12_MESI = sorted(list(set(
    BALANCE_SHEET_STRUCTURE['equity_liabilities']['liabilities']['bonds_issued'] + 
    BALANCE_SHEET_STRUCTURE['equity_liabilities']['liabilities']['convertible_bonds_issued'] + 
    BALANCE_SHEET_STRUCTURE['equity_liabilities']['liabilities']['amounts_owed_to_shareholders_for_loans'] + 
    [BALANCE_SHEET_STRUCTURE['equity_liabilities']['liabilities']['amounts_owed_to_banks'][0]] + # Index 0 for long-term part
    [BALANCE_SHEET_STRUCTURE['equity_liabilities']['liabilities']['amounts_owed_to_other_lenders'][0]] + # Index 0 for long-term part
    [BALANCE_SHEET_STRUCTURE['equity_liabilities']['liabilities']['debt_represented_by_credit_instruments'][0]] + # Index 0 for long-term part
    [BALANCE_SHEET_STRUCTURE['equity_liabilities']['liabilities']['amounts_owed_to_group_companies'][0]] # Index 0 for long-term part
)))

# New POS list for Current Financial Assets
POS_ATTIVITA_FINANZIARIE_CORRENTI = [str(x) for x in get_all_positions(BALANCE_SHEET_STRUCTURE['assets']['current_assets']['current_financial_assets'])]

# Re-populate KPI_REQUIREMENTS with the new POS_ lists for accuracy
# Ensure these lists are flat lists of unique integers.
_kpi_req_current_assets = [31, 32, 33, 34, 35, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50]
_kpi_req_liquid_assets = [39, 40, 41, 42, 43, 45]
_kpi_req_cash = [49, 50]
_kpi_req_current_liabilities = [79, 80, 81, 82, 83, 84, 85, 86, 87, 88]
_kpi_req_total_liabilities = [67, 68, 69, 100, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88]
_kpi_req_total_equity = [52, 53, 54, 55, 56, 57, 58, 59, 64, 65, 66]

KPI_REQUIREMENTS = {
    'current_ratio': sorted(list(set([str(x) for x in POS_CURRENT_ASSETS] + [str(y) for y in POS_CURRENT_LIABILITIES]))),
    'quick_ratio': sorted(list(set( [str(x) for x in POS_LIQUID_ASSETS] + [str(x) for x in POS_CASH] + POS_ATTIVITA_FINANZIARIE_CORRENTI + [str(x) for x in POS_CURRENT_LIABILITIES] ))),
    'cash_ratio': sorted(list(set([str(x) for x in POS_CASH] + [str(y) for y in POS_CURRENT_LIABILITIES]))),
    'debt_to_equity': sorted(list(set([str(x) for x in POS_TOTAL_LIABILITIES] + [str(y) for y in POS_TOTAL_EQUITY]))),
    'debt_ratio': sorted(list(set([str(x) for x in POS_TOTAL_LIABILITIES] + [str(y) for y in POS_TOTAL_ASSETS]))),
    'working_capital': sorted(list(set([str(x) for x in POS_CURRENT_ASSETS] + [str(y) for y in POS_CURRENT_LIABILITIES]))),
    'asset_rigidity_index': sorted(list(set([str(x) for x in POS_IMMOBILIZZAZIONI_NETTE] + [str(y) for y in POS_TOTAL_ASSETS]))),
    'asset_elasticity_index': sorted(list(set([str(x) for x in POS_CURRENT_ASSETS] + [str(y) for y in POS_TOTAL_ASSETS]))),
    'fixed_asset_coverage_ratio': sorted(list(set([str(x) for x in POS_TOTAL_EQUITY] + [str(y) for y in POS_IMMOBILIZZAZIONI_NETTE]))),
    'tax_social_debt_on_assets_ratio': sorted(list(set([str(x) for x in POS_DEBITI_TRIBUTARI] + [str(y) for y in POS_DEBITI_PREVIDENZIALI] + [str(z) for z in POS_TOTAL_ASSETS]))),
    'tangible_net_worth': sorted(list(set([str(x) for x in POS_TOTAL_EQUITY] + [str(y) for y in POS_IMMOBILIZZAZIONI_IMMATERIALI]))),
    'equity_multiplier': sorted(list(set([str(x) for x in POS_TOTAL_ASSETS] + [str(y) for y in POS_TOTAL_EQUITY]))),
    'long_term_debt_to_equity': sorted(list(set([str(x) for x in POS_DEBITI_OLTRE_12_MESI] + [str(y) for y in POS_TOTAL_EQUITY]))),
    'intangible_assets_ratio': sorted(list(set([str(x) for x in POS_IMMOBILIZZAZIONI_IMMATERIALI] + [str(y) for y in POS_TOTAL_ASSETS]))),
    'financial_assets_ratio': sorted(list(set(
        [str(x) for x in POS_IMMOBILIZZAZIONI_FINANZIARIE] +
        [str(x) for x in POS_ATTIVITA_FINANZIARIE_CORRENTI] +
        [str(x) for x in POS_TOTAL_ASSETS]
    ))),
    'non_current_assets_coverage': sorted(list(set(
        [str(x) for x in POS_TOTAL_EQUITY] +
        [str(x) for x in POS_DEBITI_OLTRE_12_MESI] +
        [str(x) for x in POS_IMMOBILIZZAZIONI_NETTE]
    ))),
    'net_working_capital_ratio': sorted(list(set([str(x) for x in POS_CURRENT_ASSETS] + [str(y) for y in POS_CURRENT_LIABILITIES] + [str(z) for z in POS_TOTAL_ASSETS])))
}

# New: Total Liabilities Excluding TFR (pos '100')
POS_TOTAL_LIABILITIES_EXCL_TFR = sorted([str(p) for p in POS_TOTAL_LIABILITIES if str(p) != '100'])

# Update KPIs that exclude TFR
KPI_REQUIREMENTS['debt_to_equity_excl_tfr'] = sorted(list(set([str(x) for x in POS_TOTAL_LIABILITIES_EXCL_TFR] + [str(y) for y in POS_TOTAL_EQUITY])))
KPI_REQUIREMENTS['debt_ratio_excl_tfr'] = sorted(list(set([str(x) for x in POS_TOTAL_LIABILITIES_EXCL_TFR] + [str(y) for y in POS_TOTAL_ASSETS])))

# Exported for calculator.py (ensure all needed are here)
__all__ = [
    'BALANCE_SHEET_STRUCTURE', 'ALL_POSITIONS', 'KPI_REQUIREMENTS', 'AVAILABLE_KPIS',
    'POSITION_NAMES', 'SECTION_TITLES', 'CEE_TO_AUTOMOTIVE_CODES', 'AVAILABLE_MAPPINGS',
    'get_all_positions',
    # Main POS lists
    'POS_CURRENT_ASSETS', 'POS_LIQUID_ASSETS', 'POS_CASH',
    'POS_CURRENT_LIABILITIES', 'POS_TOTAL_LIABILITIES', 'POS_TOTAL_EQUITY',
    'POS_TOTAL_ASSETS',
    # Dynamically defined POS lists
    'POS_IMMOBILIZZAZIONI_IMMATERIALI', 'POS_IMMOBILIZZAZIONI_MATERIALI',
    'POS_IMMOBILIZZAZIONI_FINANZIARIE', 'POS_IMMOBILIZZAZIONI_NETTE',
    'POS_DEBITI_TRIBUTARI', 'POS_DEBITI_PREVIDENZIALI',
    'POS_DEBITI_OLTRE_12_MESI', 'POS_DEBITI_FINANZIARI_OLTRE_12_MESI',
    'POS_ATTIVITA_FINANZIARIE_CORRENTI',
    'POS_TOTAL_LIABILITIES_EXCL_TFR'
] 