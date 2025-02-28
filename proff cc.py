import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import requests

# GUI Setup
root = tk.Tk()
root.title("Currency Converter")
root.geometry("500x600")
root.configure(background='#ffffff')  # White background

# Center the window on the screen
window_width = 500
window_height = 600
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Create frames
header_frame = tk.Frame(root, bg='#2c3e50', pady=10, relief="ridge")
header_frame.grid(row=0, column=0, columnspan=3, sticky="nsew")

input_frame = tk.Frame(root, bg='#ffffff', padx=20, pady=20)
input_frame.grid(row=1, column=0, columnspan=3, sticky="nsew")

graph_frame = tk.Frame(root, bg='#ffffff', pady=10)
graph_frame.grid(row=2, column=0, columnspan=3, sticky="nsew")

footer_frame = tk.Frame(root, bg='#2c3e50', pady=5)
footer_frame.grid(row=3, column=0, columnspan=3, sticky="nsew")

# Header Label
header_label = tk.Label(header_frame, font=('Segoe UI', 24, 'bold'), text='Currency Converter',
                        bg='#2c3e50', fg='white')
header_label.pack(pady=5)

# Currency variables
variable1 = tk.StringVar(root)
variable2 = tk.StringVar(root)
variable1.set("USD")
variable2.set("INR")

# List of currencies for the dropdown menu
currency_list = ["USD", "INR", "EUR", "GBP", "CAD", "PKR", "AUD", "JPY", "CNY", "HKD", "IDR", "AED", "JOD", "KRW"]

# Function to fetch and display conversion result
def RealTimeCurrencyConversion():
    from_currency = variable1.get()
    to_currency = variable2.get()
    amount = Amount1_field.get()

    # Check if the amount is entered
    if not amount:
        messagebox.showinfo("Error !!", "Amount Not Entered.\n Please enter a valid amount.")
        return

    if from_currency not in currency_list or to_currency not in currency_list:
        messagebox.showinfo("Error !!", "Currency Not Selected.\n Please select FROM and TO Currency from the menu.")
        return

    try:
        amount = float(amount)
        # Fetch conversion rate from API
        url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
        response = requests.get(url)
        data = response.json()
        conversion_rate = data['rates'][to_currency]
        new_amount = round(amount * conversion_rate, 4)

        Amount2_field.delete(0, tk.END)
        Amount2_field.insert(0, str(new_amount))

        # Calculate the difference
        difference = round(new_amount - amount, 4)
        difference_label.config(text=f"{difference} {to_currency}")

        # Show graphical representation
        plot_graph(from_currency, to_currency, new_amount)
    except ValueError:
        messagebox.showinfo("Error !!", "Invalid amount entered. Please enter a numeric value.")
    except requests.exceptions.RequestException as e:
        messagebox.showinfo("Conversion Error", f"Failed to fetch conversion rates: {e}")
    except KeyError:
        messagebox.showinfo("Conversion Error", "Currency conversion data not available.")

# Function to plot the graphical representation
def plot_graph(from_currency, to_currency, new_amt):
    # Clear previous graph
    for widget in graph_frame.winfo_children():
        widget.destroy()

    # Create the plot
    fig, ax = plt.subplots(figsize=(4, 2))
    currencies = [from_currency, to_currency]
    amounts = [float(Amount1_field.get()), new_amt]
    
    ax.bar(currencies, amounts, color=['#3498db', '#2ecc71'])
    ax.set_title(f"Conversion: {from_currency} to {to_currency}", fontsize=14, fontweight='bold')
    ax.set_ylabel("Amount", fontsize=12)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Embed the plot in the Tkinter window
    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas.get_tk_widget().grid(row=0, column=0, padx=10, pady=10)
    canvas.draw()

# Function to clear all fields
def clear_all():
    Amount1_field.delete(0, tk.END)
    Amount2_field.delete(0, tk.END)
    difference_label.config(text="")  # Clear the difference label
    for widget in graph_frame.winfo_children():
        widget.destroy()

# Labels and Dropdowns for currency conversion
tk.Label(input_frame, font=('Segoe UI', 14), text="Amount : ", bg="#ffffff", fg="#2c3e50").grid(row=0, column=0, sticky="e", padx=10, pady=10)
tk.Label(input_frame, font=('Segoe UI', 14), text="From Currency : ", bg="#ffffff", fg="#2c3e50").grid(row=1, column=0, sticky="e", padx=10, pady=10)
tk.Label(input_frame, font=('Segoe UI', 14), text="To Currency : ", bg="#ffffff", fg="#2c3e50").grid(row=2, column=0, sticky="e", padx=10, pady=10)
tk.Label(input_frame, font=('Segoe UI', 14), text="Converted Amount : ", bg="#ffffff", fg="#2c3e50").grid(row=3, column=0, sticky="e", padx=10, pady=10)

# Label for Difference
tk.Label(input_frame, font=('Segoe UI', 14), text="Difference : ", bg="#ffffff", fg="#2c3e50").grid(row=4, column=0, sticky="e", padx=10, pady=10)
difference_label = tk.Label(input_frame, font=('Segoe UI', 14), text="", bg="#ffffff", fg="#2c3e50")
difference_label.grid(row=4, column=1, sticky="w", padx=10, pady=10)

# Currency Dropdowns
FromCurrency_option = tk.OptionMenu(input_frame, variable1, *currency_list)
ToCurrency_option = tk.OptionMenu(input_frame, variable2, *currency_list)
FromCurrency_option.config(font=('Segoe UI', 12), bg="#3498db", fg="white")
ToCurrency_option.config(font=('Segoe UI', 12), bg="#3498db", fg="white")
FromCurrency_option.grid(row=1, column=1, sticky="w", padx=10, pady=10)
ToCurrency_option.grid(row=2, column=1, sticky="w", padx=10, pady=10)

# Amount Fields
Amount1_field = tk.Entry(input_frame, font=('Segoe UI', 12))
Amount1_field.grid(row=0, column=1, sticky="w", padx=10, pady=10)

Amount2_field = tk.Entry(input_frame, font=('Segoe UI', 12))
Amount2_field.grid(row=3, column=1, sticky="w", padx=10, pady=10)

# Buttons
convert_button = tk.Button(input_frame, font=('Segoe UI', 14, 'bold'), text=" Convert ", padx=10, pady=5, bg="#3498db", fg="white", command=RealTimeCurrencyConversion)
convert_button.grid(row=5, column=0, columnspan=2, pady=20)

clear_button = tk.Button(input_frame, font=('Segoe UI', 14, 'bold'), text=" Clear All ", padx=10, pady=5, bg="#e74c3c", fg="white", command=clear_all)
clear_button.grid(row=6, column=0, columnspan=2, pady=10)

# Footer Label
footer_label = tk.Label(footer_frame, font=('Segoe UI', 10), text="Powered by ExchangeRate-API", bg="#2c3e50", fg="white")
footer_label.pack(pady=5)

# Center the content in the root window
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)

root.mainloop()
