import cv2
import numpy as np


def detect_crack(image_path):

    # ===============================
    # Membaca gambar
    # ===============================

    image = cv2.imread(image_path)

    if image is None:
        raise Exception("Gambar tidak ditemukan.")

    result = image.copy()

    # ===============================
    # Resize
    # ===============================

    width = 800

    ratio = width / image.shape[1]

    height = int(image.shape[0] * ratio)

    image = cv2.resize(image, (width, height))

    result = image.copy()

    # ===============================
    # Grayscale
    # ===============================

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # ===============================
    # Histogram Equalization
    # ===============================

    equalized = cv2.equalizeHist(gray)

    # ===============================
    # Gaussian Blur
    # ===============================

    blur = cv2.GaussianBlur(equalized, (5, 5), 0)

    # ===============================
    # Canny Edge Detection
    # ===============================

    edges = cv2.Canny(
        blur,
        threshold1=50,
        threshold2=150
    )

    # ===============================
    # Morphology Closing
    # ===============================

    kernel = np.ones((3, 3), np.uint8)

    morph = cv2.morphologyEx(
        edges,
        cv2.MORPH_CLOSE,
        kernel,
        iterations=2
    )

    # ===============================
    # Cari Contour
    # ===============================

    contours, _ = cv2.findContours(
        morph,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    total_crack_area = 0

    # ===============================
    # Seleksi Contour Retakan
    # ===============================

    for contour in contours:

        area = cv2.contourArea(contour)

        if area < 20:
            continue

        x, y, w, h = cv2.boundingRect(contour)

        ratio = max(w, h) / (min(w, h) + 1)

        # Retakan biasanya panjang dan tipis
        if ratio > 2:

            total_crack_area += area

            cv2.drawContours(
                result,
                [contour],
                -1,
                (0, 0, 255),
                2
            )

            cv2.rectangle(
                result,
                (x, y),
                (x + w, y + h),
                (0, 255, 0),
                1
            )

    # ===============================
    # Hitung Persentase Retakan
    # ===============================

    total_area = image.shape[0] * image.shape[1]

    crack_percent = (total_crack_area / total_area) * 100

    # ===============================
    # Menentukan Status
    # ===============================

    if crack_percent < 1:
        status = "NORMAL"
        color = (0, 255, 0)

    elif crack_percent < 3:
        status = "RETak RINGAN"
        color = (0, 255, 255)

    else:
        status = "RETAK"
        color = (0, 0, 255)

    # ===============================
    # Menampilkan Informasi
    # ===============================

    cv2.putText(
        result,
        f"Status : {status}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        color,
        2
    )

    cv2.putText(
        result,
        f"Retakan : {crack_percent:.2f} %",
        (20, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.9,
        color,
        2
    )

    cv2.putText(
        result,
        f"Jumlah Kontur : {len(contours)}",
        (20, 120),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 0),
        2
    )

    return status, crack_percent, result