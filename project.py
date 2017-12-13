import smtplib
import RPi.GPIO as GPIO
from picamera import PiCamera
from time import sleep


def sendEmail():
	smtpServer = "smtp.gmail.com"
	recepient  = "receiver@email.com"
	username   = "sender@gmail.com"
	password   = "password"
	port       = 587

	server = smtplib.SMTP(smtpServer, port)
	server.starttls()
	server.login(username, password)
 
	message = "Motion has been detected"
	server.sendmail(username, recepient, message)
	server.quit()

def recordClip(fileName):
	camera.start_preview()
    camera.start_recording(fileName)
    sleep(10)
    camera.stop_recording()
    camera.stop_preview()


# Configure pin numbering to Broadcom reference and
# set GPIO pin to input to activate pull_down resistor

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


# Setup up PiCamera

camera = PiCamera()
camera.resolution = (800, 600)


print ("Starting....")
sleep(2)


try:
    counter = 1
    
    while True:
        if GPIO.input(17):
        	fileName = '/home/pi/video-' + str(counter) + '.h264'
	        print ("----- Motion detected -----")
	        counter = counter + 1
		    recordClip(fileName)
		    sendEmail()
        else:
		    print('----- No motion -----')
		    sleep(2)

except KeyboardInterrupt:
    print ("Shutting Down")

except:
    print("An error occured")

finally:
    print ("Resetting GPIO pins")
    GPIO.cleanup()
    