import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame
from ttkbootstrap.tooltip import ToolTip
from app_logic.constants import (
    AVAILABLE_KPIS, AVAILABLE_MAPPINGS, CEE_TO_AUTOMOTIVE_CODES, 
    POSITION_NAMES, BALANCE_SHEET_STRUCTURE, SECTION_TITLES, ALL_POSITIONS
)
# It seems validate_balance_sheet is called by the controller or main app, not directly here.
# from app_logic.calculator import validate_balance_sheet 

# For Messagebox in process_calculation, if kept directly in frame
# from ttkbootstrap.dialogs import Messagebox 

class InputDataFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.entry_widgets = {}
        self.mapping_var = tk.StringVar()

        header_frame = ttk.Frame(self)
        header_frame.pack(fill=X, padx=10, pady=(10,0))

        title_label = ttk.Label(header_frame, text="Inserisci i Dati di bilancio", font=("Helvetica", 16, "bold"))
        title_label.pack(side=LEFT, anchor="w", pady=(0,5))

        self.selected_kpis_display_frame = ttk.Frame(header_frame)
        self.selected_kpis_display_frame.pack(side=RIGHT, anchor="e", padx=(10,0), fill=X)

        top_controls_frame = ttk.Frame(self, padding=(0, 5, 0, 5))
        top_controls_frame.pack(fill=X, padx=10, pady=(5,5))
        top_controls_frame.grid_columnconfigure(0, weight=1)
        top_controls_frame.grid_columnconfigure(1, weight=0)
        top_controls_frame.grid_columnconfigure(2, weight=0)

        mapping_container_frame = ttk.Frame(top_controls_frame)
        mapping_container_frame.grid(row=0, column=0, sticky="ew")
        
        mapping_label = ttk.Label(mapping_container_frame, text="Mappatura Conti:")
        mapping_label.pack(side=LEFT, padx=(0,5))
        self.mapping_options = {"Nessuna Mappatura": None}
        if AVAILABLE_MAPPINGS:
            for key, details in AVAILABLE_MAPPINGS.items():
                display_name = details.get("display_name", key.replace("_", " ").title())
                self.mapping_options[display_name] = key
        self.mapping_combobox = ttk.Combobox(mapping_container_frame, textvariable=self.mapping_var,
                                           values=list(self.mapping_options.keys()), state="readonly", width=30)
        self.mapping_combobox.pack(side=LEFT, fill=X, expand=True)
        self.mapping_combobox.set("Nessuna Mappatura")
        self.mapping_combobox.bind("<<ComboboxSelected>>", self.on_mapping_selected)

        buttons_container_frame = ttk.Frame(top_controls_frame)
        buttons_container_frame.grid(row=0, column=1, columnspan=2, sticky="e")

        self.calculate_button = ttk.Button(buttons_container_frame, text="Calcola KPI Selezionati", 
                                           command=self.process_calculation, bootstyle="primary")
        self.calculate_button.pack(side=RIGHT, padx=(5,0))

        self.back_to_kpi_button = ttk.Button(buttons_container_frame, text="Indietro", 
                                   command=lambda: self.controller.show_frame("SelectKpiFrame"), bootstyle="secondary")
        self.back_to_kpi_button.pack(side=RIGHT, padx=(0,5))
        
        explanatory_text_content = "Utilizza il menu \"Mappatura Conti\" per visualizzare i codici corrispondenti nel piano dei conti selezionato (es. Automotive Dealer). \nInserisci i valori numerici nelle caselle sottostanti utilizzando il punto (.) come separatore decimale (es. 1234.56). Puoi anche inserire semplici somme (es. 1000 + 250.50)."
        # Fixed wraplength
        explanatory_label = ttk.Label(self, text=explanatory_text_content, bootstyle="secondary", justify=LEFT, wraplength=700) 
        explanatory_label.pack(fill=X, padx=10, pady=(5,10))

        # Fixed wraplength
        self.error_display_label = ttk.Label(self, text="", bootstyle="danger", wraplength=700) 

        ttk.Separator(self, orient=HORIZONTAL).pack(fill=X, padx=10, pady=(0,10))
        
        self.scrolled_container_parent = ttk.Frame(self)
        self.scrolled_container_parent.pack(fill=BOTH, expand=True, padx=10, pady=(5,0))
        
        self.inputs_frame_scrollable = None
        self.create_scrolled_frame()

    def create_scrolled_frame(self):
        if self.inputs_frame_scrollable:
            self.inputs_frame_scrollable.destroy()
        
        self.inputs_frame_scrollable = ScrolledFrame(self.scrolled_container_parent, autohide=True)
        self.inputs_frame_scrollable.pack(fill=BOTH, expand=True)
        self.inputs_frame_scrollable.update_idletasks()

    def on_mapping_selected(self, event=None):
        selected_display_name = self.mapping_var.get()
        selected_key = self.mapping_options.get(selected_display_name)
        self.controller.set_data("selected_mapping_key", selected_key)
        self.update_view()

    def _create_input_entry(self, parent_frame, pos_code, current_financial_data):
        pos_name_cee = POSITION_NAMES.get(pos_code, f"Posizione CEE {pos_code}")
        current_mapping_key = self.controller.get_data("selected_mapping_key")
        
        cee_label_text = f"{pos_name_cee} (Cod: {pos_code})"

        entry_row_frame = ttk.Frame(parent_frame)
        entry_row_frame.pack(fill=X, pady=(2, 4), padx=5)

        cee_input_frame = ttk.Frame(entry_row_frame)
        cee_input_frame.pack(fill=X)
        
        lbl_cee = ttk.Label(cee_input_frame, text=cee_label_text, width=60) # Consider wraplength if names are very long
        lbl_cee.pack(side=LEFT, padx=(0, 5), pady=(0,2))
        
        entry_var = tk.StringVar()
        initial_value = current_financial_data.get(str(pos_code), "")
        if initial_value is None: initial_value = ""
        entry_var.set(str(initial_value))

        entry = ttk.Entry(cee_input_frame, textvariable=entry_var, width=20)
        entry.pack(side=LEFT, padx=(0,5), fill=X, expand=True)
        self.entry_widgets[str(pos_code)] = entry_var

        if current_mapping_key and CEE_TO_AUTOMOTIVE_CODES:
            # This check should be more generic if more mappings are added
            if current_mapping_key == "automotive_dealer" and pos_code in CEE_TO_AUTOMOTIVE_CODES:
                mapped_codes = CEE_TO_AUTOMOTIVE_CODES[pos_code]
                if mapped_codes: # Ensure mapped_codes is not None or empty
                    mapped_codes_str = ", ".join(mapped_codes)
                    map_label_text = f"  └─ Mappato {current_mapping_key.replace('_', ' ').title()}: [{mapped_codes_str}]"
                    lbl_map = ttk.Label(entry_row_frame, text=map_label_text, font=("Helvetica", 9, "italic"))
                    lbl_map.pack(anchor="w", padx=(15,0), pady=(0, 2))

    def _create_structured_inputs(self, parent_frame, structure_part, required_positions, current_financial_data):
        for key, value in structure_part.items():
            section_title_text = SECTION_TITLES.get(key, key.replace("_", " ").title())
            
            has_relevant_content = False
            if isinstance(value, dict):
                def check_dict_relevance(sub_dict):
                    for _k_val, v_item in sub_dict.items():
                        if isinstance(v_item, dict):
                            if check_dict_relevance(v_item): return True
                        elif isinstance(v_item, list):
                            if any(p in required_positions for p in v_item): return True
                        elif isinstance(v_item, int):
                            if v_item in required_positions: return True
                    return False
                has_relevant_content = check_dict_relevance(value)
            elif isinstance(value, list):
                has_relevant_content = any(p in required_positions for p in value)
            elif isinstance(value, int):
                has_relevant_content = value in required_positions

            if not has_relevant_content:
                continue

            # Create a Frame for the section with a title Label
            # Padding: more top/bottom padding for sections, less for subsections in recursive helper
            section_frame = ttk.Frame(parent_frame, padding=(2, 10, 2, 10)) # Main sections get more vertical padding
            section_frame.pack(fill=X, expand=True, pady=(10,0), padx=0)

            if section_title_text: # Only add title if one exists for this key
                title_label = ttk.Label(section_frame, text=section_title_text, font=("Helvetica", 11, "bold")) # Slightly smaller than main titles
                title_label.pack(side=TOP, anchor="w", pady=(0, 8))
            
            # Content Frame for this section (children will go here)
            # This helps ensure content is below the title_label
            content_sub_frame = ttk.Frame(section_frame)
            content_sub_frame.pack(fill=X, expand=True, padx=(10,0)) # Indent content slightly

            if isinstance(value, dict):
                for sub_key, sub_value in value.items():
                    # Pass content_sub_frame as the parent for the recursive call
                    self._create_structured_inputs_recursive_helper(content_sub_frame, {sub_key: sub_value}, required_positions, current_financial_data)
            elif isinstance(value, list):
                for pos_code in sorted([p for p in value if p in required_positions]):
                    self._create_input_entry(content_sub_frame, pos_code, current_financial_data)
            elif isinstance(value, int):
                if value in required_positions:
                     self._create_input_entry(content_sub_frame, value, current_financial_data)
    
    def _create_structured_inputs_recursive_helper(self, parent_frame, structure_node, required_positions, current_financial_data):
        for key, value in structure_node.items():
            section_title_text = SECTION_TITLES.get(key, key.replace("_", " ").title())
            
            has_relevant_content = False
            if isinstance(value, dict):
                def check_dict_relevance_helper(sub_dict):
                    for _, v_item in sub_dict.items():
                        if isinstance(v_item, dict): 
                            if check_dict_relevance_helper(v_item): return True
                        elif isinstance(v_item, list):
                            if any(p in required_positions for p in v_item): return True
                        elif isinstance(v_item, int):
                            if v_item in required_positions: return True
                    return False
                has_relevant_content = check_dict_relevance_helper(value)
            elif isinstance(value, list):
                has_relevant_content = any(p in required_positions for p in value)
            elif isinstance(value, int):
                has_relevant_content = value in required_positions

            if not has_relevant_content:
                continue

            # Create a Frame for the subsection with a title Label
            # Subsections get less vertical padding
            subsection_frame = ttk.Frame(parent_frame, padding=(2, 5, 2, 5))
            subsection_frame.pack(fill=X, expand=True, pady=(5,0), padx=0)
            
            if section_title_text: # Only add title if one exists for this key
                # Sub-category titles are slightly smaller/less prominent
                title_label = ttk.Label(subsection_frame, text=section_title_text, font=("Helvetica", 10, "normal")) 
                title_label.pack(side=TOP, anchor="w", pady=(0, 5))

            # Content Frame for this subsection
            content_sub_frame = ttk.Frame(subsection_frame)
            content_sub_frame.pack(fill=X, expand=True, padx=(10,0)) # Indent content slightly

            if isinstance(value, dict):
                # Recursive call for the content of this new Frame
                self._create_structured_inputs_recursive_helper(content_sub_frame, value, required_positions, current_financial_data)
            elif isinstance(value, list):
                for pos_code in sorted([p for p in value if p in required_positions]):
                    self._create_input_entry(content_sub_frame, pos_code, current_financial_data)
            elif isinstance(value, int):
                if value in required_positions:
                    self._create_input_entry(content_sub_frame, value, current_financial_data)

    def update_view(self):
        for widget in self.selected_kpis_display_frame.winfo_children():
            widget.destroy()
        
        selected_kpi_keys = self.controller.get_data("selected_kpis", [])
        if selected_kpi_keys:
            kpi_tags_container = ttk.Frame(self.selected_kpis_display_frame) 
            kpi_tags_container.pack(fill=X, anchor='e')

            if selected_kpi_keys:
                 selected_kpis_title_label = ttk.Label(kpi_tags_container, text="KPI Selezionati: ", font=("Helvetica", 9, "italic"))
                 selected_kpis_title_label.pack(side=LEFT, padx=(0,3), pady=(0,0))

            for i, kpi_key in enumerate(selected_kpi_keys):
                kpi_details = AVAILABLE_KPIS.get(kpi_key, {})
                display_name = kpi_details.get("name_display", kpi_key).replace('Indice di ', '')
                
                kpi_tag = ttk.Frame(kpi_tags_container, padding=0, bootstyle="light")
                kpi_tag.pack(side=LEFT, padx=(0,4), pady=(2,2))

                kpi_label_in_tag = ttk.Label(kpi_tag, text=display_name, padding=(5,3), bootstyle="light")
                kpi_label_in_tag.pack()

                tooltip_text_plain = "\n".join([
                    f"{kpi_details.get('name_display', kpi_key)}",
                    f"Formula: {kpi_details.get('tooltip_info', {}).get('formula_display', 'N/D')}",
                    f"Range Ottimale: {kpi_details.get('tooltip_info', {}).get('optimal_range_cee', 'N/D')}",
                    f"Interpretazione: {kpi_details.get('tooltip_info', {}).get('interpretation_notes', 'N/D')}"
                ])
                if tooltip_text_plain and tooltip_text_plain != kpi_details.get('name_display', kpi_key):
                    ToolTip(kpi_tag, text=tooltip_text_plain, bootstyle=(INFO, INVERSE), wraplength=300)

        self.error_display_label.config(text="")
        self.error_display_label.pack_forget()

        current_map_key = self.controller.get_data("selected_mapping_key")
        found_key_in_options = False
        if self.mapping_options:
            for display_name, key_val in self.mapping_options.items():
                if key_val == current_map_key:
                    self.mapping_var.set(display_name)
                    found_key_in_options = True
                    break
            if not found_key_in_options:
                self.mapping_var.set("Nessuna Mappatura")
        
        self.create_scrolled_frame()
        inputs_frame_inner = self.inputs_frame_scrollable.container
        self.entry_widgets = {}

        inputs_frame_inner.grid_columnconfigure(0, weight=1)
        inputs_frame_inner.grid_columnconfigure(1, weight=1)

        # --- Left Column (ATTIVO) ---
        left_column_container = ttk.Frame(inputs_frame_inner, padding=(0,0,5,0)) # Container with slight right padding
        left_column_container.grid(row=0, column=0, sticky="nsew", pady=5)
        
        left_title_text = SECTION_TITLES.get('assets', 'ATTIVO')
        left_title_label = ttk.Label(left_column_container, text=left_title_text, font=("Helvetica", 13, "bold"))
        left_title_label.pack(side=TOP, anchor="w", pady=(0,10))
        # This frame will hold the subsections for assets
        self.left_content_frame = ttk.Frame(left_column_container)
        self.left_content_frame.pack(fill=BOTH, expand=True)

        # --- Right Column (PASSIVO E PATRIMONIO NETTO) ---
        right_column_container = ttk.Frame(inputs_frame_inner, padding=(5,0,0,0)) # Container with slight left padding
        right_column_container.grid(row=0, column=1, sticky="nsew", pady=5)

        right_title_text = SECTION_TITLES.get('equity_liabilities', 'PASSIVO E PATRIMONIO NETTO')
        right_title_label = ttk.Label(right_column_container, text=right_title_text, font=("Helvetica", 13, "bold"))
        right_title_label.pack(side=TOP, anchor="w", pady=(0,10))
        # This frame will hold the subsections for equity/liabilities
        self.right_content_frame = ttk.Frame(right_column_container)
        self.right_content_frame.pack(fill=BOTH, expand=True)
        
        required_positions = self.controller.get_data("required_positions", [])
        required_positions = {int(p) for p in required_positions if str(p).isdigit()}
        current_financial_data = self.controller.get_data("financial_data", {})
        
        if not required_positions:
            no_req_label = ttk.Label(inputs_frame_inner, text="Nessuna posizione richiesta. Seleziona prima i KPI.")
            no_req_label.grid(row=0, column=0, columnspan=2, pady=20, padx=10, sticky="n")
            return # Added return to prevent further processing when no positions are required
        
        # Ensure the specific structure parts exist before trying to access them
        assets_structure = BALANCE_SHEET_STRUCTURE.get('assets', {})
        equity_liabilities_structure = BALANCE_SHEET_STRUCTURE.get('equity_liabilities', {})

        if assets_structure: # only call if there is something to build for assets
            self._create_structured_inputs(self.left_content_frame, assets_structure, required_positions, current_financial_data)
        if equity_liabilities_structure: # only call if there is something to build for equity/liabilities
            self._create_structured_inputs(self.right_content_frame, equity_liabilities_structure, required_positions, current_financial_data)

        all_rendered_pos_codes = {int(str_code) for str_code in self.entry_widgets.keys()}
        missing_from_structure = [p for p in required_positions if p not in all_rendered_pos_codes and p in ALL_POSITIONS]
        if missing_from_structure:
            # Use self.right_content_frame for "Altre Voci"
            misc_section_frame = ttk.Frame(self.right_content_frame, padding=(5,5), relief=SOLID, borderwidth=1, bootstyle="secondary") # Example border
            misc_section_frame.pack(fill=X, expand=True, pady=(15,5), padx=2) # More top padding to separate
            
            misc_title_label = ttk.Label(misc_section_frame, text="Altre Voci Richieste (Non Strutturate)", font=("Helvetica", 11, "bold"))
            misc_title_label.pack(side=TOP, anchor="w", pady=(0,5))
            
            for pos_code in sorted(missing_from_structure):
                self._create_input_entry(misc_section_frame, pos_code, current_financial_data)

        inputs_frame_inner.update_idletasks()
        self.inputs_frame_scrollable.update_idletasks()

    def process_calculation(self):
        raw_data = {code: var.get() for code, var in self.entry_widgets.items()}
        
        input_data = {}
        errors = []
        for code, value_str in raw_data.items():
            if not value_str.strip():
                input_data[str(code)] = 0.0 
                continue
            try:
                processed_value = value_str.replace(',', '.')
                if '+' in processed_value or '-' in processed_value and not any(c.isalpha() for c in processed_value):
                    try:
                        input_data[str(code)] = float(eval(processed_value)) # UNSAFE
                    except Exception:
                        pos_name = POSITION_NAMES.get(int(code) if code.isdigit() else code, f"Posizione {code}")
                        errors.append(f"Calcolo non valido per '{pos_name}': '{value_str}'.")
                else:
                    input_data[str(code)] = float(processed_value)
            except ValueError:
                pos_name = POSITION_NAMES.get(int(code) if code.isdigit() else code, f"Posizione {code}")
                errors.append(f"Valore non valido per '{pos_name}': '{value_str}'.")

        if errors:
            error_message = "Errori di Validazione:\n" + "\n".join(errors)
            self.error_display_label.config(text=error_message)
            self.error_display_label.pack(fill=X, padx=10, pady=(5,10), before=self.scrolled_container_parent)
            try:
                from ttkbootstrap.dialogs import Messagebox # Local import
                Messagebox.show_error("Errori nei dati. Controlla i messaggi.", title="Errore di Input")
            except ImportError:
                pass
            return
        else:
            self.error_display_label.config(text="")
            self.error_display_label.pack_forget()

        self.controller.set_data("financial_data", input_data)
        
        # Balance sheet validation is now done by the main controller (KpiApp) or a dedicated logic function
        # This keeps the frame focused on UI and data collection.
        # The controller will call validate_balance_sheet and then pass results to ResultsFrame.
        # For now, we assume the controller handles this before showing ResultsFrame.
        
        # Trigger calculation and switch frame via controller
        # The controller can fetch financial_data, call calculators, then show results.
        # This method should primarily focus on gathering and validating UI inputs.
        self.controller.set_data("financial_data", input_data) # Ensure it's set
        
        # Let the KpiApp controller handle the next steps (validation, calculation, showing results)
        self.controller.handle_data_submission() # New method in KpiApp 