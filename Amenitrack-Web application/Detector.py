from detectron2.engine import DefaultPredictor
from detectron2.utils.logger import setup_logger

setup_logger()
from detectron2.config import get_cfg
from detectron2.utils.visualizer import ColorMode, Visualizer
from detectron2 import model_zoo
import cv2


class Metadata:
    def get(self, _):
        return ["Amenities", "B-Hoop", "BBQ", "Bathtub", "Billiards table", "Blender",
                "Chair", "Coffemaker", "Couch", "Crib", "Dish Washer", "Fireplace",
                "Hair dryer", "Jacuzzi", "LoungerChaise", "Microwave", "Refrigerator",
                "Shower", "Stand Mixer", "Stove", "Swimming_Pool", "Table", "Toaster", "Umbrella",
                "baking oven", "bed", "bed side table", "dresser", "foosball table",
                "sink", "table lamp", "television", "wall clock"]


class Detector:
    def __init__(self):
        ARCHITECTURE = "mask_rcnn_R_101_FPN_3x"
        CONFIG_FILE_PATH = f"COCO-InstanceSegmentation/{ARCHITECTURE}.yaml"
        NUM_CLASSES = 33
        self.cfg = get_cfg()
        self.cfg.merge_from_file(model_zoo.get_config_file(CONFIG_FILE_PATH))
        self.cfg.MODEL_WEIGHTS = model_zoo.get_checkpoint_url(CONFIG_FILE_PATH)
        self.cfg.MODEL.ROI_HEADS.BATCH_SIZE_PER_IMAGE = 32
        self.cfg.DATALOADER.NUM_WORKERS = 2
        self.cfg.SOLVER.IMS_PER_BATCH = 4
        self.cfg.INPUT.MASK_FORMAT = 'bitmask'
        self.cfg.MODEL.ROI_HEADS.NUM_CLASSES = NUM_CLASSES
        self.cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.8
        self.cfg.MODEL.WEIGHTS = './model/detectron2_model.pth'
        self.cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.8
        self.cfg.MODEL.DEVICE = 'cpu'
        self.predictor = DefaultPredictor(self.cfg)

    def onImage(self, imagePath):
        image = cv2.imread(imagePath)
        predictions = self.predictor(image)
        viz = Visualizer(image[:, :, ::-1], Metadata,
                         scale=1.2, instance_mode=ColorMode.IMAGE_BW)
        output = viz.draw_instance_predictions(predictions['instances'].to('cpu'))
        filename = 'result.jpg'
        cv2.imwrite(filename, output.get_image()[:, :, ::-1])
        metadata_instance = Metadata()
        item_list = metadata_instance.get(None)
        new_list = []
        for data in predictions["instances"].pred_classes:
            new_list.append(item_list[data.item()])
        #cv2.imshow("Result",output.get_image()[:,:,::-1])
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()
        return new_list



