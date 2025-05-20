import threading
import cv2
import serial
import time
from picamera2 import Picamera2
import libcamera
import pedestrian_logic
import vehicle_logic

# === Serial Setup ===
ser = serial.Serial('/dev/serial0', 115200, timeout=1)  # Adjust your port and baud rate as needed
time.sleep(2) 

# === Camera Setup for Pedestrian ===
picam2_pedestrian = Picamera2(0)
config_pedestrian = picam2_pedestrian.create_preview_configuration(
    main={"format": 'RGB888', "size": (1920, 1080)},
    raw=picam2_pedestrian.sensor_modes[1]
)
picam2_pedestrian.set_controls({"AeFlickerMode": libcamera.controls.AeFlickerModeEnum.Manual})
picam2_pedestrian.configure(config_pedestrian)
picam2_pedestrian.start()

# === Camera Setup for Vehicle ===
vehicle_detection = vehicle_logic.VehicleDetection()
picam2_vehicle = Picamera2(1)
config_vehicle = picam2_vehicle.create_preview_configuration(
    main={"format": 'RGB888', "size": (1920, 1080)},
    raw=picam2_vehicle.sensor_modes[1]
)
picam2_vehicle.set_controls({"AeFlickerMode": libcamera.controls.AeFlickerModeEnum.Manual})
picam2_vehicle.configure(config_vehicle)
picam2_vehicle.start()

# === Shared Data Variables ===
shared_data = {
    "pedestrian_count": 0,
    "zone1_pwd": 0,
    "zone1_vehicle": 0,
    "zone2_vehicle": 0
}
data_lock = threading.Lock()

#Pedestrian.py Part
def process_pedestrian():
    pedestrian_detector = pedestrian_logic.PedestrianDetection()
    while True:
        frame = picam2_pedestrian.capture_array()
        frame = cv2.rotate(frame, cv2.ROTATE_180) 
        pedestrian_count, zone1_pwd = pedestrian_detector.get_pedestrian_info(frame)
        with data_lock:
            shared_data["pedestrian_count"] = pedestrian_count
            shared_data["zone1_pwd"] = int(zone1_pwd)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

#Vehicle.py Part
def process_vehicle():
    while True:
        frame = picam2_vehicle.capture_array()
        frame = cv2.rotate(frame, cv2.ROTATE_180)  # <<< rotate here
        Zone1Vehicle, Zone2Vehicle = vehicle_detection.get_vehicle_zone_counts(frame)
        with data_lock:
            shared_data["zone1_vehicle"] = Zone1Vehicle
            shared_data["zone2_vehicle"] = Zone2Vehicle

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

#Serial data sending thread
def send_serial_data():
    while True:
        with data_lock:
            message = f"{shared_data['pedestrian_count']},{shared_data['zone1_pwd']},{shared_data['zone1_vehicle']},{shared_data['zone2_vehicle']}\n"
        ser.write(message.encode('utf-8'))
        print(f"Sent: {message.strip()}")
        time.sleep(0.5)  # Send every 0.5 seconds (adjust as needed)

# Main function to start threads
if __name__ == "__main__":
    pedestrian_thread = threading.Thread(target=process_pedestrian)
    vehicle_thread = threading.Thread(target=process_vehicle)
    serial_thread = threading.Thread(target=send_serial_data)

    pedestrian_thread.start()
    vehicle_thread.start()
    serial_thread.start()

    pedestrian_thread.join()
    vehicle_thread.join()
    serial_thread.join()

    # Cleanup
    picam2_vehicle.stop()
    picam2_vehicle.close()
    picam2_pedestrian.stop()
    picam2_pedestrian.close()
    ser.close()
    cv2.destroyAllWindows()
