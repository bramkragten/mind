"""
For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/sensor.mind/
"""
import logging

from custom_components.mind import DATA_MIND
from homeassistant.const import (LENGTH_KILOMETERS, VOLUME_LITERS)
from homeassistant.helpers.entity import Entity

_LOGGER = logging.getLogger(__name__)

DEPENDENCIES = ['mind']

SENSOR_TYPES = {
    'mileage': ['Mileage', LENGTH_KILOMETERS, 'mdi:counter'],
    'mileage_left': ['Mileage Left', LENGTH_KILOMETERS, 'mdi:fuel'],
    'fuel_left': ['Fuel Left', VOLUME_LITERS, 'mdi:fuel'],
    'battery': ['Battery', 'V', 'mdi:car-battery']
}


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Set up a Mind sensor."""
    if discovery_info is None:
        return

    devs = list()
    for vehicle in hass.data[DATA_MIND].vehicles():
        devs.append(MindSensor(vehicle.license_plate, 'mileage', vehicle))
        devs.append(MindSensor(vehicle.license_plate, 'mileage_left', vehicle))
        devs.append(MindSensor(vehicle.license_plate, 'fuel_left', vehicle))
        devs.append(MindSensor(vehicle.license_plate, 'battery', vehicle))

    add_devices(devs, True)


class MindSensor(Entity):
    """A Mind sensor."""

    def __init__(self, name, sensor_type, vehicle):
        """Initialize sensors from the car."""
        self._name = name + ' ' + SENSOR_TYPES[sensor_type][0]
        self._type = sensor_type
        self._vehicle = vehicle
        self._state = None
        self._unit_of_measurement = SENSOR_TYPES[sensor_type][1]
        self._icon = SENSOR_TYPES[sensor_type][2]

    @property
    def name(self):
        """Return the name of the car."""
        return self._name

    @property
    def state(self):
        """Return the current state."""
        return self._state

    @property
    def icon(self):
        return self._icon

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return self._unit_of_measurement

    def update(self):
        """Retrieve sensor data from the car."""
        if self._type == 'mileage':
            self._state = self._vehicle.mileage/1000
        elif self._type == 'mileage_left':
            self._state = self._vehicle.mileage_left
        elif self._type == 'fuel_left':
            self._state = self._vehicle.fuellevel
        elif self._type == 'battery':
            self._state = self._vehicle.batteryVoltage
        else:
            self._state = None
            _LOGGER.warning("Could not retrieve state from %s", self.name)
