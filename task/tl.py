import cv2
import time
from moviepy.editor import *
import uuid
import os
import supervision as sv
from supervision import VideoSink
from ultralytics import YOLO
from celery.utils.log import get_task_logger
import json
from django.templatetags.static import static
logger = get_task_logger(__name__)

# Load configuration from JSON file
with open('task/config.json', 'r') as config_file:
    config = json.load(config_file)

CLASS_ID = config["CLASS_ID"]
YOLO_VERSION = config["YOLO_VERSION"]

def record_video(street, target_fps=5, duration=3600, recording_dir="recording"):
    """
    Record a video from a streaming URL and save it to a file.

    Args:
        street (dict): Dictionary containing information about the street including 'stream_url'.
        target_fps (int, optional): Target frames per second for the output video. Default is 5.
        duration (int, optional): Duration of the recording in seconds. Default is 3600 (1 hour).
        recording_dir (str, optional): Directory where the recorded video will be saved. Default is 'recording'.

    Returns:
        str: Path to the saved video file or None if recording failed.
    """
    logger.info("Starting record_video function")

    if not os.path.exists(recording_dir):
        os.makedirs(recording_dir)
        logger.info(f"Created recording directory: {recording_dir}")

    output_filename = os.path.join(recording_dir, str(uuid.uuid1()) + ".mp4")
    temp_file = os.path.join(recording_dir, str(uuid.uuid1()) + ".mp4")

    logger.info(f"Output filename: {output_filename}")
    logger.info(f"Temporary filename: {temp_file}")

    stream_url = street["stream_url"]
    logger.info(f"Stream URL: {stream_url}")

    cap = cv2.VideoCapture(stream_url)
    if not cap.isOpened():
        logger.info("Cannot open video stream")
        return None

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    out = cv2.VideoWriter(temp_file, fourcc, fps, (width, height))

    logger.info(f"Video dimensions: {width}x{height}")
    logger.info(f"Original FPS: {fps}")

    logger.info("Start recording")
    start = time.time()
    while time.time() - start <= duration:
        ret, frame = cap.read()
        if not ret:
            logger.info("Frame could not be read, ending recording early")
            break
        frame = cv2.resize(frame, (1280, 720))
        out.write(frame)

    cap.release()
    out.release()
    logger.info("Recording finished, temporary file created")

    try:
        clip = VideoFileClip(temp_file)
        clip.write_videofile(output_filename, fps=target_fps)
        logger.info(f"Final video saved as: {output_filename}")
    except Exception as e:
        logger.info(f"Error processing video: {e}")
        return None
    finally:
        clip.reader.close()
        if clip.audio:
            clip.audio.reader.close_proc()
        os.remove(temp_file)
        logger.info("Temporary file deleted")

    return output_filename

day_period2time = {
    "morning": "07.00-08.00",
    "afternoon": "12.00-13.00",
    "night": "18.00-19.00"
}

