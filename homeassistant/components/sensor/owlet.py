"""
Support for the Owlet baby monitor.

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/sensor.owlet/
"""
from datetime import timedelta
import logging

import voluptuous as vol

from homeassistant.components.sensor import PLATFORM_SCHEMA
import homeassistant.helpers.config_validation as cv
from homeassistant.const import CONF_USERNAME, CONF_PASSWORD
from homeassistant.helpers.entity import Entity

REQUIREMENTS = ['pyowlet==1.0.0']

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_USERNAME): cv.string,
    vol.Required(CONF_PASSWORD): cv.string,
})


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the Owlet sensor."""
    from pyowlet.PyOwlet import PyOwlet

    pyowletClient = PyOwlet(config[CONF_USERNAME], config[CONF_PASSWORD], 5)

    add_entities([OwletMonitor(pyowletClient)])


class OwletMonitor(Entity):
    def __init__(self, owlet):
        """Initialize the meter."""
        self.owlet = owlet
        self._data = {}
        self._state = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return 'Owlet'

    def update(self):
        """Get the latest data from owlet."""
        self._state = self._determine_state()
        self._data = {
            'base_station_on': self.owlet.base_station_on,
            'batt_level': self.owlet.batt_level,
            'crit_batt_alrt': self.owlet.crit_batt_alrt,
            'crit_ox_alrt': self.owlet.crit_ox_alrt,
            'heart_rate': self.owlet.heart_rate,
            'high_hr_alrt': self.owlet.high_hr_alrt,
            'low_batt_alrt': self.owlet.low_batt_alrt,
            'low_batt_prcnt': self.owlet.low_batt_prcnt,
            'low_hr_alrt': self.owlet.low_hr_alrt,
            'low_ox_alrt': self.owlet.low_ox_alrt,
            'low_pa_alrt': self.owlet.low_pa_alrt,
            'movement': self.owlet.movement,
            'nursery_mode': self.owlet.nursery_mode,
            'sock_off': self.owlet.sock_off,
            'sock_rec_placed': self.owlet.sock_rec_placed
        }

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    def _determine_state(self):

        crit_alarms = self.owlet.high_hr_alrt + \
            self.owlet.low_hr_alrt + self.owlet.low_ox_alrt + self.owlet.low_pa_alrt
        if crit_alarms > 0:
            return 'CRITICAL_ALARM'

        if self.owlet.charge_status > 0:
            return 'CHARGING'

        return 'NORMAL'

    @property
    def device_state_attributes(self):

        return self._data
