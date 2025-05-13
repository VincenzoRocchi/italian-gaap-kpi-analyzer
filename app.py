from flask import Flask, render_template, request, session, redirect, url_for, flash
import os
from datetime import datetime # Import datetime
import json

app = Flask(__name__)
# Secret key for session management. Replace with a strong, random key in production.
app.secret_key = os.urandom(24)

# Context Processor to make datetime available in templates
@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()} # Use utcnow for consistency

# Define the structure based on CEE positions (Art. 2424 Codice Civile)
BALANCE_SHEET_STRUCTURE = {
    'assets': {
        # A) Crediti verso soci per versamenti ancora dovuti
        'due_from_shareholders': [], # Placeholder, as no specific 1-88 pos typically assigned here
        # B) Immobilizzazioni
        'non_current_assets': { # B) (Kept key 'non_current_assets' for consistency, maps to B)
            'intangible_assets': list(range(1, 11)),        # B.I
            'tangible_assets': list(range(11, 26)),          # B.II
            'financial_investments_non_current': list(range(26, 31)) # B.III
        },
        # C) Attivo Circolante
        'current_assets': { # C) (Kept key 'current_assets')
            'inventories': list(range(31, 39)),              # C.I
            'trade_and_other_receivables': list(range(39, 45)), # C.II
            'current_financial_assets': list(range(46, 49)), # C.III
            'cash_and_cash_equivalents': list(range(49, 51)) # C.IV
        },
        # D) Ratei e Risconti Attivi
        'prepaid_expenses_and_accrued_income': [51] # D)
    },
    'equity_liabilities': {
        # A) Patrimonio Netto
        'equity': { # A)
            'capital_social': [52],                             # A.I Capitale Sociale
            # Pos 53 "Fondo di dotazione" - can be added if needed, often for specific entity types.
            'share_premium_reserve': [54],                      # A.II Riserva da sovrapprezzo azioni
            'revaluation_reserve': [55],                        # A.III Riserve di rivalutazione
            'legal_reserve': [56],                              # A.IV Riserva legale
            'statutory_reserves': [57],                         # A.V Riserve statutarie
            'other_reserves': [58],                             # A.VI Altre riserve (can include 53, 59-63 concepts)
            # A.VII Riserva per operazioni di copertura dei flussi finanziari attesi - often in Altre riserve or requires specific new pos if available
            'retained_earnings_or_accumulated_loss_bf': [64],   # A.VIII Utili (perdite) portati a nuovo
            'profit_or_loss_for_the_year': [65],                # A.IX Utile (perdita) dell'esercizio
            'negative_reserve_for_treasury_shares': [66]        # A.X Riserva negativa per azioni proprie in portafoglio
        },
        # B) Fondi per Rischi e Oneri
        'provisions_for_risks_and_charges': list(range(67, 70)), # B)
        # C) Trattamento di Fine Rapporto di Lavoro Subordinato
        'employee_severance_indemnity_tfr': [100], # C) Assigned custom position 100 (Non-CEE standard)
        # D) Debiti
        'liabilities': { # D)
            'bonds_issued': [70],                               # D.1 Obbligazioni (non-convertible)
            'convertible_bonds_issued': [71],                   # D.2 Obbligazioni Convertibili
            'amounts_owed_to_shareholders_for_loans': [72],     # D.3 Debiti verso soci per finanziamenti
            'amounts_owed_to_banks': [73, 80],                  # D.4 Debiti verso banche (73 > 1yr, 80 <= 1yr)
            'amounts_owed_to_other_lenders': [74, 81],          # D.5 Debiti verso altri finanziatori (74 > 1yr, 81 <= 1yr)
            'advances_received_from_customers': [75, 82],       # D.6 Acconti da clienti (75 > 1yr, 82 <= 1yr)
            'trade_payables': [76, 79],                         # D.7 Debiti verso fornitori (76 > 1yr, 79 <= 1yr)
            'debt_represented_by_credit_instruments': [77, 83], # D.8 Debiti rappresentati da titoli di credito (77 > 1yr, 83 <= 1yr)
            'amounts_owed_to_group_companies': [78, 84],        # D.9 Debiti verso imprese del gruppo (parent, subs, assoc.) (78 > 1yr, 84 <= 1yr)
            # D.10, D.11, D.12 for specific controlled, associated, parent co if not aggregated in D.9
            'tax_payables': [85],                               # D.13 Debiti tributari (assuming this refers to the specific CEE/It number)
            'social_security_payables': [86],                   # D.14 Debiti verso istituti di previdenza (assuming CEE/It number)
            'other_payables': [87]                              # D.15 Altri debiti (assuming CEE/It number)
        },
        # E) Ratei e Risconti Passivi
        'accrued_expenses_and_deferred_income': [88] # E)
    }
}

# Helper to get all position numbers - needs adjustment for nested structure
def get_all_positions(structure_part):
    positions = []
    if isinstance(structure_part, dict):
        for key, value in structure_part.items():
            positions.extend(get_all_positions(value)) # Recurse for dictionaries
    elif isinstance(structure_part, list):
        # Check if list contains integers (positions) or other types
        if all(isinstance(item, int) for item in structure_part):
             positions.extend(structure_part) # Extend if it's a list of positions
    # Ignore other types or empty structures
    return sorted(list(set(positions))) # Return unique sorted positions

ALL_POSITIONS = get_all_positions(BALANCE_SHEET_STRUCTURE)