def count_vehicles_and_annotate(street, source_video_path, day_period, date, day_period2time=day_period2time, annotated_dir="annotated"):
    """
    Annotate a video with vehicle detection and count the number of cars and motorcycles.

    Args:
        street (dict): Dictionary containing information about the street including start and end points.
        source_video_path (str): Path to the source video file.
        day_period (str): The period of the day (e.g., 'morning', 'afternoon', 'night').
        date (str): The date of the recording.
        day_period2time (dict, optional): Dictionary mapping day periods to time ranges. Default is predefined mapping.
        annotated_dir (str, optional): Directory where the annotated video will be saved. Default is 'annotated'.

    Returns:
        list: List of dictionaries with counts of cars and motorcycles.
    """
    logger.info("Starting count_vehicles_and_annotate function")

    if not os.path.exists(annotated_dir):
        os.makedirs(annotated_dir)
        logger.info(f"Created annotated directory: {annotated_dir}")

    start_point = sv.Point(street["start_x"], street["start_y"])
    end_point = sv.Point(street["end_x"], street["end_y"])

    line_zone = sv.LineZone(start=start_point, end=end_point)
    line_zone_annotator = sv.LineZoneAnnotator(thickness=2, text_thickness=2, text_scale=2)
    bounding_box_annotator = sv.BoundingBoxAnnotator(thickness=2)
    trace_annotator = sv.TraceAnnotator(thickness=2)
    byte_tracker = sv.ByteTrack()
    model = YOLO(YOLO_VERSION)

    logger.info(f"YOLO model loaded: {YOLO_VERSION}")

    video_info = sv.VideoInfo.from_video_path(source_video_path)
    id_prediction = os.path.splitext(os.path.basename(source_video_path))[0]
    annotated_path = os.path.join(annotated_dir, f"{id_prediction}.mp4")

    logger.info(f"Source video path: {source_video_path}")
    logger.info(f"Annotated video path: {annotated_path}")

    with VideoSink(annotated_path, video_info) as sink:
        car_crossed_total = 0
        motor_crossed_total = 0

        logger.info("Starting frame processing")

        for frame in sv.get_video_frames_generator(source_video_path):
            results = model(frame, verbose=False, classes=[2, 3], conf=0.1)[0]
            detections = sv.Detections.from_ultralytics(results)
            detections = byte_tracker.update_with_detections(detections)

            annotated_frame = frame.copy()
            annotated_frame = trace_annotator.annotate(
                scene=annotated_frame,
                detections=detections)
            annotated_frame = bounding_box_annotator.annotate(
                scene=annotated_frame,
                detections=detections)

            crossed_in, crossed_out = line_zone.trigger(detections)
            if True in crossed_in or True in crossed_out:
                d = detections.class_id
                car_crossed = len(d[d == 2])
                motor_crossed = len(d[d == 3])

                car_crossed_total += car_crossed
                motor_crossed_total += motor_crossed

                logger.info(f"Vehicles crossed - Cars: {car_crossed_total}, Motorcycles: {motor_crossed_total}")

            annotated_frame = line_zone_annotator.annotate(annotated_frame, line_counter=line_zone)
            sink.write_frame(annotated_frame)

        logger.info("Finished processing frames")

    output = [
        {
            "id": id_prediction + "-motor",
            "street": street["street_name"],
            "time": day_period2time[day_period],
            "date": date,
            "count": motor_crossed_total,
            "type": "motor",
            "annotated_result_path": annotated_path
        },
        {
            "id": id_prediction + "-car",
            "street": street["street_name"],
            "time": day_period2time[day_period],
            "date": date,
            "count": car_crossed_total,
            "type": "car",
            "annotated_result_path": annotated_path
        },
    ]

    logger.info("Function finished. Returning output.")
    return output

def record_and_annotate_vehicles(street, day_period, date, recording_duration=30, annotated_dir="annotated", target_fps=5):
    """
    Record a video from a streaming URL and annotate it with vehicle detection and counting.

    Args:
        street (dict): Dictionary containing information about the street including 'stream_url' and coordinates.
        day_period (str): The period of the day (e.g., 'morning', 'afternoon', 'night').
        date (str): The date of the recording.
        recording_duration (int, optional): Duration of the recording in seconds. Default is 30 seconds.
        annotated_dir (str, optional): Directory where the annotated video will be saved. Default is 'annotated'.
        target_fps (int, optional): Target frames per second for the output video. Default is 5.

    Returns:
        list: List of dictionaries with counts of cars and motorcycles.
    """
    # Record the video
    source_video_path = record_video(street=street, duration=recording_duration, target_fps=target_fps)
    if source_video_path is None:
        logger.info("Recording failed. Exiting.")
        return None

    # Annotate the video and count vehicles
    result = count_vehicles_and_annotate(street=street, source_video_path=source_video_path, day_period=day_period, date=date, day_period2time=day_period2time, annotated_dir=annotated_dir)
    return result
