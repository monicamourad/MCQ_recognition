import cv2
import numpy as np
import math

kernel_cir1 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))


def rotate_image(img, angle):
    image_center = tuple(np.array(img.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv2.warpAffine(img, rot_mat, img.shape[1::-1], flags=cv2.INTER_LINEAR)
    return result


# read image, resize it, threshold and dilate it then uses connected component fn
# to get the x and y position of every circle
def get_circles(im, name):
    img = cv2.imread(im, 0)
    cv2.imshow('')
# code to detect horizontal lines in picture and if picture tilted send img to rotate_image to fix it
    img1 = cv2.resize(img, (556, 800))
    # img_r = img1
    img_r = cv2.bitwise_not(img1)
    img_edges = cv2.Canny(img_r, 100, 100, apertureSize=3)
    lines = cv2.HoughLinesP(img_edges, 1, math.pi / 180.0, 100, minLineLength=50, maxLineGap=5)
    angles = []
    for x1, y1, x2, y2 in lines[0]:
        angle = math.degrees(math.atan2(y2 - y1, x2 - x1))
        angles.append(angle)
    median_angle = np.median(angles)
    print(median_angle)
    img1 = rotate_image(img_r, median_angle)

    thresh = cv2.threshold(img1, 235, 255, cv2.THRESH_BINARY)[1]
    dil = cv2.dilate(thresh, kernel_cir1)
    output = cv2.connectedComponentsWithStats(dil, 4, cv2.CV_32S)
    print(output[0]-1)
    loop = output[2]
    loop2 = loop[1:23]
    answers = {}
    i = 0
    for c in loop2:
        # get answer corresponding to each circle identified
        print(c[0], c[1])
        answers[i] = question(c[0], c[1])
        i = i + 1
    # sending array of questions' answers of file
    write_in_file(answers, name + 'results.txt')


# specify answer of each circle
def question(x, y):
    if y < 323:
        z = "habal"
        if (457 < x) & (x < 467) & (y < 100) & (y > 90):
            z = "Female"
        if (412 < x) & (x < 422) & (y < 100) & (y > 90):
            z = "Male"
        if (176 < x) & (x < 186) & (y < 128) & (y > 118):
            z = "fall"
        if (260 < x) & (x < 280) & (y < 128) & (y > 118):
            z = "spring"
        if (355 < x) & (x < 365) & (y < 128) & (y > 118):
            z = "summer"
        if (142 < x) & (x < 152) & (y < 156) & (y > 146):
            z = "MCTA"
        if (187 < x) & (x < 197) & (y < 156) & (y > 146):
            z = "ENVER"
        if (232 < x) & (x < 242) & (y < 156) & (y > 146):
            z = "BLDG"
        if (277 < x) & (x < 287) & (y < 156) & (y > 146):
            z = "CESS"
        if (322 < x) & (x < 332) & (y < 156) & (y > 146):
            z = "ERGY"
        if (367 < x) & (x < 377) & (y < 156) & (y > 146):
            z = "COMM"
        if (412 < x) & (x < 422) & (y < 156) & (y > 146):
            z = "MANF"
        if (143 < x) & (x < 153) & (y < 169) & (y > 159):
            z = "LAAR"
        if (188 < x) & (x < 198) &  (y < 169) & (y > 159):
            z = "MATL"
        if (233 < x) & (x < 243) &  (y < 169) & (y > 159):
            z = "CISE"
        if (278 < x) & (x < 288) & (y < 169) & (y > 159):
            z = "HAUD"

    else:
        z = "habal"
        if (367 < x) & (x < 377):
            z = "Strongly Agree"
        if (400 < x) & (x < 410):
            z = "Agree"
        if (436 < x) & (x < 446):
            z = "Neutral"
        if (468 < x) & (x < 478):
            z = "Disagree"
        if (502 < x) & (x < 512):
            z = "Strongly Disagree"
    return z


# gets the array of answers and the file name to be created
def write_in_file(ans, f):
    text_file = open(f, 'w')
    text_file.write('\n Gender: ' + ans[0])
    text_file.write('\n Semester: ' + ans[1])
    text_file.write('\n Program: ' + ans[2])
    text_file.write('\n\n 1 Teaching sessions')
    text_file.write('\n 1.1: ' + ans[3])
    text_file.write('\n 1.2: ' + ans[4])
    text_file.write('\n 1.3: ' + ans[5])
    text_file.write('\n 1.4: ' + ans[6])
    text_file.write('\n 1.5: ' + ans[7])
    text_file.write('\n\n 2 Course/Module Support')
    text_file.write('\n 2.1: ' + ans[8])
    text_file.write('\n 2.2: ' + ans[9])
    text_file.write('\n 2.3: ' + ans[10])
    text_file.write('\n 2.4: ' + ans[11])
    text_file.write('\n 2.5: ' + ans[12])
    text_file.write('\n 2.6: ' + ans[13])
    text_file.write('\n\n 3 Course/Module Organization')
    text_file.write('\n 3.1: ' + ans[14])
    text_file.write('\n 3.2: ' + ans[15])
    text_file.write('\n 3.3: ' + ans[16])
    text_file.write('\n\n 4 Course/Module Resources')
    text_file.write('\n 4.1: ' + ans[17])
    text_file.write('\n 4.2: ' + ans[18])
    text_file.write('\n 4.3: ' + ans[19])
    text_file.write('\n\n 5 Course/Module Satisfaction')
    text_file.write('\n 5.1: ' + ans[20])
    text_file.write('\n 5.2: ' + ans[21])
    text_file.close()


# get_circles pass each image to get_circles function and a string needed for naming result file
get_circles('test1.jpg', 'test1')
# get_circles('test2.jpg', 'test2')
# get_circles('test3.jpg', 'test3')
# get_circles('test4.jpg', 'test4')
# get_circles('test5.jpg', 'test5')
# get_circles('test6.jpg', 'test6')
# get_circles('test7.jpg', 'test7')
# get_circles('test8.jpg', 'test8')
# get_circles('test9.jpg', 'test9')
# get_circles('test10.jpg', 'test10')

cv2.waitKey(0)

# rotate_img rotate the image if needed




