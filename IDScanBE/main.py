import cv2

import DetectMRZ
import FaceRecognition
import ImageOrientation
from PersonalInformation import PersonalInformation



# rotatedImage=ImageOrientation.rotateImg(img)
image_path = "D:\Bia\College\Licenta\CI_DataSet\IDcard\WhatsApp Image 2023-03-28 at 15.07.30.jpeg"
# image_path='D:\Bia\College\Licenta\Buletine\WhatsApp Image 2023-03-28 at 15.07.27.jpeg'
# image_path='D:\Bia\College\Licenta\Buletine\WhatsApp Image 2023-03-24 at 11.50.07.jpeg'
# image_path='D:\Bia\College\Licenta\CI_Pictures_Costin\RK756289_White.jpg'
# image_path='D:\Bia\College\Licenta\CI_Pictures_Costin\SB335115_White.jpg'

image = cv2.imread(image_path)

personal_information = FaceRecognition.getInfoFromCI(image)

print("O IESIT DIN FaceRecognition.getInfoFromCI(image)")

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
        # mrz="",
        mrz=DetectMRZ.detectMRZ("rotatedImage.jpg"),
        id=id
    )

print("SFARSIT")
print(Person1)