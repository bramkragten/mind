"""
Support for Mind Mobility connected cars.

For more details about this component, please refer to the documentation at
https://home-assistant.io/components/mind/
"""
import logging
import socket
import asyncio
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from homeassistant.const import (
    CONF_USERNAME, CONF_PASSWORD, CONF_SCAN_INTERVAL)
from homeassistant.helpers import discovery

_LOGGER = logging.getLogger(__name__)

CONF_CLIENT_ID = 'client_id'
CONF_CLIENT_SECRET = 'client_secret'

DOMAIN = 'mind'

DATA_MIND = 'mind'

TOKEN_FILE = 'mind.conf'

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Required(CONF_USERNAME): cv.string,
        vol.Required(CONF_PASSWORD): cv.string,
        vol.Optional(CONF_SCAN_INTERVAL, default=270): cv.positive_int,
        vol.Optional(CONF_CLIENT_ID, default='f531922867194c7197b8df82da18042e'): cv.string,
        vol.Optional(CONF_CLIENT_SECRET, default='eB7ecfF84ed94CBDA825AC6dee503Fca'): cv.string,
    })
}, extra=vol.ALLOW_EXTRA)


def setup(hass, config):
    """Set up the Mind component."""
    conf = config.get(DOMAIN)
    hass.data[DATA_MIND] = Mind(hass, conf)

    _LOGGER.debug("Setup Mind")

    discovery.load_platform(hass, 'device_tracker', DOMAIN, {}, config)
    discovery.load_platform(hass, 'sensor', DOMAIN, {}, config)
    discovery.load_platform(hass, 'binary_sensor', DOMAIN, {}, config)

    return True

class Mind(object):
    """Structure Mind functions for hass."""
    
    def __init__(self, hass, conf):
        """Init Mind devices."""
        import mind
        access_token_cache_file = hass.config.path(TOKEN_FILE)
        #_LOGGER.debug("conf: %s" % conf)
        self.mind = mind.Mind(
                                  token_cache_file=access_token_cache_file,
                                  client_id=conf.get(CONF_CLIENT_ID), 
                                  client_secret=conf.get(CONF_CLIENT_SECRET),
                                  username=conf.get(CONF_USERNAME),
                                  password=conf.get(CONF_PASSWORD), cache_ttl=conf.get(CONF_SCAN_INTERVAL))

    @property
    def data(self):
      return self.mind

    def drivers(self):
        """Generate a list of drivers."""
        for driver in self.mind.drivers:
            yield driver

    def vehicles(self):
        """Generate a list of vehicles and their location."""
        for vehicle in self.mind.vehicles:
            yield vehicle