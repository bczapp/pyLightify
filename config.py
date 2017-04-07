# Lightify Login Data
user = 'your_mail_addr@mail.de'
password = 'YourPass'
serialnumber = 'OSR0XXXXXXX'

# GroupID of Group that should be controlled
# Use Rest API to get the group id
groupid = '2'

# Some additional settings
additionalseconds = 5 # Delay for testing
loglevel = 'DEBUG'

# when should the lights be switched off? Format [xx,xx]
lightsout = [22,15]
# how many minutes after the sunset should the lights be turned on?
minutesaftersunset = 1

# Your position? Used to calculate the sunset.
location = ['50.000000', '7.000000']
hight = 30
