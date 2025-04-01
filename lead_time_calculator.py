import datetime
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
# Using python-dateutil for easier date calculations if needed, though timedelta might suffice
# from dateutil.relativedelta import relativedelta
import holidays as pyholidays # Using pyholidays as a potential fallback/reference

# --- Configuration & Data ---

# --- Default Lead Times (Modifiable) ---
DEFAULT_FABRIC_GREIGE_LEAD_TIME_DAYS = 25
DEFAULT_FABRIC_DYEING_LEAD_TIME_DAYS = 15
DEFAULT_WAREHOUSE_TO_STORE_TRANSIT_DAYS = 7

# --- Transit Time: Finished Garment to USA Warehouse (by Lading Point) ---
GARMENT_TRANSIT_TIMES_USA = {
    "CGPBD": {"country": "Bangladesh", "port": "Chittagong", "days": 66},
    "PNHKH": {"country": "Cambodia", "port": "Phnom Penh", "days": 55},
    "NGBCN": {"country": "China", "port": "Ningbo", "days": 42},
    "SHACN": {"country": "China", "port": "Shanghai", "days": 42},
    "TAOCN": {"country": "China", "port": "Qingdao", "days": 44},
    "XMNCN": {"country": "China", "port": "Xiamen", "days": 42},
    "YTNCN": {"country": "China", "port": "Yantian", "days": 42},
    "DLCCN": {"country": "China", "port": "Dalian", "days": 41},
    "STCGT": {"country": "Guatemala", "port": "Guatemala", "days": 18},
    "HKGHK": {"country": "Hong Kong", "port": "Hong Kong", "days": 42}, # Assuming HK is separate entity for holidays
    "MAAIN": {"country": "India", "port": "Chennai", "days": 76},
    "ENRIN": {"country": "India", "port": "Chennai", "days": 76}, # Duplicate code, same data
    "MUNIN": {"country": "India", "port": "Mundra/Nhava Sheva", "days": 62},
    "BOMIN": {"country": "India", "port": "Mundra/Nhava Sheva", "days": 62}, # Duplicate code, same data
    "JKTID": {"country": "Indonesia", "port": "Jakarta", "days": 61},
    "SRGID": {"country": "Indonesia", "port": "Semarang", "days": 65},
    "SUBID": {"country": "Indonesia", "port": "Surabaya", "days": 61},
    "AMMJO": {"country": "Jordan", "port": "Haifa", "days": 42},
    "PUSKR": {"country": "Korea", "port": "Busan", "days": 42},
    "BQMPK": {"country": "Pakistan", "port": "Qasim", "days": 64}, # Pakistan wasn't in initial list but is here
    "CMBLK": {"country": "Sri Lanka", "port": "Colombo", "days": 55},
    "LCHTH": {"country": "Thailand", "port": "Laem Chabanag", "days": 48},
    "HPHVN": {"country": "Vietnam", "port": "Haiphong", "days": 51},
    "SGNVN": {"country": "Vietnam", "port": "Saigon", "days": 48},
    "VUTVN": {"country": "Vietnam", "port": "Vung Tao", "days": 48},
    # Add other lading points if necessary
}

