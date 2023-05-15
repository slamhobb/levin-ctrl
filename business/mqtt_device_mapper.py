from lib.models.mqtt_data import DeviceType, MqttDevice, MqttDeviceSwitch, MqttDeviceTempHum, MqttDeviceButton, \
    MqttDeviceMotion, MqttDeviceSocket, MqttDeviceLight, MqttDeviceMotor, MqttDeviceCO2


class MqttDeviceMapper:
    @staticmethod
    def map_device(name: str, device_type: DeviceType, payload: dict) -> MqttDevice:
        if device_type == DeviceType.SWITCH:
            signal_strength = MqttDeviceMapper._map_signal_strength(payload)
            state = payload.get('state', 'off').lower() == 'on'
            return MqttDeviceSwitch(name=name, type=device_type, signal_strength=signal_strength, state=state)

        if device_type == DeviceType.SOCKET:
            signal_strength = MqttDeviceMapper._map_signal_strength(payload)
            state = payload.get('state', 'off').lower() == 'on'
            power = payload.get('power', 0.0)
            return MqttDeviceSocket(name=name, type=device_type, signal_strength=signal_strength, state=state,
                                    power=power)

        if device_type == DeviceType.LIGHT:
            signal_strength = MqttDeviceMapper._map_signal_strength(payload)
            state = payload.get('state', 'off').lower() == 'on'
            brightness = payload.get('brightness', 0)
            color_temp = payload.get('color_temp', 0)
            return MqttDeviceLight(name=name, type=device_type, signal_strength=signal_strength, state=state,
                                   brightness=brightness, color_temp=color_temp)

        if device_type == DeviceType.TEMP_HUM:
            signal_strength = MqttDeviceMapper._map_signal_strength(payload)
            battery, voltage = MqttDeviceMapper._map_battery_voltage(payload)
            temperature = payload.get('temperature', 0.0)
            humidity = payload.get('humidity', 0.0)
            return MqttDeviceTempHum(name=name, type=device_type, signal_strength=signal_strength,
                                     battery=battery, voltage=voltage, temperature=temperature, humidity=humidity)

        if device_type == DeviceType.BUTTON:
            signal_strength = MqttDeviceMapper._map_signal_strength(payload)
            battery, voltage = MqttDeviceMapper._map_battery_voltage(payload)
            action = payload.get('action', '')
            return MqttDeviceButton(name=name, type=device_type, signal_strength=signal_strength,
                                    battery=battery, voltage=voltage, action=action)

        if device_type == DeviceType.MOTION:
            signal_strength = MqttDeviceMapper._map_signal_strength(payload)
            battery, voltage = MqttDeviceMapper._map_battery_voltage(payload)
            occupancy = payload.get('occupancy', False)
            return MqttDeviceMotion(name=name, type=device_type, signal_strength=signal_strength,
                                    battery=battery, voltage=voltage, occupancy=occupancy)

        if device_type == DeviceType.MOTOR:
            signal_strength = MqttDeviceMapper._map_signal_strength(payload)
            position = payload.get('position', -1)
            return MqttDeviceMotor(name=name, type=device_type, signal_strength=signal_strength,
                                   position=position)

        if device_type == DeviceType.CO2:
            signal_strength = MqttDeviceMapper._map_signal_strength(payload)
            co2 = payload.get('co2', 0)
            return MqttDeviceCO2(name=name, type=device_type, signal_strength=signal_strength,
                                 co2=co2)

        raise Exception('Unsupported device')

    @staticmethod
    def _map_signal_strength(payload: dict) -> str:
        signal_strength = payload.get('linkquality', None)
        if signal_strength is None:
            return 'Неизветсно'
        return f'{signal_strength} lqi'

    @staticmethod
    def _map_battery_voltage(payload: dict) -> (str, str):
        battery = payload.get('battery', 0)
        voltage = payload.get('voltage', 0)
        return battery, voltage
