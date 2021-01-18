"""Livebox TV"""

import logging
import requests
import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.helpers.aiohttp_client import async_create_clientsession
from homeassistant.const import CONF_HOST, EVENT_HOMEASSISTANT_STOP

DOMAIN = "livebox_tv"
player_path = "/remoteControl/cmd"

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {vol.Required(CONF_HOST): cv.string}
        )
    },
    extra=vol.ALLOW_EXTRA,
)

REMOTE_SCHEMA = vol.Schema(
    {
        vol.Optional("code"): cv.string
    }
)

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass, config):
    """Set up the Livebox TV component."""
    conf = config.get(DOMAIN)

    if conf is not None:
        host = conf.get(CONF_HOST)
        global player_path
        player_path = "http://"+host+player_path+"?operation=01&mode=0&key="

        await async_setup_livebox_tv(hass, config, host)

    return True

async def async_setup_livebox_tv(hass, config, host):

    async def async_livebox_tv_remote(call):
        """Handle old player control (remote emulation)"""

        code_list = call.data.get('code')

        code_array = code_list.split(',')

        """Handle multiple codes, separated by comma"""
        for code in code_array:
            requests.get(player_path+code, verify=False)

    hass.services.async_register(DOMAIN, "remote", async_livebox_tv_remote)
