# iss_position_with_sms_notfication
Get the position of the international space station with api and if the iss in your near, you'll get a sms from twilio

This is my first project on Github. I would be happy if you leave any feedback or comments.


1. It is checked via open Api whether it is after sunset or before sunrise. (so it's dark) 
  - Berlin is set as the standard location
  - Choose your city

2. Then the data is fetched from the ISS Api and the distance to the ISS and the specified location are transmitted

3. If the distance is less than 500km with the Twilio Api, an SMS is then sent to a cell phone number with the address where the ISS is above (if there is one, not above the sea)

Enter your Twilio data: 
  - auth_token
  - sid
  - phone number
  
   https://www.twilio.com
