from datetime import datetime

config = {
    "morning_opening_time": datetime.strptime("09:00", '%H:%M'),
    "morning_closing_time": datetime.strptime("13:30", '%H:%M'),
    "afternoon_opening_time": datetime.strptime("15:00", '%H:%M'),
    "afternoon_closing_time": datetime.strptime("20:00", '%H:%M')
}