import datetime
import streamlit as st
import holidays as pyholidays # Using pyholidays as a potential fallback/reference

# --- Configuration & Data --- (Copied from lead_time_calculator.py)

# --- Default Lead Times ---
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
    "HKGHK": {"country": "Hong Kong", "port": "Hong Kong", "days": 42},
    "MAAIN": {"country": "India", "port": "Chennai", "days": 76},
    "ENRIN": {"country": "India", "port": "Chennai", "days": 76},
    "MUNIN": {"country": "India", "port": "Mundra/Nhava Sheva", "days": 62},
    "BOMIN": {"country": "India", "port": "Mundra/Nhava Sheva", "days": 62},
    "JKTID": {"country": "Indonesia", "port": "Jakarta", "days": 61},
    "SRGID": {"country": "Indonesia", "port": "Semarang", "days": 65},
    "SUBID": {"country": "Indonesia", "port": "Surabaya", "days": 61},
    "AMMJO": {"country": "Jordan", "port": "Haifa", "days": 42},
    "PUSKR": {"country": "Korea", "port": "Busan", "days": 42},
    "BQMPK": {"country": "Pakistan", "port": "Qasim", "days": 64},
    "CMBLK": {"country": "Sri Lanka", "port": "Colombo", "days": 55},
    "LCHTH": {"country": "Thailand", "port": "Laem Chabanag", "days": 48},
    "HPHVN": {"country": "Vietnam", "port": "Haiphong", "days": 51},
    "SGNVN": {"country": "Vietnam", "port": "Saigon", "days": 48},
    "VUTVN": {"country": "Vietnam", "port": "Vung Tao", "days": 48},
}

# --- Transit Time: Fabric to Factory ---
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
    ("USA", "Guatemala"): 14,
    ("Vietnam", "Bangladesh"): 28, ("Vietnam", "Cambodia"): 21, ("Vietnam", "Guatemala"): 35,
    ("Vietnam", "India"): 28, ("Vietnam", "Indonesia"): 21, ("Vietnam", "Jordan"): 35,
    ("Vietnam", "Sri Lanka"): 28, ("Vietnam", "Thailand"): 21, ("Vietnam", "Vietnam"): 5,
}

# --- Garment Production Time ---
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
}

# --- Specific Holiday Closing Periods ---
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
    "USA": [],
}

# --- Country Mapping ---
COUNTRY_HOLIDAY_MAP = {
    "Bangladesh": "Bangladesh", "Cambodia": "Cambodia", "China": "China",
    "Guatemala": "Guatemala", "Hong Kong": "Hong Kong", "India": "India",
    "Indonesia": "Indonesia", "Jordan": "Jordan", "Korea": "Korea",
    "Pakistan": "Pakistan", "Sri Lanka": "Sri Lanka", "Taiwan": "Taiwan",
    "Thailand": "Thailand", "Vietnam": "Vietnam", "USA": "USA"
}

# --- Helper Functions --- (Modified for webapp - no print statements)

