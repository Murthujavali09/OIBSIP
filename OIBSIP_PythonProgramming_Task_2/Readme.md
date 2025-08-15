# BMI Calculator (Tkinter, Python, SQLite)

A desktop GUI application to calculate BMI, save daily results per user, review history in a table, and visualize trends with a chart. The app includes account management (create/login), persistent storage, and clean navigation across Dashboard, History, and Trends.

## Objective

- Provide a simple, accurate BMI calculator with immediate categorization.
- Persist daily BMI entries per user with the ability to update the current day’s record.
- Offer history browsing and trend visualization with key statistics.
- Ensure a smooth, guided UX with validation, feedback, and clear navigation.


## Tools and Technologies Used

- Python 3
- Tkinter for GUI (Frames, Labels, ttk Entry/Treeview, Buttons, messagebox)
- SQLite via sqlite3 for persistence
- Matplotlib for trend chart embedding in Tkinter
- Pandas (read SQL to DataFrame for History view)


## Features

- User accounts:
    - Create account with name, email, password (basic email validation, uniqueness check)
    - Login/logout; session tracked in memory
- BMI calculation:
    - Input height(m) and weight(kg)
    - Validations for empty/invalid ranges
    - BMI formula: weight/height², 2‑decimal rounding
    - Category: Underweight, Normal, Overweight
- History:
    - Per‑user daily log stored in SQLite
    - If a BMI for today exists, option to replace it
    - Tabular view with scrolling
- Trends:
    - Line chart of BMI over time with shaded ranges (Underweight/Normal/Overweight)
    - Key statistics: Average, Highest, Lowest BMI
    - Update notice showing percentage change vs. last entry
- UX:
    - Three-page navigation (Login/Create Account, Dashboard, History, Trends)
    - Clear feedback via dialogs and status texts
    - Responsive layout with consistent styling


## Project Structure

- main.py 
- database.py 
- login.py 
- create_account.py 
- dashboard.py 
- history.py 
- trends.py 
- database.db 


## How It Works

1. App initialization:
    - Creates the Tk root, container frame, and loads all pages.
    - Opens/initializes the SQLite database and tables if they do not exist.
2. Accounts:
    - CreateAccount inserts new user if email is valid and unique.
    - Login checks credentials and sets current_user_id for the session.
3. BMI flow (Dashboard):
    - User inputs height(m) and weight(kg); validations ensure sensible ranges.
    - BMI is computed and categorized; results are shown immediately.
    - Entry is saved to BMI history for today; if already present, the user can replace it.
    - History and Trends pages are refreshed after save/update.
4. History view:
    - Loads user’s rows from bmi_history into a DataFrame, then into a Treeview table with a scrollbar.
    - Presents a “Calculate BMI” call-to-action if there is no data.
5. Trends view:
    - Reads user’s history, computes key stats, and embeds a matplotlib chart.
    - The chart highlights typical BMI ranges and plots the series over time.

## Database Schema (SQLite)

- users:
    - id (PrimaryKey), username, email (unique), password
- bmi_history:
    - id (PrimaryKey), user_id (ForeignKey), date (ISO), height, weight, bmi, category

Tables are created automatically on first run.

## Steps Performed 

- Designed a multi-frame Tkinter application with centralized navigation.
- Implemented robust form validations and user feedback with messageboxes.
- Built database helper functions for user and BMI history operations.
- Created a dashboard workflow that calculates, categorizes, and persists BMI with replacement logic for the current day.
- Implemented a history table with scrolling and clear column formatting.
- Embedded a trends chart with shaded BMI ranges and computed key stats.
- Ensured clean shutdown by closing the SQLite connection on exit.


## Usage

- Requirements:
    - Python 3.x
    - Recommended installs:
        - pip install matplotlib pandas
- Run the app:
    - python main.py
- In the app:
    - Create an account or log in.
    - Go to Dashboard, enter height(m) and weight(kg), click “Calculate BMI.”
    - Check “History” for saved entries; view “Trends” for charts and statistics.
    - Use “Logout” in the navbar to end the session.


## Validation and Error Handling

- Email format check and uniqueness on account creation.
- Non-empty fields for all forms.
- Height and weight validated for realistic ranges.
- Clear error/info dialogs for invalid input, duplicates, and general exceptions.
- Safe DB closure on app exit.


## Outcome

- A complete, multi-user BMI tracker with accurate calculations, persistent storage, history browsing, and insightful trend visualization—implemented with a clean, maintainable Python/Tkinter codebase.


## Possible Enhancements

- Password hashing and secure credential storage.
- Input units toggle (cm/kg ↔ ft/in/lb) with conversion.
- Export history to CSV.
- Date picker to log past entries.
- Additional stats (moving averages, weekly/monthly summaries).
- Theming and accessibility improvements.


<div style="text-align: center">⁂</div>

[^1]: image.jpg

[^2]: create_account.py

[^3]: dashboard.py

[^4]: database.py

[^5]: history.py

[^6]: login.py

[^7]: main.py

[^8]: trends.py

