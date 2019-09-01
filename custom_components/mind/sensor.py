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
    'battery': ['Battery', 'V', 'mdi:car-battery'],
    'maintenancedate': ['Maintenance Date','','mdi:calendar'],
    'servicedate': ['Service Date','','mdi:calendar'],
    'daysuntilmaintenance': ['Days Until Maintenance','Days','mdi:counter'],
    'daysuntilservice': ['Days Until Service','Days','mdi:counter'],
    'enginefueltype': ['Engine Fueltype','','mdi:gas-station'],
    'licenseplate': ['License Plate','','mdi:card-text'],
    'brand': ['Brand','','mdi:card-text'],
    'model': ['Model','','mdi:card-text'],
    'edition': ['Edition','','mdi:card-text'],
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
        devs.append(MindSensor(vehicle.license_plate, 'maintenancedate', vehicle))
        devs.append(MindSensor(vehicle.license_plate, 'servicedate', vehicle))
        devs.append(MindSensor(vehicle.license_plate, 'daysuntilmaintenance', vehicle))
        devs.append(MindSensor(vehicle.license_plate, 'daysuntilservice', vehicle))
        devs.append(MindSensor(vehicle.license_plate, 'enginefueltype', vehicle))
        devs.append(MindSensor(vehicle.license_plate, 'licenseplate', vehicle))
        devs.append(MindSensor(vehicle.license_plate, 'model', vehicle))
        devs.append(MindSensor(vehicle.license_plate, 'brand', vehicle))
        devs.append(MindSensor(vehicle.license_plate, 'edition', vehicle))

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
            self._state = round(self._vehicle.batteryVoltage,2)
        elif self._type == 'maintenancedate':
            self._state = self._vehicle.maintenanceDate
        elif self._type == 'servicedate':
            self._state = self._vehicle.serviceDate
        elif self._type == 'daysuntilmaintenance':
            self._state = self._vehicle.remainingDaysUntilMaintenance
        elif self._type == 'daysuntilservice':
            self._state = self._vehicle.remainingDaysUntilService
        elif self._type == 'enginefueltype':
            self._state = self._vehicle.engineFuelType
        elif self._type == 'licenseplate':
            self._state = self._vehicle.license_plate
        elif self._type == 'brand':
            self._state = self._vehicle.brand
        elif self._type == 'model':
            self._state = self._vehicle.model
        elif self._type == 'edition':
            self._state = self._vehicle.edition
        else:
            self._state = None
            _LOGGER.warning("Could not retrieve state from %s", self.name)
