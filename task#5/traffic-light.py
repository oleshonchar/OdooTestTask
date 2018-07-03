import time
import sys
from threading import Thread


car_traffic_light_list = []
pedestrian_traffic_light_list = []
relationship_dict = {}


class TraficLight(object):
    # day/night mode can be changed for all
    mode = 'day'

    def __init__(self, id, type, red_state_time=30, green_state_time=60, red_state_time_night=30, green_state_time_night=120):
        """
        Initial data

        id = integerf ield
        __type = ('car' / 'pedestrian')
        red_state_time = integer field (time for red light for day mode)
        green_state_time_night = integer field (time for green light for day mode)
        red_state_time_night = integer field (time for red light for night mode)
        green_state_time_night = integer field (time for green light for night mode)
        red = default False
        green = default True
        automode = default True
        """
        self.id = id
        self.__type = type
        self.ticker = 0
        self.red_state_time = red_state_time
        self.green_state_time = green_state_time
        self.red_state_time_night = red_state_time_night
        self.green_state_time_night = green_state_time_night
        self.red = False
        self.green = True
        self.automode = True

    def start(self):
        if self.mode == 'day':
            while self.automode:
                self.green = True
                self.red = False
                relationship_dict[self].green = False
                relationship_dict[self].red = True
                self.timer(self.green_state_time)
                self.green = False
                self.red = True
                relationship_dict[self].green = True
                relationship_dict[self].red = False
                self.timer(self.red_state_time)
        elif self.mode == 'night':
            while self.automode:
                self.green = True
                self.red = False
                relationship_dict[self].green = False
                relationship_dict[self].red = True
                self.timer(self.green_state_time_night)
                self.green = False
                self.red = True
                relationship_dict[self].green = True
                relationship_dict[self].red = False
                self.timer(self.red_state_time_night)

    def timer(self, second):
        t = time.time()
        while second:
            if time.time() - t >= 1.0:
                self.ticker = second
                t = time.time()
                second -= 1


def add_trafic_light(id, type):
    if type == 'car':
        lighter = TraficLight(id, type)
        car_traffic_light_list.append(lighter)
    elif type == 'pedestrian':
        lighter = TraficLight(id, type)
        pedestrian_traffic_light_list.append(lighter)
    else:
        print('This type is not available')
    create_relationship()


def remove_traffic_light(id, type):
    if type == 'car':
        for i in car_traffic_light_list:
            if i.id == id:
                car_traffic_light_list.remove(i)
    elif type == 'pedestrian':
        for i in pedestrian_traffic_light_list:
            if i.id == id:
                pedestrian_traffic_light_list.remove(i)
    else:
        print('This type is not available')
    create_relationship()


def start_all():
    for i in car_traffic_light_list:
        car = Thread(target=i.start)
        car.start()


def create_relationship():
    for c in car_traffic_light_list:
        for p in pedestrian_traffic_light_list:
            if c.id == p.id:
                relationship_dict[c] = p
            else:
                continue


def menu():
    print(
            """
            [1] Добавить светофор
            [2] Убрать светофор
            [3] Все светофоры
            [4] Изменить режим работы (день/ночь)
            [5] Запустить светофоры
            
            [0] Выход
            """
    )
    print('Для выбора пункта меню нужно ввести цифру')
    enter = input('Введите соответствующую цифру: ')
    if enter == '1':
        print('\nДобавление светофороа')
        id = input('Введите номер-идентификатор светофора: ')
        type = input('Введите тип светофора (пешеходный/автомобильный): ')
        if type == 'пешеходный':
            add_trafic_light(int(id), type='pedestrian')
            print('\n УСПЕХ! Светофор добавлен')
        elif type == 'автомобильный':
            add_trafic_light(int(id), type='car')
            print('\n УСПЕХ! Светофор добавлен')
        else:
            print('ОШИБКА! Некорректный ввод типа')
        menu()
    if enter == '2':
        print('\nУдаление светофороа')
        id = input('Введите номер-идентификатор светофора: ')
        type = input('Введите тип светофора (пешеходный/автомобильный): ')
        if type == 'пешеходный':
            remove_traffic_light(int(id), type='pedestrian')
            print('\n УСПЕХ! Светофор удален')
        elif type == 'автомобильный':
            remove_traffic_light(int(id), type='car')
            print('\n УСПЕХ! Светофор удален')
        else:
            print('ОШИБКА! Некорректный ввод типа')
        menu()
    if enter == '3':
        print(
            """
            [1] Пешеходные светофоры
            [2] Автомобильные светофоры
            
            [0] Меню
            """
        )
        enter_type = input('Введите соответствующую цифру: ')
        if enter_type == '1':
            for i in pedestrian_traffic_light_list:
                print('[{}] Светофор'.format(i.id))
        elif enter_type == '2':
            for i in car_traffic_light_list:
                print('[{}] Светофор'.format(i.id))
        elif enter_type == '0':
            menu()
        else:
            print('ОШИБКА! Некорректный ввод')
        print('\n[0] Меню')

        print('\n Чтобы перейти к управлению светофором введите его id')
        id = input('ID: ')
        print('\n Светофор [{}]'.format(id))
        if enter_type == '1':
            list = pedestrian_traffic_light_list
        elif enter_type == '2':
            list = car_traffic_light_list

        for i in list:
            if i.id == int(id):
                mode = str(TraficLight.mode)
                red_or_green = ('Зеленый' if i.green else 'Красный')
                if list == pedestrian_traffic_light_list:
                    for k, v in relationship_dict.items():
                        if v == i:
                            time = k.ticker
                else:
                    time = i.ticker

        print(
            """
            Режим: {}
            Состояние: {}
            К следующему состоянию осталось: {}
            
            [1] Ручное управление

            [0] Меню
            """.format(mode, red_or_green, time)
        )
        enter = input('\nВыберите пунт меню: ')
        if enter == '1':
            print(
                """
                \nРучное управление светофором [{}]
                
                [1] Красный свет
                [2] Зеленый свет
                
                [0] Меню
                """.format(id)
            )
            enter = input('\nВыберите пунт меню: ')
            if enter == '1':
                for i in list:
                    if i.id == int(id):
                        i.red = True
                        i.green = False
                        i.automode = False
            elif enter == '2':
                for i in list:
                    if i.id == int(id):
                        i.red = False
                        i.green = True
                        i.automode = False
            elif enter == '0':
                menu()
            else:
                print('ОШИБКА! Некорректный ввод')
            menu()
        elif enter == '0':
            menu()
    if enter == '4':
        print('\nВыбор режима работы')
        print(
            """
            [1] Дневной режим
            [2] Ночной режим
            
            [0] Меню
            """
        )
        enter = input('Введите номер режима: ')
        if enter == '1':
            TraficLight.mode = 'day'
            print('\n УСПЕХ! Установелен дневной режим')
        elif enter == '2':
            TraficLight.mode = 'night'
            print('\n УСПЕХ! Установелен ночной режим')
        else:
            print('ОШИБКА! Некорректный ввод')
        menu()
    if enter == '5':
        print('\n УСПЕХ! Светофоры запущены')
        start_all()
        menu()
    if enter == '0':
        sys.exit()


if __name__ == "__main__":
    add_trafic_light(176, 'car')
    add_trafic_light(178, 'car')
    add_trafic_light(176, 'pedestrian')
    add_trafic_light(178, 'pedestrian')

    create_relationship()
    menu()
