import tkinter as tk
from tkinter import messagebox


class SimpleCalculator:
    def __init__(self):
        # Create the main window
        self.window = tk.Tk()
        self.window.title("Simple Calculator")
        self.window.geometry("300x400")
        self.window.resizable(False, False)

        # Create the display
        self.create_display()

        # Create the buttons
        self.create_buttons()

        # Initialize Ui Elements
        self.display_var = None
        self.display = None

    def create_display(self):
        """Create the calculator display field"""
        self.display_var = tk.StringVar()
        self.display_var.set("0")

        self.display = tk.Entry(
            self.window,
            textvariable=self.display_var,
            font=("Arial", 16),
            width=20,
            justify="right",
            state="readonly",
            bd=5
        )
        self.display.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="ew")

    def create_buttons(self):
        """Create all calculator buttons with proper layout"""
        # Button configuration
        button_config = {
            "font": ("Arial", 14),
            "width": 5,
            "height": 2,
            "bd": 3
        }

        # Define button layout (4x4 grid)
        button_layout = [
            ["C", "CE", "±", "÷"],
            ["7", "8", "9", "×"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["0", "", ".", "="]
        ]

        # Create buttons
        for row_idx, row in enumerate(button_layout):
            for col_idx, button_text in enumerate(row):
                if button_text == "":  # Skip empty cells
                    continue

                # Special handling for '0' button (spans 2 columns)
                if button_text == "0":
                    btn = tk.Button(
                        self.window,
                        text=button_text,
                        command=lambda t=button_text: self.on_button_click(t),
                        **button_config
                    )
                    btn.grid(row=row_idx + 1, column=col_idx, columnspan=2,
                             padx=2, pady=2, sticky="ew")
                else:
                    btn = tk.Button(
                        self.window,
                        text=button_text,
                        command=lambda t=button_text: self.on_button_click(t),
                        **button_config
                    )
                    btn.grid(row=row_idx + 1, column=col_idx, padx=2, pady=2, sticky="ew")

        # Configure grid weights for responsive layout
        for i in range(4):
            self.window.grid_columnconfigure(i, weight=1)

    def on_button_click(self, button_text):
        """Handle button clicks"""
        current_display = self.display_var.get()

        if button_text in "0123456789":
            self.handle_number(button_text, current_display)
        elif button_text == ".":
            self.handle_decimal(current_display)
        elif button_text in "+-×÷":
            self.handle_operator(button_text, current_display)
        elif button_text == "=":
            self.calculate_result()
        elif button_text == "C":
            self.clear_all()
        elif button_text == "CE":
            self.clear_entry()
        elif button_text == "±":
            self.toggle_sign()

    def handle_number(self, number, current_display):
        """Handle number button clicks"""
        if current_display == "0":
            self.display_var.set(number)
        else:
            self.display_var.set(current_display + number)

    def handle_decimal(self, current_display):
        """Handle decimal point button click"""
        # Check if decimal already exists in current number
        if "." not in current_display.split()[-1]:
            if current_display == "0":
                self.display_var.set("0.")
            else:
                self.display_var.set(current_display + ".")

    def handle_operator(self, operator, current_display):
        """Handle operator button clicks"""
        # Convert display symbols to calculation symbols
        operator_map = {"×": "*", "÷": "/"}
        calc_operator = operator_map.get(operator, operator)

        # Add operator to display
        if current_display and current_display[-1] not in "+-*/":
            self.display_var.set(current_display + " " + calc_operator + " ")

    def calculate_result(self):
        """Calculate and display the result"""
        try:
            expression = self.display_var.get()
            if expression and expression != "0":
                # Replace display symbols with calculation symbols
                expression = expression.replace("×", "*").replace("÷", "/")
                result = eval(expression)

                # Handle division by zero and large numbers
                if result == float('inf') or result == float('-inf'):
                    raise ZeroDivisionError("Cannot divide by zero")

                # Format result (remove unnecessary decimal places)
                if result == int(result):
                    self.display_var.set(str(int(result)))
                else:
                    self.display_var.set(str(round(result, 8)))

        except ZeroDivisionError:
            messagebox.showerror("Error", "Cannot divide by zero!")
            self.clear_all()
        except Exception:
            messagebox.showerror("Error", "Invalid expression!")
            self.clear_all()

    def clear_all(self):
        """Clear the entire display"""
        self.display_var.set("0")

    def clear_entry(self):
        """Clear the last entry"""
        current = self.display_var.get()
        if len(current) > 1:
            self.display_var.set(current[:-1])
        else:
            self.display_var.set("0")

    def toggle_sign(self):
        """Toggle the sign of the current number"""
        current = self.display_var.get()
        try:
            if current != "0":
                if current.startswith("-"):
                    self.display_var.set(current[1:])
                else:
                    self.display_var.set("-" + current)
        except:
            pass

    def run(self):
        """Start the calculator application"""
        self.window.mainloop()


# Create and run the calculator
if __name__ == "__main__":
    calculator = SimpleCalculator()
    calculator.run()