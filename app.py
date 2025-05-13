import tkinter as tk
from tkinter import messagebox # For potential error popups
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

# Import from our modules
from app_logic.constants import (
    BALANCE_SHEET_STRUCTURE, 
    ALL_POSITIONS, 
    KPI_REQUIREMENTS, 
    AVAILABLE_KPIS,
    POSITION_NAMES, 
    SECTION_TITLES, 
    CEE_TO_AUTOMOTIVE_CODES, 
    AVAILABLE_MAPPINGS,
    get_all_positions
)
from app_logic.calculator import calculate_selected_kpis, validate_balance_sheet
from app_logic.validators import validate_financial_data, validate_kpi_selection

class KpiApp:
    def __init__(self, root):
        self.root = root
        self.root.title("KPI CEE Calculator - v0.3.0")
        self.root.geometry("800x600") # Adjust as needed

        # --- Persisted data (equivalent to Flask session) ---
        # We'll manage these as instance variables
        self.selected_kpi_keys = []
        self.required_positions = []
        self.balance_sheet_data = {}
        self.calculated_kpis = {}
        # --- End Persisted data ---

        # --- Main application frames ---
        # We'll switch between these frames to simulate pages
        self.container = ttk.Frame(root, padding=10)
        self.container.pack(fill=BOTH, expand=YES)

        self.frames = {}
        for F in (SelectKpiFrame, InputDataFrame, ResultsFrame): # Define these classes later
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            # Place all frames in the same spot; we'll raise one at a time
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("SelectKpiFrame")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()
        # You might want to call a 'refresh' or 'on_show' method on the frame here
        if hasattr(frame, 'on_show'):
            frame.on_show()

    def get_selected_kpis(self):
        return self.selected_kpi_keys

    def set_selected_kpis(self, kpi_keys):
        self.selected_kpi_keys = kpi_keys
        # Determine required positions based on selected KPIs
        required_pos_set = set()
        for key in self.selected_kpi_keys:
            if key in KPI_REQUIREMENTS:
                required_pos_set.update(KPI_REQUIREMENTS[key])
        self.required_positions = sorted(list(required_pos_set))
        # Initialize balance sheet data for these positions
        self.balance_sheet_data = {str(pos): 0.0 for pos in self.required_positions}


class SelectKpiFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = ttk.Label(self, text="Select KPIs to Calculate", font=("Helvetica", 16, "bold"))
        label.pack(pady=20)

        # --- KPI Selection Area ---
        self.kpi_vars = {}
        kpi_frame = ttk.Frame(self)
        kpi_frame.pack(pady=10, padx=20, fill=X)

        # Create two columns for KPIs
        col1 = ttk.Frame(kpi_frame)
        col1.pack(side=LEFT, fill=X, expand=True, padx=5)
        col2 = ttk.Frame(kpi_frame)
        col2.pack(side=LEFT, fill=X, expand=True, padx=5)

        kpi_items = list(AVAILABLE_KPIS.items())
        midpoint = (len(kpi_items) + 1) // 2

        for i, (key, kpi_details) in enumerate(kpi_items):
            var = tk.BooleanVar()
            # The kpi_details already contains the name directly from AVAILABLE_KPIS.items()
            cb = ttk.Checkbutton(col1 if i < midpoint else col2, text=kpi_details["name_display"], variable=var, bootstyle="primary")
            cb.pack(anchor="w", pady=2)
            self.kpi_vars[key] = var
        # --- End KPI Selection Area ---

        proceed_button = ttk.Button(self, text="Next: Input Financial Data",
                                   command=self.proceed_to_input, bootstyle="success")
        proceed_button.pack(pady=20)

    def proceed_to_input(self):
        selected_keys = [key for key, var in self.kpi_vars.items() if var.get()]
        
        # AVAILABLE_KPIS is imported at the module level and can be used directly here.
        valid, error_message = validate_kpi_selection(selected_keys, AVAILABLE_KPIS)
        if not valid:
            messagebox.showwarning("Invalid Selection", error_message)
            return

        self.controller.set_selected_kpis(selected_keys)
        self.controller.show_frame("InputDataFrame")

    def on_show(self):
        # Reset checkboxes when this frame is shown
        for key in self.kpi_vars:
            self.kpi_vars[key].set(False)
        # Reset controller data that depends on this page
        self.controller.selected_kpi_keys = []
        self.controller.required_positions = []
        self.controller.balance_sheet_data = {}


class InputDataFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        # Placeholder - We will build this UI next
        self.title_label = ttk.Label(self, text="Input Financial Data", font=("Helvetica", 16, "bold"))
        self.title_label.pack(pady=10)
        
        self.inputs_frame = ttk.Frame(self) # Frame to hold dynamic inputs
        self.inputs_frame.pack(pady=10, padx=10, fill=BOTH, expand=True)

        # Navigation buttons frame
        nav_frame = ttk.Frame(self)
        nav_frame.pack(fill=X, pady=10, padx=10)

        back_button = ttk.Button(nav_frame, text="Back to KPI Selection",
                                 command=lambda: controller.show_frame("SelectKpiFrame"),
                                 bootstyle="secondary")
        back_button.pack(side=LEFT, padx=5)

        calculate_button = ttk.Button(nav_frame, text="Calculate KPIs",
                                 command=self.process_calculation, # Changed to a method
                                 bootstyle="primary")
        calculate_button.pack(side=RIGHT, padx=5)
        
        self.data_entries = {} # To store Entry widgets


    def on_show(self):
        # Clear previous dynamic content from inputs_frame
        for widget in self.inputs_frame.winfo_children():
            widget.destroy()
        self.data_entries.clear()

        if not self.controller.selected_kpi_keys:
            self.title_label.config(text="No KPIs Selected. Go Back.")
            return

        self.title_label.config(text=f"Input Data for {len(self.controller.selected_kpi_keys)} Selected KPIs")
        
        # Dynamically build the input form here
        # This is a simplified version; a scrollable area would be better for many inputs
        
        # Group inputs by main category and subcategory from BALANCE_SHEET_STRUCTURE
        # For simplicity, let's just list all required positions for now
        # A more complex layout would iterate through BALANCE_SHEET_STRUCTURE
        
        current_row = 0
        for pos_key_str in self.controller.required_positions:
            pos_key = int(pos_key_str) # Assuming positions in constants are integers
            pos_name = POSITION_NAMES.get(pos_key, f"Position {pos_key}")

            ttk.Label(self.inputs_frame, text=pos_name + ":").grid(row=current_row, column=0, sticky="w", padx=5, pady=2)
            
            entry_var = tk.StringVar(value=str(self.controller.balance_sheet_data.get(pos_key_str, 0.0)))
            entry_widget = ttk.Entry(self.inputs_frame, textvariable=entry_var, width=20)
            entry_widget.grid(row=current_row, column=1, sticky="ew", padx=5, pady=2)
            self.data_entries[pos_key_str] = entry_var
            current_row += 1
        
        self.inputs_frame.columnconfigure(1, weight=1) # Make entry column expandable

    def process_calculation(self):
        # 1. Retrieve data from self.data_entries
        raw_form_data = {key: var.get() for key, var in self.data_entries.items()}

        # 2. Validate financial data
        # validate_financial_data expects a Flask-like form object or a dict.
        # We need to adapt its usage or adapt the data.
        # For now, let's assume direct usage with the dict is fine if types are okay.
        # The original validator might need adjustment if it heavily relies on Flask's MultiDict.
        
        # Convert to float, handle potential errors
        parsed_data = {}
        errors = {}
        for key, value_str in raw_form_data.items():
            try:
                parsed_data[key] = float(value_str)
            except ValueError:
                errors[key] = f"Invalid number for {POSITION_NAMES.get(int(key), key)}" # Assuming key is int convertible

        if errors:
            error_message = "\n".join(errors.values())
            messagebox.showerror("Input Error", error_message)
            return

        self.controller.balance_sheet_data = parsed_data

        # 3. Perform balance sheet validation (from calculator.py)
        balance_check_messages = validate_balance_sheet(self.controller.balance_sheet_data)
        # For now, just print this. In a real UI, display it.
        if balance_check_messages: # If returns a list of messages
             messagebox.showwarning("Balance Check", "\n".join(balance_check_messages))
             # Decide if you want to proceed despite warnings, or return

        # 4. Calculate KPIs
        self.controller.calculated_kpis = calculate_selected_kpis(
            self.controller.balance_sheet_data,
            self.controller.selected_kpi_keys
        )
        
        self.controller.show_frame("ResultsFrame")


class ResultsFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        self.title_label = ttk.Label(self, text="KPI Results", font=("Helvetica", 16, "bold"))
        self.title_label.pack(pady=10)

        self.results_text_area = ttk.ScrolledText(self, wrap=WORD, height=20, width=70)
        self.results_text_area.pack(pady=10, padx=10, fill=BOTH, expand=True)
        self.results_text_area.config(state=DISABLED) # Make it read-only initially

        # Navigation buttons frame
        nav_frame = ttk.Frame(self)
        nav_frame.pack(fill=X, pady=10, padx=10)
        
        back_button = ttk.Button(nav_frame, text="Back to Input Data",
                                 command=lambda: controller.show_frame("InputDataFrame"),
                                 bootstyle="secondary")
        back_button.pack(side=LEFT, padx=5)
        
        restart_button = ttk.Button(nav_frame, text="Start Over",
                                 command=lambda: controller.show_frame("SelectKpiFrame"),
                                 bootstyle="info")
        restart_button.pack(side=RIGHT, padx=5)

    def on_show(self):
        self.results_text_area.config(state=NORMAL) # Enable writing
        self.results_text_area.delete(1.0, END) # Clear previous results

        if not self.controller.calculated_kpis:
            self.results_text_area.insert(END, "No KPIs calculated yet. Go back to input data.")
            self.results_text_area.config(state=DISABLED)
            return

        results_str = "Calculated KPIs:\n\n"
        for kpi_key, result_info in self.controller.calculated_kpis.items():
            kpi_name = AVAILABLE_KPIS.get(kpi_key, {}).get("name", kpi_key)
            results_str += f"--- {kpi_name} ---\n"
            results_str += f"  Value: {result_info.get('value', 'N/A')}\n"
            results_str += f"  Interpretation: {result_info.get('interpretation', 'N/A')}\n"
            results_str += f"  Formula: {result_info.get('formula', 'N/A')}\n"
            
            results_str += "  Input Data Used:\n"
            # Assuming KPI_REQUIREMENTS maps kpi_key to a list of position keys (integers)
            if kpi_key in KPI_REQUIREMENTS:
                for pos_key in KPI_REQUIREMENTS[kpi_key]:
                    pos_key_str = str(pos_key)
                    pos_name = POSITION_NAMES.get(pos_key, f"Position {pos_key_str}")
                    value = self.controller.balance_sheet_data.get(pos_key_str, "N/A")
                    results_str += f"    {pos_name}: {value}\n"
            results_str += "\n"
        
        self.results_text_area.insert(END, results_str)
        self.results_text_area.config(state=DISABLED) # Make it read-only again

def main():
    # Use a ttkbootstrap theme, e.g., "litera", "darkly", "superhero"
    root = ttk.Window(themename="litera") 
    app = KpiApp(root)
    root.mainloop()

if __name__ == '__main__':
    main() 