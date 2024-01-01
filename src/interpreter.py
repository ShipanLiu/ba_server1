import os
import re

os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"   # see issue #152
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

import json
import logging
import os
import zipfile
from pathlib import Path
from zipfile import ZipFile

import numpy as np
import pandas as pd

from matplotlib import pyplot as plt
from PIL import Image, ImageDraw
from sklearn.cluster import DBSCAN


class Floor:
    def __init__(self, rooms):
        self.rooms = rooms
    
    def to_list(self):
        data = []
        for room in self.rooms:
            data.append({
                'name': room.name,
                'code': room.code,

                'wand_material': room.wand_material,
                'boden_material': room.boden_material,
                'decken_material': room.decken_material,

                'umfang': room.umfang,
                'flaeche': room.flaeche,
                'hoehe': room.hoehe,
                'fenster_flaeche': room.fenster_flaeche,

                'einheit_laenge': room.einheit_laenge,
                'einheit_flaeche': room.einheit_flaeche,

                'position_on_drawing': room.position_on_drawing,

            })
        
        return data

class Room:
    """
    Repräsentiert ein Raumobjekt mit den folgenden Inhalten:

    :param: nummer: Raumnummer
    :type: int

    :param: name: Raumname, gibt eventuell die Nutzung an
    :type: str

    :param: code: Raumcode, kann die Raumnummer, die Nummer innerhalb einer Etage, die Wohnungsnummmer oder die
    Wohnungsnummer innerhalb einer Etage enthalten
    :type: str

    :param: wand_material: Wandmaterial des Raums
    :type: str

    :param: boden_material: Bodenmaterial des Raums
    :type: str

    :param: decken_material: Deckenmaterial des Raums
    :type: str

    :param: umfang: Raumumfang angegeben in einheit_laenge
    :type: float

    :param: flaeche: Raumfläche angegeben in einheit_flaeche
    :type: float

    :param: hoehe: Raumhoehe angegeben in einheit_laenge
    :type: float

    :param: fenster_flaeche: Fensterfläche angegeben in einheit_flaeche
    :type: float

    :param: einheit_laenge: Längeneinheit für alle Längenangaben (Umfang und Höhe)
    :type: str

    :param: einheit_flaeche: Flächeneinheit für alle Flächenangaben (Fläche und Fensterfläche)
    :type: str
    """

    def __init__(self, nummer=None, name=None, code=None, wand_material=None, boden_material=None,
                 decken_material=None, umfang=None, flaeche=None, hoehe=None, fenster_flaeche=None, einheit_laenge=None,
                 einheit_flaeche=None, position_on_drawing=None):

        # Eingaben prüfen
        assert type(nummer) == int or nummer is None, f'nummer sollte integer sein, ist aber: {type(nummer)}'
        assert type(name) == str or name is None, f'name sollte sting sein, ist aber: {type(name)}'
        assert type(code) == str or code is None, f'code sollte sting sein, ist aber: {type(code)}'

        assert type(wand_material) == str or wand_material is None, f'wand_material sollte sting sein, ist aber: ' \
                                                                    f'{type(wand_material)}'
        assert type(boden_material) == str or wand_material is None, f'boden_material sollte sting sein, ' \
                                                                     f'ist aber: {type(boden_material)}'
        assert type(decken_material) == str or decken_material is None, f'decken_material sollte sting sein, ist ' \
                                                                        f'aber: {type(decken_material)}'
        assert type(umfang) == float or umfang is None, f'umfang sollte float sein, ist aber: {type(umfang)}'
        assert type(flaeche) == float or flaeche is None, f'flaeche sollte float sein, ist aber: {type(flaeche)}'
        assert type(hoehe) == float or hoehe is None, f'hoehe sollte float sein, ist aber: {type(hoehe)}'
        assert type(fenster_flaeche) == float or fenster_flaeche is None, f'fenster_flaeche sollte float sein, ' \
                                                                          f'ist aber: {type(fenster_flaeche)}'
        assert type(einheit_laenge) == str or einheit_laenge is None, f'einheit_laenge sollte sting sein, ist aber: ' \
                                                                      f'{type(einheit_laenge)}'
        assert type(einheit_flaeche) == str or einheit_flaeche is None, f'einheit_flaeche sollte ein sting sein, ' \
                                                                        f'ist aber: {type(einheit_flaeche)}'

        # Eingaben speichern
        self.nummer = nummer
        self.name = name
        self.code = code

        self.wand_material = wand_material
        self.boden_material = boden_material
        self.decken_material = decken_material

        self.umfang = umfang
        self.flaeche = flaeche
        self.hoehe = hoehe
        self.fenster_flaeche = fenster_flaeche

        self.einheit_laenge = einheit_laenge
        self.einheit_flaeche = einheit_flaeche

        self.position_on_drawing = position_on_drawing

    # String Methode überschreiben, um den Raumstempel ausgeben zu können
    def __str__(self):
        return "Nummer: " + str(self.nummer) + "\n" + "Name: " + str(self.name) + "\n" + "Code: " + str(self.code) + \
               "\n" + "Wandmaterial: " + str(self.wand_material) + "\n" + "Bodenmaterial: " + str(self.boden_material)\
               + "\n" + "Deckenmaterial: " + str(self.decken_material) + "\n" + "Umfang: " + str(self.umfang) + "\n" + \
               "Fläche: " + str(self.flaeche) + "\n" + "Höhe: " + str(self.hoehe) + "\n" + "Fensterfläche: " \
               + str(self.fenster_flaeche) + "\n" + "Längeneinheit: " + str(self.einheit_laenge) + "\n" + \
               "Flächeneinheit: " + str(self.einheit_flaeche) + "\n" + "Position auf Plan: " + str(self.position_on_drawing) + "\n"


