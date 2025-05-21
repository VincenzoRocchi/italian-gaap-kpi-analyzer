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