# --- Transit Time: Fabric to Factory (by Origin/Destination Country) ---
FABRIC_TRANSIT_TIMES = {
    ("Bangladesh", "Bangladesh"): 5, ("Bangladesh", "Cambodia"): 28, ("Bangladesh", "Guatemala"): 35,
    ("Bangladesh", "India"): 14, ("Bangladesh", "Indonesia"): 28, ("Bangladesh", "Jordan"): 35,
    ("Bangladesh", "Sri Lanka"): 14, ("Bangladesh", "Thailand"): 28, ("Bangladesh", "Vietnam"): 28,
    ("Cambodia", "Bangladesh"): 28, ("Cambodia", "Cambodia"): 5, ("Cambodia", "Guatemala"): 35,
    ("Cambodia", "India"): 28, ("Cambodia", "Indonesia"): 21, ("Cambodia", "Jordan"): 35,
    ("Cambodia", "Sri Lanka"): 28, ("Cambodia", "Thailand"): 21, ("Cambodia", "Vietnam"): 21,
    ("China", "Bangladesh"): 28, ("China", "Cambodia"): 21, ("China", "Guatemala"): 35,
    ("China", "India"): 28, ("China", "Indonesia"): 21, ("China", "Jordan"): 35,
    ("China", "Sri Lanka"): 28, ("China", "Thailand"): 21, ("China", "Vietnam"): 14,
    ("Guatemala", "Guatemala"): 5,
    ("India", "Bangladesh"): 14, ("India", "Cambodia"): 28, ("India", "Guatemala"): 35,
    ("India", "India"): 5, ("India", "Indonesia"): 28, ("India", "Jordan"): 35,
    ("India", "Sri Lanka"): 21, ("India", "Thailand"): 28, ("India", "Vietnam"): 28,
    ("Indonesia", "Bangladesh"): 21, ("Indonesia", "Cambodia"): 21, ("Indonesia", "Guatemala"): 35,
    ("Indonesia", "India"): 21, ("Indonesia", "Indonesia"): 5, ("Indonesia", "Jordan"): 35,
    ("Indonesia", "Sri Lanka"): 21, ("Indonesia", "Thailand"): 21, ("Indonesia", "Vietnam"): 21,
    ("Korea", "Bangladesh"): 28, ("Korea", "Cambodia"): 21, ("Korea", "Guatemala"): 35,
    ("Korea", "India"): 28, ("Korea", "Indonesia"): 28, ("Korea", "Jordan"): 35,
    ("Korea", "Sri Lanka"): 28, ("Korea", "Thailand"): 21, ("Korea", "Vietnam"): 21,
    ("Sri Lanka", "Bangladesh"): 14, ("Sri Lanka", "Cambodia"): 21, ("Sri Lanka", "Guatemala"): 35,
    ("Sri Lanka", "India"): 21, ("Sri Lanka", "Indonesia"): 21, ("Sri Lanka", "Jordan"): 35,
    ("Sri Lanka", "Sri Lanka"): 5, ("Sri Lanka", "Thailand"): 21, ("Sri Lanka", "Vietnam"): 21,
    ("Taiwan", "Bangladesh"): 28, ("Taiwan", "Cambodia"): 21, ("Taiwan", "Guatemala"): 35,
    ("Taiwan", "India"): 28, ("Taiwan", "Indonesia"): 21, ("Taiwan", "Jordan"): 35,
    ("Taiwan", "Sri Lanka"): 28, ("Taiwan", "Thailand"): 21, ("Taiwan", "Vietnam"): 14,
    ("Thailand", "Bangladesh"): 28, ("Thailand", "Cambodia"): 21, ("Thailand", "Guatemala"): 35,
    ("Thailand", "India"): 28, ("Thailand", "Indonesia"): 21, ("Thailand", "Jordan"): 35,
    ("Thailand", "Sri Lanka"): 28, ("Thailand", "Thailand"): 5, ("Thailand", "Vietnam"): 21,
    ("USA", "Guatemala"): 14, # Fabric from USA?
    ("Vietnam", "Bangladesh"): 28, ("Vietnam", "Cambodia"): 21, ("Vietnam", "Guatemala"): 35,
    ("Vietnam", "India"): 28, ("Vietnam", "Indonesia"): 21, ("Vietnam", "Jordan"): 35,
    ("Vietnam", "Sri Lanka"): 28, ("Vietnam", "Thailand"): 21, ("Vietnam", "Vietnam"): 5,
    # Add other combinations if needed
}

# --- Garment Production Time (by Category & Bonding) ---
GARMENT_PRODUCTION_TIMES = {
    ("Undies", "No Bonding"): 30, ("Undies", "With Bonding"): 35,
    ("Bra/Bralette", "No Bonding"): 33, ("Bra/Bralette", "With Bonding"): 38,
    ("Offline Legging/Short", "No Bonding"): 28, ("Offline Legging/Short", "With Bonding"): 33,
    ("Offline Sports Bra", "No Bonding"): 30, ("Offline Sports Bra", "With Bonding"): 35,
    ("Offline Active Apparel", "No Bonding"): 30, ("Offline Active Apparel", "With Bonding"): 35,
    ("Apparel Top & Bottom", "No Bonding"): 28, ("Apparel Top & Bottom", "With Bonding"): 35,
    ("Apparel Dresses", "No Bonding"): 28, ("Apparel Dresses", "With Bonding"): 35,
    ("Swim Top", "No Bonding"): 28,
    ("Swim Bottom", "No Bonding"): 28,
    ("Swim One Pc", "No Bonding"): 28,
    # Assume bonding not applicable for Swim unless specified otherwise
}

