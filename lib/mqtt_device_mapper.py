from lib.models.mqtt_data import DeviceType, MqttDevice, MqttDeviceSwitch, MqttDeviceTempHum, MqttDeviceButton, \
    MqttDeviceMotion


def map_device(name: str, device_type: DeviceType, payload: dict) -> MqttDevice:
    if device_type == DeviceType.SWITCH:
        signal_strength = _map_signal_strength(payload)
        state = payload.get('state', 'off').lower() == 'on'
        return MqttDeviceSwitch(name=name, type=device_type, signal_strength=signal_strength, state=state)

    if device_type == DeviceType.TEMP_HUM:
        signal_strength = _map_signal_strength(payload)
        battery, voltage = _map_battery_voltage(payload)
        temperature = payload.get('temperature', 0.0)
        humidity = payload.get('humidity', 0.0)
        return MqttDeviceTempHum(name=name, type=device_type, signal_strength=signal_strength,
                                 battery=battery, voltage=voltage, temperature=temperature, humidity=humidity)

    if device_type == DeviceType.BUTTON:
        signal_strength = _map_signal_strength(payload)
        battery, voltage = _map_battery_voltage(payload)
        action = payload.get('action', '')
        return MqttDeviceButton(name=name, type=device_type, signal_strength=signal_strength,
                                battery=battery, voltage=voltage, action=action)

    if device_type == DeviceType.MOTION:
        signal_strength = _map_signal_strength(payload)
        battery, voltage = _map_battery_voltage(payload)
        occupancy = payload.get('occupancy', False)
        return MqttDeviceMotion(name=name, type=device_type, signal_strength=signal_strength,
                                battery=battery, voltage=voltage, occupancy=False)

    return None


def _map_signal_strength(payload: dict) -> str:
    signal_strength = payload.get('linkquality', None)
    if signal_strength is None:
        return 'Неизветсно'
    return f'{signal_strength} дБ'


def _map_battery_voltage(payload: dict) -> (str, str):
    battery = payload.get('battery', 0)
    voltage = payload.get('voltage', 0)
    return battery, voltage
