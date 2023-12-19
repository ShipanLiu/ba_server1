import json
import logging
import os
import zipfile
from pathlib import Path
from zipfile import ZipFile

import cv2
import torch
from PIL import Image
from .parseq.strhub.data.module import SceneTextDataModule

class Recognizer:
    
    def __init__(self, config):
        
        self.config = config

        # Load model and image transforms
        # self.device = "cuda:0" #modified by shipan
        self.device = torch.device('cpu')
        self.parseq = torch.hub.load('baudm/parseq', 'parseq', pretrained=True).eval()
        self.parseq.to(self.device)
        self.img_transform = SceneTextDataModule.get_transform(self.parseq.hparams.img_size)

        # dirs
        self.cache_path = self.config["paths"]["text_recognition"]["cache_path"]
        self.final_path = self.config["paths"]["text_recognition"]["final_path"]

    def make_snippets_from_images_and_coords(self, input_path, cache_path):
        '''Processes results from the previous text localization
        service, in particular, this function expects the following file structure:
        input_file/
            - original/ --> from here, snippets are taken
            - visual/
            results.json --> snippets are defined in here
        '''
        
        # Get image files
        filenames = [filename for filename in os.listdir(input_path)
                    if filename.endswith(".json")]
        logging.info("Number of found image files: "+ str(len(filenames)))
        input_json = filenames[0]

        with open(str(Path(input_path, input_json))) as in_file:
            data = json.load(in_file)

            # for each image, create snippets
            for image_filename in data:

                # get the image
                image_path = str(Path(input_path, "original", image_filename))
                img = cv2.imread(image_path)
                w, h = img.shape[1], img.shape[0]

                # get text snippets with conf over threshold
                for i, element in enumerate(data[image_filename]["elements"]):

                    bbox_xyxy_abs = element['bbox_xyxy_abs']
                        
                    snippet = img[
                        int(bbox_xyxy_abs[1]):int(bbox_xyxy_abs[3]),
                        int(bbox_xyxy_abs[0]):int(bbox_xyxy_abs[2]),
                        :
                    ]
                    snippet_path = str(Path(cache_path, Path(image_filename).stem + "_snippet_{}".format(str(i)) + ".png"))

                    # save abs coords
                    data[image_filename]["elements"][i]["bbox_xyxy_abs"] = bbox_xyxy_abs
                    
                    # save snippet
                    data[image_filename]["elements"][i]["snippet"] = snippet
                    
                    logging.info("Saving snippet at {}".format(snippet_path))
        
        return data
    

    def inference(self, input_path):

        # ---------------------------- PREPROCESSING --------------------------- #
        # gather images
        data = self.make_snippets_from_images_and_coords(
            input_path,
            self.cache_path)

        # iterate input images
        for image_filename in data:

            logging.info("Load original image ...")
            visual_result = cv2.imread(str(Path(input_path, "original", image_filename)))
            logging.info("Save original image for further processing ...")
            cv2.imwrite(
                str(Path(self.final_path, "original", image_filename)),
                visual_result
            )
            
            logging.info("Iterate text snippets...")
            # iterate text snippets per image
            for i, element in enumerate(data[image_filename]["elements"]):
                
                logging.info("Recognizing snippet ...")

                # get snippet path and load snippet
                # snippet_path = element["snippet_path"]
                # img = Image.open(str(Path(cache_path, snippet_path))).convert('RGB')
                
                # load snippet
                snippet = cv2.cvtColor(element["snippet"], cv2.COLOR_BGR2RGB)
                img = Image.fromarray(snippet)
            
                # Preprocess. Model expects a batch of images with shape: (B, C, H, W)
                img = self.img_transform(img).unsqueeze(0).to(self.device)

                logits = self.parseq(img)
                logits.shape  # torch.Size([1, 26, 95]), 94 characters + [EOS] symbol

                # Greedy decoding
                pred = logits.softmax(-1)
                label, confidence = self.parseq.tokenizer.decode(pred)

                data[image_filename]["elements"][i]["text"] = label[0]
                
                # make visual result
                cv2.putText(
                    img=visual_result,
                    text=label[0],
                    org=(element['bbox_xyxy_abs'][0],element['bbox_xyxy_abs'][1]),
                    fontFace=cv2.FONT_HERSHEY_DUPLEX,
                    fontScale=1,
                    color=(255,0,0)
                )

                cv2.rectangle(
                    visual_result,
                    (element['bbox_xyxy_abs'][0], element['bbox_xyxy_abs'][1]),
                    (element['bbox_xyxy_abs'][2], element['bbox_xyxy_abs'][3]),
                    color=(255,0,0),
                    thickness=1
                )

                cv2.imwrite(
                    str(Path(self.final_path, "visual", image_filename)),
                    visual_result
                )
        
                # Pop snippet from output dict
                data[image_filename]["elements"][i].pop("snippet")
                
        # save output as json
        logging.info("Save results ...")
        result_path = str(Path(self.final_path, "results.json"))
        with open(result_path, "w+") as out_file:
            json.dump(data, out_file)
        out_file.close()

        return