def parse_date(date_str):
    try:
        # Check if it's already a date object (from st.date_input)
        if isinstance(date_str, datetime.date):
            return date_str
        return datetime.datetime.strptime(str(date_str), "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return None

def add_lead_time(start_date, lead_days, country_code=None, is_transit=False):
    if is_transit:
        return start_date + datetime.timedelta(days=lead_days)
    else:
        current_date = start_date
        days_added = 0
        total_holiday_offset = 0
        country_key = COUNTRY_HOLIDAY_MAP.get(country_code)
        while days_added < lead_days:
            current_date += datetime.timedelta(days=1)
            is_holiday = False
            if country_key and country_key in HOLIDAY_CLOSURES:
                for start_str, end_str in HOLIDAY_CLOSURES[country_key]:
                    h_start, h_end = parse_date(start_str), parse_date(end_str)
                    if h_start and h_end and h_start <= current_date <= h_end:
                        is_holiday = True
                        break
            if is_holiday:
                total_holiday_offset += 1
                continue
            days_added += 1
        return start_date + datetime.timedelta(days=lead_days + total_holiday_offset)

def subtract_lead_time(end_date, lead_days, country_code=None, is_transit=False):
    if is_transit:
        return end_date - datetime.timedelta(days=lead_days)
    else:
        current_date = end_date
        days_subtracted = 0
        total_holiday_offset = 0
        holidays_in_range = set()
        country_key = COUNTRY_HOLIDAY_MAP.get(country_code)
        if country_key and country_key in HOLIDAY_CLOSURES:
            check_start = end_date - datetime.timedelta(days=lead_days * 2 + 45)
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
            if is_holiday:
                total_holiday_offset += 1
                continue
            days_subtracted += 1
        return end_date - datetime.timedelta(days=lead_days + total_holiday_offset)

# --- Calculation Logic --- (Modified for webapp)

def calculate_arrival_date(buy_date, fabric_country, garment_lading_point, product_category, bonding_option):
    start_date = parse_date(buy_date)
    if not start_date:
        return "Error: Invalid buy date format. Please use YYYY-MM-DD."

    # 1. Fabric Greige Production
    greige_days = DEFAULT_FABRIC_GREIGE_LEAD_TIME_DAYS
    fabric_prod_country = fabric_country
    current_date = add_lead_time(start_date, greige_days, fabric_prod_country)

    # 2. Fabric Dyeing Production
    dyeing_days = DEFAULT_FABRIC_DYEING_LEAD_TIME_DAYS
    current_date = add_lead_time(current_date, dyeing_days, fabric_prod_country)

    # 3. Fabric Transit to Factory
    garment_country_info = GARMENT_TRANSIT_TIMES_USA.get(garment_lading_point)
    if not garment_country_info: return f"Error: Lading point '{garment_lading_point}' not found."
    garment_country = garment_country_info.get("country")
    if not garment_country: return f"Error: Lading point '{garment_lading_point}' missing country info."
    fabric_transit_key = (fabric_country, garment_country)
    fabric_transit_days = FABRIC_TRANSIT_TIMES.get(fabric_transit_key)
    if fabric_transit_days is None: return f"Error: Fabric transit from '{fabric_country}' to '{garment_country}' not found."
    current_date = add_lead_time(current_date, fabric_transit_days, is_transit=True)

    # 4. Garment Production
    garment_prod_key = (product_category, bonding_option)
    garment_prod_days = GARMENT_PRODUCTION_TIMES.get(garment_prod_key)
    if garment_prod_days is None:
        garment_prod_key_nobond = (product_category, "No Bonding")
        garment_prod_days = GARMENT_PRODUCTION_TIMES.get(garment_prod_key_nobond)
        if garment_prod_days is None: return f"Error: Production time for '{product_category}' not found."
        # Use No Bonding time if specific bonding option time is missing
    current_date = add_lead_time(current_date, garment_prod_days, garment_country)

    # 5. Finished Garment Transit to USA Warehouse
    garment_transit_days_usa = garment_country_info["days"]
    current_date = add_lead_time(current_date, garment_transit_days_usa, is_transit=True)

    # 6. Warehouse to Store Transit
    warehouse_store_days = DEFAULT_WAREHOUSE_TO_STORE_TRANSIT_DAYS
    current_date = add_lead_time(current_date, warehouse_store_days, "USA")

    final_date_str = current_date.strftime('%Y-%m-%d')
    return f"Estimated Store Arrival Date: {final_date_str}"

def calculate_buy_date(arrival_date, fabric_country, garment_lading_point, product_category, bonding_option):
    end_date = parse_date(arrival_date)
    if not end_date:
        return "Error: Invalid arrival date format. Please use YYYY-MM-DD."

    # 6. Warehouse to Store Transit (Subtract)
    warehouse_store_days = DEFAULT_WAREHOUSE_TO_STORE_TRANSIT_DAYS
    current_date = subtract_lead_time(end_date, warehouse_store_days, "USA")

    # 5. Finished Garment Transit to USA Warehouse (Subtract)
    garment_country_info = GARMENT_TRANSIT_TIMES_USA.get(garment_lading_point)
    if not garment_country_info: return f"Error: Lading point '{garment_lading_point}' not found."
    garment_transit_days_usa = garment_country_info["days"]
    current_date = subtract_lead_time(current_date, garment_transit_days_usa, is_transit=True)

    # 4. Garment Production (Subtract)
    garment_prod_key = (product_category, bonding_option)
    garment_prod_days = GARMENT_PRODUCTION_TIMES.get(garment_prod_key)
    if garment_prod_days is None:
         garment_prod_key_nobond = (product_category, "No Bonding")
         garment_prod_days = GARMENT_PRODUCTION_TIMES.get(garment_prod_key_nobond)
         if garment_prod_days is None: return f"Error: Production time for '{product_category}' not found."
         # Use No Bonding time if specific bonding option time is missing
    garment_country = garment_country_info.get("country")
    if not garment_country: return f"Error: Lading point '{garment_lading_point}' missing country info."
    current_date = subtract_lead_time(current_date, garment_prod_days, garment_country)

    # 3. Fabric Transit to Factory (Subtract)
    fabric_transit_key = (fabric_country, garment_country)
    fabric_transit_days = FABRIC_TRANSIT_TIMES.get(fabric_transit_key)
    if fabric_transit_days is None: return f"Error: Fabric transit from '{fabric_country}' to '{garment_country}' not found."
    current_date = subtract_lead_time(current_date, fabric_transit_days, is_transit=True)

    # 2. Fabric Dyeing Production (Subtract)
    dyeing_days = DEFAULT_FABRIC_DYEING_LEAD_TIME_DAYS
    fabric_prod_country = fabric_country
    current_date = subtract_lead_time(current_date, dyeing_days, fabric_prod_country)

    # 1. Fabric Greige Production (Subtract)
    greige_days = DEFAULT_FABRIC_GREIGE_LEAD_TIME_DAYS
    current_date = subtract_lead_time(current_date, greige_days, fabric_prod_country)

    final_date_str = current_date.strftime('%Y-%m-%d')
    return f"Required Buy Placement Date: {final_date_str}"

# --- Streamlit UI ---

st.set_page_config(layout="wide")
st.title("Supply Chain Lead Time Calculator")

# --- Inputs ---
col1, col2 = st.columns(2)

with col1:
    direction = st.radio(
        "Calculation Direction",
        ("Forward (Buy -> Arrival)", "Backward (Arrival -> Buy)"),
        key="direction"
    )

    date_label = "Buy Date" if direction.startswith("Forward") else "Desired Store Arrival Date"
    known_date = st.date_input(date_label, datetime.date.today(), key="known_date")

    fabric_countries_list = sorted(list(set(k[0] for k in FABRIC_TRANSIT_TIMES.keys())))
    fabric_country = st.selectbox("Fabric Origin Country", fabric_countries_list, key="fabric_country")

with col2:
    lading_points_keys = sorted(GARMENT_TRANSIT_TIMES_USA.keys())
    lading_points_display = {f"{p} ({GARMENT_TRANSIT_TIMES_USA[p].get('port','?')}, {GARMENT_TRANSIT_TIMES_USA[p].get('country','?')})": p for p in lading_points_keys}
    display_selection = st.selectbox("Garment Lading Point", list(lading_points_display.keys()), key="lading_point_display")
    garment_lading_point = lading_points_display.get(display_selection)

    categories_list = sorted(list(set(k[0] for k in GARMENT_PRODUCTION_TIMES.keys())))
    product_category = st.selectbox("Product Category", categories_list, key="product_category")

    # Dynamically update bonding options
    valid_bonding_keys = [k for k in GARMENT_PRODUCTION_TIMES if k[0] == product_category]
    bonding_options_list = sorted(list(set(key[1] for key in valid_bonding_keys)))
    if not bonding_options_list: # Handle cases where category might not have bonding options defined
        bonding_options_list = ["N/A"] # Provide a default or handle error
        if (product_category, "No Bonding") in GARMENT_PRODUCTION_TIMES:
            bonding_options_list = ["No Bonding"] # Use No Bonding if available

    bonding_option = st.selectbox("Bonding Option", bonding_options_list, key="bonding_option")

# --- Calculation Trigger & Output ---
st.divider()

if st.button("Calculate Lead Time", type="primary"):
    result = ""
    # Validate inputs
    if not all([direction, known_date, fabric_country, garment_lading_point, product_category, bonding_option]) or bonding_option == "N/A":
        st.error("Error: Please ensure all fields are selected and valid.")
    else:
        try:
            if direction.startswith("Forward"):
                result = calculate_arrival_date(known_date, fabric_country, garment_lading_point, product_category, bonding_option)
            else: # Backward
                result = calculate_buy_date(known_date, fabric_country, garment_lading_point, product_category, bonding_option)

            # Display result
            if result.startswith("Error:"):
                st.error(result)
            else:
                st.success(result)
        except Exception as e:
            st.error(f"An unexpected calculation error occurred: {e}")
else:
    st.info("Please select all options and click 'Calculate Lead Time'.")

# --- Optional: Display Data Tables (for reference) ---
with st.expander("View Configuration Data"):
    st.subheader("Default Lead Times (Days)")
    st.json({
        "Fabric Greige": DEFAULT_FABRIC_GREIGE_LEAD_TIME_DAYS,
        "Fabric Dyeing": DEFAULT_FABRIC_DYEING_LEAD_TIME_DAYS,
        "Warehouse to Store Transit": DEFAULT_WAREHOUSE_TO_STORE_TRANSIT_DAYS
    })

    st.subheader("Garment Transit to USA (Days)")
    st.dataframe(GARMENT_TRANSIT_TIMES_USA)

    st.subheader("Fabric Transit Times (Days)")
    # Convert tuple keys to strings for display
    fab_transit_display = {f"{k[0]} -> {k[1]}": v for k, v in FABRIC_TRANSIT_TIMES.items()}
    st.json(fab_transit_display)

    st.subheader("Garment Production Times (Days)")
    garment_prod_display = {f"{k[0]} ({k[1]})": v for k, v in GARMENT_PRODUCTION_TIMES.items()}
    st.json(garment_prod_display)

    st.subheader("Holiday Closures (YYYY-MM-DD)")
    st.json(HOLIDAY_CLOSURES) 