import traceback

import pandas as pd
import numpy as np
import pickle
import torch
import requests
from io import BytesIO
from sklearn.cluster import KMeans
from collections import Counter
from PIL import Image
from transformers import DetrFeatureExtractor, DetrForSegmentation, \
    SegformerFeatureExtractor, SegformerForImageClassification
from social_net_img_classifier.settings import COCO_CATEGORIES, FEATURES, MODEL_IMG_DIR, MODEL_TEXT_DIR, MODEL_TEXT_BERT_DIR, TOP_OBJECTS
from social_net_img_classifier.training import TrainClassModel, TrainClfTextModel
from social_net_img_classifier.aws_utils import AwsS3


class ClassifyImg:
    """
    :Date: 2022-10-27
    :Version: 0.4
    :Authors: Joan Felipe Mendoza - David Prada - Whale & Jaguar Consultants S.A.S.
    :Description: CLASIFICAR UNA IMAGEN USANDO UN MODELO PRE-ENTRENADO
    """
    def __init__(self, img, features=FEATURES):
        """
        :Description: inicializar proceso y preparar datos para clasificar
        :param img: dirección de la imagen, o la imagen en formato PIL
        :param features: lista de variables independientes numéricas (:type: list)
        """
        self.img_pil = GetFeaturesImg(img)
        self.model = pickle.load(open(MODEL_IMG_DIR, "rb"))
        self.colors = {} #img_pil.colors()
        self.features = features

    def predict_ml(self):
        """
        :Description: clasificar la imagen usando un modelo pre-entrenado de Machine Learning
        :return: clase predecida
        """
        detr_obj = self.img_pil.objects_detr()
        objects = {f: detr_obj[f] if f in detr_obj else 0 for f in self.features}
        df_objects = pd.DataFrame([objects])[self.features]
        df_colors = pd.DataFrame()  # pd.DataFrame([self.colors])
        df = pd.concat([df_objects, df_colors], axis=1)
        return TrainClassModel.predict(self.model, df)[0], detr_obj

    def predict(self):
        """
        :Description: clasificar la imagen
        :return: clase predecida
        """
        detr_obj = self.img_pil.objects_detr()
        # Si no hay personas en los objetos detr, no es de interés
        if "person" not in detr_obj:
            return 0, detr_obj, {}
        # Revisar objetos segformer
        segformer_obj = self.img_pil.objects_segformer()
        obj0 = {k: segformer_obj[k] for k in segformer_obj if k in TOP_OBJECTS["SEGFORMER_0"]}
        obj1 = {k: segformer_obj[k] for k in segformer_obj if k in TOP_OBJECTS["SEGFORMER_1"]}
        score0 = max(obj0.values()) if obj0 else 0
        score1 = max(obj1.values()) if obj1 else 0
        if score0 > score1:
            return 0, detr_obj, segformer_obj
        if score1 > score0:
            return 1, detr_obj, segformer_obj
        # Revisar objetos detr
        for obj in TOP_OBJECTS["DETR_1"]:
            if obj in detr_obj:
                return 1, detr_obj, segformer_obj
        return 0, detr_obj, segformer_obj


class ClassifyText:
    """
    :Date: 2022-09-20
    :Version: 0.3
    :Authors: Joan Felipe Mendoza - David Prada - Whale & Jaguar Consultants S.A.S.
    :Description: CLASIFICAR TEXTO USANDO UN MODELO PRE-ENTRENADO
    """
    def __init__(self, model_type="traditional"):
        self.model_type = model_type
        if model_type == "bert":
            self.model = pickle.loads(AwsS3().read_file(MODEL_TEXT_BERT_DIR))
        else:
            self.model = pickle.load(open(MODEL_TEXT_DIR, "rb"))

    def predict(self, texts, clean_mode="normal"):
        """
        :description: predecir texto
        :param texts: textos crudos (:type: list)
        :param clean_mode: método de limpieza (pre-procesamiento) -'normal', 'stemma', 'lemma' o None-
        :return: predicción (:type: string)
        """
        if self.model_type == "bert":
            preds, _ = self.model.predict([str(t).lower() for t in texts])
        else:
            preds = TrainClfTextModel.predict(self.model, texts, clean_mode=clean_mode)
        return preds


