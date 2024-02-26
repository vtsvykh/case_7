'''
Case 7: Simulate gas station.
Group:
Fischukova Sofia
Tsvykh Vika
'''


def read_gas_data(file_gas_data):
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
    input_data = []
    time_list = []
    with open(file_input_data, 'r', encoding='utf-8') as file:
        for line in file:
            data = line.split()
            time_1 = data[0]
            hrs, m = data[0].split(':')
            time = int(hrs) * 60 + int(m)
            litres = int(data[1])
            fuel_type = data[2]
            time_list.append(time_1)
            input_data.append((time, litres, fuel_type))
    return input_data


fuel_price = {'АИ-80': 43, 'АИ-92': 47, 'АИ-95': 50, 'АИ-98': 65}


def time_pump(input_data):
    time_list = []
    for i in range(len(input_data)):
        litres = input_data[i][1]
        t = litres // 10
        if litres % 10 != 0:
            t += 1
        time_list.append(t)
    return time_list


def situation(gas_data, input_data, time_list):
    for t in range(1, 1441):
        for i in range(len(input_data)):
            time = input_data[i][0]
            litres = input_data[i][1]
            fuel_type = input_data[i][2]
            if t == time:
                time_list[t + 1]

            for j in range(1, len(gas_data) + 1):
                if fuel_type in gas_data[j]['fuel_types']:
                    if len(gas_data[j]['queue']) < gas_data[j]['max_queue']:
                        print(f'Во время пришел заказ на {litres} {fuel_type} бензина ')
                        gas_data[j]['queue'].append((time, litres, fuel_type))
