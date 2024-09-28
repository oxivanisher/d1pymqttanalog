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
                        user=mqtt_user, password=mqtt_password)
    client.set_callback(sub_cb)
    client.set_last_will(topic_status, b'offline')
    client.connect()
    client.publish(topic_status, b'online')
    client.subscribe(topic_sub)
    print('Connected to %s MQTT broker, subscribed to %s topic' %
          (mqtt_server, topic_sub))
    return client


def reconnect(max_attempts=3, delay_between_attempts=10):
    print('Attempting to reconnect to Wi-Fi...')
    attempt = 0
    while attempt < max_attempts:
        print('Reconnect attempt %d' % (attempt + 1))

        # Reset Wi-Fi interface before each attempt
        sta_if.active(False)
        time.sleep(1)  # Give it a second to fully reset
        sta_if.active(True)

        sta_if.connect(ssid, password)
        timeout = 0
        while not sta_if.isconnected() and timeout < 20:
            time.sleep(1)
            timeout += 1

        if sta_if.isconnected():
            print('Reconnected to Wi-Fi successfully')
            return True
        else:
            attempt += 1
            print('Reconnect attempt %d failed' % attempt)
            time.sleep(delay_between_attempts)  # Add delay before retrying

    print('Max reconnect attempts reached, rebooting ESP...')
    reset()


def restart_and_reconnect():
    led.value(0)
    if reconnect():
        try:
            client = connect_and_subscribe()
        except OSError:
            print('Failed to connect to MQTT broker. Rebooting...')
            time.sleep(10)
            reset()
    else:
        reset()


print('Connecting to ssid %s' % ssid)
sta_if.active(True)
sta_if.connect(ssid, password)

# Wi-Fi connection loop with timeout
timeout = 0
while not sta_if.isconnected() and timeout < 20:
    time.sleep(1)
    timeout += 1

if sta_if.isconnected():
    ap_if.active(False)
    print('Wi-Fi connected')
    print(sta_if.ifconfig())
    print('MAC address: %s' % mac)

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
                print('Analog value: %s' % analog_value)
                client.publish(topic_pub, b'%s' % analog_value)
                last_message = time.time()
                counter += 1
                led.value(1)

        except OSError as e:
            restart_and_reconnect()

        time.sleep_ms(loop_sleep_ms)

else:
    print('Failed to connect to Wi-Fi initially. Rebooting...')
    reset()
