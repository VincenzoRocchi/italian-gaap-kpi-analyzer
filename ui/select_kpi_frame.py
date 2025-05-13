import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame
from ttkbootstrap.tooltip import ToolTip
from app_logic.constants import AVAILABLE_KPIS
from app_logic.validators import validate_kpi_selection

class SelectKpiFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.kpi_vars = {}

        # Main title
        title_label = ttk.Label(self, text="Seleziona gli Indicatori (KPI) da Calcolare", font=("Helvetica", 16, "bold"))
        title_label.pack(pady=(10,5)) # Adjusted padding

        # Introductory text from Flask template
        intro_text = "Scegli uno o più indicatori cliccando sulle relative schede. Verranno richiesti solo i dati necessari per i calcoli selezionati."
        # Using a fixed reasonable wraplength as winfo_width() can be unreliable during __init__
        intro_label = ttk.Label(self, text=intro_text, wraplength=600, justify=LEFT, bootstyle="secondary") 
        intro_label.pack(pady=(0, 10), padx=20, fill=X)

        ttk.Separator(self, orient=HORIZONTAL).pack(fill=X, padx=20, pady=(0,10))

        # ScrolledFrame to contain the grid of KPI cards
        kpi_scrolled_frame = ScrolledFrame(self, autohide=True)
        kpi_scrolled_frame.pack(fill=BOTH, expand=True, padx=10, pady=(0,10))
        
        kpi_grid_container = kpi_scrolled_frame.container 
        kpi_grid_container.grid_columnconfigure(0, weight=1, uniform="kpi_col")
        kpi_grid_container.grid_columnconfigure(1, weight=1, uniform="kpi_col")
        kpi_grid_container.grid_columnconfigure(2, weight=1, uniform="kpi_col")

        row_num = 0
        col_num = 0
        max_cols = 3

        for kpi_key, kpi_details in AVAILABLE_KPIS.items():
            var = tk.BooleanVar()
            self.kpi_vars[kpi_key] = var

            # Create a card (Frame) for each KPI
            card_frame = ttk.Frame(kpi_grid_container, padding=(10,10), relief=SOLID, borderwidth=1, bootstyle="light") # Example: light border
            card_frame.grid(row=row_num, column=col_num, sticky="nsew", padx=5, pady=5)
            card_frame.columnconfigure(1, weight=1) # Make name/desc column expand

            # Checkbox on the left
            checkbox = ttk.Checkbutton(card_frame, variable=var, bootstyle="primary")
            checkbox.grid(row=0, column=0, rowspan=2, sticky="ns", padx=(0,10))

            # KPI Name (Title)
            name_display = kpi_details.get("name_display", kpi_key).replace('Indice di ', '')
            name_label = ttk.Label(card_frame, text=name_display, font=("Helvetica", 11, "bold")) # Slightly larger font for name
            name_label.grid(row=0, column=1, sticky="nw")

            # KPI Description
            description_short = kpi_details.get("description_short", "Nessuna descrizione breve.")
            desc_label = ttk.Label(card_frame, text=description_short, wraplength=180, justify=LEFT, font=("Helvetica", 9))
            desc_label.grid(row=1, column=1, sticky="new")
            
            # Tooltip for the entire card
            tooltip_text_plain = "\n".join([
                f"{kpi_details.get('name_display', kpi_key)}",
                f"Formula: {kpi_details.get('tooltip_info', {}).get('formula_display', 'N/D')}",
                f"Range Ottimale: {kpi_details.get('tooltip_info', {}).get('optimal_range_cee', 'N/D')}",
                f"Interpretazione: {kpi_details.get('tooltip_info', {}).get('interpretation_notes', 'N/D')}"
            ])
            if tooltip_text_plain and tooltip_text_plain != kpi_details.get('name_display', kpi_key):
                ToolTip(card_frame, text=tooltip_text_plain, bootstyle=(INFO, INVERSE), wraplength=400)
            
            # Make the card clickable to toggle the checkbox
            # Ensure a click on the frame or labels also toggles the checkbox
            clickable_elements = [card_frame, name_label, desc_label]
            for element in clickable_elements:
                element.bind("<Button-1>", lambda e, v=var: v.set(not v.get()))

            col_num += 1
            if col_num >= max_cols:
                col_num = 0
                row_num += 1
        
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=20, fill=X, side=BOTTOM)
        button_frame.grid_columnconfigure(0, weight=1)
        next_button = ttk.Button(button_frame, text="Avanti -> Inserisci Dati", command=self.process_kpi_selection, bootstyle="success")
        next_button.grid(row=0, column=0, padx=10, pady=10)

    def process_kpi_selection(self):
        selected_keys = [key for key, var in self.kpi_vars.items() if var.get()]
        
        valid, error_message = validate_kpi_selection(selected_keys, AVAILABLE_KPIS)
        if not valid:
            print(f"Errore Selezione KPI: {error_message}") 
            try:
                from ttkbootstrap.dialogs import Messagebox # Import here for optional use
                Messagebox.show_warning(error_message, title="Selezione KPI Non Valida")
            except ImportError:
                pass # Silently fail if Messagebox not available, error already printed
            return

        self.controller.set_data("selected_kpis", selected_keys)
        self.controller.show_frame("InputDataFrame")

    def update_view(self):
        current_selected_kpis = self.controller.get_data("selected_kpis", [])
        for key, var in self.kpi_vars.items():
            var.set(key in current_selected_kpis) 