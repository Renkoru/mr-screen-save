from datetime import datetime

from mss import mss
import typer
import pyautogui
from time import sleep
from dasbus.connection import SessionMessageBus
from PIL import ImageGrab, ImageDraw, Image

bus = SessionMessageBus()

proxy = bus.get_proxy(
    "org.freedesktop.Notifications",
    "/org/freedesktop/Notifications"
)

app = typer.Typer()

def send_notification(text: str):
    proxy.Notify(
        "", 0, "face-smile", "Screen & save",
        text,
        [], {}, 3000
    )

def find_border(image) -> tuple[int, int, int, int]:
    top = 0
    right = 0
    bottom = 0
    left = 0
    width, height = image.size # get the size of the image

    image_data = list(image.getdata())
    border_color = image_data[0]
    image_matrix = []

    print(width, height)

    for y in range(height):
        image_matrix.append(image_data[y*width : y*width + width])

    # Find top
    for y in range(height):
        if image_matrix[y][width // 2] != border_color:
            top = y
            break

    # Find right
    for x in reversed(range(width)):
        if image_matrix[height // 2][x] != border_color:
            right = x
            break

    # Find bottom
    for y in reversed(range(height)):
        if image_matrix[y][width // 2] != border_color:
            bottom = y
            break

    # Find left
    for x in range(width):
        if image_matrix[height // 2][x] != border_color:
            # print(f"{image_matrix[height // 2][x]} != {border_color}")
            left = x
            break

    return left, top, right, bottom

def screenshot():
    # with Image.open("screenshots/2023-02-03-14:53:46:884836.jpg") as img:
    #     # img = ImageGrab.grab()
    #     # timestamp = datetime.today().strftime('%Y-%m-%d-%H:%M:%S:%f')
    #     # grayscale_img = img.convert("L") # convert to grayscale

    #     # print(list(img.getdata())[2])
    #     border_box = find_border(img)
    #     print(f"Border_box: {border_box}")
    #     draw = ImageDraw.Draw(img)
    #     draw.rectangle((800, 80, 1678, 1359), outline="red")
    #     img.show()

    img = ImageGrab.grab()
    timestamp = datetime.today().strftime('%Y-%m-%d-%H:%M:%S:%f')
    # grayscale_img = img.convert("L") # convert to grayscale

    # print(list(img.getdata())[2])
    border_box = find_border(img)
    # print(f"Border_box: {border_box}")
    # draw = ImageDraw.Draw(img)
    # draw.rectangle(border_box, outline="red")
    cropped = img.crop(border_box)
    # img.show()
    cropped.save(f"screenshots/{timestamp}.png")


    # grayscale_img.save(f"screenshots/{timestamp}.jpg")
    # print(img.getbbox())
    # typer.echo(f"{timestamp} Saved")

@app.command()
def hello(name: str):
    print(f"Hello {name}")

@app.callback(invoke_without_command=True)
def main(name: str):
    # pyautogui.write('Hello world!', interval=0.25)

    send_notification("Screenshot saving will start in 3 seconds")
    sleep(3)
    # for _ in range(1):
    # TODO: check image hash and stop the loop
    while True:
        sleep(0.5)
        screenshot()
        pyautogui.press('right')  

    # hello(name)


if __name__ == "__main__":
    app()
