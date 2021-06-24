import cv2
import numpy as np
import os
import shutil


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


def get_images():
    XBOX_FRONT = {'name': "xbx_front.jpg", 'res': (1350, 759)}
    XBOX_TOP = {'name': "xbx_top.jpg", 'res': (1350, 759)}
    PATH = os.path.join(os.getcwd(), 'resources')

    img1 = cv2.imread(os.path.join(PATH, XBOX_FRONT.get('name')), 0)
    img2 = cv2.imread(os.path.join(PATH, XBOX_TOP.get('name')), 0)
    combined = np.concatenate((img1, img2), axis=1)

    return combined


def put_text(image, text: list, controller: str):
    i = image
    cv2.putText(i, controller.capitalize(), (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 255), 3, cv2.LINE_AA)
    for val in text:
        cv2.putText(i, val[1], btn_locations.get(val[0]), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 2, cv2.LINE_AA)

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


def read_from_file(name: str):
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


if __name__ == '__main__':
    NAME = "TitanMain"

    debug = False
    for f in os.listdir(os.path.join(os.getcwd(), 'control_maps')):
        if f.endswith('.txt'):
            f_robot, f_name, f_driver, f_operator = read_from_file(f.replace('.txt', ''))

            res_image_d = get_images()
            res_image_o = get_images()
            res_image_d = put_text(res_image_d, f_driver, 'driver')
            res_image_o = put_text(res_image_o, f_operator, 'operator')

            if debug:
                disp(res_image_o)
                disp(res_image_d)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
            else:
                save((res_image_d, res_image_o), f_robot, f_name)
