class buttons_name:
    display = "Dsiplay Buttons"
    start = "Start"
    add_button = "Add New Button"
    del_button = "Delete a Button"
    set_channel = "Set Channel"
    set_time = "Set Time"
    clear_messages = "clear_messages"

buttons_empty = "Buttons is Empty !"


add_button = """
Replace the position number you want and order as follows :

Url Buttons :
```add_url 1
text
google.com```

Inline Buttons :
```add_inline 1
text```
"""


delete_button = """
Replace the text number below with the number of the button you want to delete and send it :
`del 1`

{buttons_list}
"""



invalid_position = """
the position {position} does not exists !
"""


del_succesfully = """
the Button Deleted Suucesfully !
"""


invalid_input = """
Invalid input !
"""

no_link = """
Invalid url !
a Correct Url : https://google.com
"""

add_succesfully = """
the Button Added Suucesfully !
"""


added_post = """
Post Added. 
"""

channel_error = """
Channel {channel} Invalid Error !
Please Set a correct channel
"""

channel_empty = """
Channel is Empty !
Please Set a channel
"""

channel_added = """
The channel `{channel}` added successfully !
"""



set_channel = """
Current Channel : {channel}
To set a channel: Use the following command :
`set_channel @telegram`
"""

inline_length_error = """
Text length should not exceed 64 characters!
"""


set_time = """
Current time loop : {time} Minutes
To set a new time, Use the following command (By Minutes):
`set_time 30`
"""

time_loop_added = """
The time added successfully !
"""


clear_messages = """
All Messages Clearde Successfully !
"""