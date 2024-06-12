from celery import shared_task
import time
from celery import Celery
from datetime import timedelta, datetime
from celery.utils.log import get_task_logger
from dashboard.models import JumlahKendaraan
import random
from task.tl import record_and_annotate_vehicles


logger = get_task_logger(__name__)


celery = Celery(__name__)
celery.config_from_object(__name__)

@shared_task
def object_detection1():
    try : 
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
        day_period = "morning" # should be 'morning' / 'afternoon' / 'night'
        date = datetime.today().strftime('%Y-%m-%d')
        duration = 20 # in seconds

        result = record_and_annotate_vehicles(street=street, day_period=day_period, date=date, recording_duration=duration)
        logger.info(result)
        today = datetime.today().date()

        for i in result :
            if i["type"] == "car":
                jenis = "Mobil"
            else :
                jenis = "Motor"
            JumlahKendaraan.objects.create(
                                    jalan=i['street'],
                                    jam=i["time"],
                                    jenis=jenis,
                                    jumlah=i["count"],
                                    tanggal=i["date"],
                                    path_video=i["annotated_result_path"]
                                    )
                
        return "save to Database"

    except Exception as e:
        logger.error(f"Error saving to database: {e}")
        return str(e)
    
@shared_task
def object_detection2():
    try : 
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
        day_period = "morning" # should be 'morning' / 'afternoon' / 'night'
        date = datetime.today().strftime('%Y-%m-%d')
        duration = 20 # in seconds

        result = record_and_annotate_vehicles(street=street, day_period=day_period, date=date, recording_duration=duration)
        logger.info(result)
        today = datetime.today().date()

        for i in result :
            if i["type"] == "car":
                jenis = "Mobil"
            else :
                jenis = "Motor"
            JumlahKendaraan.objects.create(
                                    jalan=i['street'],
                                    jam=i["time"],
                                    jenis=jenis,
                                    jumlah=i["count"],
                                    tanggal=i["date"],
                                    path_video=i["annotated_result_path"]
                                    )
                
        return "save to Database"

    except Exception as e:
        logger.error(f"Error saving to database: {e}")
        return str(e)
    
@shared_task
def object_detection3():
    try : 
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
        day_period = "morning" # should be 'morning' / 'afternoon' / 'night'
        date = datetime.today().strftime('%Y-%m-%d')
        duration = 20 # in seconds

        result = record_and_annotate_vehicles(street=street, day_period=day_period, date=date, recording_duration=duration)
        logger.info(result)
        today = datetime.today().date()

        for i in result :
            if i["type"] == "car":
                jenis = "Mobil"
            else :
                jenis = "Motor"
            JumlahKendaraan.objects.create(
                                    jalan=i['street'],
                                    jam=i["time"],
                                    jenis=jenis,
                                    jumlah=i["count"],
                                    tanggal=i["date"],
                                    path_video=i["annotated_result_path"]
                                    )
                
        return "save to Database"

    except Exception as e:
        logger.error(f"Error saving to database: {e}")
        return str(e)