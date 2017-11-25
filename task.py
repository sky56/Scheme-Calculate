from flask import Flask, render_template, request
from datetime import datetime, timedelta
import pandas

app = Flask(__name__)

@app.route("/",methods=['GET','POST'])
def homepage():
    if request.method=='POST':
        date = request.form["given_date"]
        amount = float(request.form["amount"])
        data = pandas.read_csv("mutual.txt",sep=';')
        dates = list(data["Date"])
        check_date = datetime.strptime(date,'%Y-%m-%d').date()
        converted_date = datetime.strftime(check_date,'%d-%b-%Y')
        if converted_date in dates:
            date_position = dates.index(converted_date)
        else:
            while converted_date not in dates:
                check_date = check_date - timedelta(days=1)
                converted_date = datetime.strftime(check_date,'%d-%b-%Y')
            date_position = dates.index(converted_date)
        given_nav = data['Net Asset Value'][date_position]
        current_nav = data['Net Asset Value'].iloc[-1]
        present_worth = amount*current_nav/given_nav
        present_worth = round(present_worth,2)
        present_worth = "Rs." + str(present_worth)
        return render_template("index.html",given_date=date,amount=amount,present_worth=present_worth)
    return render_template("index.html")

if __name__ == "__main__":
    app.run()
