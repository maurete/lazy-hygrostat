"""Config flow for Generic hygrostat."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, cast

import voluptuous as vol

from homeassistant.components import fan, switch
from homeassistant.components.humidifier import HumidifierDeviceClass
from homeassistant.components.sensor import DOMAIN as SENSOR_DOMAIN, SensorDeviceClass
from homeassistant.const import CONF_NAME, PERCENTAGE
from homeassistant.helpers import selector
from homeassistant.helpers.schema_config_entry_flow import (
    SchemaConfigFlowHandler,
    SchemaFlowFormStep,
)

from . import (
    CONF_DEVICE_CLASS,
    CONF_DRY_TOLERANCE,
    CONF_HUMIDIFIER,
    CONF_MIN_DUR,
    CONF_SENSOR,
    CONF_WET_TOLERANCE,
    CONF_ADJUSTMENT_RATE,
    DEFAULT_TOLERANCE,
    DEFAULT_ADJUSTMENT_RATE,
    DOMAIN,
    CONF_BOOST_DURATION,
    DEFAULT_BOOST_DURATION,
)

OPTIONS_SCHEMA = {
    vol.Required(CONF_DEVICE_CLASS): selector.SelectSelector(
        selector.SelectSelectorConfig(
            options=[
                HumidifierDeviceClass.HUMIDIFIER,
                HumidifierDeviceClass.DEHUMIDIFIER,
            ],
            translation_key=CONF_DEVICE_CLASS,
            mode=selector.SelectSelectorMode.DROPDOWN,
        ),
    ),
    vol.Required(CONF_SENSOR): selector.EntitySelector(
        selector.EntitySelectorConfig(
            domain=SENSOR_DOMAIN, device_class=SensorDeviceClass.HUMIDITY
        )
    ),
    vol.Required(CONF_HUMIDIFIER): selector.EntitySelector(
        selector.EntitySelectorConfig(domain=[switch.DOMAIN, fan.DOMAIN])
    ),
    vol.Required(
        CONF_DRY_TOLERANCE, default=DEFAULT_TOLERANCE
    ): selector.NumberSelector(
        selector.NumberSelectorConfig(
            min=-50,
            max=50,
            step=0.5,
            unit_of_measurement=PERCENTAGE,
            mode=selector.NumberSelectorMode.BOX,
        )
    ),
    vol.Required(
        CONF_WET_TOLERANCE, default=DEFAULT_TOLERANCE
    ): selector.NumberSelector(
        selector.NumberSelectorConfig(
            min=-50,
            max=50,
            step=0.5,
            unit_of_measurement=PERCENTAGE,
            mode=selector.NumberSelectorMode.BOX,
        )
    ),
    vol.Optional(CONF_MIN_DUR): selector.DurationSelector(
        selector.DurationSelectorConfig(allow_negative=False)
    ),
    vol.Optional(
        CONF_ADJUSTMENT_RATE, default=DEFAULT_ADJUSTMENT_RATE
    ): selector.NumberSelector(
        selector.NumberSelectorConfig(
            min=0,
            max=50,  # Set a reasonable max value (% per hour)
            step=0.1,
            unit_of_measurement="% per hour",
            mode=selector.NumberSelectorMode.BOX,
        )
    ),
    vol.Optional(
        CONF_BOOST_DURATION, default=DEFAULT_BOOST_DURATION
    ): selector.NumberSelector(
        selector.NumberSelectorConfig(
            min=1,
            max=3600,
            step=1,
            unit_of_measurement="seconds",
            mode=selector.NumberSelectorMode.BOX,
        )
    ),
}

CONFIG_SCHEMA = {
    vol.Required(CONF_NAME): selector.TextSelector(),
    **OPTIONS_SCHEMA,
}


CONFIG_FLOW = {
    "user": SchemaFlowFormStep(vol.Schema(CONFIG_SCHEMA)),
}

OPTIONS_FLOW = {
    "init": SchemaFlowFormStep(vol.Schema(OPTIONS_SCHEMA)),
}


class ConfigFlowHandler(SchemaConfigFlowHandler, domain=DOMAIN):
    """Handle a config or options flow."""

    config_flow = CONFIG_FLOW
    options_flow = OPTIONS_FLOW

    def async_config_entry_title(self, options: Mapping[str, Any]) -> str:
        """Return config entry title."""
        return cast(str, options["name"])
