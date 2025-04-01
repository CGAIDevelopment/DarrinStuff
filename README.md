# Lead Time Calculator

This script calculates estimated lead times for garment production based on various stages and transit times, accounting for specific country holidays. It provides a graphical user interface (GUI) for easy interaction.

## Features

*   Calculates estimated **Store Arrival Date** given a **Buy Placement Date** (Forward calculation).
*   Calculates required **Buy Placement Date** given a desired **Store Arrival Date** (Backward calculation).
*   Accounts for lead times in:
    *   Fabric Greige Production
    *   Fabric Dyeing Production
    *   Fabric Transit to Factory
    *   Garment Production (based on product category and bonding)
    *   Finished Garment Transit to USA Warehouse (based on lading point)
    *   USA Warehouse to Store Transit
*   Incorporates specific holiday closure periods for various countries, extending production lead times when overlaps occur.
*   Provides a simple Tkinter-based GUI for input and output.

## Setup

1.  **Prerequisites:**
    *   Python 3.x installed.
    *   `pip` (Python package installer) available.

2.  **Install Dependencies:**
    Open your terminal or command prompt in the project directory (where `lead_time_calculator.py` and `requirements.txt` are located) and run:
    ```bash
    pip install -r requirements.txt
    ```
    This will install the necessary `python-dateutil` and `holidays` libraries.

## Running the Calculator

1.  Navigate to the project directory in your terminal.
2.  Run the script using Python:
    ```bash
    python lead_time_calculator.py
    ```
3.  The GUI window will open.
4.  **Select Direction:** Choose "Forward" or "Backward" calculation.
5.  **Enter Date:** Input the known date (Buy Date for Forward, Arrival Date for Backward) in YYYY-MM-DD format.
6.  **Select Options:** Use the dropdown menus to choose:
    *   Fabric Origin Country
    *   Garment Lading Point (determines Garment Factory Country and Transit Time to USA)
    *   Product Category
    *   Bonding Option (options update based on the selected category)
7.  **Calculate:** Click the "Calculate" button.
8.  **View Result:** The calculated date or any error messages will appear in the "Result" box at the bottom. Calculation steps (if enabled) will print to the console where you ran the script.

## Configuration & Data Modification

The core data (lead times, transit times, holidays) is stored directly within the `lead_time_calculator.py` script. You can modify these Python variables if needed:

*   **Default Lead Times:**
    *   `DEFAULT_FABRIC_GREIGE_LEAD_TIME_DAYS`
    *   `DEFAULT_FABRIC_DYEING_LEAD_TIME_DAYS`
    *   `DEFAULT_WAREHOUSE_TO_STORE_TRANSIT_DAYS`
*   **Garment Transit to USA:** Modify the `GARMENT_TRANSIT_TIMES_USA` dictionary. Add or update lading points, associated countries, ports, and transit days.
*   **Fabric Transit:** Modify the `FABRIC_TRANSIT_TIMES` dictionary. Keys are tuples of `(Fabric Origin Country, Garment Factory Country)`.
*   **Garment Production Times:** Modify the `GARMENT_PRODUCTION_TIMES` dictionary. Keys are tuples of `(Product Category, Bonding Option)`.
*   **Holiday Closures:** Modify the `HOLIDAY_CLOSURES` dictionary. Keys are country names (matching those used in `COUNTRY_HOLIDAY_MAP`). Values are lists of tuples, where each tuple is `("YYYY-MM-DD", "YYYY-MM-DD")` representing the inclusive start and end date of a closure period.
    *   **Important:** Ensure the years in the holiday dates are kept up-to-date for accurate calculations in the future.
*   **Country Mapping:** The `COUNTRY_HOLIDAY_MAP` connects the country names used in the transit time data to the keys used in the `HOLIDAY_CLOSURES` dictionary. Ensure consistency if you add or rename countries. 