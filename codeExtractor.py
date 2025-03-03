import cv2
import numpy as np
import pytesseract
import pygetwindow as gw
import pyautogui
import time

pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract.exe"

languages = {
    "1": ("Python", "py"),
    "2": ("JavaScript", "js"),
    "3": ("C++", "cpp"),
    "4": ("Java", "java"),
    "5": ("HTML", "html"),
}

print("\nSelect the programming language for the extracted code:")
for key, (lang, ext) in languages.items():
    print(f"{key}. {lang}")

lang_choice = input("\nEnter the number of your choice: ")

if lang_choice not in languages:
    print("Invalid choice. Exiting...")
    exit()

lang_name, file_extension = languages[lang_choice]
filename = f"extracted_code.{file_extension}"

print(f"\n🔹 Code will be saved in: {filename}")

windows = gw.getAllTitles()
filtered_windows = [w for w in windows if w.strip()]


print("\nAvailable Windows:")
for i, title in enumerate(filtered_windows):
    print(f"{i + 1}. {title}")

choice = int(input("\nEnter the number of the window to capture: ")) - 1
if choice < 0 or choice >= len(filtered_windows):
    print("Invalid selection!")
    exit()

selected_window = filtered_windows[choice]
print(f"\n🔹 Selected Window: {selected_window}")

window = gw.getWindowsWithTitle(selected_window)[0]
x, y, width, height = window.left, window.top, window.width, window.height

time.sleep(5)
screenshot = pyautogui.screenshot(region=(x, y, width, height))
frame = np.array(screenshot)
frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
rect = []
dragging = False

def select_area(event, x, y, flags, param):
    global rect, dragging, frame_copy

    if event == cv2.EVENT_LBUTTONDOWN:
        rect = [(x, y)]
        dragging = True

    elif event == cv2.EVENT_MOUSEMOVE and dragging:
        frame_copy = frame.copy()
        cv2.rectangle(frame_copy, rect[0], (x, y), (0, 255, 0), 2)
        cv2.imshow("Select Code", frame_copy)

    elif event == cv2.EVENT_LBUTTONUP:
        rect.append((x, y))
        dragging = False
        cv2.destroyWindow("Select Code")


frame_copy = frame.copy()
cv2.imshow("Select Code", frame)
cv2.setMouseCallback("Select Code", select_area)
cv2.waitKey(0)

if len(rect) == 2:
    x1, y1 = rect[0]
    x2, y2 = rect[1]

    x1, x2 = min(x1, x2), max(x1, x2)
    y1, y2 = min(y1, y2), max(y1, y2)

    cropped = frame[y1:y2, x1:x2]
    gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)

    gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    extracted_text = pytesseract.image_to_string(gray, config="--psm 6 --oem 3")

    print("\n🔹 Extracted Code:\n", extracted_text)

    with open(filename, "w", encoding="utf-8") as f:
        f.write(extracted_text)
    print(f"\n✅ Code saved successfully in {filename}")


cv2.destroyAllWindows()



