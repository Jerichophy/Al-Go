import degirum as dg
import degirum_tools
import time

class PedestrianDetection:
    def __init__(self):
        # Initialize the necessary variables for detection, model, etc.
        self.inference_host_address = '@local'
        self.zoo_url = '/home/Chophy/hailo_examples/models' #Place here the folder directory of your model (Not the directory to the model itself)
        self.model_name = 'Mobility-aid4--960x960_quant_hailort_multidevice_1' #This is the model name for the Pedestrian and Mobility Aid Detection.
        window_name="Al-Go" 
        
        self.model = dg.load_model(
            model_name=self.model_name,
            inference_host_address=self.inference_host_address,
            zoo_url=self.zoo_url,
            output_confidence_threshold=0.3,
            overlay_font_scale=2.5,
            overlay_show_probabilities=True
        )

        # Tracker for pedestrians (heads)
        self.tracker = degirum_tools.ObjectTracker(
            class_list=["head"],
            track_thresh=0.35,
            track_buffer=100,
            match_thresh=0.9999,
            trail_depth=20,
            anchor_point=degirum_tools.AnchorPoint.BOTTOM_CENTER,
        )

        # Zone counter for PWDs (mobility aid)
        polygon_zones = [
            [[0, 0], [0, 1080], [1925, 1080], [1925, 0]],    # Zone 1, This is the whole frame
        ]
        self.zone_counter = degirum_tools.ZoneCounter( #This counts the number of detected Mobility-Aids in the zone
            polygon_zones,
            class_list=["Mobility-Aid"],
            per_class_display=True,
            triggering_position=degirum_tools.AnchorPoint.CENTER,
            window_name=window_name,  # attach display window for interactive zone adjustment
        )

        # Attach both analyzers (tracker for pedestrians, zone counter for PWDs)
        degirum_tools.attach_analyzers(self.model, [self.tracker, self.zone_counter])

    def get_pedestrian_info(self, frame):
        pedestrian_count = 0
        passerby_count = 0
        zone1_pwd = 0
        try:
            for result in self.model.predict_batch([frame]):  # Run inference on the frame
                trails = result.trails

                # Pedestrian tracking (heads)
                for _, bboxes in trails.items():
                    if len(bboxes) >= 2:
                        x1_prev, y1_prev, x2_prev, y2_prev = bboxes[0]
                        x1_last, y1_last, x2_last, y2_last = bboxes[-1]
                        dx = ((x1_last + x2_last) / 2) - ((x1_prev + x2_prev) / 2)
                        dy = ((y1_last + y2_last) / 2) - ((y1_prev + y2_prev) / 2)
                        distance = (dx ** 2 + dy ** 2) ** 0.5
                        if distance <= 80:  # Movement threshold (Edit to your liking)
                            pedestrian_count += 1
                        else:
                            passerby_count += 1

                # PWD zone counting
                zone1_pwd = result.zone_counts[0].get("Mobility-Aid", 0)

            return pedestrian_count, passerby_count, zone1_pwd
        except KeyboardInterrupt:
            print("Pedestrian detection stopped.")
            return pedestrian_count, passerby_count, zone1_pwd

