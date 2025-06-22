import tkinter as tk
from tkinter import messagebox
import math


class Calculator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Advanced Calculator")
        self.window.geometry("320x500")
        self.window.resizable(False, False)
        self.window.configure(bg='#2c3e50')

        # Variables
        self.current_expression = ""
        self.display_var = tk.StringVar()
        self.display_var.set("0")
        self.last_operation = ""
        self.should_reset_display = False

        self.setup_ui()
        self.bind_keyboard()

    def setup_ui(self):
        # Display frame
        display_frame = tk.Frame(self.window, bg='#2c3e50', pady=10)
        display_frame.pack(fill='x', padx=10)

        # Main display
        self.display = tk.Entry(
            display_frame,
            textvariable=self.display_var,
            font=('Arial', 24, 'bold'),
            justify='right',
            state='readonly',
            bg='#1a252f',
            fg='#ecf0f1',
            bd=2,
            relief='sunken',
            insertbackground='#ecf0f1'
        )
        self.display.pack(fill='x', ipady=10)

        # Expression label (shows current calculation)
        self.expr_label = tk.Label(
            display_frame,
            text="",
            font=('Arial', 10),
            fg='#bdc3c7',
            bg='#2c3e50',
            anchor='e'
        )
        self.expr_label.pack(fill='x', pady=(5, 0))

        # Button frame
        button_frame = tk.Frame(self.window, bg='#2c3e50')
        button_frame.pack(fill='both', expand=True, padx=10, pady=(0, 10))

        # Configure grid weights
        for i in range(6):
            button_frame.grid_rowconfigure(i, weight=1)
        for i in range(4):
            button_frame.grid_columnconfigure(i, weight=1)

        # Button layout
        buttons = [
            # Row 0: Memory and special functions
            ('C', 0, 0, '#e74c3c', 'white', self.clear_all),
            ('⌫', 0, 1, '#f39c12', 'white', self.backspace),
            ('√', 0, 2, '#9b59b6', 'white', lambda: self.special_operation('sqrt')),
            ('±', 0, 3, '#9b59b6', 'white', self.toggle_sign),

            # Row 1: Operations
            ('(', 1, 0, '#34495e', 'white', lambda: self.add_to_expression('(')),
            (')', 1, 1, '#34495e', 'white', lambda: self.add_to_expression(')')),
            ('%', 1, 2, '#9b59b6', 'white', lambda: self.add_operator('%')),
            ('÷', 1, 3, '#e67e22', 'white', lambda: self.add_operator('/')),

            # Row 2: Numbers and operations
            ('7', 2, 0, '#34495e', 'white', lambda: self.add_number('7')),
            ('8', 2, 1, '#34495e', 'white', lambda: self.add_number('8')),
            ('9', 2, 2, '#34495e', 'white', lambda: self.add_number('9')),
            ('×', 2, 3, '#e67e22', 'white', lambda: self.add_operator('*')),

            # Row 3
            ('4', 3, 0, '#34495e', 'white', lambda: self.add_number('4')),
            ('5', 3, 1, '#34495e', 'white', lambda: self.add_number('5')),
            ('6', 3, 2, '#34495e', 'white', lambda: self.add_number('6')),
            ('−', 3, 3, '#e67e22', 'white', lambda: self.add_operator('-')),

            # Row 4
            ('1', 4, 0, '#34495e', 'white', lambda: self.add_number('1')),
            ('2', 4, 1, '#34495e', 'white', lambda: self.add_number('2')),
            ('3', 4, 2, '#34495e', 'white', lambda: self.add_number('3')),
            ('+', 4, 3, '#e67e22', 'white', lambda: self.add_operator('+')),

            # Row 5
            ('0', 5, 0, '#34495e', 'white', lambda: self.add_number('0')),
            ('.', 5, 1, '#34495e', 'white', lambda: self.add_number('.')),
            ('CE', 5, 2, '#e74c3c', 'white', self.clear_entry),
            ('=', 5, 3, '#27ae60', 'white', self.calculate),
        ]

        # Create buttons
        for text, row, col, bg_color, fg_color, command in buttons:
            btn = tk.Button(
                button_frame,
                text=text,
                font=('Arial', 16, 'bold'),
                bg=bg_color,
                fg=fg_color,
                bd=0,
                relief='flat',
                command=command,
                activebackground=self.lighten_color(bg_color),
                activeforeground=fg_color
            )
            btn.grid(row=row, column=col, sticky='nsew', padx=2, pady=2)

    def lighten_color(self, color):
        """Lighten a color for button hover effect"""
        color_map = {
            '#e74c3c': '#ec7063',
            '#f39c12': '#f7c12b',
            '#9b59b6': '#bb8ed1',
            '#34495e': '#5d6d7e',
            '#e67e22': '#f1912e',
            '#27ae60': '#52c27d'
        }
        return color_map.get(color, color)

    def bind_keyboard(self):
        """Bind keyboard shortcuts"""
        self.window.bind('<Key>', self.on_key_press)
        self.window.focus_set()

    def on_key_press(self, event):
        """Handle keyboard input"""
        key = event.char
        if key.isdigit():
            self.add_number(key)
        elif key == '.':
            self.add_number('.')
        elif key in '+-*/':
            self.add_operator(key)
        elif key in '\r=':  # Enter or =
            self.calculate()
        elif event.keysym == 'BackSpace':
            self.backspace()
        elif event.keysym == 'Delete' or key.lower() == 'c':
            self.clear_all()
        elif event.keysym == 'Escape':
            self.clear_entry()

    def add_number(self, number):
        # If we should reset display (after operator), clear display but keep expression
        if self.should_reset_display:
            self.display_var.set("")
            self.should_reset_display = False

        if self.display_var.get() == "0" or self.display_var.get() == "Error" or self.display_var.get() == "":
            self.display_var.set(number)
        else:
            current = self.display_var.get()
            self.display_var.set(current + number)

        self.update_expression_display()

    def add_operator(self, operator):
        current_display = self.display_var.get()
        if current_display and current_display != "Error":
            # Build the expression properly
            if not self.current_expression:
                # First time - just add the number and operator
                self.current_expression = current_display + operator
            elif self.current_expression[-1] in '+-*/%':
                # Replace the last operator if user clicked operator twice
                self.current_expression = self.current_expression[:-1] + operator
            else:
                # Add current display + operator to expression
                self.current_expression += current_display + operator

            self.should_reset_display = True
            self.update_expression_display()

    def add_to_expression(self, char):
        """Add parentheses to expression"""
        if self.display_var.get() == "0" or self.display_var.get() == "Error":
            self.current_expression = char
            self.display_var.set(char)
        else:
            self.current_expression += char
            current = self.display_var.get()
            self.display_var.set(current + char)
        self.update_expression_display()

    def backspace(self):
        """Delete last character"""
        current = self.display_var.get()
        if len(current) > 1:
            new_value = current[:-1]
            self.display_var.set(new_value)
            if self.current_expression:
                self.current_expression = self.current_expression[:-1]
        else:
            self.display_var.set("0")
            self.current_expression = ""
        self.update_expression_display()

    def clear_all(self):
        """Clear everything"""
        self.display_var.set("0")
        self.current_expression = ""
        self.should_reset_display = False
        self.expr_label.config(text="")

    def clear_entry(self):
        """Clear only current entry"""
        self.display_var.set("0")

    def toggle_sign(self):
        """Toggle positive/negative"""
        current = self.display_var.get()
        if current != "0" and current != "Error":
            if current.startswith('-'):
                self.display_var.set(current[1:])
            else:
                self.display_var.set('-' + current)

    def special_operation(self, operation):
        """Handle special operations like square root"""
        try:
            current = float(self.display_var.get())
            if operation == 'sqrt':
                if current < 0:
                    raise ValueError("Cannot calculate square root of negative number")
                result = math.sqrt(current)
                self.display_var.set(str(result))
                self.current_expression = str(result)
        except (ValueError, ZeroDivisionError) as e:
            self.display_var.set("Error")
            messagebox.showerror("Error", str(e))

    def calculate(self):
        """Perform calculation"""
        try:
            # Add current display to expression if needed
            current_display = self.display_var.get()
            if current_display and current_display != "Error":
                if not self.current_expression:
                    return
                elif self.current_expression[-1] in '+-*/%':
                    self.current_expression += current_display

            if not self.current_expression:
                return

            # Replace display symbols with Python operators
            expression = self.current_expression.replace('×', '*').replace('÷', '/')

            # Evaluate the expression safely
            result = eval(expression)

            # Handle division by zero and other math errors
            if math.isinf(result) or math.isnan(result):
                raise ValueError("Mathematical error")

            # Format result
            if isinstance(result, float) and result.is_integer():
                result = int(result)

            self.display_var.set(str(result))
            self.last_operation = f"{self.current_expression} = {result}"
            self.current_expression = str(result)
            self.should_reset_display = True

        except (ValueError, ZeroDivisionError, SyntaxError) as e:
            self.display_var.set("Error")
            messagebox.showerror("Error", "Invalid expression or mathematical error")
            self.current_expression = ""
            self.should_reset_display = True
        except Exception as e:
            self.display_var.set("Error")
            messagebox.showerror("Error", "An unexpected error occurred")
            self.current_expression = ""
            self.should_reset_display = True

        self.update_expression_display()

    def update_expression_display(self):
        """Update the expression display"""
        # Show what's being built
        current_display = self.display_var.get()
        if self.current_expression:
            if self.current_expression[-1] in '+-*/%':
                # Show expression + current number being typed
                if current_display and current_display != "0" and not self.should_reset_display:
                    display_expr = self.current_expression + current_display
                else:
                    display_expr = self.current_expression
            else:
                display_expr = self.current_expression
        else:
            # Just starting, show current number
            display_expr = current_display if current_display != "0" else ""

        # Replace operators with display symbols
        display_expr = display_expr.replace('*', '×').replace('/', '÷')
        self.expr_label.config(text=display_expr)

    def run(self):
        self.window.mainloop()


# Create and run the calculator
if __name__ == "__main__":
    calc = Calculator()
    calc.run()