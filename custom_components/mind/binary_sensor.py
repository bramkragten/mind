"""
For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/binary_sensor.mind/
"""
import logging

from custom_components.mind import DATA_MIND
from homeassistant.components.binary_sensor import (
    BinarySensorDevice, PLATFORM_SCHEMA)

_LOGGER = logging.getLogger(__name__)

DEPENDENCIES = ['mind']

SENSOR_TYPES = {
    'ignition': ['Ignition', True, 'power', 'mdi:power', 'mdi:power'],
    'doors_locked': ['Locked', False, 'opening', 'mdi:lock', 'mdi:lock-open'],
    'parking_brake': ['Parking brake', False, 'safety', 'mdi:parking', 'mdi:parking']
}

def setup_platform(hass, config, add_devices, discovery_info=None):
    """Set up a Mind binary sensor."""
    if discovery_info is None:
        return

    devs = list()
    mind = hass.data[DATA_MIND]
    for vehicle in mind.vehicles():
        devs.append(MindBinarySensor(vehicle.license_plate, 'ignition', mind, vehicle))
        devs.append(MindBinarySensor(vehicle.license_plate, 'doors_locked', mind, vehicle))
        devs.append(MindBinarySensor(vehicle.license_plate, 'parking_brake', mind, vehicle))

    add_devices(devs, True)


class MindBinarySensor(BinarySensorDevice):
    """A Mind binary sensor."""

    def __init__(self, name, sensor_type, mind, vehicle):
        """Initialize sensors from the car."""
        self._name = name + ' ' + SENSOR_TYPES[sensor_type][0]
        self._type = sensor_type
        self._vehicle = vehicle
        self._mind = mind
        self._state = None
        self._on_state = SENSOR_TYPES[sensor_type][1]
        self._device_class = SENSOR_TYPES[sensor_type][2]
        self._icon_off = SENSOR_TYPES[sensor_type][3]
        self._icon_on = SENSOR_TYPES[sensor_type][4]

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def device_class(self):
        """Return the class of this sensor."""
        return self._device_class

    @property
    def icon(self):
        """Return the icon of this sensor."""
        if self.is_on:
            return self._icon_on
        else:
            return self._icon_off

    @property
    def is_on(self):
        """Return the state of the entity."""
        return self._state == self._on_state

    def update(self):
        """Retrieve sensor data from the car."""
        if self._type == 'ignition':
            self._state = self._vehicle.ignition
            if self._state == True:
                self._mind.cache_ttl = 30
            else:
                self._mind.cache_ttl = 60
        elif self._type == 'doors_locked':
            self._state = self._vehicle.doors_locked
        elif self._type == 'parking_brake':
            self._state = self._vehicle.parking_brake
        else:
            self._state = None
            _LOGGER.warning("Could not retrieve state from %s", self.name)
