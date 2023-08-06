import json
from ..utils.mqtt import MqttTopic
from ..interfaces import database
from ..utils import datetime, data_formatter, config, bluetooth

today_production = 0
today_independence = 0


def send_summary(client, update=False):
    global today_independence, today_production

    payload = {
        "solar_production": database.get_sensor_data(
            measurement=config.homesolar_config['DATA']['solar_production_measurement'],
            field=config.homesolar_config['DATA']['solar_production_field']
        ), "battery_usage": database.get_sensor_data(
            measurement=config.homesolar_config['DATA']['battery_power_measurement'],
            field=config.homesolar_config['DATA']['battery_power_field']
        ), "battery_charge": database.get_sensor_data(
            measurement=config.homesolar_config['DATA']['battery_charge_measurement'],
            field=config.homesolar_config['DATA']['battery_charge_field']
        ), "grid_usage": database.get_sensor_data(
            measurement=config.homesolar_config['DATA']['grid_power_measurement'],
            field=config.homesolar_config['DATA']['grid_power_field']
        ), "inverter_usage": database.get_sensor_data(
            measurement=config.homesolar_config['DATA']['inverter_power_measurement'],
            field=config.homesolar_config['DATA']['inverter_power_field']
        )}

    if payload["grid_usage"] is None or payload["inverter_usage"] is None:
        payload["home_usage"] = None
    else:
        payload["home_usage"] = payload["grid_usage"] + payload["inverter_usage"]

    if update:
        payload["today_production"] = today_production = \
            data_formatter.get_sum_from_serialized_data(
                database.get_solar_production(date=datetime.get_today(), timescale="DAY")
            )
        grid = data_formatter.get_sum_from_serialized_data(
            database.get_grid_usage(date=datetime.get_today(), timescale="DAY")
        )
        inverter = data_formatter.get_sum_from_serialized_data(
            database.get_inverter_usage(date=datetime.get_today(), timescale="DAY")
        )
        payload["today_independence"] = today_independence = (inverter / (grid + inverter)) * 100.0
    else:
        payload["today_production"] = today_production
        payload["today_independence"] = today_independence

    client.publish(MqttTopic.SUMMARY, json.dumps(payload), retain=True)


def send_battery(client):
    payload = {
        "status": database.get_sensor_data(
            measurement=config.homesolar_config['DATA']['battery_status_measurement'],
            field=config.homesolar_config['DATA']['battery_status_field']
        ), "pack_voltage": database.get_sensor_data(
            measurement=config.homesolar_config['DATA']['battery_voltage_measurement'],
            field=config.homesolar_config['DATA']['battery_voltage_field']
        ), "pack_amperage": database.get_sensor_data(
            measurement=config.homesolar_config['DATA']['battery_amperage_measurement'],
            field=config.homesolar_config['DATA']['battery_amperage_field']
        ), "pack_power": database.get_sensor_data(
            measurement=config.homesolar_config['DATA']['battery_power_measurement'],
            field=config.homesolar_config['DATA']['battery_power_field']
        ), "soc": database.get_sensor_data(
            measurement=config.homesolar_config['DATA']['battery_charge_measurement'],
            field=config.homesolar_config['DATA']['battery_charge_field']
        )}

    if payload["status"] is not None:
        payload["status"] = bluetooth.MOSFET_Discharge_St[payload["status"]]

    single_cell = config.homesolar_config['DATA']['battery_single_cell']
    formatted_cells = []

    cells = config.homesolar_config['DATA']['battery_cells_fields'].split()
    balances = config.homesolar_config['DATA']['battery_cells_balance_fields'].split()
    if not single_cell:
        for index, cell in enumerate(cells):
            formatted_cell = {
                "name": f"Cell {index}",
                "balance": database.get_sensor_data(
                    measurement=config.homesolar_config['DATA']['battery_cells_balance_measurement'],
                    field=balances[index]
                ) == 1,
                "voltage": database.get_sensor_data(
                    measurement=config.homesolar_config['DATA']['battery_cells_measurement'],
                    field=cells[index]
                )
            }
            formatted_cells.append(formatted_cell)

    payload["cells"] = formatted_cells

    client.publish(MqttTopic.BATTERY, json.dumps(payload), retain=True)
