#Import necessary libraries
from flask import Flask, render_template

# Cretae instance of flask app
app=Flask(__name__)

#Create route that renedrs index.html template
@app.route("/")
def echo():
    return render_template("/index.html", text="Mission to Mars")


if __name__=="__main__":
    app.run(debug=True)