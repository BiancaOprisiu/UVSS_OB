import cv2
from matplotlib import pyplot as plt
import easyocr
from PIL import Image
import re

import DetectMRZ
import ImageOrientation
from PersonalInformation import PersonalInformation
# import Validations

# X, Y, W, H = 0, 10, 20, 30
def is_face_inside(face1, face2):
    xa, ya, wa, ha = face1
    xb, yb, wb, hb = face2

    if xb <= xa and yb <= ya and xb + wb >= xa + wa and yb + hb >= ya + ha:
        return True
    else:
        return False


def get_cropped_picture(input_path, output_path, x1, y1, x2, y2):
    img = Image.open(input_path)
    img_res = img.crop((x1, y1, x2, y2))
    img_res.save(output_path)
    return output_path


def perform_ocr_and_save_results(input_image_path, output_file_path, x1, y1, x2, y2):
    cropped_image_path = get_cropped_picture(input_image_path, 'ImgCrop.jpeg', x1, y1, x2, y2)
    cropped_image = cv2.imread(cropped_image_path, cv2.IMREAD_GRAYSCALE)

    reader = easyocr.Reader(['en'])
    result = reader.readtext(cropped_image)

    with open(output_file_path, 'w') as file:
        pass

    with open(output_file_path, 'a') as file:
        for entry in result:
            bounding_box = entry[0]
            if (output_file_path == 'ocr_results_validation.txt'):
                text = entry[1].replace(" ", "")
            else:
                text = entry[1]
            confidence = entry[2]

            file.write(f"Bounding Box: {bounding_box}, Text: {text}, Confidence: {confidence}\n")

    print(result)


def perform_ocr_and_save_results_only_text(input_image_path, output_file_path, x1, y1, x2, y2):
    cropped_image_path = get_cropped_picture(input_image_path, 'ImgCrop.jpeg', x1, y1, x2, y2)
    cropped_image = cv2.imread(cropped_image_path, cv2.IMREAD_GRAYSCALE)

    reader = easyocr.Reader(['en'])
    result = reader.readtext(cropped_image)

    with open(output_file_path, 'w') as file:
        pass

    with open(output_file_path, 'a') as file:
        for entry in result:
            if (
                    output_file_path == 'ocr_results_validation.txt' or output_file_path == 'ocr_results_validation_text.txt'):
                text = entry[1].replace(" ", "")
            else:
                text = entry[1]

            file.write(text + '\n')

    print(result)


def detectFaces(img):
    face_cascade = cv2.CascadeClassifier('venv/Lib/site-packages/cv2/data/haarcascade_frontalface_default.xml')

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    output_path = 'gray_image.jpg'
    cv2.imwrite(output_path, gray)

    #Detect faces
    faces = face_cascade.detectMultiScale(gray, 1.5, 4)

    #Border around faces
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)

    print("Number of faces detected:", len(faces))


    #Get faces coordinates
    for i, (x, y, w, h) in enumerate(faces, 1):
        print(f"Face {i}: x={x}, y={y}, width={w}, height={h}")
        if i == 1:
            x1 = x
            y1 = y
            w1 = w
            h1 = h
        if i == 2:
            x2 = x
            y2 = y
            w2 = w
            h2 = h

    face1 = (x1, y1, w1, h1)
    face2 = (x2, y2, w2, h2)

    #Check which face is more on the left and use that one for refference
    if is_face_inside(face1, face2):
        print("Face 1 is inside Face 2")
        X, Y, W, H = face1
    elif is_face_inside(face2, face1):
        print("Face 2 is inside Face 1")
        X, Y, W, H = face2
    else:
        if x1 < x2:
            print("Face 1 is more on the left")
            X, Y, W, H = face1
        else:
            print("Face 2 is more on the left")
            X, Y, W, H = face2

    #TODO: gaseste o formula mai buna sau scapa de formula
    #imparte in cele 3+1 cadrane imaginea
    # cv2.rectangle(img, (X + W + int(W * 0.25), Y - int(H * 0.5)), (X + int(5.25 * W), Y + int(2.23 * H)), (255, 0, 0), 3)
    # cv2.rectangle(img, (X - int(W * 0.25), Y + int(H * 2.15)), (X + int(5.25 * W), Y + int(3 * H)), (0, 0, 255), 3)
    # cv2.rectangle(img, (X - int(W * 0.5), Y - int(H)), (X + int(1.25 * W), Y - H + int(0.6 * H)), (255, 0, 255), 3)

    input_image_path = "gray_image.jpg"

    # output_file_path = 'ocr_results_roumanie_text.txt'
    # perform_ocr_and_save_results_only_text(input_image_path, output_file_path, X - int(W * 0.35), Y - int(H * 0.85),
    #                                        X + int(1.25 * W), Y - H + int(0.6 * H))
    #
    # output_file_path = 'ocr_results_validation_text.txt'
    # perform_ocr_and_save_results_only_text(input_image_path, output_file_path, X - int(W * 0.25), Y + int(H * 2.15),
    #                                        X + int(5.25 * W), Y + int(3 * H))

    output_file_path = 'ocr_results_CI_info_text.txt'
    get_cropped_picture(input_image_path, "InfoCrop.jpg", X + W + int(W * 0.25), Y - int(H * 0.5),
                        X + int(5.25 * W), Y + int(2.23 * H))

    rotatedImage = ImageOrientation.rotateImg("InfoCrop.jpg", img)
    cv2.imwrite("rotatedImage.jpg", rotatedImage)

    gray = cv2.cvtColor(rotatedImage, cv2.COLOR_BGR2GRAY)
    output_path = 'gray_image.jpg'
    cv2.imwrite(output_path, gray)

    perform_ocr_and_save_results_only_text(input_image_path, output_file_path, X + W + int(W * 0.25), Y - int(H * 0.5),
                                           X + int(5.25 * W), Y + int(2.23 * H))