# --- Specific Holiday Closing Periods (Country -> List of Tuples (Start Date, End Date)) ---
# Dates are inclusive. Format: YYYY-MM-DD
# Ensure years are updated or handled dynamically if calculator is used long-term
HOLIDAY_CLOSURES = {
    "China": [("2025-01-20", "2025-02-10"), ("2025-05-01", "2025-05-06"), ("2025-10-01", "2025-10-08")],
    "Vietnam": [("2025-01-26", "2025-02-04")],
    "Hong Kong": [("2025-01-27", "2025-02-03"), ("2025-05-01", "2025-05-06"), ("2025-10-01", "2025-10-08")],
    "Cambodia": [("2025-01-25", "2025-02-10"), ("2025-04-14", "2025-04-16"), ("2025-05-01", "2025-05-01"), ("2025-05-14", "2025-05-15"), ("2025-09-21", "2025-09-24")],
    "Taiwan": [("2025-01-24", "2025-02-04")],
    "Indonesia": [("2025-03-29", "2025-04-13"), ("2025-06-06", "2025-06-13")],
    "Jordan": [("2025-03-29", "2025-04-13"), ("2025-06-06", "2025-06-13")],
    "Bangladesh": [("2025-03-29", "2025-04-13"), ("2025-06-06", "2025-06-13")],
    "Thailand": [("2025-04-13", "2025-04-16"), ("2025-05-01", "2025-05-01")],
    "Sri Lanka": [("2025-04-12", "2025-04-20")],
    "India": [("2025-10-28", "2025-11-11")],
    "USA": [], # Add major US holidays if warehouse closure needs to be factored in
    # Add other countries/holidays as needed (e.g., Korea, Guatemala, Pakistan)
}

# Map Lading Point Countries to Holiday Country Keys if needed
# Ensures GARMENT_TRANSIT_TIMES_USA country names match HOLIDAY_CLOSURES keys
COUNTRY_HOLIDAY_MAP = {
    "Bangladesh": "Bangladesh",
    "Cambodia": "Cambodia",
    "China": "China",
    "Guatemala": "Guatemala", # No specific 2025 closures provided
    "Hong Kong": "Hong Kong",
    "India": "India",
    "Indonesia": "Indonesia",
    "Jordan": "Jordan",
    "Korea": "Korea", # No specific 2025 closures provided
    "Pakistan": "Pakistan", # No specific 2025 closures provided
    "Sri Lanka": "Sri Lanka",
    "Taiwan": "Taiwan", # Fabric country only
    "Thailand": "Thailand",
    "Vietnam": "Vietnam",
    "USA": "USA"
}


# --- Helper Functions ---

def parse_date(date_str):
    """Parses a date string (YYYY-MM-DD) into a date object."""
    try:
        return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return None

def get_specific_holidays_in_range(country_key, period_start_date, period_end_date):
    """Finds the number of specific closure days falling within a given period."""
    closure_days_count = 0
    closure_dates_in_period = set()

    if country_key and country_key in HOLIDAY_CLOSURES:
        for start_str, end_str in HOLIDAY_CLOSURES[country_key]:
            h_start = parse_date(start_str)
            h_end = parse_date(end_str)
            if not h_start or not h_end: continue # Skip invalid date formats

            # Check for overlap between holiday period [h_start, h_end]
            # and calculation period [period_start_date, period_end_date]
            overlap_start = max(period_start_date, h_start)
            overlap_end = min(period_end_date, h_end)

            if overlap_start <= overlap_end:
                current_day = overlap_start
                while current_day <= overlap_end:
                    # Ensure we only count days within the *original* period duration being calculated
                    # And avoid double-counting if multiple holidays overlap the same day
                    if period_start_date <= current_day <= period_end_date and current_day not in closure_dates_in_period:
                        # Optionally exclude weekends if holidays shouldn't count on weekends
                        # if current_day.weekday() < 5: # Monday to Friday
                        closure_dates_in_period.add(current_day)
                        # print(f"DEBUG: Adding holiday {current_day} for {country_key}")
                    current_day += datetime.timedelta(days=1)

    closure_days_count = len(closure_dates_in_period)
    # if closure_days_count > 0:
        # print(f"DEBUG: Found {closure_days_count} closure days for {country_key} between {period_start_date} and {period_end_date}")
    return closure_days_count

