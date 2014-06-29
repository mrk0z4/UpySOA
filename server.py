from flask import Flask, request, make_response, json, jsonify
import sys
import rdflib
import select
import sys
import pybonjour
import threading
import RPi.GPIO as GPIO

app = Flask(__name__)
PIN = 1

#Definitions for DNS Service Discovery
name = "cristal"
regtype = "_%s._tcp" % (name)
port = int("8310")

def register_callback(sdRef, flags, errorCode, name, regtype, domain):
	if errorCode == pybonjour.kDNSServiceErr_NoError:
		print 'Registered service:'
		print '  name	=', name
		print '  regtype =', regtype
		print '  domain  =', domain

def runDnsServiceDiscovery(sdRef):
	while True:
		ready = select.select([self.sdRef], [], [])
		if self.sdRef in ready[0]:
			pybonjour.DNSServiceProcessResult(self.sdRef)

def cristal_init():
	print "Initializing RPi GPIO..."
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(PIN, GPIO.OUT)
	GPIO.output(PIN, False)

@app.route("/", methods=["GET"])
def send_format():
	if request.method == "GET":
		output = request.args.get("output", "")
		if output == "json":
			jsonStr = json.dumps({"state" : GPIO.input(PIN)})
			resp = make_response(jsonStr, 200)
			resp.headers["Content-type"] = "application/json"
			return resp
		elif output == "xml":
			xmlStr = getXmlRepresentation(GPIO.input(PIN))
			resp = make_response(xmlStr, 200)
			resp.headers["Content-type"] = "application/xml"
			return resp
		elif output == "html":
			htmlStr = getHtmlRepresentation(GPIO.input(PIN))
			resp = make_response(htmlStr, 200)
			resp.headers["Content-type"] = "application/html"
			return resp
		else:
			return "no format specified"		
	else:
		return "not a GET request"

@app.route("/", methods=["POST"])
def set_pin_state():
	if request.method == "POST":
		jsonResponse = request.get_json()
		state = jsonResponse["state"]
		if state == "1" or state == "True" or state == "true" or state == "on":
			GPIO.output(PIN, 1);
			jsonStr = json.dumps({"state" : 1})			
			return jsonStr
		elif state == "0" or state == "False" or state == "false" or state == "off":
			GPIO.output(PIN, 0);
			jsonStr = json.dumps({"state" : 0})	
			return jsonStr
		else:
			return "not a valid state"
	else:
		return "not a POST request"

def getXmlRepresentation(state):
	xmlStr = "<cristal><state>%s</state></cristal>" % (state)
	return xmlStr

def getHtmlRepresentation(state):
	htmlStr = "<p>Current state: <strong>%s</strong></p><br /><form id=\"form\" method=\"POST\"><input type=\"text\" name=\"state\" placeholder=\"%s\"/><input type\"submit\" value=\"Submit\"/></form>" % (state, state)
	return htmlStr

if __name__ == "__main__":
	#Init DNS Service Discovery
	sdRef = pybonjour.DNSServiceRegister(name = "cristal", 
										regtype = "_cristal._tcp", 
										port = int("8310"), 
										callBack = register_callback)
	runDnsServiceDiscovery(sdRef)
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(PIN, GPIO.OUT)
	GPIO.output(PIN, False)
	app.run(host="0.0.0.0", port=port, debug=True)