def getInfoFromText(personal_information):

    output_file_path = 'ocr_results_CI_info_text.txt'

    with open(output_file_path, 'r') as file:
        lines = file.readlines()

    for i in range(len(lines) - 1):
        current_line = lines[i].strip()
        next_line = lines[i + 1].strip()

        if current_line.startswith("SERIA"):
            if len(current_line) >= 2 and current_line[-3] == ' ':
                personal_information['seria'] = current_line[-2:]
            else:
                personal_information['seria'] = next_line
        elif current_line == "NR":
            personal_information['nr'] = next_line
        elif current_line == "CNP":
            personal_information['cnp'] = next_line
        elif current_line.startswith("Nume"):
            if any(char.isdigit() for char in next_line):
                personal_information['last_name'] = lines[i + 2].strip()
            else:
                personal_information['last_name'] = next_line
        elif current_line.startswith("Pre"):
            personal_information['first_name'] = next_line
        elif current_line.startswith("Cet"):
            personal_information['nationality'] = lines[i + 2].strip()
        elif current_line == "F" or current_line == "M":
            personal_information['sex'] = current_line
        elif current_line.startswith("Loc"):
            if len(next_line) == 1:
                personal_information['place_of_birth'] = lines[i + 2].strip()
            else:
                personal_information['place_of_birth'] = next_line
        elif current_line.startswith("Dom"):
            personal_information['address'] = next_line + ' ' + lines[i + 2].strip()
        elif current_line.startswith("Emis"):
            if len(lines)-1+2 <= i+2:
                personal_information['issued_by'] = lines[i + 2].strip()
            else:
                # print("list index out of range -> nu s-a citit randul respectiv din poza")
                personal_information['issued_by'] = ''
        elif current_line.startswith("Val"):
            if len(lines)-1+2 <= i+2:
                personal_information['validity'] = lines[i + 2].strip()
            else:
                # print("list index out of range -> nu s-a citit randul respectiv din poza")
                personal_information['validity'] = ''


        if i == len(lines) - 2 and next_line.startswith("ap"):
            personal_information['address'] = personal_information['address'] + " " + next_line


def getInfoFromCI(img):
    # img = cv2.imread(image_path)
    img_path = "image0.jpeg"

    print("START DETECT FACES")
    detectFaces(img)
    print("END DETECT FACES")

    personal_information = {
        'seria': "",
        'nr': "",
        'cnp': "",
        'sex': "",
        'last_name': "",
        'first_name': "",
        'nationality': "",
        'place_of_birth': "",
        'address': "",
        'issued_by': "",
        'validity': ""
    }

    getInfoFromText(personal_information)


    validation_text = ""

    id = img_path

    Person1 = PersonalInformation(
        seria=personal_information['seria'],
        nr=personal_information['nr'],
        cnp=personal_information['cnp'],
        sex=personal_information['sex'],
        last_name=personal_information['last_name'],
        first_name=personal_information['first_name'],
        nationality=personal_information['nationality'],
        place_of_birth=personal_information['place_of_birth'],
        address=personal_information['address'],
        issued_by=personal_information['issued_by'],
        validity=personal_information['validity'],
        mrz=validation_text,
        id=id
    )

    print(Person1)

    personal_information['seria'] = Person1.get_seria()
    personal_information['nr'] = Person1.get_nr()
    personal_information['cnp'] = Person1.get_cnp()
    personal_information['sex'] = Person1.get_sex()
    personal_information['last_name'] = Person1.get_last_name()
    personal_information['first_name'] = Person1.get_first_name()
    personal_information['nationality'] = Person1.get_nationality()
    personal_information['place_of_birth'] = Person1.get_place_of_birth()
    personal_information['address'] = Person1.get_address()
    personal_information['issued_by'] = Person1.get_issued_by()
    personal_information['validity'] = Person1.get_validity()

    return personal_information