def add_lead_time(start_date, lead_days, country_code=None, description="", is_transit=False, log_details=False):
    """Adds lead time days. Adds calendar days for transit, otherwise adds lead days + holidays."""
    if log_details:
        print(f"Calculating {description}: Adding {lead_days} days to {start_date} (Country: {country_code or 'N/A'})")

    if is_transit:
        end_date = start_date + datetime.timedelta(days=lead_days)
        if log_details:
            print(f"  - Transit: Added {lead_days} calendar days.")
            print(f"  - Result: {end_date}")
        return end_date
    else:
        # Production/Warehouse steps: Add lead days and check for holidays within that period
        current_date = start_date
        days_added = 0
        total_holiday_offset = 0

        while days_added < lead_days:
            current_date += datetime.timedelta(days=1)
            country_key = COUNTRY_HOLIDAY_MAP.get(country_code)
            is_holiday = False
            if country_key and country_key in HOLIDAY_CLOSURES:
                for start_str, end_str in HOLIDAY_CLOSURES[country_key]:
                    h_start, h_end = parse_date(start_str), parse_date(end_str)
                    if h_start and h_end and h_start <= current_date <= h_end:
                        is_holiday = True
                        break

            # Optional: Skip weekends too?
            # is_weekend = current_date.weekday() >= 5
            # if is_holiday or is_weekend:
            if is_holiday:
                total_holiday_offset += 1
                # print(f"DEBUG: Skipping holiday {current_date} for {country_key}")
                continue # Skip this day, don't increment days_added

            days_added += 1 # Count as a working day added

        final_end_date = start_date + datetime.timedelta(days=lead_days + total_holiday_offset)

        if log_details:
            print(f"  - Added {lead_days} lead days + {total_holiday_offset} holiday days.")
            total_days = lead_days + total_holiday_offset
            print(f"  - Result: {final_end_date} ({total_days} total calendar days)")
        return final_end_date

def subtract_lead_time(end_date, lead_days, country_code=None, description="", is_transit=False, log_details=False):
    """Subtracts lead time days. Subtracts calendar days for transit, otherwise subtracts lead days + holidays."""
    if log_details:
        print(f"Calculating {description}: Subtracting {lead_days} days from {end_date} (Country: {country_code or 'N/A'})")

    if is_transit:
        start_date = end_date - datetime.timedelta(days=lead_days)
        if log_details:
            print(f"  - Transit: Subtracted {lead_days} calendar days.")
            print(f"  - Result: {start_date}")
        return start_date
    else:
        # Production/Warehouse steps: Subtract lead days, skipping holidays
        current_date = end_date
        days_subtracted = 0
        total_holiday_offset = 0

        # Pre-fetch holidays in a plausible range to avoid checking dict repeatedly
        holidays_in_range = set()
        country_key = COUNTRY_HOLIDAY_MAP.get(country_code)
        if country_key and country_key in HOLIDAY_CLOSURES:
            check_start = end_date - datetime.timedelta(days=lead_days * 2 + 45) # Estimate range
            check_end = end_date
            for start_str, end_str in HOLIDAY_CLOSURES[country_key]:
                h_start, h_end = parse_date(start_str), parse_date(end_str)
                if h_start and h_end:
                    curr_h = h_start
                    while curr_h <= h_end:
                        if check_start <= curr_h <= check_end:
                             holidays_in_range.add(curr_h)
                        curr_h += datetime.timedelta(days=1)

        while days_subtracted < lead_days:
            current_date -= datetime.timedelta(days=1)
            is_holiday = current_date in holidays_in_range

            # Optional: Skip weekends too?
            # is_weekend = current_date.weekday() >= 5
            # if is_holiday or is_weekend:
            if is_holiday:
                total_holiday_offset += 1
                # print(f"DEBUG: Skipping holiday {current_date} for {country_key}")
                continue # Skip this day, don't increment days_subtracted

            days_subtracted += 1 # Count as a working day subtracted

        final_start_date = end_date - datetime.timedelta(days=lead_days + total_holiday_offset)

        if log_details:
            print(f"  - Subtracted {lead_days} lead days + {total_holiday_offset} holiday days.")
            total_days = lead_days + total_holiday_offset
            print(f"  - Result: {final_start_date} ({total_days} total calendar days)")
        return final_start_date


