from lib.models.mqtt_data import DeviceType, MqttDevice, MqttDeviceSwitch, MqttDeviceTempHum


def map_device(name: str, device_type: DeviceType, payload: dict) -> MqttDevice:
    if device_type == DeviceType.SWITCH:
        signal_strength = _map_signal_strength(payload)
        state = payload.get('state', 'off').lower() == 'on'
        return MqttDeviceSwitch(name=name, type=device_type, signal_strength=signal_strength, state=state)

    if device_type == DeviceType.TEMP_HUM:
        signal_strength = _map_signal_strength(payload)
        temperature = payload.get('temperature', 0.0)
        humidity = payload.get('humidity', 0.0)
        battery = payload.get('battery', 0)
        voltage = payload.get('voltage', 0)
        return MqttDeviceTempHum(name=name, type=device_type, signal_strength=signal_strength,
                                 temperature=temperature, humidity=humidity, battery=battery, voltage=voltage)

    return None


def _map_signal_strength(payload: dict) -> str:
    signal_strength = payload.get('linkquality', None)
    if signal_strength is None:
        return 'Неизветсно'
    return f'{signal_strength} дБ'