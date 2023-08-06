import asyncio
import json

from loguru import logger

# project's imports
from ..services import influxdb, sqlite
from ..utils import datetime, config, data_formatter
from ..utils import influxdb as influx_utils
from ..utils import sqlite as sqlite_utils
from ..utils.sqlite import SensorData


# Used on All database
async def write_sensor_data(data):
    sensor_data = data_formatter.format_sensor_data(data)
    await influxdb.write(sensor_data)
    await sqlite.write(sqlite_utils.generate_add_sensor_data_sql(sensor_data))
    logger.debug(json.dumps(sensor_data))


# Used only on InfluxDB
def get_battery_charge(date):
    flux = influx_utils.generate_flux(
        config.homesolar_config['DATA']['battery_charge_measurement'],
        config.homesolar_config['DATA']['battery_charge_field'],
        datetime.stringify_timestamp(date),
        datetime.get_next_day(date), "DAY"
    )
    result = asyncio.run(influxdb.query(flux))
    logger.debug(result)
    return influx_utils.serialize(result)


def get_battery_usage(date, timescale):
    start_time, stop_time = datetime.get_date_pair(date, timescale)
    flux = influx_utils.generate_flux(
        config.homesolar_config['DATA']['battery_power_measurement'],
        config.homesolar_config['DATA']['battery_power_field'],
        start_time,
        stop_time,
        timescale
    )
    result = asyncio.run(influxdb.query(flux))
    logger.debug(result)
    return influx_utils.serialize(result, timescale)


def get_solar_production(date, timescale):
    start_time, stop_time = datetime.get_date_pair(date, timescale)
    flux = influx_utils.generate_flux(
        config.homesolar_config['DATA']['solar_production_measurement'],
        config.homesolar_config['DATA']['solar_production_field'],
        start_time,
        stop_time,
        timescale
    )
    result = asyncio.run(influxdb.query(flux))
    logger.debug(result)
    return influx_utils.serialize(result, timescale)


def get_grid_usage(date, timescale):
    start_time, stop_time = datetime.get_date_pair(date, timescale)
    flux = influx_utils.generate_flux(
        config.homesolar_config['DATA']['grid_power_measurement'],
        config.homesolar_config['DATA']['grid_power_field'],
        start_time,
        stop_time,
        timescale
    )
    result = asyncio.run(influxdb.query(flux))
    logger.debug(result)
    return influx_utils.serialize(result, timescale)


def get_inverter_usage(date, timescale):
    start_time, stop_time = datetime.get_date_pair(date, timescale)
    flux = influx_utils.generate_flux(
        config.homesolar_config['DATA']['inverter_power_measurement'],
        config.homesolar_config['DATA']['inverter_power_field'],
        start_time,
        stop_time,
        timescale
    )
    result = asyncio.run(influxdb.query(flux))
    logger.debug(result)
    return influx_utils.serialize(result, timescale)


def get_home_usage(date, timescale):
    start_time, stop_time = datetime.get_date_pair(date, timescale)
    flux = influx_utils.generate_combined_tables_flux(
        [config.homesolar_config['DATA']['grid_power_measurement'],
         config.homesolar_config['DATA']['grid_power_field']],
        [config.homesolar_config['DATA']['inverter_power_measurement'],
         config.homesolar_config['DATA']['inverter_power_field']],
        start_time,
        stop_time,
        timescale
    )
    result = asyncio.run(influxdb.query(flux))
    logger.debug(result)
    return influx_utils.serialize(result, timescale)


# Used only on Sqlite
def get_sensor_data(measurement, field):
    sql = sqlite_utils.generate_get_sensor_data_sql(measurement, field)
    result = asyncio.run(sqlite.execute(sql))

    sensor_data: SensorData = result.scalar()
    if sensor_data is None:
        logger.warning("No sensor data with specified name found")
        return None
    else:
        return data_formatter.parse_to_float_if_possible(sensor_data.value)
