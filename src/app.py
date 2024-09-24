#!/usr/bin/env python3

from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def main():
    return '''
     <form action="/echo_user_input" method="POST">
         <input name="user_input">
         <input type="submit" value="Submit!">
     </form>
     '''

@app.route("/echo_user_input", methods=["POST"])
def echo_input():
    input_text = request.form.get("user_input", "")

    # Input validation
    if not input_text:
        return "Empty input."
    elif len(input_text) > 100:
        return "Input too long."
    elif not input_text.isalnum():
        return "Input must be alphanumeric."

    return "You entered: " + input_text