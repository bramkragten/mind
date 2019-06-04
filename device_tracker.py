"""
For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/device_tracker.mind/
"""
import logging
from datetime import timedelta

from custom_components.mind import DATA_MIND, DOMAIN
from homeassistant.components.device_tracker import (PLATFORM_SCHEMA)
from homeassistant.components.device_tracker.const import (
    CONF_SCAN_INTERVAL, SCAN_INTERVAL)
from homeassistant.helpers.event import track_point_in_utc_time
from homeassistant.util.dt import utcnow

_LOGGER = logging.getLogger(__name__)

DEPENDENCIES = ['mind']

def setup_scanner(hass, config, see, discovery_info=None):
    """Set up a Mind tracker."""
    if discovery_info is None:
        return
    
    _LOGGER.debug('Setting up device_tracker')

    interval = config.get(CONF_SCAN_INTERVAL, SCAN_INTERVAL)
    
    mind = hass.data[DATA_MIND]

    trackers = list()

    for vehicle in mind.vehicles():
        trackers.append(MindDeviceTracker(see, vehicle))


    def update(now):
        """Update the car on every interval time."""
        try:
            for tracker in trackers:
                tracker.update()
        finally:
            track_point_in_utc_time(hass, update, now + interval)

    update(utcnow())


    def handle_update_location(call):
        """Update location on demand."""
        for tracker in trackers:
            tracker.update()

    hass.services.register(
        DOMAIN, "update_location", handle_update_location)

    return True


class MindDeviceTracker:
    """Mind Connected Car device tracker."""

    def __init__(self, see, vehicle):
        """Initialize the Tracker."""
        self._see = see
        self.vehicle = vehicle

    def update(self) -> None:
        """Update the device info."""

        _LOGGER.debug('Updating %s', self.vehicle.license_plate)
        
        attrs = {
            'street': self.vehicle.street,
            'number': self.vehicle.number,
            'city': self.vehicle.city,
            'country': self.vehicle.country,
        }

        self._see(
            dev_id=self.vehicle.license_plate, host_name=self.vehicle.brand,
            gps=(self.vehicle.lat, self.vehicle.lon), attributes=attrs,
            icon='mdi:car'
        )

