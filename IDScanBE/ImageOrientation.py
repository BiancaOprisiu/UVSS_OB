# Image orientation correction based on text orientation

import cv2
import numpy as np
from matplotlib import pyplot as plt

debug = True

# Display image
def display(img, frameName="OpenCV Image"):
    if not debug:
        return
    h, w = img.shape[0:2]
    neww = 800
    newh = int(neww * (h / w))
    img = cv2.resize(img, (neww, newh))
    # cv2.imshow(frameName, img)
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))


# rotate the image with given theta value
def rotate(img, theta):
    rows, cols = img.shape[0], img.shape[1]
    image_center = (cols / 2, rows / 2)

    M = cv2.getRotationMatrix2D(image_center, theta, 1)

    abs_cos = abs(M[0, 0])
    abs_sin = abs(M[0, 1])

    bound_w = int(rows * abs_sin + cols * abs_cos)
    bound_h = int(rows * abs_cos + cols * abs_sin)

    M[0, 2] += bound_w / 2 - image_center[0]
    M[1, 2] += bound_h / 2 - image_center[1]

    # rotate orignal image to show transformation
    rotated = cv2.warpAffine(img, M, (bound_w, bound_h), borderValue=(255, 255, 255))
    return rotated


def slope(x1, y1, x2, y2):
    if x1 == x2:
        return 0
    slope = (y2 - y1) / (x2 - x1)
    theta = np.rad2deg(np.arctan(slope))
    return theta


def rotateImg(filePath, img_original):
    img = cv2.imread(filePath)
    textImg = img.copy()

    small = cv2.cvtColor(textImg, cv2.COLOR_BGR2GRAY)

    # find the gradient map
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    grad = cv2.morphologyEx(small, cv2.MORPH_GRADIENT, kernel)

    # display(grad)

    # Binarize the gradient image
    _, bw = cv2.threshold(grad, 0.0, 255.0, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    # display(bw)

    # connect horizontally oriented regions
    # kernal value (9,1) can be changed to improved the text detection
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 1))
    connected = cv2.morphologyEx(bw, cv2.MORPH_CLOSE, kernel)
    # display(connected)

    # using RETR_EXTERNAL instead of RETR_CCOMP
    # _ , contours, hierarchy = cv2.findContours(connected.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    contours, hierarchy = cv2.findContours(connected.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)  # opencv >= 4.0

    mask = np.zeros(bw.shape, dtype=np.uint8)
    # display(mask)
    # cumulative theta value
    cummTheta = 0
    # number of detected text regions
    ct = 0
    for idx in range(len(contours)):
        x, y, w, h = cv2.boundingRect(contours[idx])
        mask[y:y + h, x:x + w] = 0
        # fill the contour
        cv2.drawContours(mask, contours, idx, (255, 255, 255), -1)
        # display(mask)
        # ratio of non-zero pixels in the filled region
        r = float(cv2.countNonZero(mask[y:y + h, x:x + w])) / (w * h)

        # assume at least 45% of the area is filled if it contains text
        if r > 0.45 and w > 8 and h > 8:
            # cv2.rectangle(textImg, (x1, y), (x+w-1, y+h-1), (0, 255, 0), 2)

            rect = cv2.minAreaRect(contours[idx])
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            cv2.drawContours(textImg, [box], 0, (0, 0, 255), 2)

            # we can filter theta as outlier based on other theta values
            # this will help in excluding the rare text region with different orientation from ususla value
            theta = slope(box[0][0], box[0][1], box[1][0], box[1][1])
            cummTheta += theta
            ct += 1
            # print("Theta", theta)

    # find the average of all cumulative theta value
    orientation = cummTheta / ct
    print("Image orientation in degress: ", orientation)
    finalImage = rotate(img_original, orientation)
    display(textImg, "Detectd Text minimum bounding box")
    display(finalImage, "Rotated Image")
    return finalImage






import cv2
import numpy as np

# Rotates an image
def rotate_image(image: np.ndarray, angle: float) -> np.ndarray:
    mean_pixel = np.median(np.median(image, axis=0), axis=0)
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=mean_pixel)
    return result

# Returns a small value if the horizontal histogram is sharp.
# Returns a large value if the horizontal histogram is blurry.
def eval_image(image: np.ndarray) -> float:
    hist = np.sum(np.mean(image, axis=1), axis=1)
    bef = 0
    aft = 0
    err = 0.
    assert(hist.shape[0] > 0)
    for pos in range(hist.shape[0]):
        if pos == aft:
            bef = pos
            while aft + 1 < hist.shape[0] and abs(hist[aft + 1] - hist[pos]) >= abs(hist[aft] - hist[pos]):
                aft += 1
        err += min(abs(hist[bef] - hist[pos]), abs(hist[aft] - hist[pos]))
    assert(err > 0)
    return err

# Measures horizontal histogram sharpness across many angles
def sweep_angles(image: np.ndarray) -> np.ndarray:
    results = np.empty((81, 2))
    for i in range(81):
        angle = (i - results.shape[0] // 2) / 4.
        rotated = rotate_image(image, angle)
        err = eval_image(rotated)
        results[i, 0] = angle
        results[i, 1] = err
    return results

# Find an angle that is a lot better than its neighbors
def find_alignment_angle(image: np.ndarray) -> float:
    best_gain = 0
    best_angle = 0.
    results = sweep_angles(image)
    for i in range(2, results.shape[0] - 2):
        ave = np.mean(results[i-2:i+3, 1])
        gain = ave - results[i, 1]
        # print('angle=' + str(results[i, 0]) + ', gain=' + str(gain))
        if gain > best_gain:
            best_gain = gain
            best_angle = results[i, 0]
    return best_angle

# input: an image that needs aligning
# output: the aligned image
def align_image(image: np.ndarray) -> np.ndarray:
    angle = find_alignment_angle(image)
    return rotate_image(image, angle)