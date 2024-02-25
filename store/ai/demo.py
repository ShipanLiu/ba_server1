import yaml
from src.cleaner import Cleaner
from src.localizer import Localizer
from src.recognizer import Recognizer
from src.interpreter import Interpreter

# Setup directories, clean up, etc.
cfg = yaml.safe_load(open('cfg2.yaml'))
cleaner = Cleaner(cfg)
cleaner.setup_dirs()
cleaner.clean_dirs()

# Load input image
localizer = Localizer(cfg)
localizer.inference([cfg["input"]["image"]])
recognizer = Recognizer(cfg)
recognizer.inference(cfg["paths"]["text_detection"]["final_path"])
interpreter = Interpreter(cfg)
interpreter.inference(cfg["paths"]["text_recognition"]["final_path"])