# Map KPIs to the positions they require (UPDATED for new structure)
KPI_REQUIREMENTS = {
    'current_ratio': 
        [31, 32, 33, 34, 35] + # Inventories (excluding placeholders)
        [39, 40, 41, 42, 43, 44, 45] + # Receivables
        [46, 47, 48] + # Current Fin Assets
        [49, 50] + # Cash
        [79, 80, 81, 82, 83, 84, 85, 86, 87, 88], # Current Liabilities
    'quick_ratio': 
        [39, 40, 41, 42, 43, 44, 45] + # Receivables
        [46, 47, 48] + # Current Fin Assets
        [49, 50] + # Cash
        [79, 80, 81, 82, 83, 84, 85, 86, 87, 88], # Current Liabilities
    'cash_ratio': 
        [49, 50] + # Cash
        [79, 80, 81, 82, 83, 84, 85, 86, 87, 88], # Current Liabilities
    'debt_to_equity': 
        [67, 68, 69] + # Provisions
        [100] + # TFR (Custom Position)
        [70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87] + # All Debts
        [88] + # Accrued Liab
        [52, 54, 55, 56, 57, 58, 59, 64, 65, 66], # Equity (excluding placeholders)
    'debt_ratio': 
        [67, 68, 69] + # Provisions
        [100] + # TFR (Custom Position)
        [70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87] + # All Debts
        [88] + # Accrued Liab
        [1, 2, 3, 4, 5, 6, 7] + # Intangible Assets (excluding placeholders)
        [11, 12, 13, 14, 15] + # Tangible Assets (excluding placeholders)
        [26, 27, 28, 29, 30] + # Financial Investments
        [31, 32, 33, 34, 35] + # Inventories (excluding placeholders)
        [39, 40, 41, 42, 43, 44, 45] + # Receivables
        [46, 47, 48] + # Current Fin Assets
        [49, 50] + # Cash
        [51], # Prepaid Exp / Accrued Inc
    'working_capital': 
        [31, 32, 33, 34, 35] + # Inventories (excluding placeholders)
        [39, 40, 41, 42, 43, 44, 45] + # Receivables
        [46, 47, 48] + # Current Fin Assets
        [49, 50] + # Cash
        [79, 80, 81, 82, 83, 84, 85, 86, 87, 88], # Current Liabilities
}

