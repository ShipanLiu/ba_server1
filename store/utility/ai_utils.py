
import yaml
import os


from django.conf import settings

from src.cleaner import Cleaner
from src.localizer import Localizer
from src.recognizer import Recognizer
from src.interpreter import Interpreter



# to generate the dynamic ymal file for running the ai models
def prepare_cfg(project_id, image_name, ai_model_id):

    # Extract the base file name without the extension
    base_image_name = os.path.splitext(image_name)[0]

    # Define the base paths
    base_media_path = settings.MEDIA_ROOT  # BASE_DIR/media
    base_output_path = os.path.join(base_media_path, 'outputs', f'project_{project_id}')  # BASE_DIR/media/outputs/project_1
    base_model_path = os.path.join(settings.BASE_DIR, 'store', 'ai', 'model_weights', 'weights')
    original_ai_outputs_path = os.path.join(settings.BASE_DIR, 'store', 'ai', 'outputs')

    # AI model files mapping based on ai_model_id
    # here will be a problem if you later add/delete the ai model
    ai_models = {
        1: 'best.pt',    # Assuming '1' corresponds to the 'best' model
        2: 'epoch_299.pt'  # And '2' corresponds to the 'epoch_299' model
    }

    # Select the AI model file based on ai_model_id
    model_file_name = ai_models.get(ai_model_id)
    if not model_file_name:
        raise ValueError(f'AI model with ID {ai_model_id} does not exist')

    # Define the configuration with dynamic paths
    cfg = {
        'input': {
            'image': os.path.join(base_media_path, f'project_{project_id}', image_name),
            'model': os.path.join(base_model_path, model_file_name)
        },
        'paths': {
            "general": {
                "output_path": os.path.join(base_output_path, base_image_name)
            },
            'text_detection': {
                "output_path": os.path.join(base_output_path, base_image_name, "text_detection"),
                "cache_path": os.path.join(base_output_path, base_image_name, "text_detection", "cache"),
                "cache_tiled_path": os.path.join(base_output_path, base_image_name, "text_detection", "cache", "tiled"),
                "cache_processed_path": os.path.join(base_output_path, base_image_name, "text_detection", "cache", "processed"),
                "cache_processed_labels_path": os.path.join(base_output_path, base_image_name, "text_detection", "cache", "processed", "labels"),
                "final_path": os.path.join(base_output_path, base_image_name, "text_detection", "final"),
                "final_visual_path": os.path.join(base_output_path, base_image_name, "text_detection", "final", "visual"),
                "final_original_path": os.path.join(base_output_path, base_image_name, "text_detection", "final", "original"),
            },
            'text_recognition': {
                "output_path": os.path.join(base_output_path, base_image_name, "text_recognition"),
                "cache_path": os.path.join(base_output_path, base_image_name, "text_recognition", "cache"),
                "cache_tiled_path": os.path.join(base_output_path, base_image_name, "text_recognition", "cache", "tiled"),
                "cache_processed_path": os.path.join(base_output_path, base_image_name, "text_recognition", "cache", "processed"),
                "cache_processed_labels_path": os.path.join(base_output_path, base_image_name, "text_recognition", "cache", "processed", "labels"),
                "final_path": os.path.join(base_output_path, base_image_name, "text_recognition", "final"),
                "final_visual_path": os.path.join(base_output_path, base_image_name, "text_recognition", "final", "visual"),
                "final_original_path": os.path.join(base_output_path, base_image_name, "text_recognition", "final", "original"),
            },
            'text_interpretation': {
                "output_path": os.path.join(base_output_path, base_image_name, "text_interpretation"),
                "cache_path": os.path.join(base_output_path, base_image_name, "text_interpretation", "cache"),
                "cache_tiled_path": os.path.join(base_output_path, base_image_name, "text_interpretation", "cache", "tiled"),
                "cache_processed_path": os.path.join(base_output_path, base_image_name, "text_interpretation", "cache", "processed"),
                "cache_processed_labels_path": os.path.join(base_output_path, base_image_name, "text_interpretation", "cache", "processed", "labels"),
                "final_path": os.path.join(base_output_path, base_image_name, "text_interpretation", "final"),
                "final_visual_path": os.path.join(base_output_path, base_image_name, "text_interpretation", "final", "visual"),
                "final_original_path": os.path.join(base_output_path, base_image_name, "text_interpretation", "final", "original"),
            },
        }
    }

    # Create only the final directories for the outputs
    for process in ['text_detection', 'text_recognition', 'text_interpretation']:
        # for cache
        os.makedirs(cfg['paths'][process]['cache_tiled_path'], exist_ok=True)
        os.makedirs(cfg['paths'][process]['cache_processed_labels_path'], exist_ok=True)

        # for final
        os.makedirs(cfg['paths'][process]['final_visual_path'], exist_ok=True)
        os.makedirs(cfg['paths'][process]['final_original_path'], exist_ok=True)

    # Write the configuration to a new yaml file within the output path
    cfg_file_path = os.path.join(base_output_path, base_image_name, 'cfg.yaml')
    with open(cfg_file_path, 'w') as cfg_file:
        yaml.safe_dump(cfg, cfg_file)

    return cfg_file_path





