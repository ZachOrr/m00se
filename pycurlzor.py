import pycurl
import json

conn = pycurl.Curl()
c.setopt(pycurl.URL, "https://api.github.com/gists")
c.setopt(pycurl.HTTPHEADER, {'Authorization': bytes('token 2583d226c3ce002513aa5a29d0b87a15e6dfa46b', 'UTF-8'), 'User-Agent': bytes('ecxinc', 'UTF-8'), 'Content-Type': bytes('application/json', 'UTF-8')})
c.setopt(pycurl.POST, 1)
c.setopt(pycurl.POSTFIELDS, json.dumps(data))
