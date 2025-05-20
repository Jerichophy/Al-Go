import degirum as dg
import degirum_tools
import time

class VehicleDetection:
    def __init__(self):
        inference_host_address = "@local"
        zoo_url = "/home/Chophy/hailo_examples/models" #Place here the folder directory of your model (Not the directory to the model itself)
        model_name = 'mobility-aid--960x960_quant_hailort_multidevice_1' #This is the model name for the Vehicle Detection.

        # define the zones of interest
        polygon_zones = [
            [[0, 0], [0, 1080], [960, 1080], [960, 0]], #Zone For Vehicle in the Left
            [[960, 0],[960, 1080], [1925, 1080], [1925, 0]], #Zone For Vehicle in the Merging Lane
        ]
        # define class list and display options
        class_list = ["Vehicles"] #Only count vehicles
        per_class_display = True
        window_name="IDK"
        # load model
        self.model = dg.load_model(
            model_name=model_name, 
            inference_host_address=inference_host_address,
            zoo_url=zoo_url,
            overlay_color=[(255,0,0)],
            output_class_set = set(class_list)
        )
        # create zone counter
        self.zone_counter = degirum_tools.ZoneCounter(
                polygon_zones,         
                class_list=class_list,
                per_class_display=per_class_display,
                triggering_position=degirum_tools.AnchorPoint.CENTER,
                window_name=window_name,  # attach display window for interactive zone adjustment
        )

        degirum_tools.attach_analyzers(self.model, [self.zone_counter])

    def get_vehicle_zone_counts(self, frame):
        for result in self.model.predict_batch([frame]):  # Run inference on the frame
            Zone1Vehicle = result.zone_counts[0].get("Vehicles", 0) #Counting Vehicles in Left Zone
            Zone2Vehicle = result.zone_counts[1].get("Vehicles", 0) #Counting Vehicles in the Merging Lane
        return Zone1Vehicle, Zone2Vehicle
