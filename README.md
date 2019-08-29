# bookMeetingRoom

Django-Rest-Framework MeetingRoom booking app

##Search Available Rooms

Make a post request at 

>localhost/api/availablerooms

example search Json Format
>{
>
>"number_of_people": 1,
>
>"date_start": "2019-08-25T09:10:00Z",
>
>"date_end": "2019-08-25T09:50:00Z"
>
>}

if is there a available room the app will response a json format

example response

>{
>
>"room_id": "room3",
>
>"number_of_people": 1,
>
>"date_start": "2019-08-25T09:10:00Z",
>
>"date_end": "2019-08-25T09:50:00Z"
>
>}


##Booking a room
Make a post request at
>localhost/api/bookroom
>

example booking Json Format ( it is search output)

>{
>
>"room_id": "room3",
>
>"number_of_people": 1,
>
>"date_start": "2019-08-25T09:10:00Z",
>
>"date_end": "2019-08-25T09:50:00Z"
>
>}