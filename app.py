from flask import Flask, request, render_template

app = Flask(__name__)

# Add a route for the root URL
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        purchase_price = float(request.form['purchase_price'].replace("$", "").replace(",", ""))
        annual_rent_income = float(request.form['annual_rent_income'].replace("$", "").replace(",", ""))
        annual_operating_expenses = float(request.form['annual_operating_expenses'].replace("$", "").replace(",", ""))
        loan_amount = float(request.form['loan_amount'].replace("$", "").replace(",", ""))
        down_payment = float(request.form['down_payment'].replace("$", "").replace(",", ""))

        # Ensure values are valid
        if any(value < 0 for value in [purchase_price, annual_rent_income, annual_operating_expenses, loan_amount, down_payment]):
            raise ValueError("Input values must be non-negative.")

        # Calculate the financial metrics
        noi = annual_rent_income - annual_operating_expenses
        cap_rate = (noi / purchase_price) * 100
        grm = purchase_price / annual_rent_income if annual_rent_income != 0 else float('inf')
        cash_on_cash_return = (noi / down_payment) * 100 if down_payment != 0 else float('inf')
        loan_to_value_ratio = (loan_amount / purchase_price) * 100 if purchase_price != 0 else float('inf')

        # Pass the calculated results to the template
        results = {
            "NOI": f"${noi:,.2f}",
            "Cap Rate": f"{cap_rate:.2f}%",
            "GRM": f"{grm:.2f}",
            "Cash-on-Cash Return": f"{cash_on_cash_return:.2f}%",
            "LTV Ratio": f"{loan_to_value_ratio:.2f}%"
        }
        return render_template('index.html', results=results, inputs=inputs)

    except ValueError as e:
        return render_template('index.html', error=f"Invalid input: {str(e)}", inputs=request.form)
    except Exception as e:
        return render_template('index.html', error="An unexpected error occurred.", inputs=request.form)
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)  # Set the port to 8080 here
    