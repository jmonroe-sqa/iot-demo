import paho.mqtt.client as mqtt
import os, urllib3
import time
import random
import socket
import paramiko
import datetime
import subprocess
import json

# Thingsboard credentialws:
# username  = rY4xwLCmV8YcKp6eJcWP
# password = ""

hostname = socket.gethostname()
pid = str(os.getpid())

TemperFile = open("Temper.txt", "w+")

# Define event callbacks
def on_connect(client, userdata, flags, rc):
    mqttc.connected_flag = True
    print("Connect ack: " + str(rc))

def on_message(client, obj, msg):  
    proc = subprocess.Popen(['sudo', 'python3', '/home/pi/Python/cloudMQTT/temper.py'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    data = proc.communicate()[0]
    data = data.split('\s+')
    temp = data[4]
    temp = temp.replace("F", "")
    mqttc.publish("topic/TopicMain", ">> Temperature: " + str(temp) )
      

def on_publish(client, obj, mid):
    #print("Published: " + str(mid))
    pass

def on_subscribe(client, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))
    pass

def on_log(client, obj, level, string):
    print(string)

mqtt.Client.connected_flag = False
mqttc = mqtt.Client()

#mqttc._port = 1344
print ( str(mqttc._port) )

# Assign event callbacks
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe

broker = "demo.thingsboard.io"
port = 1883
username = "rY4xwLCmV8YcKp6eJcWP"
password = ""
mqttc.username_pw_set(username, password)
topic="v1/devices/me/telemetry"
#ret = mqttc.connect('postman.cloudmqtt.com', 18133)
ret = mqttc.connect(broker, port)

#mqttc.loop_start()

while not mqttc.connected_flag:
    mqttc.loop()
    time.sleep(1)
    print("Waiting on broker connection...")
print ("Connection established with broker")
time.sleep(2)

data=dict()
for i in range(9):
    data["test-data"] = random.randint(1,10000)
    data_out = json.dumps(data)
    print ("Publishing data " + str(data) )
    mqttc.publish(topic,data_out,0)
    time.sleep(5)
    mqttc.loop()

#while(1):
#    randint = random.randint(1,10000)
#    timestamp = datetime.datetime.now().time()    
#    print ( "Publishing @ [" + str(timestamp) + "] random number = " + str(randint) )
#    mqttc.publish("topic/TopicMain", str(hostname) + "[" + pid + "]" + "-" + str(timestamp) + " RandomNum = " + str(randint) )
#    time.sleep(2)

print ("Done sending topics...")