class TextFieldFinder:

    def __init__(self, data):

        self.data = data
    
    def find_text_fields(self):
        # for each image, go through text elements
        for image_filename in self.data:
            _, cluster_labels = self.get_cluster_labels(self.data[image_filename]["elements"])
            clusters = self.get_clusters(cluster_labels)
            
            # add clusters to data
            self.add_text_fields_to_data(clusters, image_filename)
        return self.data

    def get_cluster_labels(self, list_of_elements, height_factor=2, min_samples=2):
        """
        Clusters a list of elements based on their bounding box coordinates using
        DBSCAN algorithm.

        :param list_of_elements: A list of dictionary elements, each containing a
            bounding box coordinates.
        :type list_of_elements: list

        :param height_factor: A factor to determine the epsilon distance for
            DBSCAN clustering. Default is 2.
        :type height_factor: int or float

        :param min_samples: The minimum number of samples required to form a 
            luster. Default is 2.
        :type min_samples: int

        :return: A tuple of the positions (upper left corner) of the elements and
            their corresponding labels.
        :rtype: tuple
        """

        points_list = []
        text_heights = []
        for element in list_of_elements:
            x1, y1, x2, y2 = element["bbox_xyxy_abs"]
            points_list.append((x1, y1))
            text_heights.append(abs(y2 - y1))

        mean_text_height = np.mean(text_heights)
        epsilon = mean_text_height * height_factor

        points_list = np.array(points_list)
        clustering = DBSCAN(eps=epsilon, min_samples=min_samples).fit(points_list)
        labels = clustering.labels_
        
        return points_list, labels

    def get_clusters(self, cluster_labels):
        clusters = []
        unique_labels = set(cluster_labels)
        
        for label in unique_labels:
            if label == -1:
                # Points that were not assigned to a cluster
                continue

            else:
                # Points that belong to the current cluster
                cluster_ids = np.where(cluster_labels == label)
                clusters.append(cluster_ids[0])
        return clusters


    def add_text_fields_to_data(self, clusters, image_filename):

        text_fields = []
        for cluster in clusters:

            text_field = {
                "text_snippet_guids": [],
                "text_snippets": [],
                "class": None,
                "position": None,
            }

            first_in_cluster = True
            for e in cluster:

                # get element from input data
                text_element_guid = self.data[image_filename]["elements"][e]["guid"]
                text_field["text_snippet_guids"].append(text_element_guid)

                text_element = self.data[image_filename]["elements"][e]["text"]
                text_field["text_snippets"].append(text_element)

                if first_in_cluster:
                    text_field["position"] = self.data[image_filename]["elements"][e]["bbox_xyxy_abs"]
                    first_in_cluster = False

                # do for last element, such that the last element defines the lower right corner
                if e == cluster[-1]:
                    text_field["position"][2] = self.data[image_filename]["elements"][e]["bbox_xyxy_abs"][2]
                    text_field["position"][3] = self.data[image_filename]["elements"][e]["bbox_xyxy_abs"][3]
            
            text_fields.append(text_field)

        self.data[image_filename]["fields"] = text_fields

        return


