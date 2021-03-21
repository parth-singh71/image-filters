import cv2
import sys
from utils import create_dir, get_output_number


class Filter:
    def __init__(self, save_mode=True, view_mode=False, dst=None):
        if dst is None:
            self.dst = "outputs/"
        else:
            self.dst = dst
        create_dir(self.dst)
        self.save_mode = save_mode
        self.view_mode = view_mode

    def resize(self, img):
        height, width = img.shape[:2]
        print(width, height)
        if height < 100:
            return cv2.resize(img, (width * 2, height * 2), interpolation=cv2.INTER_CUBIC)
        elif height >= 700 and height < 1400:
            return cv2.resize(img, (width - 100, height - 100), interpolation=cv2.INTER_AREA)
        elif height >= 1400 and height < 2100:
            return cv2.resize(img, (width // 2, height // 2), interpolation=cv2.INTER_AREA)
        elif height >= 2100 and height < 2800:
            return cv2.resize(img, (width // 4, height // 4), interpolation=cv2.INTER_AREA)
        elif height >= 2800 and height < 3500:
            return cv2.resize(img, (width // 8, height // 8), interpolation=cv2.INTER_AREA)
        else:
            return img

    def execute(self, filepath):
        data = {}
        img = cv2.imread(filepath)
        data["original"] = img
        img = self.resize(img)
        data["resized"] = img
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        data["grayscale"] = gray
        median_blur = cv2.medianBlur(img, 5)
        data["blurred"] = median_blur
        adaptive_thresh = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 9)
        data["bw_sketch"] = adaptive_thresh
        bilateral = cv2.bilateralFilter(img, 9, 100, 100)
        data["painting"] = bilateral
        toonified = cv2.bitwise_and(
            bilateral, bilateral, mask=adaptive_thresh)
        data["toonified"] = toonified
        num = get_output_number(self.dst) + 1
        if self.save_mode:
            self.save(f"output-{num}", data)
        if self.view_mode:
            self.view(data)

    def view(self, data):
        filenames = list(data.keys())
        imgs = data.values()
        for index, img in enumerate(imgs):
            cv2.imshow(f"{filenames[index]}", img)
        cv2.waitKey(0)

    def save(self, foldername, data):
        filenames = list(data.keys())
        imgs = data.values()
        create_dir(f"{self.dst}/{foldername}")
        for index, img in enumerate(imgs):
            cv2.imwrite(f"{self.dst}/{foldername}/{filenames[index]}.png", img)
            print(f"[INFO] Saved {filenames[index]}.png")
        print(f"[INFO] Output saved in folder: \"{foldername}/\"")
        if not self.view_mode:
            print(f"[EXITING]")
            sys.exit()
