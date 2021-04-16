import time
import subprocess

from board import SCL, SDA
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

# create the I2C interface
i2c = busio.I2C(SCL, SDA)

# create the SSD1306 OLED class
disp = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)

# clear the display
disp.fill(0)
disp.show()

# create blank image for drawing, mode 1 is 1-bit color
width = disp.width
height = disp.height
image = Image.new("1", (width, height))

# get drawing object to draw on image
draw = ImageDraw.Draw(image)

# draw a black filled box to clear the image
draw.rectangle((0, 0, width, height), outline=0, fill=0)

#define constants to allow easy resizing of shapes
padding = -2
top = padding
bottom = height - padding

# move left to right keeping track of the current x position for drawing shapes
x = 0

# load default font
font = ImageFont.load_default()

while True:

	draw.rectangle((0, 0, width, height), outline=0, fill=0)

	cmd = "hostname -I | cut -d' ' -f1"
	IP = subprocess.check_output(cmd, shell=True).decode("utf-8")
	cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\",$(NF-2)}'"
	CPU = subprocess.check_output(cmd, shell=True).decode("utf-8")
	cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%s MB %.2f%%\", $3,$2,$3*100/$2 }'"
	memUsage = subprocess.check_output(cmd, shell=True).decode("utf-8")
	cmd = 'df -h | awk \'$NF=="/"{printf "Disk: %d%d GB %s", $3,$2,$5}\''
	Disk = subprocess.check_output(cmd, shell=True).decode("utf-8")

	# write four lines of text

	draw.text((x, top + 0), "IP: " + IP, font=font, fill=255)
	draw.text((x, top + 8), CPU, font=font, fill=255)
	draw.text((x, top + 16), MemUsage, font=font, fill=255)
	draw.text((x, top + 25), Disk, font=font, fill=255)

	# display image
	disp.image(image)
	disp.show()
	disp.sleep(0.1)