class GetFeaturesImg:
    """
    :Date: 2022-09-23
    :Version: 0.4
    :Authors: Joan Felipe Mendoza - David Prada - Oscar Riojas - Whale & Jaguar Consultants S.A.S.
    :Description: HERRAMIENTAS AUXILIARES PARA EXTRACCIÓN DE INFORMACIÓN DESDE IMÁGENES
    """
    def __init__(self, img):
        self.img_pil = self.read_img(img)

    @staticmethod
    def read_img(img):
        try:
            if isinstance(img, str):
                if img[:4] == "http":
                    response = requests.get(img)
                    image = Image.open(BytesIO(response.content))
                else:
                    image = Image.open(img)
            else:
                image = img
        except Exception:
            traceback.print_exc()
            image = Image.new("RGB", (256, 256), (255, 255, 255))
        return image

    def objects_detr(self, model_name="facebook/detr-resnet-50-panoptic"):
        try:
            obj_img = {}
            feature_extractor = DetrFeatureExtractor.from_pretrained(model_name)
            model = DetrForSegmentation.from_pretrained(model_name)
            encoding = feature_extractor(images=self.img_pil, return_tensors="pt")
            outputs = model(**encoding)
            processed_sizes = torch.as_tensor(encoding['pixel_values'].shape[-2:]).unsqueeze(0)
            results = feature_extractor.post_process_panoptic(outputs, processed_sizes)[0]
            data_img = results.get('segments_info')
            data_img = pd.DataFrame(data_img)
            if len(data_img):
                obj_img = dict(Counter(data_img["category_id"]))
                obj_img = {COCO_CATEGORIES[k]: v for k, v in obj_img.items()}
        except Exception:
            print(f"objects_detr: problemas con modelo {model_name} detectando objetos.")
            obj_img = {}
        return obj_img

    def objects_segformer(self, model_name="nvidia/mit-b2", top_labels=10):
        try:
            feature_extractor = SegformerFeatureExtractor.from_pretrained(model_name)
            model = SegformerForImageClassification.from_pretrained(model_name)
            inputs = feature_extractor(images=self.img_pil, return_tensors="pt")
            outputs = model(**inputs)
            logits = outputs.logits
            logits = logits.sort(stable=True, descending=True)
            scores = logits[0].tolist()[0]
            labels = logits[1].tolist()[0]
            data_img = {model.config.id2label[labels[i]]: scores[i] for i in range(len(scores))}
            obj_img = {k.replace("'", "").replace(",", " -"): data_img[k] for k in list(data_img)[:top_labels]}
        except Exception:
            print(f"objects_segformer: problemas con modelo {model_name} detectando objetos.")
            obj_img = {}
        return obj_img

    def colors(self, number_of_colors=10):
        try:
            image = self.img_pil.resize((256, 256))
            image = np.array(image)
            modified_image = image.reshape(image.shape[0] * image.shape[1], 3)
            clf = KMeans(n_clusters=number_of_colors)
            labels = clf.fit_predict(modified_image)
            counts = Counter(labels)
            # sort to ensure correct color percentage
            counts = dict(sorted(counts.items()))
            center_colors = clf.cluster_centers_
            # We get ordered colors by iterating through the keys
            ordered_colors = [center_colors[i] for i in counts.keys()]
            int_colors = np.array(ordered_colors).astype(int)
            dict_colors = pd.Series(list(np.concatenate(int_colors, axis=None))).to_dict()
        except Exception:
            print(f"colors: problemas detectando colores.")
            dict_colors = {}
        return dict_colors
