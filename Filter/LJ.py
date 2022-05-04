import cv2
import numpy as np

def cowboy_effect(img):
    new_img = img.copy()
    h, w, n = img.shape
    for i in range(w):
        for j in range(h):
            b = img[j, i, 0]
            g = img[j, i, 1]
            r = img[j, i, 2]
            B = int(0.272 * r + 0.534 * g + 0.131 * b)
            G = int(0.349 * r + 0.686 * g + 0.168 * b)
            R = int(0.393 * r + 0.769 * g + 0.189 * b)
            new_img[j, i, 0] = max(0, min(B, 255))
            new_img[j, i, 1] = max(0, min(G, 255))
            new_img[j, i, 2] = max(0, min(R, 255))
    return new_img
 

# 连环画滤镜
def comics_effect(img):
    new_img = img.copy()
    h, w, n = img.shape
    for i in range(w):
        for j in range(h):
            b = img[j, i, 0]
            g = img[j, i, 1]
            r = img[j, i, 2]
            R = int(int(abs(g - b + g + r)) * r / 256)
            G = int(int(abs(b - g + b + r)) * r / 256)
            B = int(int(abs(b - g + b + r)) * g / 256)
            new_img[j, i, 0] = R
            new_img[j, i, 1] = G
            new_img[j, i, 2] = B
    return new_img

def cyberpunk_effect(image):
    # 反转色相
    image_hls = cv2.cvtColor(image, cv2.COLOR_BGR2HLS)
    image_hls = np.asarray(image_hls, np.float32)
    hue = image_hls[:, :, 0]
    hue[hue < 90] = 180 - hue[hue < 90]
    image_hls[:, :, 0] = hue

    image_hls = np.asarray(image_hls, np.uint8)
    image = cv2.cvtColor(image_hls, cv2.COLOR_HLS2BGR)

    image_lab = cv2.cvtColor(image, cv2.COLOR_BGR2Lab)
    image_lab = np.asarray(image_lab, np.float32)
    
    # 提高像素亮度，让亮的地方更亮
    light_gamma_high = np.power(image_lab[:, :, 0], 0.8)
    light_gamma_high = np.asarray(light_gamma_high / np.max(light_gamma_high) * 255, np.uint8)

     # 降低像素亮度，让暗的地方更暗
    light_gamma_low = np.power(image_lab[:, :, 0], 1.2)
    light_gamma_low = np.asarray(light_gamma_low / np.max(light_gamma_low) * 255, np.uint8)

    # 调色至偏紫
    dark_b = image_lab[:, :, 2] * (light_gamma_low / 255) * 0.1
    dark_a = image_lab[:, :, 2] * (1 - light_gamma_high / 255) * 0.3

    image_lab[:, :, 2] = np.clip(image_lab[:, :, 2] - dark_b, 0, 255)
    image_lab[:, :, 2] = np.clip(image_lab[:, :, 2] - dark_a, 0, 255)

    image_lab = np.asarray(image_lab, np.uint8)
    return cv2.cvtColor(image_lab, cv2.COLOR_Lab2BGR)    


if __name__ == "__main__":
    img = cv2.imread("Lenna.png")
    cv2.imshow("Lenna", img)
    cv2.imshow("demo01", cowboy_effect(img))
    cv2.imshow("demo2" , comics_effect(img))
    cv2.imshow("demo3",cyberpunk_effect(img))
    cv2.waitKey()
    cv2.destroyAllWindows()