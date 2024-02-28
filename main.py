import math
import random
import ru_local as ru
import matplotlib.pyplot




def read_gas_data(file_gas_data):
    """
    The function collects data about gas stations from an incoming file in the dictionary
    :param file_gas_data: file with information about gas stations
    :return: dictionary with information about all gas stations
    """
    gas_data = {}
    with open(file_gas_data, 'r', encoding='utf-8') as file:
        for line in file:
            data = line.strip().split()
            num_pump = int(data[0])
            gas_data[num_pump] = {
                'max_queue': int(data[1]),
                'fuel_types': data[2:],
                'queue': []
            }
    return gas_data


def read_input_data(file_input_data):
    """
    The function collects data about customer visits from an incoming file in the list.
    :param file_input_data: file with information about customer visits
    :return: list with information about all customer visits
    """
    input_data = []
    with open(file_input_data, 'r', encoding='utf-8') as file:
        for line in file:
            data = line.strip().split()
            hrs, minutes = data[0].split(':')
            time = int(hrs) * 60 + int(minutes)
            client_data = {
                'time': time,
                'litres': int(data[1]),
                'fuel_type': data[2],
                'time_watch': data[0]
            }

            input_data.append(client_data)

    return input_data


def format_time(time):
    """
    The function converts the number to a time format (hh:mm).
    :param time: time in numerical terms
    :return: time in time format
    """
    hrs = time // 60
    minutes = time - hrs * 60

    if hrs == 0:
        hrs = '00'
    elif 1 <= hrs <= 9:
        hrs = '0' + str(hrs)
    else:
        hrs = str(hrs)

    if minutes == 0:
        minutes = '00'
    elif 1 <= minutes <= 9:
        minutes = '0' + str(minutes)
    else:
        minutes = str(minutes)
    convert_time = hrs + ':' + minutes

    return convert_time


def simulate(gas_data, input_data):
    """
    The function simulates a model of an autorouting station.
    :param gas_data: Dictionary with information about all gas stations.
    :param input_data: List with information about all customer visits.
    :return: sales: dictionary with data on fuel sold (in liters)
             sales_lost: dictionary with data on lost fuel (in liters)
             revenue: a dictionary with data on revenue received
             revenue_lost: dictionary with data on lost revenue
             clients_lost: number of missed customers
    """
    fuel_price = {
        'АИ-80': 43,
        'АИ-92': 47,
        'АИ-95': 50,
        'АИ-98': 65
    }
    sales = {fuel_type: 0 for fuel_type in ['АИ-80', 'АИ-92', 'АИ-95', 'АИ-98']}
    revenue = {fuel_type: 0 for fuel_type in ['АИ-80', 'АИ-92', 'АИ-95', 'АИ-98']}
    sales_lost = {fuel_type: 0 for fuel_type in ['АИ-80', 'АИ-92', 'АИ-95', 'АИ-98']}
    revenue_lost = {fuel_type: 0 for fuel_type in ['АИ-80', 'АИ-92', 'АИ-95', 'АИ-98']}
    clients_lost = 0
    refuel_time = 0

    for time in range(1, 1441):
        for client in input_data:
            for gas_station in gas_data:
                time_queue_client = gas_data[gas_station]['queue']
                if time_queue_client:
                    if time == min(time_queue_client) and gas_data[gas_station]['queue']:
                        print(f"\n{format_time(refuel_time)} - {ru.end_refueling}")

                        gas_data[gas_station]['queue'].pop(0)

                        for gas_station, data in gas_data.items():
                            print(f"{ru.gas_station}{gas_station} : {'🚗' * len(data['queue'])}")

            if client['time'] == time:
                available_gas_station = [gas_station for gas_station, data in gas_data.items() if
                                         client['fuel_type'] in data['fuel_types']]
                selected_pump = min(available_gas_station, key=lambda gas_station: len(gas_data[gas_station]['queue']))
                service_time = math.ceil(client['litres'] / 10)

                add_time = random.randint(-1, 1)
                if service_time + add_time == 0:
                    add_time = random.randint(0, 1)

                refuel_time = time + service_time + add_time
                print(
                    f"\n{client['time_watch']} - {ru.new_client}: {client['litres']} {ru.litres} {client['fuel_type']} "
                    f"{ru.during} {service_time + add_time} {ru.minutes}.")

                if selected_pump:
                    if refuel_time <= 1440:
                        gas_data[selected_pump]['queue'].append(int(client['time']) + service_time)
                        print(f"{client['time_watch']} - {ru.took_turn} {selected_pump}")

                        sales[client['fuel_type']] += client['litres']
                        revenue[client['fuel_type']] += client['litres'] * fuel_price[client['fuel_type']]

                        for gas_station, data in gas_data.items():
                            print(f"{ru.gas_station}{gas_station} : {'🚗' * len(data['queue'])}")

                    else:
                        print(f"{client['time_watch']} - {ru.fail_refueling}")
                        clients_lost += 1
                        sales_lost[client['fuel_type']] += client['litres']
                        revenue_lost[client['fuel_type']] += client['litres'] * fuel_price[client['fuel_type']]

                else:
                    print(f"{client['time_watch']} - {ru.fail_refueling}")
                    clients_lost += 1
                    sales_lost[client['fuel_type']] += client['litres']
                    revenue_lost[client['fuel_type']] += client['litres'] * fuel_price[client['fuel_type']]

    return sales, sales_lost, revenue, revenue_lost, clients_lost


def result(sales, sales_lost, revenue, revenue_lost, clients_lost):
    """
    The function calculates and print the results of the day of the gas station.
    :param sales: dictionary with data on fuel sold (in liters)
    :param sales_lost: dictionary with data on lost fuel (in liters)
    :param revenue: a dictionary with data on revenue received
    :param revenue_lost: dictionary with data on lost revenue
    :param clients_lost: number of missed customers
    :return:
    """
    print(ru.result)

    print(f"\n{ru.sold_gasoline_litres}:")
    for fuel_type, litres in sales.items():
        print(f"{fuel_type}: {litres} {ru.litres}.")

    print(f"\n{ru.sold_gasoline_curn}:")
    income = 0
    for fuel_type, sales in revenue.items():
        income += sales
        print(f"{fuel_type}: {sales} {ru.currency}")
    print(f"\n{ru.income}: {income} {ru.currency}")

    print(f"\n{ru.clients_lost}: {clients_lost}")

    print(f"\n{ru.sold_gasoline_litres_lost}:")
    for fuel_type, litres in sales_lost.items():
        print(f"{fuel_type}: {litres} {ru.litres}.")

    print(f"\n{ru.sold_gasoline_curn_lost}:")
    income_lost = 0
    for fuel_type, sales in revenue_lost.items():
        income += sales
        print(f"{fuel_type}: {sales} {ru.currency}")
    print(f"\n{ru.income_lost}: {income_lost} {ru.currency}")


def main():
    """
    Main function.
    :return:
    """
    file_input_data = 'input_data.txt'
    file_gas_data = 'gas_data.txt'
    gas_data = read_gas_data(file_gas_data)
    input_data = read_input_data(file_input_data)
    sales, sales_lost, revenue, revenue_lost, clients_lost = simulate(gas_data, input_data)
    result(sales, sales_lost, revenue, revenue_lost, clients_lost)
    matplotlib.pyplot.bar(sales.keys(), sales.values())
    matplotlib.pyplot.show()
if __name__ == '__main__':
    main()
