def sub_cb(topic, msg):
    global topic_sub
    if topic == topic_sub and msg == b'ping':
        print('Ping received, sending pong')
        client.publish(topic_sub, b'pong')

    if topic == b'notification' and msg == b'received':
        print('ESP received hello message')


def connect_and_subscribe():
    global client_id, mqtt_server, mqtt_user, mqtt_password, topic_sub, mqtt_root_topic
    client = MQTTClient(client_id, mqtt_server,
                        user=mqtt_user, password=mqtt_password, keepalive=60)
    client.set_callback(sub_cb)
    client.set_last_will(topic_status, b'offline')
    client.connect()
    client.publish(topic_status, b'online')
    client.subscribe(topic_sub)
    print('Connected to %s MQTT broker, subscribed to %s topic' %
          (mqtt_server, topic_sub))
    return client


def reset_esp():
    print('Resetting ESP...')
    time.sleep(1)  # Optional delay to ensure logging
    reset()


print('Connecting to SSID: %s' % ssid)
sta_if.active(True)
sta_if.connect(ssid, password)

# Wi-Fi connection loop with timeout
timeout = 0
while not sta_if.isconnected() and timeout < 10:
    time.sleep(1)
    timeout += 1

if sta_if.isconnected():
    ap_if.active(False)
    print('Connection successful')
    print(sta_if.ifconfig())
    print('My MAC address: %s' % mac)

    analog_pin = ADC(0)

    try:
        client = connect_and_subscribe()
    except OSError as e:
        print('Failed to connect to MQTT broker, resetting...')
        reset_esp()

    led.value(1)
    print('Starting main loop')
    while True:
        try:
            # Check for new messages and send updates
            client.check_msg()
            if (time.time() - last_message) > message_interval:
                led.value(0)
                analog_value = analog_pin.read()
                print('Read analog value: %s' % analog_value)
                client.publish(topic_pub, b'%s' % analog_value)
                last_message = time.time()
                counter += 1
                led.value(1)

        except OSError as e:
            print('Connection error in main loop, resetting...')
            reset_esp()

        time.sleep_ms(loop_sleep_ms)

else:
    print('Failed to connect to Wi-Fi, resetting...')
    reset_esp()
