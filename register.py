import select
import sys
import pybonjour


name = "cristal"
regtype = "_%s._tcp" % (name)
port = int("8310")


def register_callback(sdRef, flags, errorCode, name, regtype, domain):
	if errorCode == pybonjour.kDNSServiceErr_NoError:
		print 'Registered service:'
		print '  name	=', name
		print '  regtype =', regtype
		print '  domain  =', domain


sdRef = pybonjour.DNSServiceRegister(name = name,
									 regtype = regtype,
									 port = port,
									 callBack = register_callback)

try:
	try:
		while True:
			ready = select.select([sdRef], [], [])
			if sdRef in ready[0]:
				pybonjour.DNSServiceProcessResult(sdRef)
	except KeyboardInterrupt:
		pass
finally:
	sdRef.close()