class Interpreter:

    def __init__(self, config):

        self.config = config

        # dirs
        self.final_path = self.config["paths"]["text_interpretation"]["final_path"]

    def to_dataframe(self, text_fields):
        snippets = []
        field_ids = []
        field_positions = []

        for i, text_field in enumerate(text_fields):

            first_of_field = True

            for snippet in text_field["text_snippets"]:

                snippets.append(snippet)

                if first_of_field:
                    field_ids.append("Raumstempel " + str(i))
                    first_of_field = False

                    field_positions.append(text_field["position"])

                else:
                    field_ids.append(None)
                    field_positions.append(None)
        
        # make dataframe
        zipped = list(zip(field_ids, snippets, field_positions))
        df = pd.DataFrame(zipped, columns=["Raumstempel", "Wort", "Position"])

        return df

    def clean_detections(self, rooms, text_field_dataframe):

        cleaned_rooms = []

        for i, room in enumerate(rooms):

            if room.name is None or room.code is None:
                continue

            # get position from original input table
            stamp_string = "Raumstempel " + str(i)
            idx = text_field_dataframe.index[text_field_dataframe['Raumstempel'] == stamp_string]
            position = list(text_field_dataframe.loc[idx]['Position'])[0]

            room.position_on_drawing = position

            cleaned_rooms.append(room)
        
        return cleaned_rooms


    def preprocess(self, fields):

        cleaned_fields = []

        for field in fields:

            if field["text_snippets"] is None:
                continue

            if len(field["text_snippets"]) < 2:
                continue
            
            cleaned_fields.append(field)
        
        return cleaned_fields

    def visualize(self, image, floor):

        # Initialize the drawing context
        draw = ImageDraw.Draw(image)

        # Define the box colors
        color = (0, 0, 255, 128)
        outline = (0, 0, 0)

        # Define font size
        font_size = 12

        # Draw the boxes with text on the image
        for i, room in enumerate(floor):

            # Extract the position of the box
            box_position = tuple(room["position_on_drawing"])
            arrow_start = (int((box_position[0] + box_position[2]) / 2), box_position[3])

            # Draw an unfilled colored rectangle around the specified position
            try:
                draw.rectangle(box_position, outline=(255, 0, 0), width=2)
            except:
                pass
            
            # Extract the text to display in the box
            text_lines = []
            max_line_length = 0
            for key, value in room.items():
                if value is not None and key != "position_on_drawing":
                    line = f"{key}: {value}"
                    text_lines.append(line)
                    max_line_length = max(max_line_length, draw.textlength(line))
            text = "\n".join(text_lines)

            # Calculate the size of the box based on the text
            box_width = max_line_length + 20
            box_height = font_size * 1.5 * text.count("\n") + 20

            # Adjust the position of the box to fit the text
            text_position = (box_position[0], box_position[3] + 10)
            box_position = (box_position[0], box_position[3] + 18, box_position[0] + box_width, box_position[3] + 18 + box_height)

            # Does the extra box fit the image?
            h, w = draw.im.size
            #if (box_position[0] < 0) or (box_position[1] < 0) or (box_position[2] > w) or (box_position[3] > h):
            #    continue

            # Draw the box with a filled color and an outline
            draw.rectangle(box_position, fill=color, outline=outline)

            # Draw the text on the image
            x = box_position[0] + 10
            y = box_position[1] + 10
            draw.text((x, y), text, fill=(255, 255, 255))

            # Connect the boxes
            draw.line((arrow_start[0], arrow_start[1], arrow_start[0], box_position[1]), fill=(255, 0, 0), width=2)

        # Return the modified image
        return image


    def inference(self, input_path):
        
        input_file = "results.json"
        with open(str(Path(input_path, input_file))) as in_file:
            data = json.load(in_file)
        
        finder = TextFieldFinder(data)
        data = finder.find_text_fields()

        floors = {}
        for image in data:

            # save original file
            print(image)
            original = Image.open(str(Path(input_path, "original", image)))
            original.save(str(Path(self.final_path, "original", image)))

            image_data = self.preprocess(data[image]["fields"])
            text_field_dataframe = self.to_dataframe(image_data)

            preds = self.parse_room_info_df(text_field_dataframe)
            print(preds)

            # discard all rooms without name
            rooms = self.clean_detections(preds, text_field_dataframe)

            # create floor object
            floor = Floor(rooms)
            floors[image] = floor.to_list()

            # save visualization file
            visual = self.visualize(original, floors[image])
            visual.save(str(Path(self.final_path, "visual", image)))

        # export floors
        result_path = str(Path(self.final_path, "floor.json"))
        with open(result_path, 'w') as out_file:
            json.dump(floors, out_file, indent=4)
        out_file.close()

        with open(result_path, encoding='utf-8') as inputfile:
            df = pd.read_json(inputfile)
        result_path = str(Path(self.final_path, "floor.csv"))
        df.to_csv(result_path, encoding='utf-8', index=False)
        
        return

    def parse_room_info_df(self, df):
        parsed_info = []
        current_lines = None
        
        for i, row in df.iterrows():
            if row['Raumstempel']:
                if current_lines:
                    info = self.parse_room_info(current_lines)
                    if info:
                        parsed_info.append(info)
                current_lines = []
            if row['Wort']:
                current_lines.append(row['Wort'])
        
        if current_lines:
            info = self.parse_room_info(current_lines)
            if info:
                parsed_info.append(info)
        
        return parsed_info

    def parse_room_info(self, lines):

        code_regex = r'^[0-9]{1,2}(\.[A-Z]?[A-Z0-9]{2,3}|\-[0-9]{1,2}(\.[A-Z]?[A-Z0-9]{2,3})?|[0-9]{1,2}[a-z])$'
        # name_regex = r'^(?!^\d+$)\w+(\s\w+)?$'
        name_regex = r'^(?!^\d+$)[\w\s?!:-]+$'
        area_regex = r'^(\d+(\.\d+)?)\s?([\w\d]+)$'
        height_regex = r'^RH\.?:\s?(\d+(\.\d+)?)\s?([a-zA-Z]+)$'
        
        code = None
        name = None
        area_value = None
        area_unit = None
        height_value = None
        height_unit = None
        
        for line in lines:
            line = line.strip()
            if re.match(code_regex, line):
                code = line
            elif re.match(name_regex, line):
                name = line
            elif re.match(area_regex, line):
                area_match = re.match(area_regex, line)
                area_value = float(area_match.group(1))
                area_unit = area_match.group(3)
            elif re.match(height_regex, line):
                height_match = re.match(height_regex, line)
                height_value = float(height_match.group(1))
                height_unit = height_match.group(3)

        room = Room(
            nummer=None,
            name=name,
            code=code,
            wand_material=None,
            boden_material=None,
            decken_material=None,
            umfang=None,
            flaeche=area_value,
            hoehe=height_value,
            fenster_flaeche=None,
            einheit_laenge=height_unit,
            einheit_flaeche=area_unit,
            position_on_drawing=None
        )
        return room
