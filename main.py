def sub_cb(topic, msg):
    global topic_sub
    # print((topic, msg))
    if topic == topic_sub and msg == b'ping':
        print('ping recieved, sending pong')
        client.publish(topic_sub, b'pong')

    if topic == b'notification' and msg == b'received':
        print('ESP received hello message')


def connect_and_subscribe():
    global client_id, mqtt_server, mqtt_user, mqtt_password, topic_sub
    client = MQTTClient(client_id, mqtt_server,
                        user=mqtt_user, password=mqtt_password)
    client.set_callback(sub_cb)
    client.connect()
    client.subscribe(topic_sub)
    print('Connected to %s MQTT broker, subscribed to %s topic' %
          (mqtt_server, topic_sub))
    return client


def restart_and_reconnect():
    led.value(0)
    print('Failed to connect to MQTT broker. Reconnecting...')
    time.sleep(10)
    reset()


analog_pin = ADC(0)

try:
    client = connect_and_subscribe()
except OSError as e:
    restart_and_reconnect()

led.value(1)
print('Starting main loop')
while True:
    try:
        client.check_msg()
        if (time.time() - last_message) > message_interval:
            led.value(0)
            analog_value = analog_pin.read()
            print('Read the following value: %s' % analog_value)
            client.publish(topic_pub, b'%s' % analog_value)
            last_message = time.time()
            counter += 1
            led.value(1)
            
    except OSError as e:
        restart_and_reconnect()

    time.sleep_ms(loop_sleep_ms)
