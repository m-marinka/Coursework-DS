import http.client
import json


host = "localhost"
port = 5000

# connection = http.client.HTTPConnection(host, port)
# connection.request("GET", "/")
# response = connection.getresponse()
# print("Status: {} and reason: {}".format(response.status, response.reason))
# connection.close()
echo_ = 'echo'
write = input("enter your test: ")
conn = http.client.HTTPConnection(host, port)

headers = {'Content-type': 'application/json'}

foo = {'echo': write}
json_data = json.dumps(foo)

conn.request('POST', '/echo', json_data)

response = conn.getresponse()

decode = response.read().decode('utf-8')
print(decode)
conn.close()



