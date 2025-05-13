import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame
# from ttkbootstrap.tooltip import ToolTip # Not directly used here
from app_logic.constants import AVAILABLE_KPIS, KPI_REQUIREMENTS, POSITION_NAMES

class ResultsFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.accordian_states = {} 
        self.accordian_frames = {}

        title_label = ttk.Label(self, text="Risultati dell'Analisi", font=("Helvetica", 18, "bold"))
        title_label.pack(pady=(10, 5))
        
        # Fixed wraplength
        desc_label = ttk.Label(self, text="Di seguito i KPI calcolati. Controlla 'Dati e Quadratura' per i dettagli.", justify=LEFT, wraplength=650) 
        desc_label.pack(pady=(0,10), fill=X, padx=10)

        ttk.Separator(self, orient=HORIZONTAL).pack(fill=X, pady=5, padx=10)

        main_content_frame = ttk.Frame(self)
        main_content_frame.pack(fill=BOTH, expand=True, padx=10, pady=(0,5))
        main_content_frame.grid_columnconfigure(0, weight=7, uniform="group1")
        main_content_frame.grid_columnconfigure(1, weight=0)
        main_content_frame.grid_columnconfigure(2, weight=5, uniform="group1")
        main_content_frame.grid_rowconfigure(0, weight=1)

        self.kpi_results_scrolled_frame = ScrolledFrame(main_content_frame, autohide=True)
        self.kpi_results_scrolled_frame.grid(row=0, column=0, sticky="nsew", padx=(0,5))
        self.kpi_results_container = self.kpi_results_scrolled_frame.container

        separator = ttk.Separator(main_content_frame, orient=VERTICAL)
        separator.grid(row=0, column=1, sticky="ns", padx=5)

        self.data_summary_scrolled_frame = ScrolledFrame(main_content_frame, autohide=True)
        self.data_summary_scrolled_frame.grid(row=0, column=2, sticky="nsew", padx=(5,0))
        self.data_summary_container = self.data_summary_scrolled_frame.container

        button_frame = ttk.Frame(self)
        button_frame.pack(pady=10, fill=X, side=BOTTOM, padx=10)
        button_frame.grid_columnconfigure(0, weight=1) 

        restart_button = ttk.Button(button_frame, text="Nuova Analisi ->",
                                    command=lambda: self.controller.show_frame("SelectKpiFrame"), bootstyle="info")
        restart_button.grid(row=0, column=2, padx=(5,0), pady=5, sticky="e")
        
        back_button = ttk.Button(button_frame, text="<- Modifica Dati",
                                 command=lambda: self.controller.show_frame("InputDataFrame"), bootstyle="secondary")
        back_button.grid(row=0, column=1, padx=(0,5), pady=5, sticky="e")

    def _toggle_accordion_item(self, kpi_key):
        frame_to_toggle = self.accordian_frames.get(kpi_key)
        var_to_toggle = self.accordian_states.get(kpi_key)
        if frame_to_toggle and var_to_toggle:
            if var_to_toggle.get():
                frame_to_toggle.pack(fill=X, expand=True, pady=(0,5), padx=5)
            else:
                frame_to_toggle.pack_forget()
        self.data_summary_container.update_idletasks()
        self.data_summary_scrolled_frame.update_idletasks()

    def update_view(self):
        for widget in self.kpi_results_container.winfo_children():
            widget.destroy()
        for widget in self.data_summary_container.winfo_children():
            widget.destroy()
        self.accordian_states = {}
        self.accordian_frames = {}
        
        # Ensure containers are fully updated before repopulating
        self.kpi_results_scrolled_frame.update_idletasks() # Update the scrolled frame itself
        self.kpi_results_container.update_idletasks()
        self.data_summary_scrolled_frame.update_idletasks() # Update the scrolled frame itself
        self.data_summary_container.update_idletasks()

        results = self.controller.get_data("calculated_results", {})
        selected_kpi_keys = self.controller.get_data("selected_kpis", [])
        financial_data = self.controller.get_data("financial_data", {})
        balance_check_result = self.controller.get_data("balance_check_result", {})
        
        # Fallback, though controller should ideally ensure this is available if needed by ResultsFrame
        available_kpis_data = AVAILABLE_KPIS 

        if not selected_kpi_keys or not results:
            no_kpi_label = ttk.Label(self.kpi_results_container, text="Nessun KPI selezionato o calcolato.")
            no_kpi_label.pack(padx=10, pady=10)
        else:
            for kpi_key in selected_kpi_keys:
                if kpi_key not in results:
                    continue
                
                result_data = results[kpi_key]
                kpi_details = available_kpis_data.get(kpi_key, {})
                kpi_name = kpi_details.get("name_display", kpi_key)
                
                # --- KPI Card Frame ---
                kpi_card_main_frame = ttk.Frame(self.kpi_results_container, padding=(10,10), relief=SOLID, borderwidth=1, bootstyle="light")
                kpi_card_main_frame.pack(fill=X, expand=True, pady=5, padx=2)

                kpi_title_label = ttk.Label(kpi_card_main_frame, text=kpi_name, font=("Helvetica", 12, "bold"))
                kpi_title_label.pack(side=TOP, anchor="w", pady=(0,8))
                # --- End KPI Card Frame Title ---
                
                value = result_data.get('value', 'N/D')
                value_str = f"{value:.2f}" if isinstance(value, (int, float)) else str(value)
                
                is_percentage = False
                if 'percentage' in kpi_name.lower() or 'percentuale' in kpi_name.lower() or \
                   kpi_key in ['roe', 'roi', 'ros']:
                   is_percentage = True
                # Ensure value is number before multiplication for percentage
                if is_percentage and isinstance(value, (int, float)):
                    # Specific KPIs like roe, roi, ros are often expressed as x100 %.
                    # Other percentages might already be in the correct scale (0-100 vs 0-1).
                    # Assuming roe, roi, ros are in decimal (0.1 for 10%) and need *100.
                    # Other kpis named 'percentage' or 'percentuale' might be direct % values.
                    # This logic might need refinement based on how raw KPI values are calculated.
                    if kpi_key in ['roe', 'roi', 'ros']:
                         value_str = f"{value*100:.2f}%" 
                    else:
                         value_str = f"{value:.2f}%"

                val_frame = ttk.Frame(kpi_card_main_frame) # Content goes into kpi_card_main_frame
                val_frame.pack(fill=X, pady=(0,5))
                ttk.Label(val_frame, text="Valore:", font=("Helvetica", 10, "bold")).pack(side=LEFT, anchor='w')
                val_style = SUCCESS if isinstance(value, (int, float)) else DANGER
                ttk.Label(val_frame, text=value_str, font=("Helvetica", 12, "bold"), bootstyle=f"{val_style}").pack(side=LEFT, padx=5, anchor='w')

                interpretation = result_data.get('interpretation')
                if not interpretation and 'tooltip_info' in kpi_details:
                    interpretation = kpi_details['tooltip_info'].get('interpretation_notes')

                # Fixed wraplengths
                fixed_wraplength = 350 
                if interpretation:
                    ttk.Label(kpi_card_main_frame, text=f"Interpretazione: {interpretation}", wraplength=fixed_wraplength).pack(anchor="w", fill=X, pady=(0,3))
                
                formula = kpi_details.get('tooltip_info', {}).get('formula_display')
                if formula:
                    ttk.Label(kpi_card_main_frame, text=f"Formula: {formula}", wraplength=fixed_wraplength, font=("Helvetica", 8, "italic")).pack(anchor="w",fill=X, pady=(0,3))
                
                optimal_range = kpi_details.get('tooltip_info', {}).get('optimal_range_cee')
                if optimal_range:
                    ttk.Label(kpi_card_main_frame, text=f"Range Ottimale (CEE): {optimal_range}", wraplength=fixed_wraplength, font=("Helvetica", 8)).pack(anchor="w",fill=X, pady=(0,3))

        # --- Populate Right Column: Data Summary & Balance Check ---
        # Main container for the right side content
        right_content_main_frame = ttk.Frame(self.data_summary_container, padding=(5,5))
        right_content_main_frame.pack(fill=BOTH, expand=True, pady=0, padx=0)
        
        right_main_title_label = ttk.Label(right_content_main_frame, text="Dati e Quadratura", font=("Helvetica", 13, "bold"))
        right_main_title_label.pack(side=TOP, anchor="w", pady=(0,10))

        # Balance Check Section
        balance_section_frame = ttk.Frame(right_content_main_frame, padding=(5,5), relief=SOLID, borderwidth=1, bootstyle="light")
        balance_section_frame.pack(fill=X, expand=False, pady=(0,10)) # Don't expand, let content dictate height

        balance_title_label = ttk.Label(balance_section_frame, text="Controllo Quadratura", font=("Helvetica", 11, "bold"))
        balance_title_label.pack(side=TOP, anchor="w", pady=(0,5))

        if balance_check_result:
            is_valid = balance_check_result.get("valid", False)
            assets = balance_check_result.get("assets", 0.0)
            liab_eq = balance_check_result.get("liabilities_equity", 0.0)
            
            status_text = "Corretto" if is_valid else "Non Corretto"
            status_style = SUCCESS if is_valid else DANGER
            ttk.Label(balance_section_frame, text=status_text, bootstyle=f"{status_style},inverse", font=("Helvetica", 10, "bold")).pack(pady=(0,5), anchor='w')
            ttk.Label(balance_section_frame, text=f"Attivo: {assets:.2f} €").pack(anchor='w')
            ttk.Label(balance_section_frame, text=f"Passivo + Netto: {liab_eq:.2f} €").pack(anchor='w')
            if not is_valid:
                diff = abs(assets-liab_eq)
                ttk.Label(balance_section_frame, text=f"Differenza: {diff:.2f} €", bootstyle=DANGER).pack(anchor='w')
        else:
            ttk.Label(balance_section_frame, text="Controllo quadratura non disponibile.").pack()

        # Input Data (Accordion style) Section
        input_data_section_frame = ttk.Frame(right_content_main_frame, padding=(5,5), relief=SOLID, borderwidth=1, bootstyle="light")
        input_data_section_frame.pack(fill=X, expand=True, pady=5)
        
        input_data_title_label = ttk.Label(input_data_section_frame, text="Dati Inseriti per KPI", font=("Helvetica", 11, "bold"))
        input_data_title_label.pack(side=TOP, anchor="w", pady=(0,5))
        
        if financial_data and selected_kpi_keys:
            for kpi_key in sorted(selected_kpi_keys):
                kpi_details = available_kpis_data.get(kpi_key, {})
                kpi_name = kpi_details.get("name_display", kpi_key)
                required_pos_for_kpi = KPI_REQUIREMENTS.get(kpi_key, [])
                
                if not required_pos_for_kpi:
                    continue

                var = tk.BooleanVar(value=False)
                self.accordian_states[kpi_key] = var
                
                # Accordion header still uses Checkbutton, parent is input_data_section_frame
                header_frame = ttk.Frame(input_data_section_frame)
                header_frame.pack(fill=X, expand=True)

                cb = ttk.Checkbutton(
                    header_frame, 
                    text=kpi_name, 
                    variable=var, 
                    bootstyle="info-toolbutton",
                    command=lambda k=kpi_key: self._toggle_accordion_item(k)
                )
                cb.pack(fill=X, expand=True, pady=(5,0), padx=2)

                # Accordion content frame, parent is input_data_section_frame
                content_frame = ttk.Frame(input_data_section_frame, padding=(5,0,5,5))
                self.accordian_frames[kpi_key] = content_frame
                
                data_found_for_kpi = False
                for pos_code in sorted(required_pos_for_kpi):
                    str_pos_code = str(pos_code)
                    value = financial_data.get(str_pos_code)
                    if value is not None:
                        data_found_for_kpi = True
                        pos_name = POSITION_NAMES.get(pos_code, f"Pos. {pos_code}")
                        item_frame = ttk.Frame(content_frame)
                        item_frame.pack(fill=X, expand=True)
                        ttk.Label(item_frame, text=f"{pos_name} (Cod: {pos_code}):", wraplength=200).pack(side=LEFT, padx=(0,5))
                        ttk.Label(item_frame, text=f"{value:.2f}" if isinstance(value, (int, float)) else str(value), bootstyle="secondary").pack(side=RIGHT)
                
                if not data_found_for_kpi:
                     ttk.Label(content_frame, text="Nessun dato specifico richiesto/inserito per questo KPI.").pack(padx=5, pady=5)
                
                self._toggle_accordion_item(kpi_key)

        else:
            ttk.Label(input_data_section_frame, text="Nessun dato finanziario o KPI selezionato.").pack(padx=5, pady=10)

        self.kpi_results_container.update_idletasks()
        self.kpi_results_scrolled_frame.update_idletasks()
        self.data_summary_container.update_idletasks()
        self.data_summary_scrolled_frame.update_idletasks() 