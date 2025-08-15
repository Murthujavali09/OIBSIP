# Secure Password Generator 

A desktop GUI tool to generate strong, customizable passwords using cryptographically secure randomness, with options to include/exclude character types and specific characters, plus instant strength feedback.

## Objective

- Build a secure, user-friendly password generator with a simple GUI.
- Allow customization of length, inclusion of numbers/uppercase/symbols, and exclusion of specific characters.
- Ensure high-quality randomness and provide a clear strength indicator.


## Tools and Technologies Used

- Python 3
- Tkinter for GUI (Labels, Entry, Checkbutton, Button, Toplevel, messagebox)
- secrets (cryptographically secure random generation)
- SystemRandom for secure shuffling


## Features

- Character options:
    - Lowercase letters (always included as a base set)
    - Optional Numbers, Uppercase, Symbols
- Exclude specific characters (user input field)
- Length validation (min 6, max 100)
- Guarantees at least one character from each selected category
- Uses secrets for selection and SystemRandom for shuffling
- Copy-to-clipboard button in the result window
- Strength indicator: Weak / Moderate / Strong based on length and included categories


## How It Works

1. Base and optional pools:
    - BASE_POOL = lowercase a–z (minus excluded characters)
    - Optional sets (minus excluded characters):
        - NUMBERS = 0–9
        - UPPERCASE = A–Z
        - SYMBOLS = ! \# \$ % \& * @ ^
2. Input validation:
    - Length must be an integer; errors show via messagebox.
    - Length must be 6–100.
    - If a category is selected (“Yes”) but exclusion removes all characters from that category, an error is shown.
3. Password generation:
    - Builds a combined pool starting from allowed lowercase, then adds selected categories.
    - Ensures at least one character from each selected category using secrets.choice.
    - Fills remaining length from the combined pool using secrets.choice.
    - Shuffles with secrets.SystemRandom().shuffle.
4. Strength calculation:
    - +2 if length≥16; +1 if length≥12 (else +0).
    - +1 for each selected category (lowercase is always considered “yes”; numbers/uppercase/symbols depend on checkboxes).
    - Score mapped to: Weak (≤1), Moderate (2–3), Strong (≥4).
5. Result window:
    - Displays the generated password (wrapped for readability).
    - Shows color-coded strength (green/orange/red).
    - Provides “Copy to clipboard” button and confirmation label on click.

## Steps Performed 

- Designed Tkinter layout: headings, checkboxes, entries, and buttons arranged with grid.
- Implemented validate_user_input():
    - Reads inputs, enforces constraints, computes allowed characters, and handles category consistency.
    - Creates a Toplevel window for results and clipboard copy action.
- Implemented generatePassword():
    - Assembles pool, enforces required-category inclusion, fills remaining characters securely, shuffles, and returns strength.
- Implemented password_strength():
    - Heuristic based on length and selected categories.

## Usage

- Requirements: Python 3 (with Tkinter available, which is bundled in most standard installations).
- Run:
    - Save the script (e.g., app.py).
    - Execute: python app.py
- In the GUI:
    - Select optional categories (Numbers, Uppercase, Symbols).
    - Optionally enter characters to exclude (e.g., O0l1).
    - Enter desired length (6–100).
    - Click “Generate Password.”
    - In the result window, click “Copy to clipboard” to copy the password.


## Outcome

- A working Python/Tkinter application that produces strong passwords with cryptographically secure randomness and predictable policy controls.
- Practical UX: category toggles, exclusions, length limits, copy button, and immediate strength feedback.


## Notes and Recommendations

- Security:
    - secrets and SystemRandom are used for selection and shuffling (avoid non-cryptographic random for security-sensitive generation).
    - Do not log or transmit generated passwords.
- Usability:
    - Consider pre-filling a sensible default length (e.g., 12 or 16).
    - Consider disabling “Generate” until a valid length is entered.


## Possible Enhancements

- Add an option to ensure no character repetition or to avoid look-alikes automatically.
- Add a visual strength meter and entropy estimate.
- Add save option to save passwords.
- Persist last used settings.


## Project Structure 

- python_generator.py 



