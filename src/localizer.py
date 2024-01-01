import json
import os
from pathlib import Path
import subprocess
from uuid import uuid4
import cv2
from tiler import Merger, Tiler
import torch


class Localizer:
    
    def __init__(self, config):
        
        self.config = config
        print(config)
        self.model = self.config["input"]["model"]

    def inference(self, filenames, tile_size=640):

        # ---------------------------- PREPROCESSING --------------------------- #
        # dirs
        cache_path = self.config["paths"]["text_detection"]["cache_path"]
        cache_tiled_path = self.config["paths"]["text_detection"]["cache_tiled_path"]
        cache_processed_path = self.config["paths"]["text_detection"]["cache_processed_path"]
        cache_processed_labels_path = self.config["paths"]["text_detection"]["cache_processed_labels_path"]
        final_output_path = self.config["paths"]["text_detection"]["final_path"]
        final_output_path_visual_results = self.config["paths"]["text_detection"]["final_visual_path"]
        final_output_path_original_images = self.config["paths"]["text_detection"]["final_original_path"]
        
        model = self.config["input"]["model"]
        
        # tile images
        tilers_dict = {}
        for filename in filenames:
            
            # read and tile image
            img = cv2.imread(filename)
            
            filename = filename.split("/")[-1]

            tiler = Tiler(data_shape=img.shape,
                        tile_shape=(tile_size, tile_size, 3),
                        channel_dimension=2)
            tilers_dict[filename] = tiler  # save for merger

            for tile_id, tile in tiler(img):
                filename_tile = (Path(filename).stem
                                + "_tile_" + str(tile_id) + ".png")
                save_path_tile = Path(cache_tiled_path, filename_tile)
                cv2.imwrite(str(save_path_tile), tile)
            
            # save original image for later services in output dir
            original_image_filename_img = str(Path(
                final_output_path_original_images, 
                filename
            ))
            cv2.imwrite(original_image_filename_img, img)

        # ---------------------------- INFERENCE ------------------------------- #
        # modified by shipanliu because no navdia gpu installed on mac-mini
        # print("Device = ", torch.cuda.get_device_name())
        if torch.cuda.is_available():
            print("Device = ", torch.cuda.get_device_name())
        else:
            print("CUDA not available, using CPU")

        subprocess.run(['python3', 'src/yolov7/detect.py',
            '--weights', model,
            '--source', str(cache_tiled_path),
            '--project', str(cache_path),
            '--augment',
            '--name', 'processed',
            '--img-size', str(tile_size),
            '--conf-thres', '0.25',
            '--iou-thres', '0.45',
            '--device', '0',
            '--save-txt',
            '--save-conf',
            '--augment',
            '--exist-ok',
            '--no-trace'
        ])

        # ---------------------------- POSTPROCESSING -------------------------- #

        # setup output dictionary with the following structure
        output = {}

        # merge processed tiles
        for filename in filenames:
            
            img = cv2.imread(filename)
            filename = filename.split("/")[-1]
            

            elements = []

            tiler = tilers_dict[filename]
            merger = Merger(tiler)
            

            # loop (processed) tiles of the original file
            for tile_id, tile in tiler(img):

                # get processed tile and add to merger
                filename_tile = (Path(filename).stem
                                + "_tile_" + str(tile_id) + ".png")
                save_path_tile = Path(cache_processed_path, filename_tile)
                img_processed = cv2.imread(str(save_path_tile))
                merger.add(tile_id, img_processed)

                # get labels from txt file and add to global labels file
                filename_tile_txt = (Path(filename).stem
                                    + "_tile_" + str(tile_id) + ".txt")
                save_path_tile_txt = Path(cache_processed_labels_path,
                                        filename_tile_txt)

                if not os.path.isfile(save_path_tile_txt):
                    continue  # no preds found in this tile, move on

                with open(save_path_tile_txt, 'r') as in_file:
                    labels_txt = in_file.readlines()


                    # test stuff
                    print(tiler.get_tile_bbox(tile_id))
                    print(tiler.get_mosaic_shape())
                    print(tiler.get_tile_mosaic_position(tile_id))

                    # transform to global coords 
                    # get bottom-left coords (attention: tiler uses different origin)
                    x_min = min(
                        tiler.get_tile_bbox(tile_id)[0][1],
                        tiler.get_tile_bbox(tile_id)[1][1]
                    )

                    x_max = max(
                        tiler.get_tile_bbox(tile_id)[0][1],
                        tiler.get_tile_bbox(tile_id)[1][1]
                    )

                    y_min = min(
                        tiler.get_tile_bbox(tile_id)[0][0],
                        tiler.get_tile_bbox(tile_id)[1][0]
                    )

                    y_max = max(
                        tiler.get_tile_bbox(tile_id)[0][0],
                        tiler.get_tile_bbox(tile_id)[1][0]
                    )

                    # get width and height of tile
                    w = x_max - x_min
                    h = y_max - y_min
                    
                    print(x_min, y_min, x_max, y_max)
                    print(w, h)

                    for line in labels_txt:
                        fields = line.split()
                        class_id = fields[0]
                        confidence = fields[5]

                        if float(confidence) < 0.5:
                            continue

                        x1 = int(((float(fields[1]) - float(fields[3])/2.0) * w) + x_min)
                        y1 = int(((float(fields[2]) - float(fields[4])/2.0) * h) + y_min)
                        x2 = int(((float(fields[1]) + float(fields[3])/2.0) * w) + x_min)
                        y2 = int(((float(fields[2]) + float(fields[4])/2.0) * h) + y_min)
                        
                        # add line to global labels file
                        elements.append({
                            "guid": str(uuid4()),
                            "class_id": class_id,
                            "confidence": confidence,
                            "bbox_xyxy_abs": [x1, y1, x2, y2]
                        })

            # save final merge
            final_image = merger.merge(unpad=True)
            output_filename_img = str(Path(
                final_output_path_visual_results,
                filename
            ))

            if not cv2.imwrite(output_filename_img, final_image):
                raise Exception("Image could not be saved: {}".format(output_filename_img))

            # sort text elements by coordinate, going from image top to bottom
            elements = sorted(elements, key=lambda item: item["bbox_xyxy_abs"][1], reverse=False)

            output[filename] = {
                "visual_result_path": "visual/" + output_filename_img.split("/")[-1],
                "elements": elements            
            }

        # save output as json
        result_path = str(Path(final_output_path, "results.json"))
        with open(result_path, "w+") as out_file:
            json.dump(output, out_file)
        out_file.close()

        return