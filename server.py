from flask import Flask, request
import json
import RPi.GPIO as GPIO

PIN = 1

def cristal_init():
	print "Initializing RPi GPIO..."
	GPIO.setup(PIN, GPIO.OUT)
	GPIO.output(PIN, False)

@app.route("/", methods=["GET"]):
	def get_html_format():
		return "html_format"

@app.route("/?output=json", methods=["GET"])
	def json_format():
		jsonStr = json.dumps({"state" : GPIO.input(PIN)})
		resp = make_response(jsonStr, 200)
		resp.headers["Content-type"] = "application/json"
		return resp

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1357, debug=True)
    cristal_init