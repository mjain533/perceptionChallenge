import cv2
import os
import numpy as np

def load_image(filename):
    image = cv2.imread(filename)
    if image is None:
        print("Error: Could not load image.")
    else:
        return image

def drawline(image, start, end, color, thickness):
    image = cv2.line(image, start, end, color, thickness)
    return image


def pixelsWithColor(image):
    coordinates = []
    for y in range(image.shape[0]):
        for x in range(image.shape[1]):
            b, g, r = image[y, x]
            if 100 <= r <= 255 and 0 <= g <= 50 and 0 <= b <= 50:
                if(y>600 and (x>925 or x<875)):
                    coordinates.append((y, x))
    return coordinates

def changeColor(image, coordinates):
    for coord in coordinates:
        image[coord[0], coord[1]] = (255, 255, 255) 
    return image

def resize_image(image, width=None, height=None, scale=None):
    resized_image = cv2.resize(image, (908, 1210), interpolation=cv2.INTER_AREA)
    return resized_image

def show_image(image):
    cv2.imshow('Image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def corrdinates(coordinates):
    x = []
    y = []
    for coord in coordinates:
        x.append(coord[1])
        y.append(coord[0])
    return x, y

def densitysX(coordinates):
    density = []
    for coord in coordinates:
        added = False
        for group in density:
            if abs(coord - group[-1]) <= 0:  # Adjust the threshold as needed
                group.append(coord)
                added = True
                break
        if not added:
            density.append([coord])
    density = sorted(density, key=len, reverse=True)[:350]

    return density
def densitysY(coordinates):
    density = []
    for coord in coordinates:
        added = False
        for group in density:
            if abs(coord - group[-1]) <= 0: 
                group.append(coord)
                added = True
                break
        if not added:
            density.append([coord])
    density = sorted(density, key=len, reverse=True)[:250]

    return density

def meanDensity(density):
    meanDensity = []
    for group in density:
        meanDensity.append(round(np.mean(group)))
    return meanDensity

def sides(x):
    left = []
    right = []
    for value in x:
        if value<908:
            left.append(value)
        else:
            right.append(value)
    return left, right



def main():
    image = load_image('red.png')
    coordinate = pixelsWithColor(image)
    image = changeColor(image, coordinate)
    x,y = corrdinates(coordinate)
    x=meanDensity(densitysX(x))
    y=meanDensity(densitysY(y))
 #   for i in range(len(x)):
 #     image = drawline(image, (x[i], 0), (x[i], 2420), (0, 255, 0), 5)
 #   for i in range(len(y)):
 #       image = drawline(image, (0, y[i]), (1816, y[i]), (255, 0, 0), 5)
    left,right = sides(x)
    left = sorted(left, key=lambda x: x)
    right  = sorted(right, key=lambda x: x)
    y = sorted(y, key=lambda x: x)
    image = drawline(image, (left[len(left)-1],y[0]), (left[0],y[len(y)-1]), (0, 0, 255), 5)
    image = drawline(image, (right[0],y[0]), (right[len(right)-1],y[len(y)-1]), (0, 0, 255), 5)
    image = resize_image(image, width=200, height=200)
    show_image(image)

if __name__ == "__main__":
    main()