# --- Calculation Logic ---

def calculate_arrival_date(buy_date_str, fabric_country, garment_lading_point, product_category, bonding_option):
    """Calculates expected arrival date given the buy placement date. Returns result string or error string."""
    start_date = parse_date(buy_date_str)
    if not start_date:
        return "Error: Invalid buy date format. Please use YYYY-MM-DD."

    log_calc = True # Set to True to print calculation steps to console
    if log_calc:
         print(f"\n--- Calculating Arrival Date from Buy Date: {start_date} ---")

    # 1. Fabric Greige Production
    greige_days = DEFAULT_FABRIC_GREIGE_LEAD_TIME_DAYS
    fabric_prod_country = fabric_country # Assume greige happens in fabric country
    current_date = add_lead_time(start_date, greige_days, fabric_prod_country, "Fabric Greige Production", log_details=log_calc)

    # 2. Fabric Dyeing Production
    dyeing_days = DEFAULT_FABRIC_DYEING_LEAD_TIME_DAYS
    # Assume dyeing also happens in fabric country, adjust if needed
    current_date = add_lead_time(current_date, dyeing_days, fabric_prod_country, "Fabric Dyeing Production", log_details=log_calc)

    # 3. Fabric Transit to Factory
    garment_country_info = GARMENT_TRANSIT_TIMES_USA.get(garment_lading_point)
    if not garment_country_info:
        return f"Error: Lading point '{garment_lading_point}' not found."
    garment_country = garment_country_info.get("country")
    if not garment_country:
        return f"Error: Lading point '{garment_lading_point}' missing country information."

    fabric_transit_key = (fabric_country, garment_country)
    fabric_transit_days = FABRIC_TRANSIT_TIMES.get(fabric_transit_key)
    if fabric_transit_days is None:
        return f"Error: Fabric transit time from '{fabric_country}' to '{garment_country}' not found."
    current_date = add_lead_time(current_date, fabric_transit_days, description="Fabric Transit to Factory", is_transit=True, log_details=log_calc)

    # 4. Garment Production
    garment_prod_key = (product_category, bonding_option)
    garment_prod_days = GARMENT_PRODUCTION_TIMES.get(garment_prod_key)
    if garment_prod_days is None:
        # Try finding category without bonding if bonding option wasn't applicable/found
        garment_prod_key_nobond = (product_category, "No Bonding")
        garment_prod_days = GARMENT_PRODUCTION_TIMES.get(garment_prod_key_nobond)
        if garment_prod_days is None:
             return f"Error: Garment production time for '{product_category}' not found (checked with/without bonding)."
        else:
             if log_calc:
                 print(f"Warning: Bonding option '{bonding_option}' not found for '{product_category}'. Using 'No Bonding' time.")

    current_date = add_lead_time(current_date, garment_prod_days, garment_country, "Garment Production", log_details=log_calc)

    # 5. Finished Garment Transit to USA Warehouse
    garment_transit_days_usa = garment_country_info["days"]
    current_date = add_lead_time(current_date, garment_transit_days_usa, description=f"Garment Transit from {garment_lading_point} to USA", is_transit=True, log_details=log_calc)

    # 6. Warehouse to Store Transit
    warehouse_store_days = DEFAULT_WAREHOUSE_TO_STORE_TRANSIT_DAYS
    # Decide if this transit includes holidays/weekends. Currently assuming it does NOT (uses add_lead_time with USA holidays)
    # Change is_transit=True if it should be pure calendar days.
    current_date = add_lead_time(current_date, warehouse_store_days, "USA", "Warehouse to Store Transit", is_transit=False, log_details=log_calc) # is_transit=False considers USA holidays

    if log_calc:
        print(f"\n--- Calculation Complete ---")
    final_date_str = current_date.strftime('%Y-%m-%d')
    return f"Estimated Store Arrival Date: {final_date_str}"

