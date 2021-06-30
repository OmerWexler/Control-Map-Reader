import cv2
import numpy as np
import os
import shutil
import configparser

DEFAULT_CONFIG_PATH = os.path.join(os.getcwd(), 'config.ini')
OVERRIDE_CONFIG_PATH = r"E:\Desktop\workspace\software\java operation parser\Control-Map-Reader\config.ini"

btn_locations = {
    'A': (910, 355),
    'B': (985, 295),
    'X': (790, 175),
    'Y': (890, 115),
    'D_UP': (495, 300),
    'D_DOWN': (495, 490),
    'D_LEFT': (350, 390),
    'D_RIGHT': (620, 390),
    'RT': (1600, 350),
    'LT': (2300, 350),
    'RB': (1700, 200),
    'LB': (2200, 200),
    'START': (700, 185),
    'BACK': (550, 185),
    'LS': (395, 140),
    'RS': (765, 470),
    'LSB': (390, 230),
    'RSB': (765, 380)
}


def get_images(front_path, top_path):
    img1 = cv2.imread(front_path, 0)
    img2 = cv2.imread(top_path, 0)
    combined = np.concatenate((img1, img2), axis=1)

    return combined


def put_text(location_map: dict, image, label_map, controller: str):
    i = image
    cv2.putText(i, controller.capitalize(), (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 255), 3, cv2.LINE_AA)
    for key in label_map:
        cv2.putText(i, label_map[key], location_map[key], cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 2, cv2.LINE_AA)

    return i


def disp(image):
    cv2.imshow('View', image)


def save(image: tuple, robot, name):
    d = os.path.join(os.getcwd(), 'map_views', robot)
    try:
        os.mkdir(d)
    except FileExistsError:
        pass

    d = os.path.join(d, name)
    if os.path.isdir(d):
        shutil.rmtree(d)

    os.mkdir(d)

    cv2.imwrite(os.path.join(d, 'driver' + '.jpg'), image[0])
    cv2.imwrite(os.path.join(d, 'operator' + '.jpg'), image[1])


def read_map(name: str):
    PATH = os.path.join(os.getcwd(), 'control_maps', name + ".txt")

    driver = []
    operator = []
    name = ""
    robot = ""

    counter = 0
    with open(PATH, 'r') as source_file:
        for line in source_file.readlines():
            counter += 1

            if counter == 1:
                name = line.replace("Name= ", '').rstrip()

            elif counter == 2:
                robot = line.replace("Robot= ", '').rstrip()

            elif line.replace(' ', '') == '':
                continue

            else:
                index = line.find(":")
                if index != -1:
                    btn = line[: index]
                    action = line[index:].rstrip().replace(':', '').replace(' ', '')
                    if counter < 23:  # Driver
                        driver.append([btn, action])

                    else:  # Operator
                        operator.append([btn, action])
    return robot, name, driver, operator


def parse_config(config_path):
    if not os.path.exists(config_path):
        return None
    
    config = configparser.ConfigParser()
    config.read(config_path)
    return config


def find_path(path):
    if os.path.exists(path):
        return path
    
    if os.path.exists(os.path.join(os.getcwd(), path)):
        return path

    return None


def parse_label_map(config):
    label_map = {}
    for key in config[type]:
        label_map[key] = config[type][key]


if __name__ == '__main__':
    if OVERRIDE_CONFIG_PATH != None:
        config = parse_config(find_path(OVERRIDE_CONFIG_PATH))
    else:
        config = parse_config(find_path(DEFAULT_CONFIG_PATH))

    debug = False
    for map in config['sources']['maps'].split(','):
        p_map = parse_config(map)
        
        controller_front = find_path(config['sources']['controller_front'])
        controller_top = find_path(config['sources']['controller_top'])

        res_image_d = get_images(controller_front, controller_top)
        res_image_o = get_images(controller_front, controller_top)

        res_image_d = put_text(config['buttons'], res_image_d, p_map['driver'], 'driver')
        res_image_o = put_text(config['buttons'], res_image_o, p_map['operator'], 'operator')

        if debug:
            disp(res_image_o)
            disp(res_image_d)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        else:
            save((res_image_d, res_image_o), p_map['general']['robot'], p_map['general']['name'])
