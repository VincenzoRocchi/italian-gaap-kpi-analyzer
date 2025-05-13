import tkinter as tk
# from tkinter import ttk as tk_ttk # No longer needed directly here
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
# ScrolledFrame and ToolTip are used in frame modules, not directly in KpiApp
# from ttkbootstrap.scrolled import ScrolledFrame, ScrolledText 
# from ttkbootstrap.tooltip import ToolTip

# Import constants used by KpiApp or its direct methods
from app_logic.constants import (
    # BALANCE_SHEET_STRUCTURE, # Used in InputDataFrame
    # AVAILABLE_KPIS, # Used in SelectKpiFrame, InputDataFrame, ResultsFrame
    KPI_REQUIREMENTS, # Used in KpiApp.set_data and handle_data_submission
    # POSITION_NAMES, # Used in other frames
    # SECTION_TITLES, # Used in InputDataFrame
    # ALL_POSITIONS, # Used in InputDataFrame
    # CEE_TO_AUTOMOTIVE_CODES, # Used in InputDataFrame
    # AVAILABLE_MAPPINGS, # Used in InputDataFrame
)
from app_logic.calculator import calculate_selected_kpis, validate_balance_sheet
# validate_financial_data, validate_kpi_selection are used in frame modules
# from app_logic.validators import validate_financial_data, validate_kpi_selection 

# Import Frame Classes from the UI package
from ui.select_kpi_frame import SelectKpiFrame
from ui.input_data_frame import InputDataFrame
from ui.results_frame import ResultsFrame

class KpiApp(ttk.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("KPI CEE - Desktop App v0.3.1") # Incremented version
        self.geometry("1000x800")

        self.selected_kpis = []
        self.financial_data = {}
        self.calculated_results = {}
        self.required_positions = [] # Should be list after sorting
        self.selected_mapping_key = None
        self.balance_check_result = None

        main_app_frame = ttk.Frame(self)
        main_app_frame.pack(fill=BOTH, expand=True)

        navbar_frame = ttk.Frame(main_app_frame, padding=(10, 5), bootstyle="primary")
        navbar_frame.pack(fill=X, side=TOP)
        app_title_label = ttk.Label(navbar_frame, text="Analisi KPI - CEE (ITA)", font=("Helvetica", 14, "bold"), bootstyle="primary-inverse")
        app_title_label.pack(side=LEFT)

        container = ttk.Frame(main_app_frame, padding="10")
        container.pack(fill=BOTH, expand=True, side=TOP)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        footer_frame = ttk.Frame(main_app_frame, padding=(10, 5), bootstyle="light")
        footer_frame.pack(fill=X, side=BOTTOM)
        footer_label = ttk.Label(footer_frame, text="© 2024 Analisi Bilancio - Beta Version", bootstyle="light")
        footer_label.pack()

        self.frames = {}
        for F in (SelectKpiFrame, InputDataFrame, ResultsFrame):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("SelectKpiFrame")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
        if hasattr(frame, "update_view"):
            frame.update_view()

    def get_data(self, key, default=None):
        if key == "selected_kpis":
            return self.selected_kpis
        elif key == "financial_data":
            return self.financial_data
        elif key == "calculated_results":
            return self.calculated_results
        elif key == "required_positions":
            return self.required_positions
        elif key == "selected_mapping_key":
            return self.selected_mapping_key
        elif key == "balance_check_result":
            return getattr(self, "balance_check_result", default)
        return default

    def set_data(self, key, value):
        if key == "selected_kpis":
            self.selected_kpis = value
            new_required_positions = set()
            for kpi_key in self.selected_kpis:
                if kpi_key in KPI_REQUIREMENTS:
                    new_required_positions.update(KPI_REQUIREMENTS[kpi_key])
            self.required_positions = sorted(list(new_required_positions))
        elif key == "financial_data":
            self.financial_data = value
        elif key == "calculated_results":
            self.calculated_results = value
        elif key == "selected_mapping_key":
            self.selected_mapping_key = value
        elif key == "balance_check_result":
            self.balance_check_result = value

    def handle_data_submission(self):
        """Called by InputDataFrame to process submitted data."""
        current_financial_data = self.get_data("financial_data", {})

        validation_result = validate_balance_sheet(current_financial_data)
        self.set_data("balance_check_result", validation_result)
        
        balance_check_valid = validation_result.get("valid", False)
        if not balance_check_valid:
            assets = validation_result.get("assets", 0.0)
            liabilities_equity = validation_result.get("liabilities_equity", 0.0)
            diff = abs(assets - liabilities_equity)
            balance_check_messages = [
                f"Sbilancio rilevato: Attivo = {assets:.2f}, "
                f"Passivo + Netto = {liabilities_equity:.2f} (Differenza: {diff:.2f})"
            ]
            print(f"Avviso quadratura bilancio: {balance_check_messages}")
            try:
                from ttkbootstrap.dialogs import Messagebox
                Messagebox.show_warning("\n".join(balance_check_messages), title="Controllo Quadratura Bilancio")
            except ImportError:
                 print("ttkbootstrap.dialogs.Messagebox not available for warning display.")
        
        current_selected_kpis = self.get_data("selected_kpis", [])
        results = calculate_selected_kpis(current_financial_data, current_selected_kpis)
        self.set_data("calculated_results", results)
        
        self.show_frame("ResultsFrame")


if __name__ == "__main__":
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except Exception as e:
        print(f"Info: Could not set DPI awareness: {e} (Might not be an issue)")

    app = KpiApp(themename="litera")
    app.mainloop() 