# Temporary static definition of available KPIs (Tier 1 for now)
# Ideally, this would be generated dynamically or from a config
AVAILABLE_KPIS = {
    'current_ratio': {
        'name_display': "Indice di Liquidità Corrente",
        'description_short': "Misura la capacità di coprire le passività a breve termine con le attività correnti.",
        'is_ratio': True,
        'tooltip_info': {
            'full_explanation': "Il Current Ratio confronta le attività che possono essere convertite in cassa entro un anno con le passività che devono essere pagate entro un anno. È un indicatore chiave della solvibilità a breve termine di un\'azienda.",
            'formula_display': "Attività Correnti / Passività Correnti",
            'optimal_range_cee': "1.2 - 2.0 (manifatturiero), 0.8 - 1.5 (servizi). Varia per settore.",
            'interpretation_notes': "Un valore > 1 indica che l\'azienda ha più attività correnti che passività correnti. Un valore troppo alto potrebbe indicare un uso inefficiente degli asset.",
            'required_inputs_display': "Attività Correnti (Rimanenze, Crediti, Titoli, Liquidità), Passività Correnti (Debiti a breve termine)"
        }
    },
    'quick_ratio': {
        'name_display': "Indice di Liquidità Immediata (Acid Test)",
        'description_short': "Misura la capacità di coprire le passività a breve termine con le attività più liquide.",
        'is_ratio': True,
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
        'tooltip_info': {
            'full_explanation': "È l\'indicatore di liquidità più conservativo, considera solo cassa e equivalenti di cassa rispetto alle passività correnti.",
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
        'tooltip_info': {
            'full_explanation': "Misura la leva finanziaria di un\'azienda, confrontando il totale dei debiti con il patrimonio netto. Un rapporto elevato può indicare un maggior rischio.",
            'formula_display': "Totale Passività / Patrimonio Netto",
            'optimal_range_cee': "Banche: 8-12 (regolamentato), Manifatturiero: 0.3-0.8, Servizi: 0.2-0.6. Varia molto per settore.",
            'interpretation_notes': "Un rapporto più basso è generalmente preferibile. Un rapporto > 1 significa che l\'azienda è finanziata più da debiti che da capitale proprio.",
            'required_inputs_display': "Fondi rischi e oneri, Debiti (L/T e B/T), Risconti Passivi, Patrimonio Netto (Capitale, Riserve, Risultato)"
        }
    },
    'debt_ratio': {
        'name_display': "Rapporto di Indebitamento Totale",
        'description_short': "Indica la percentuale di attivi finanziati tramite debito.",
        'is_ratio': True,
        'tooltip_info': {
            'full_explanation': "Mostra quale proporzione degli asset di un\'azienda è finanziata attraverso il debito.",
            'formula_display': "Totale Passività / Totale Attivo",
            'optimal_range_cee': "Generalmente < 0.6 per aziende stabili. Dipende dal settore e dalla fase del ciclo di vita dell\'azienda.",
            'interpretation_notes': "Un rapporto più basso indica minore dipendenza dal debito. Un rapporto > 1 significa che l\'azienda ha più debiti che attivi (improbabile per aziende sane).",
            'required_inputs_display': "Fondi rischi e oneri, Debiti (L/T e B/T), Risconti Passivi, Tutte le categorie di Attivo"
        }
    },
    'working_capital': {
        'name_display': "Capitale Circolante Netto",
        'description_short': "Differenza tra attività correnti e passività correnti.",
        'is_ratio': False,
        'tooltip_info': {
            'full_explanation': "Rappresenta le risorse finanziarie disponibili per le operazioni quotidiane di un\'azienda dopo aver coperto gli obblighi a breve termine.",
            'formula_display': "Attività Correnti - Passività Correnti",
            'optimal_range_cee': "Positivo è generalmente buono. Un valore negativo persistente può indicare problemi di liquidità.",
            'interpretation_notes': "Un capitale circolante positivo indica che l\'azienda può finanziare le sue operazioni correnti e investire in attività future. Non è un rapporto, ma un valore assoluto.",
            'required_inputs_display': "Attività Correnti, Passività Correnti"
        }
    }
}

# Map position numbers to Italian names (Aligned with Art. 2424 C.C. based on analysis)
POSITION_NAMES = {
    # Attivo - Immobilizzazioni - Immateriali (1-10)
    1: "Costi di impianto e di ampliamento",
    2: "Costi di sviluppo",
    3: "Diritti di brevetto industriale e diritti di utilizzazione delle opere dell'ingegno",
    4: "Concessioni, licenze, marchi e diritti simili",
    5: "Avviamento",
    6: "Immobilizzazioni in corso e acconti",
    7: "Altre immobilizzazioni immateriali",
    8: "(Non standard C.C. - Placeholder 8)",
    9: "(Non standard C.C. - Placeholder 9)",
    10: "(Non standard C.C. - Placeholder 10)",
    # Attivo - Immobilizzazioni - Materiali (11-25)
    11: "Terreni e fabbricati",
    12: "Impianti e macchinario",
    13: "Attrezzature industriali e commerciali",
    14: "Altri beni",
    15: "Immobilizzazioni in corso e acconti",
    16: "(Non standard C.C. - Placeholder 16)",
    17: "(Non standard C.C. - Placeholder 17)",
    18: "(Non standard C.C. - Placeholder 18)",
    19: "(Non standard C.C. - Placeholder 19)",
    20: "(Non standard C.C. - Placeholder 20)",
    21: "(Non standard C.C. - Placeholder 21)",
    22: "(Non standard C.C. - Placeholder 22)",
    23: "(Non standard C.C. - Placeholder 23)",
    24: "(Non standard C.C. - Placeholder 24)",
    25: "(Non standard C.C. - Placeholder 25)",
    # Attivo - Immobilizzazioni - Finanziarie (Partecipazioni) (26-30)
    26: "Partecipazioni in imprese controllate",
    27: "Partecipazioni in imprese collegate",
    28: "Partecipazioni in imprese controllanti",
    29: "Altre partecipazioni",
    30: "Altri titoli immobilizzati",
    # Attivo - Circolante - Rimanenze (31-38)
    31: "Materie prime, sussidiarie e di consumo",
    32: "Prodotti in corso di lavorazione e semilavorati",
    33: "Lavori in corso su ordinazione",
    34: "Prodotti finiti e merci",
    35: "Acconti", # Corrected name for advances/prepayments on inventory
    36: "(Non standard C.C. - Rimanenze Placeholder 36)",
    37: "(Non standard C.C. - Rimanenze Placeholder 37)",
    38: "(Non standard C.C. - Rimanenze Placeholder 38)",
    # Attivo - Circolante - Crediti (39-45)
    39: "Crediti verso clienti",
    40: "Crediti verso imprese controllate",
    41: "Crediti verso imprese collegate",
    42: "Crediti verso imprese controllanti",
    43: "Crediti tributari", # Refined terminology (Imposte anticipate is Pos 44)
    44: "Imposte anticipate", # Standard position, distinct from 43
    45: "Crediti verso altri",
    # Attivo - Circolante - Titoli (Attività finanziarie non immobilizzate) (46-48)
    46: "Partecipazioni in altre imprese",
    47: "Altri titoli",
    48: "Strumenti finanziari derivati attivi",
    # Attivo - Circolante - Liquidità (Disponibilità liquide) (49-50)
    49: "Depositi bancari e postali",
    50: "Assegni e denaro in cassa",
    # Attivo - Risconti Attivi (51)
    51: "Risconti attivi",
    # Passivo - Patrimonio Netto - Capitale (52-58)
    52: "Capitale sociale",
    53: "Fondo di dotazione",
    54: "Riserva da sovrapprezzo delle azioni", # Corrected spelling
    55: "Riserve di rivalutazione",
    56: "Riserva legale",
    57: "Riserve statutarie",
    58: "Altre riserve, distintamente indicate", # Corrected to match C.C. more closely
    # Passivo - Patrimonio Netto - Riserve (59-63)
    59: "Riserva per operazioni di copertura di flussi finanziari attesi", # Added specific reserve
    60: "(Non standard C.C. - Riserve Placeholder 60)",
    61: "(Non standard C.C. - Riserve Placeholder 61)",
    62: "(Non standard C.C. - Riserve Placeholder 62)",
    63: "(Non standard C.C. - Riserve Placeholder 63)",
    # Passivo - Patrimonio Netto - Risultato (64-66)
    64: "Utili (perdite) portati a nuovo",
    65: "Utile (perdita) dell'esercizio",
    66: "Riserva negativa per azioni proprie in portafoglio",
    # Passivo - Fondi Rischi e Oneri (67-69)
    67: "Fondi per imposte, anche differite",
    68: "Fondi per quiescenza e obblighi simili",
    69: "Altri fondi",
    # Passivo - TFR (Implicitly between 69 and 70 in standard layout)
    # Position number assignment varies, often handled separately
    # Passivo - Debiti - Lungo Termine (70-78 - Analytical grouping, mapping needed)
    70: "Obbligazioni",
    71: "Obbligazioni convertibili",
    72: "Debiti verso soci per finanziamenti",
    73: "Debiti verso banche (oltre 12 mesi)",
    74: "Debiti verso altri finanziatori (oltre 12 mesi)",
    75: "Acconti da clienti (oltre 12 mesi)",
    76: "Debiti verso fornitori (oltre 12 mesi)",
    77: "Debiti rappresentati da titoli di credito (oltre 12 mesi)",
    78: "Debiti verso imprese controllate/collegate/controllanti (oltre 12 mesi)", # Aggregated
    # Passivo - Debiti - Breve Termine (79-87 - Analytical grouping, mapping needed)
    79: "Debiti verso fornitori (entro 12 mesi)",
    80: "Debiti verso banche (entro 12 mesi)",
    81: "Debiti verso altri finanziatori (entro 12 mesi)",
    82: "Acconti da clienti (entro 12 mesi)",
    83: "Debiti rappresentati da titoli di credito (entro 12 mesi)",
    84: "Debiti verso imprese controllate/collegate/controllanti (entro 12 mesi)", # Aggregated
    85: "Debiti tributari",
    86: "Debiti verso istituti di previdenza e sicurezza sociale",
    87: "Altri debiti (entro 12 mesi)",
    # Passivo - Risconti Passivi (88)
    88: "Risconti passivi",
    # Custom Positions (Non-CEE)
    100: "Trattamento di fine rapporto di lavoro subordinato" # Added for TFR
}

# Mapping for section titles displayed on input page
SECTION_TITLES = {
    # Main Categories
    'assets': "ATTIVO",
    'equity_liabilities': "PASSIVO E PATRIMONIO NETTO",

    # Assets
    'due_from_shareholders': "A) Crediti verso soci per versamenti ancora dovuti",
    'non_current_assets': "B) Immobilizzazioni", # Changed from 'non_current'
    'intangible_assets': "B.I) Immobilizzazioni Immateriali", # Changed from 'intangible'
    'tangible_assets': "B.II) Immobilizzazioni Materiali", # Changed from 'tangible'
    'financial_investments_non_current': "B.III) Immobilizzazioni Finanziarie", # Changed from 'investments' or 'financial_investments'
    
    'current_assets': "C) Attivo Circolante", # Changed from 'current'
    'inventories': "C.I) Rimanenze", # Changed from 'inventory'
    'trade_and_other_receivables': "C.II) Crediti", # Changed from 'receivables'
    'current_financial_assets': "C.III) Attività Finanziare che non costituiscono immobilizzazioni", # Changed from 'securities'
    'cash_and_cash_equivalents': "C.IV) Disponibilità Liquide", # Changed from 'cash'
    
    'prepaid_expenses_and_accrued_income': "D) Ratei e Risconti Attivi", # Changed from 'prepaid' or 'prepaid_accrued_assets'

    # Equity & Liabilities
    'equity': "A) Patrimonio Netto",
    'capital_social': "A.I) Capitale Sociale",
    'share_premium_reserve': "A.II) Riserva da sovrapprezzo azioni",
    'revaluation_reserve': "A.III) Riserve di rivalutazione",
    'legal_reserve': "A.IV) Riserva legale",
    'statutory_reserves': "A.V) Riserve statutarie",
    'other_reserves': "A.VI) Altre riserve, distintamente indicate",
    # 'specific_hedging_reserve': "A.VII) Riserva per operazioni di copertura dei flussi finanziari attesi", # If added as a separate key
    'retained_earnings_or_accumulated_loss_bf': "A.VIII) Utili (perdite) portati a nuovo",
    'profit_or_loss_for_the_year': "A.IX) Utile (perdita) dell'esercizio",
    'negative_reserve_for_treasury_shares': "A.X) Riserva negativa per azioni proprie in portafoglio",

    'provisions_for_risks_and_charges': "B) Fondi per Rischi e Oneri", # Changed from 'provisions'
    'employee_severance_indemnity_tfr': "C) Trattamento di Fine Rapporto di Lavoro Subordinato", # NEW

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
    'tax_payables': "D.12) Debiti tributari", # Standard Italian Civil code uses D.12 for Tax (after D.9 group, D.10 related parties, D.11 other related parties)
    'social_security_payables': "D.13) Debiti verso istituti di previdenza e sicurezza sociale", # D.13 for social security
    'other_payables': "D.14) Altri debiti", # D.14 for other payables

    'accrued_expenses_and_deferred_income': "E) Ratei e Risconti Passivi" # Changed from 'accrued'
}

# -- Start Automotive Mapping Data --
CEE_TO_AUTOMOTIVE_CODES = {
    # CEE POSITION 1 - Costi di impianto e di ampliamento
    1: ["0102000001"],
    # CEE POSITION 2 - Costi di sviluppo 
    2: ["0102000005"],
    # CEE POSITION 4 - Concessioni, licenze, marchi e diritti simili
    4: ["0102000008"],
    # CEE POSITION 5 - Avviamento
    5: ["0102000010"],
    # CEE POSITION 7 - Altre immobilizzazioni immateriali
    7: [
        "0102000030",  # SOFTWARE E PROGRAMMI
        "0102000040",  # MIGLIORIE SU IMMOBILI (various locations)
        "0102000041",
        "0102000042", 
        "0102000043",
        "0102000044",
        "0102000045",
        "0102000050",  # SPESE PLURIENNALI
        "0102000051",  # INSEGNE VARIE
        "0102000052"   # PAGINE INTERNET / WEB
    ],
    # CEE POSITION 12 - Impianti e macchinario
    12: [
        "0104000070",  # MACCHINE ELETTRONICHE
        "0104000090",  # IMPIANTI
        "0104000092",  # IMPIANTI COMUNICAZ E TELEF.
        "0104000095"   # IMPIANTO FOTOVOLTAICO
    ],
    # CEE POSITION 13 - Attrezzature industriali e commerciali
    13: [
        "0104000015",  # ATTREZZATURE
        "0104000020",  # ATTREZZATURE OFFICINE
        "0104000021",  # ATTREZZATURE OFFICINA (various locations)
        "0104000022",
        "0104000023",
        "0104000080",  # ATTREZZATURE MINUTE
        "0104000100",  # ATTREZZATURE SPECIFICHE OFFICINE
        "0104000140"   # ATTREZZATURE VARIE CARROZZERIA
    ],
    # CEE POSITION 14 - Altri beni
    14: [
        "0104000050",  # AUTOVEICOLI DI SERVIZIO
        "0104000110",  # MOBILI E ARREDI
        "0104000120",  # TELEFONI PORTATILI
        "0104000130"   # BENI INTERAMENTE AMMORTIZ./ANNO
    ],
    # CEE POSITION 26 - Partecipazioni in imprese controllate
    26: ["0106000011"],
    # CEE POSITION 30 - Altri titoli immobilizzati
    30: [
        "0106000041",  # DEPOSITI CAUZIONALI (various types)
        "0106000050",
        "0106000051",
        "0106000052",
        "0106000053",
        "0106000055",
        "0106000056"
    ],
    # CEE POSITION 31 - Materie prime, sussidiarie e di consumo
    31: [
        "0109000030",  # RIMANENZE ACCESSORI (various brands)
        "0109000050",
        "0109000060",
        "0109000070",
        "0109000150",
        "0109000200"   # RIMANENZE MAT. CONSUMO
    ],
    # CEE POSITION 34 - Prodotti finiti e merci
    34: [
        "0109000001",  # RIMANENZE VEICOLI (various brands)
        "0109000003",
        "0109000004",
        "0109000005",
        "0109000006",
        "0109000007",
        "0109000008",
        "0109000009",
        "0109000020",  # RIMANENZE VEICOLI USATI
        "0109000025"
    ],
    # CEE POSITION 39 - Crediti verso clienti
    39: [
        "0110",        # CLIENTI MAGAZZINO
        "0111",        # CLIENTI OFFICINA
        "0112",        # CLIENTI VEICOLI
        "0113",        # CLIENTI VARI
        "0114000010",  # CLIENTI COOP SINCRO
        "0116"         # CLIENTI IN CONTENZIOSO
    ],
    # CEE POSITION 43 - Crediti tributari
    43: [
        "0130000001",  # CONTRIB.D.L. RILANCIO
        "0130000002",  # CONTRIB.ECOBONUS
        "0130000004",
        "0130000007",
        "0130000035",  # CREDITO IVA
        "0130000060",
        "0130000072",  # CREDITO IMPOSTA ENERGIA
        "0130000100",  # ACCONTO IRES
        "0130000110",  # ACCONTO IRAP
        "0130000130",  # RITEN. ERARIALI
        "0130000131",  # RITEN.ENASARCO
        "0130000140",
        "0130000150",  # CREDITO INAIL
        "0130000161",
        "0130000300",  # CREDITI PER CONTRIBUTI
        "0130000310",  # CREDITI D\'IMPOSTA
        "0130000315"
    ],
    # CEE POSITION 45 - Crediti verso altri
    45: [
        "0130000005",  # CREDITI STELLANTIS
        "0130000020",  # CAUZIONI ATTIVE
        "0130000021",  # CAUZIONI A FORNITORE
        "0130000023",  # DIPENDENTI C/ANTICIPI
        "0130000025",  # FCA BANK DEP.GARANZIA
        "0130000205",  # ROMEO AUTOMOTIVE
        "0130000230",  # CREDITI DIVERSI
        "0130000240",  # CREDITI PER CAUZIONI
        "0130000241",
        "0130000260",  # ANTICIPI A PERSONALE
        "0130000350",  # DECIMI CAP. SOC.
        "0130000512",  # CREDITI VERSO TRE ESSE
        "0130000600",  # CREDITI USATO
        "0130000601",
        "0130000602"
    ],
    # CEE POSITION 49 - Depositi bancari e postali
    49: [
        "0153000001",  # UNICREDIT C/C
        "0153000002",
        "0153000003",  # MPS C/C
        "0153000007",  # BANCO DESIO C/C
        "0153000008",  # SANTANDER C/C
        "0153000009",
        "0153000011",  # BANCA PSA C/C
        "0153000012",
        "0153000014",
        "0153000015",
        "0153000016",
        "0153000020",  # INTESA SAN PAOLO C/C
        "0153000030",  # UNICREDIT CARTA PREPAG.
        "0153000031",
        "0153000032",
        "0153000033",
        "0153000037",
        "0153000040",  # BANCA SELLA C/C
        "0153000051",  # B.POP.CORTONA
        "0153000052",
        "0153000053"
    ],
    # CEE POSITION 50 - Assegni e denaro in cassa
    50: [
        "0150000001",  # CASSA GENERALE
        "0150000002",  # CASSA POS
        "0151000001",  # CASSA ASSEGNI
        "0151000002",
        "0151000031",  # A.B. SMARRITI
        "0152000007"   # INC. C/TRANSITORIO
    ],
    # CEE POSITION 51 - Risconti attivi
    51: [
        "0160000010",  # RATEI ATTIVI
        "0160000025",  # RISCONTI ATTIVI
        "0160000030",
        "0160000040",  # FORNITORI C/ANTICIPI
        "0160000042",  # CAPARRE A FORNITORI
        "0160000045",  # ACC. CANONE LOCAZIONE
        "0160000060",  # FATTURE DA EMETTERE
        "0160000070",  # NOTE DI CREDITO DA RICEVERE
        "0160000075"
    ],
    # CEE POSITION 52 - Capitale sociale
    52: ["0310000010"],
    # CEE POSITION 54 - Riserva da sovrapprezzo delle azioni
    54: ["0320000010"],
    # CEE POSITION 55 - Riserve di rivalutazione
    55: ["0320000041"],
    # CEE POSITION 56 - Riserva legale
    56: ["0320000020"],
    # CEE POSITION 57 - Riserve statutarie
    57: ["0320000021"],
    # CEE POSITION 58 - Altre riserve
    58: ["0320000060"],
    # CEE POSITION 68 - Fondi per quiescenza e obblighi simili
    68: ["0210000011"],
    # CEE POSITION 73 - Debiti verso banche (oltre 12 mesi)
    73: [
        "0220000020",  # MUTUI BANCARI
        "0220000030",
        "0220000031",
        "0220000040",
        "0220000044",
        "0220000050",
        "0220000060",
        "0220000065",
        "0220000090"
    ],
    # CEE POSITION 79 - Debiti verso fornitori (entro 12 mesi)
    79: [
        "0235",        # DEBITO V/ FORNITORE
        "0241"         # FORNITORI CON RITENUTE
    ],
    # CEE POSITION 80 - Debiti verso banche (entro 12 mesi)
    80: [
        "0270000001",  # UNICREDIT C/ANT
        "0270000005",  # BANCO DESIO C/ANT
        "0270000006",  # UNICREDIT ANT.FATT.
        "0270000010",  # INT. DA RINV.
        "0270000012",
        "0270000013",
        "0270000014",  # INTESA SAN PAOLO ANTICIPO
        "0270000015",  # INTESA SAN PAOLO FACTORING
        "0270000016"   # INTESA SAN PAOLO CESS.FACTORING
    ],
    # CEE POSITION 81 - Debiti verso altri finanziatori (entro 12 mesi)
    81: [
        "0271000001",  # OPEL BANK CONFORMITA'
        "0271000002",  # HYUNDAI CAPITAL
        "0271000004",  # VISION FINANCE
        "0271000005",  # BANCA PSA STOCK
        "0271000014",  # SANTANDER CONFORMITA'
        "0271000015",
        "0271000016",  # SANTANDER DEMO
        "0271000018",  # CREDIT AGRICOLE
        "0271000022",  # BANCA PSA STOCK DEMO
        "0271000025",
        "0271000026"
    ],
    # CEE POSITION 85 - Debiti tributari
    85: [
        "0230000020",  # IMPOSTA PUBBL.COMUNI
        "0230000054",  # DEBITO IVA
        "0230000060",  # DEBITI IMPOSTE IRES
        "0230000061",  # DEBITI IMPOSTE IRAP
        "0230000100",  # DEBITI V/ERARIO
        "0230000130",  # IRPEF DIPENDENTI
        "0230000154",  # RATEAZ. CONTRIB.
        "0230000155"
    ],
    # CEE POSITION 86 - Debiti verso istituti di previdenza
    86: [
        "0230000070",  # DEBITI VERSO INPS
        "0230000090",  # DEBITI INAIL
        "0230000160",  # TRATTENUTE SINDACALI
        "0230000180",  # ENTE BILATERALE
        "0230000185"   # FONDO EST
    ],
    # CEE POSITION 87 - Altri debiti
    87: [
        "0230000120",  # STIP.SAL.E COMP.
        "0230000201",  # INCASSO PER C/ALD
        "0230000202",  # MOVIMENTI PER CONTO TERZI
        "0230000205",  # INCASSO PER C/G.M.I.
        "0230000206",  # INCASSO PER CONTO POLIZ.
        "0230000210",  # ACCONTI DA CLIENTI
        "0230000211",  # CAPARRE CONFIRMATORIE
        "0230000212",
        "0230000214",  # DEP.CAUZ.PER AUTO
        "0230000216",
        "0231"         # CLIENTI DEP. CAUZIONALI
    ],
    # CEE POSITION 88 - Risconti passivi
    88: [
        "0260000020",  # RISCONTI PASSIVI CONTRIBUTI
        "0260000060",  # NOTE DI CREDITO DA EMETTERE
        "0260000080",  # FORNITORE C/FATTURE DA RICEVERE
        "0260000085"
    ],
    # CEE POSITION 100 - TFR
    100: [
        "0210000010",  # FONDO T.F.R. DIPENDENTI
        "0210000051",  # GEST. T.F.R. (various funds)
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
    # Add other mappings here in the future
}
# -- End Automotive Mapping Data --

@app.route('/', methods=['GET'])
def index():
    """Displays the KPI selection page."""
    # Clear previous session data on new start
    session.pop('balance_sheet_data', None)
    session.pop('required_positions', None)
    session.pop('selected_kpis', None)
    session.pop('calculated_kpis', None)

    return render_template('select_kpi.html', available_kpis=AVAILABLE_KPIS)

@app.route('/input', methods=['GET', 'POST'])
def input_required_fields():
    """Determines required fields based on selected KPIs (POST) 
       or reloads existing input state from session (GET).
    """
    if request.method == 'POST':
        # This is the flow from KPI selection
        selected_kpi_keys = request.form.getlist('kpi_keys')
        if not selected_kpi_keys:
            flash("Selezionare almeno un KPI.", "warning")
            return redirect(url_for('index'))

        required_positions = set()
        for key in selected_kpi_keys:
            if key in KPI_REQUIREMENTS:
                required_positions.update(KPI_REQUIREMENTS[key])

        sorted_required_positions = sorted(list(required_positions))
        session['required_positions'] = sorted_required_positions
        session['selected_kpis'] = selected_kpi_keys

        # Initialize data only for newly required fields, keep old if navigating back/forth
        existing_data = session.get('balance_sheet_data', {}) # Get existing if any
        session['balance_sheet_data'] = {str(pos): existing_data.get(str(pos), 0.0) for pos in sorted_required_positions}

        # FLASH REMOVED FROM HERE for initial load from KPI selection
        # flash("Inserisci i valori per i KPI selezionati.", "info") 

    elif request.method == 'GET':
        # This is the flow when clicking "Modifica Dati" from results
        if 'selected_kpis' not in session or 'required_positions' not in session:
            flash("Sessione non valida o scaduta. Seleziona nuovamente i KPI.", "warning")
            return redirect(url_for('index'))
        
        selected_kpi_keys = session['selected_kpis']
        sorted_required_positions = session['required_positions']
        # balance_sheet_data should already be in the session
        if 'balance_sheet_data' not in session:
             # Fallback: initialize if somehow missing, though it shouldn't be
             session['balance_sheet_data'] = {str(pos): 0.0 for pos in sorted_required_positions}
        
        flash("Modifica i valori inseriti e ricalcola.", "info") # Keep this one for re-edit

    else: # Should not happen with methods=['GET', 'POST']
        return redirect(url_for('index'))

    # --- Common logic for both GET and POST to render the input form --- 

    # Ensure we have the keys and positions needed
    selected_kpi_keys = session.get('selected_kpis', [])
    sorted_required_positions = session.get('required_positions', [])
    current_data = session.get('balance_sheet_data', {})

    if not selected_kpi_keys or not sorted_required_positions:
        # If session somehow lost state, redirect to start
        flash("Errore di sessione. Si prega di ricominciare.", "danger")
        return redirect(url_for('index'))

    # Get details for selected KPIs to display on input page
    selected_kpi_details = {key: AVAILABLE_KPIS[key] for key in selected_kpi_keys if key in AVAILABLE_KPIS}

    # Generate a structure containing only required fields for the template
    required_structure = {}
    for main_cat, sub_cats in BALANCE_SHEET_STRUCTURE.items():
        req_main_cat = {}
        for sub_cat_name, content in sub_cats.items():
            if isinstance(content, dict):
                req_sub_cat = {}
                for nested_name, nested_positions in content.items():
                    req_nested_pos = [p for p in nested_positions if p in sorted_required_positions]
                    if req_nested_pos:
                        req_sub_cat[nested_name] = req_nested_pos
                if req_sub_cat:
                     req_main_cat[sub_cat_name] = req_sub_cat
            elif isinstance(content, list): # Handle lists like provisions, prepaid, accrued
                req_pos = [p for p in content if p in sorted_required_positions]
                if req_pos:
                    req_main_cat[sub_cat_name] = req_pos
        if req_main_cat:
            required_structure[main_cat] = req_main_cat

    # --- Pass Mapping Information ---
    # For now, we only have one mapping, but structure for multiple
    all_mapping_data = {
        "automotive_dealer": CEE_TO_AUTOMOTIVE_CODES
        # Add other mapping data here keyed by the key in AVAILABLE_MAPPINGS
    }

    return render_template('input.html',
                           structure=required_structure, 
                           data=current_data, 
                           required_positions=sorted_required_positions,
                           position_names=POSITION_NAMES,
                           selected_kpi_details=selected_kpi_details, 
                           section_titles=SECTION_TITLES,
                           available_mappings=AVAILABLE_MAPPINGS, # For dropdown
                           all_mapping_data_json=json.dumps(all_mapping_data) # Pass all data as JSON for JS
                           )

@app.route('/calculate', methods=['POST'])
def calculate():
    """Processes the input data for required fields, calculates selected KPIs, and shows results."""
    if 'required_positions' not in session or 'selected_kpis' not in session:
         flash("Sessione scaduta o invalida. Si prega di ricominciare.", "danger")
         return redirect(url_for('index'))

    required_positions = session['required_positions']
    selected_kpi_keys = session['selected_kpis']

    balance_sheet_data = {} # This will hold data keyed by CEE position string

    try:
        # --- REVERTED to only handle CEE pos_X inputs --- 
        for pos in required_positions:
            pos_str = str(pos)
            # Get value for the CEE position input field
            value_str = request.form.get(f'pos_{pos}', '0').replace(',', '.') 
            
            # Basic handling: Try to convert directly to float.
            # Rely on client-side JS (safeCalculate) to handle sums before submission.
            try:
                calculated_value = float(value_str)
            except ValueError:
                 # If conversion fails after JS formatting, default to 0.0
                 print(f"Warning: Could not convert value '{value_str}' for pos {pos_str} to float. Defaulting to 0.0.")
                 calculated_value = 0.0

            balance_sheet_data[pos_str] = calculated_value

        # Store the final CEE-keyed data in session
        session['balance_sheet_data'] = balance_sheet_data

    except Exception as e: # Catch potential broader errors during form processing
        flash(f'Errore durante l\'elaborazione dei dati: {e}', 'danger')
        # Redirect to input page, preserving existing session data for correction
        return redirect(url_for('input_required_fields'))

    # --- Calculations using balance_sheet_data (now always CEE-keyed) --- 

    # --- Basic Validation (using only available data) ---
    # Note: Full validation might not be possible if not all positions are present
    total_assets = sum(balance_sheet_data.get(str(pos), 0.0) for pos in get_all_positions(BALANCE_SHEET_STRUCTURE['assets']))
    total_liabilities = sum(balance_sheet_data.get(str(pos), 0.0) for pos in get_all_positions(BALANCE_SHEET_STRUCTURE['equity_liabilities']['liabilities']))
    total_equity = sum(balance_sheet_data.get(str(pos), 0.0) for pos in get_all_positions(BALANCE_SHEET_STRUCTURE['equity_liabilities']['equity']))
    # Need to include provisions and accrued expenses in the equity/liabilities side for a full check
    total_provisions = sum(balance_sheet_data.get(str(pos), 0.0) for pos in get_all_positions(BALANCE_SHEET_STRUCTURE['equity_liabilities']['provisions_for_risks_and_charges']))
    total_accrued = sum(balance_sheet_data.get(str(pos), 0.0) for pos in get_all_positions(BALANCE_SHEET_STRUCTURE['equity_liabilities']['accrued_expenses_and_deferred_income']))
    # And include TFR (Pos 100)
    total_tfr = balance_sheet_data.get('100', 0.0) # TFR is a single value, key is '100'

    total_liabilities_equity_side = total_liabilities + total_equity + total_provisions + total_accrued + total_tfr # Added total_tfr

    balance_check = {"valid": abs(total_assets - total_liabilities_equity_side) < 0.01, "assets": total_assets, "liabilities_equity": total_liabilities_equity_side} # Use tolerance for float comparison

    # --- KPI Calculation (Only Selected KPIs) ---
    # Pass selected KPIs list to calculation function
    kpis_results = calculate_selected_kpis(balance_sheet_data, selected_kpi_keys)

    session['calculated_kpis'] = kpis_results # Store KPIs for potential export later

    # Prepare display data for input_data_by_kpi
    input_data_by_kpi_display = {}
    for kpi_key in selected_kpi_keys:
        input_data_by_kpi_display[kpi_key] = {}
        if kpi_key in KPI_REQUIREMENTS:
            for pos in KPI_REQUIREMENTS[kpi_key]:
                # Ensure to use string key for balance_sheet_data and check if pos is in required_positions
                pos_str = str(pos) # Convert pos to string for lookup
                if pos_str in balance_sheet_data: # Check if the data was actually submitted
                    input_data_by_kpi_display[kpi_key][pos_str] = balance_sheet_data[pos_str]
                else:
                    # If a position in KPI_REQUIREMENTS wasn't in the submitted data (e.g. not required by any selected KPI)
                    # We can either mark it as N/A or not include it.
                    # For clarity that it was considered but not available, let's use None.
                    # The template already handles None as N/D.
                    input_data_by_kpi_display[kpi_key][pos_str] = None

    return render_template(
        "results.html",
        results=kpis_results,              # Calculated KPI values
        input_data=balance_sheet_data,      # All cleaned input data (pos: value)
        balance_check=balance_check,        # Balance sheet validation result
        input_data_by_kpi=input_data_by_kpi_display, # Input data grouped by KPI (kpi: {pos: value})
        available_kpis=AVAILABLE_KPIS,      # All KPI definitions for tooltips etc.
        position_names=POSITION_NAMES,      # Position number to Italian name mapping
        selected_kpi_keys=selected_kpi_keys, # List of keys for selected KPIs
        section_titles=SECTION_TITLES        # Pass section titles to template
    )

# Renamed and modified function
def calculate_selected_kpis(data, selected_kpi_keys):
    """Calculates Selected KPIs based on the provided data dictionary and keys.
       Returns a dictionary where keys are KPI keys, and values are dicts
       containing 'value' and 'details' (from AVAILABLE_KPIS).
       Uses updated position lists aligned with the compliant structure.
    """
    kpis_results = {}

    # Define position lists based on the new structure and analysis
    POS_CURRENT_ASSETS = [31, 32, 33, 34, 35, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50]
    POS_LIQUID_ASSETS = [39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50]
    POS_CASH = [49, 50]
    POS_CURRENT_LIABILITIES = [79, 80, 81, 82, 83, 84, 85, 86, 87, 88]
    POS_TOTAL_LIABILITIES = [67, 68, 69, 100, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88] # Added 100 (TFR)
    POS_TOTAL_EQUITY = [52, 54, 55, 56, 57, 58, 59, 64, 65, 66]
    POS_TOTAL_ASSETS = [1, 2, 3, 4, 5, 6, 7, 11, 12, 13, 14, 15, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51]

    # Helper to safely get sum of positions from the input data dict
    def get_sum(positions):
        return sum(data.get(str(p), 0.0) for p in positions) # data keys are strings

    # Calculate only requested KPIs using the defined position lists
    if 'current_ratio' in selected_kpi_keys:
        if 'current_ratio' in AVAILABLE_KPIS:
            current_assets = get_sum(POS_CURRENT_ASSETS)
            current_liabilities = get_sum(POS_CURRENT_LIABILITIES)
            value = current_assets / current_liabilities if current_liabilities else 0
            kpis_results['current_ratio'] = {'value': value, 'details': AVAILABLE_KPIS['current_ratio']}

    if 'quick_ratio' in selected_kpi_keys:
        if 'quick_ratio' in AVAILABLE_KPIS:
            liquid_assets = get_sum(POS_LIQUID_ASSETS)
            current_liabilities = get_sum(POS_CURRENT_LIABILITIES)
            value = liquid_assets / current_liabilities if current_liabilities else 0
            kpis_results['quick_ratio'] = {'value': value, 'details': AVAILABLE_KPIS['quick_ratio']}

    if 'cash_ratio' in selected_kpi_keys:
        if 'cash_ratio' in AVAILABLE_KPIS:
            cash_equivalents = get_sum(POS_CASH)
            current_liabilities = get_sum(POS_CURRENT_LIABILITIES)
            value = cash_equivalents / current_liabilities if current_liabilities else 0
            kpis_results['cash_ratio'] = {'value': value, 'details': AVAILABLE_KPIS['cash_ratio']}

    if 'debt_to_equity' in selected_kpi_keys:
        if 'debt_to_equity' in AVAILABLE_KPIS:
            total_liabilities = get_sum(POS_TOTAL_LIABILITIES)
            total_equity = get_sum(POS_TOTAL_EQUITY)
            value = total_liabilities / total_equity if total_equity else 0
            kpis_results['debt_to_equity'] = {'value': value, 'details': AVAILABLE_KPIS['debt_to_equity']}

    if 'debt_ratio' in selected_kpi_keys:
        if 'debt_ratio' in AVAILABLE_KPIS:
            total_liabilities = get_sum(POS_TOTAL_LIABILITIES)
            total_assets = get_sum(POS_TOTAL_ASSETS)
            value = total_liabilities / total_assets if total_assets else 0
            kpis_results['debt_ratio'] = {'value': value, 'details': AVAILABLE_KPIS['debt_ratio']}

    if 'working_capital' in selected_kpi_keys:
        if 'working_capital' in AVAILABLE_KPIS:
            current_assets = get_sum(POS_CURRENT_ASSETS)
            current_liabilities = get_sum(POS_CURRENT_LIABILITIES)
            value = current_assets - current_liabilities
            kpis_results['working_capital'] = {'value': value, 'details': AVAILABLE_KPIS['working_capital']}

    return kpis_results

if __name__ == '__main__':
    app.run(debug=True) # Enable debug mode for development 