def calculate_buy_date(arrival_date_str, fabric_country, garment_lading_point, product_category, bonding_option):
    """Calculates the required buy placement date given the desired arrival date. Returns result string or error string."""
    end_date = parse_date(arrival_date_str)
    if not end_date:
        return "Error: Invalid arrival date format. Please use YYYY-MM-DD."

    log_calc = True # Set to True to print calculation steps to console
    if log_calc:
        print(f"\n--- Calculating Buy Date from Store Arrival Date: {end_date} ---")

    # 6. Warehouse to Store Transit (Subtract)
    warehouse_store_days = DEFAULT_WAREHOUSE_TO_STORE_TRANSIT_DAYS
    # Assume reverse is also not just calendar days (skips USA holidays if defined)
    current_date = subtract_lead_time(end_date, warehouse_store_days, "USA", "Warehouse to Store Transit", is_transit=False, log_details=log_calc)

    # 5. Finished Garment Transit to USA Warehouse (Subtract)
    garment_country_info = GARMENT_TRANSIT_TIMES_USA.get(garment_lading_point)
    if not garment_country_info:
        return f"Error: Lading point '{garment_lading_point}' not found."
    garment_transit_days_usa = garment_country_info["days"]
    current_date = subtract_lead_time(current_date, garment_transit_days_usa, description=f"Garment Transit from {garment_lading_point} to USA", is_transit=True, log_details=log_calc)

    # 4. Garment Production (Subtract)
    garment_prod_key = (product_category, bonding_option)
    garment_prod_days = GARMENT_PRODUCTION_TIMES.get(garment_prod_key)
    if garment_prod_days is None:
         garment_prod_key_nobond = (product_category, "No Bonding")
         garment_prod_days = GARMENT_PRODUCTION_TIMES.get(garment_prod_key_nobond)
         if garment_prod_days is None:
              return f"Error: Garment production time for '{product_category}' not found (checked with/without bonding)."
         else:
              if log_calc:
                  print(f"Warning: Bonding option '{bonding_option}' not found for '{product_category}'. Using 'No Bonding' time.")

    garment_country = garment_country_info.get("country")
    if not garment_country:
         return f"Error: Lading point '{garment_lading_point}' missing country information."
    current_date = subtract_lead_time(current_date, garment_prod_days, garment_country, "Garment Production", log_details=log_calc)

    # 3. Fabric Transit to Factory (Subtract)
    fabric_transit_key = (fabric_country, garment_country)
    fabric_transit_days = FABRIC_TRANSIT_TIMES.get(fabric_transit_key)
    if fabric_transit_days is None:
        return f"Error: Fabric transit time from '{fabric_country}' to '{garment_country}' not found."
    current_date = subtract_lead_time(current_date, fabric_transit_days, description="Fabric Transit to Factory", is_transit=True, log_details=log_calc)

    # 2. Fabric Dyeing Production (Subtract)
    dyeing_days = DEFAULT_FABRIC_DYEING_LEAD_TIME_DAYS
    fabric_prod_country = fabric_country # Assume dyeing happens in fabric country
    current_date = subtract_lead_time(current_date, dyeing_days, fabric_prod_country, "Fabric Dyeing Production", log_details=log_calc)

    # 1. Fabric Greige Production (Subtract)
    greige_days = DEFAULT_FABRIC_GREIGE_LEAD_TIME_DAYS
    current_date = subtract_lead_time(current_date, greige_days, fabric_prod_country, "Fabric Greige Production", log_details=log_calc)

    if log_calc:
        print(f"\n--- Calculation Complete ---")
    final_date_str = current_date.strftime('%Y-%m-%d')
    return f"Required Buy Placement Date: {final_date_str}"

