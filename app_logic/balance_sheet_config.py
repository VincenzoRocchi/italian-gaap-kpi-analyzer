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