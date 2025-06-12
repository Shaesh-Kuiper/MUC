import cv2 as cv 

img = cv.imread(r"background_image.png")

img = cv.resize(img, (1920,1080),interpolation=cv.INTER_LANCZOS4)

cv.imshow("Image", img)
print(img.shape)

cv.waitKey(0)