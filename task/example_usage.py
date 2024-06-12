from models import record_and_annotate_vehicles
from datetime import datetime

streets = [
    {
        "street_name": "Jl. Jenderal Basuki Rahmat Arah Selatan",
        "stream_url": "http://stream.cctv.malangkota.go.id/WebRTCApp/streams/771615331018457682499213.m3u8?token=null",
        "start_x": 16,
        "start_y": 487,
        "end_x": 933,
        "end_y": 201
    }
]

street = streets[0] 
day_period = "night" # should be 'morning' / 'afternoon' / 'night'
date = datetime.today().strftime('%Y-%m-%d')
duration = 5 # in seconds

result = record_and_annotate_vehicles(street=street, day_period=day_period, date=date, recording_duration=duration)
print(result)