def run_ai_model(cfg_path):
    try:
        # Load the configuration
        with open(cfg_path, 'r') as cfg_file:
            cfg = yaml.safe_load(cfg_file)

        # Setup directories, clean up, etc.
        cleaner = Cleaner(cfg)
        cleaner.setup_dirs()
        cleaner.clean_dirs()

        # Load input image and run localizer
        localizer = Localizer(cfg)
        localizer.inference([cfg["input"]["image"]])

        # Run recognizer
        recognizer = Recognizer(cfg)
        recognizer.inference(cfg["paths"]["text_detection"]["final_path"])

        # Run interpreter
        interpreter = Interpreter(cfg)
        interpreter.inference(cfg["paths"]["text_recognition"]["final_path"])

        # You might want to return some results or status from this function
        return True
    except Exception as e:
        print(f"AI model processing failed: {e}")
        # Log the error for debugging
        return False










"""
'paths': {
            # Add additional paths as needed for text detection, recognition, and interpretation
            'text_detection': {
                # 'output_path': os.path.join(base_output_path, 'text_detection'),
                "cache_path": f"{original_ai_outputs_path}/text_detection/cache/",
                "cache_tiled_path": f"{original_ai_outputs_path}/text_detection/cache/tiled/",
                "cache_processed_path": f"{original_ai_outputs_path}/text_detection/cache/processed/",
                "cache_processed_labels_path": f"{original_ai_outputs_path}/text_detection/cache/processed/labels/",

                # for results.json
                "final_path": f"{base_output_path}/{base_image_name}/text_detection/",
                # for visulized image
                "final_visual_path": f"{base_output_path}/{base_image_name}/text_detection/",
                "final_original_path": f"{original_ai_outputs_path}/text_detection/final/original/",

            },
            'text_recognition': {
                # 'output_path': os.path.join(base_output_path, 'text_recognition'),
                "cache_path": f"{original_ai_outputs_path}/text_recognition/cache/",
                "cache_tiled_path": f"{original_ai_outputs_path}/text_recognition/cache/tiled/",
                "cache_processed_path": f"{original_ai_outputs_path}/text_recognition/cache/processed/",
                "cache_processed_labels_path": f"{original_ai_outputs_path}/text_recognition/cache/processed/labels/",

                # for results.json
                "final_path": f"{base_output_path}/{base_image_name}/text_recognition/",
                # for visulized image
                "final_visual_path": f"{base_output_path}/{base_image_name}/text_recognition/",
                "final_original_path": f"{original_ai_outputs_path}/text_recognition/final/original/",

            },
            'text_interpretation': {
                # 'output_path': os.path.join(base_output_path, 'text_interpretation'),
                "cache_path": f"{original_ai_outputs_path}/text_interpretation/cache/",
                "cache_tiled_path": f"{original_ai_outputs_path}/text_interpretation/cache/tiled/",
                "cache_processed_path": f"{original_ai_outputs_path}/text_interpretation/cache/processed/",
                "cache_processed_labels_path": f"{original_ai_outputs_path}/text_interpretation/cache/processed/labels/",

                # for results.json
                "final_path": f"{base_output_path}/{base_image_name}/text_interpretation/",
                # for visulized image
                "final_visual_path": f"{base_output_path}/{base_image_name}/text_interpretation/",
                "final_original_path": f"{original_ai_outputs_path}/text_interpretation/final/original/",

            },
        }

"""