# --- GUI Implementation ---

class LeadTimeApp:
    def __init__(self, master):
        self.master = master
        master.title("Lead Time Calculator")
        master.geometry("450x450") # Adjusted size

        # Style
        self.style = ttk.Style()
        self.style.theme_use('clam') # Use a modern theme if available

        # Input Frame
        input_frame = ttk.Frame(master, padding="10")
        input_frame.pack(expand=True, fill=tk.BOTH)

        # --- Widgets ---
        row_num = 0

        # Calculation Direction
        ttk.Label(input_frame, text="Direction:").grid(row=row_num, column=0, sticky=tk.W, pady=2)
        self.direction_var = tk.StringVar(value="F")
        ttk.Radiobutton(input_frame, text="Forward (Buy->Arrival)", variable=self.direction_var, value="F", command=self.update_date_label).grid(row=row_num, column=1, sticky=tk.W)
        ttk.Radiobutton(input_frame, text="Backward (Arrival->Buy)", variable=self.direction_var, value="B", command=self.update_date_label).grid(row=row_num, column=2, sticky=tk.W)
        row_num += 1

        # Date Input
        self.date_label = ttk.Label(input_frame, text="Buy Date (YYYY-MM-DD):")
        self.date_label.grid(row=row_num, column=0, sticky=tk.W, pady=2)
        self.date_entry = ttk.Entry(input_frame, width=25)
        self.date_entry.grid(row=row_num, column=1, columnspan=2, sticky=tk.W)
        # Pre-fill with today's date
        self.date_entry.insert(0, datetime.date.today().strftime('%Y-%m-%d'))
        row_num += 1

        # Fabric Country
        ttk.Label(input_frame, text="Fabric Origin Country:").grid(row=row_num, column=0, sticky=tk.W, pady=2)
        self.fabric_countries = sorted(list(set(k[0] for k in FABRIC_TRANSIT_TIMES.keys())))
        self.fabric_country_combo = ttk.Combobox(input_frame, values=self.fabric_countries, state="readonly", width=23)
        self.fabric_country_combo.grid(row=row_num, column=1, columnspan=2, sticky=tk.W)
        if self.fabric_countries: self.fabric_country_combo.current(0)
        row_num += 1

        # Garment Lading Point
        ttk.Label(input_frame, text="Garment Lading Point:").grid(row=row_num, column=0, sticky=tk.W, pady=2)
        self.lading_points_display = [f"{p} ({GARMENT_TRANSIT_TIMES_USA[p].get('port','?')}, {GARMENT_TRANSIT_TIMES_USA[p].get('country','?')})" for p in sorted(GARMENT_TRANSIT_TIMES_USA.keys())]
        self.lading_points_keys = sorted(GARMENT_TRANSIT_TIMES_USA.keys())
        self.lading_point_combo = ttk.Combobox(input_frame, values=self.lading_points_display, state="readonly", width=35)
        self.lading_point_combo.grid(row=row_num, column=1, columnspan=2, sticky=tk.W)
        if self.lading_points_display: self.lading_point_combo.current(0)
        row_num += 1

        # Product Category
        ttk.Label(input_frame, text="Product Category:").grid(row=row_num, column=0, sticky=tk.W, pady=2)
        self.categories = sorted(list(set(k[0] for k in GARMENT_PRODUCTION_TIMES.keys())))
        self.category_combo = ttk.Combobox(input_frame, values=self.categories, state="readonly", width=23)
        self.category_combo.grid(row=row_num, column=1, columnspan=2, sticky=tk.W)
        if self.categories: self.category_combo.current(0)
        self.category_combo.bind("<<ComboboxSelected>>", self.update_bonding_options)
        row_num += 1

        # Bonding Option
        ttk.Label(input_frame, text="Bonding Option:").grid(row=row_num, column=0, sticky=tk.W, pady=2)
        self.bonding_combo = ttk.Combobox(input_frame, state="readonly", width=23)
        self.bonding_combo.grid(row=row_num, column=1, columnspan=2, sticky=tk.W)
        row_num += 1

        # Calculate Button
        self.calc_button = ttk.Button(input_frame, text="Calculate", command=self.perform_calculation)
        self.calc_button.grid(row=row_num, column=1, columnspan=2, pady=10)
        row_num += 1

        # Result Area Frame
        result_frame = ttk.Frame(master, padding="10")
        result_frame.pack(expand=True, fill=tk.BOTH)

        # Result Label
        ttk.Label(result_frame, text="Result:").pack(anchor=tk.W)
        self.result_var = tk.StringVar()
        result_label = ttk.Label(result_frame, textvariable=self.result_var, wraplength=400, justify=tk.LEFT, relief=tk.SUNKEN, padding=5)
        result_label.pack(expand=True, fill=tk.BOTH, pady=5)

        # Initial Population
        self.update_date_label() # Set initial date label text
        self.update_bonding_options() # Populate bonding options for default category

    def update_date_label(self):
        """Updates the date label based on calculation direction."""
        if self.direction_var.get() == 'F':
            self.date_label.config(text="Buy Date (YYYY-MM-DD):")
        else:
            self.date_label.config(text="Arrival Date (YYYY-MM-DD):")

    def update_bonding_options(self, event=None):
        """Updates the bonding combobox based on selected category."""
        selected_category = self.category_combo.get()
        if not selected_category:
            self.bonding_combo['values'] = []
            self.bonding_combo.set("")
            return

        valid_keys = [k for k in GARMENT_PRODUCTION_TIMES if k[0] == selected_category]
        options = sorted(list(set(key[1] for key in valid_keys)))

        self.bonding_combo['values'] = options
        if options:
            self.bonding_combo.current(0)
        else:
            self.bonding_combo.set("") # Clear if no options

    def perform_calculation(self):
        """Gathers inputs, calls calculation function, displays result."""
        try:
            # Get inputs
            direction = self.direction_var.get()
            date_str = self.date_entry.get()
            fabric_country = self.fabric_country_combo.get()
            lading_point_index = self.lading_point_combo.current()
            # Check if index is valid
            if lading_point_index < 0 or lading_point_index >= len(self.lading_points_keys):
                messagebox.showerror("Input Error", "Please select a valid Garment Lading Point.")
                return
            garment_lading_point = self.lading_points_keys[lading_point_index]

            product_category = self.category_combo.get()
            bonding_option = self.bonding_combo.get()

            # Basic Validation
            if not all([direction, date_str, fabric_country, garment_lading_point, product_category, bonding_option]):
                messagebox.showerror("Input Error", "Please fill in all fields.")
                return

            if not parse_date(date_str):
                 messagebox.showerror("Input Error", "Invalid date format. Please use YYYY-MM-DD.")
                 return

            # Call calculation function
            result = ""
            if direction == 'F':
                result = calculate_arrival_date(date_str, fabric_country, garment_lading_point, product_category, bonding_option)
            else: # direction == 'B'
                result = calculate_buy_date(date_str, fabric_country, garment_lading_point, product_category, bonding_option)

            # Display result
            self.result_var.set(result)

        except Exception as e:
            self.result_var.set(f"An unexpected error occurred: {e}")
            messagebox.showerror("Error", f"An unexpected error occurred:\n{e}")

# --- Main Execution (GUI) ---
if __name__ == "__main__":
    # # --- Original CLI Execution (Commented Out) ---
    # user_inputs = get_user_input() # Function no longer exists
    # if user_inputs:
    #     direction, known_date_str, fabric_country, garment_lading_point, product_category, bonding_option = user_inputs
    #     if direction == 'F':
    #         calculate_arrival_date(known_date_str, fabric_country, garment_lading_point, product_category, bonding_option)
    #     elif direction == 'B':
    #         calculate_buy_date(known_date_str, fabric_country, garment_lading_point, product_category, bonding_option)
    # else:
    #     print("\nExiting due to input error or missing configuration.")

    # --- Run GUI ---
    root = tk.Tk()
    app = LeadTimeApp(root)
    root.mainloop() 