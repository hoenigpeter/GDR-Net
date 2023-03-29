import argparse
import os
import sys
from pathlib import Path

import cv2
import numpy as np
import torch
import torch.backends.cudnn as cudnn

import rospy
from std_msgs.msg import String, Float32MultiArray, Int64
from sensor_msgs.msg import Image
from sensor_msgs.msg import RegionOfInterest
from vision_msgs.msg import Detection2DArray
from vision_msgs.msg import Detection2D
from vision_msgs.msg import BoundingBox2D
from vision_msgs.msg import ObjectHypothesisWithPose
from geometry_msgs.msg import Pose2D
from cv_bridge import CvBridge, CvBridgeError

import numpy as np

import rospy
from std_msgs.msg import Header
from object_detector_msgs.msg import BoundingBox, Detection, Detections, PoseWithConfidence
from object_detector_msgs.srv import detectron2_service_server, estimate_poses, estimate_posesResponse
from geometry_msgs.msg import Pose, Point, Quaternion

import os
import os.path as osp
cur_dir = osp.dirname(osp.abspath(__file__))
sys.path.insert(0, osp.join(cur_dir, "../../"))
import ref
from mmcv import Config
from core.utils.data_utils import crop_resize_by_warp_affine, get_2d_coord_np, read_image_cv2, xyz_to_region
from core.gdrn_modeling.data_loader import GDRN_DatasetFromList
from detectron2.data import MetadataCatalog
from detectron2.data import get_detection_dataset_dicts
from lib.pysixd import inout, misc
from pytorch_lightning.lite import LightningLite

import json

if __name__ == "__main__":

    cfg = Config.fromfile("config.py")
    print(f"Used GDRN module name: {cfg.MODEL.CDPN.NAME}")
    model, optimizer = eval(cfg.MODEL.CDPN.NAME).build_model_optimizer(cfg)

    def normalize_image(cfg, image):
        # image: CHW format
        pixel_mean = np.array(cfg.MODEL.PIXEL_MEAN).reshape(-1, 1, 1)
        pixel_std = np.array(cfg.MODEL.PIXEL_STD).reshape(-1, 1, 1)
        return (image - pixel_mean) / pixel_std

    def get_extents(cfg, roi_classes):
        f = open('../../datasets/BOP_DATASETS/ycbv/models/models_info.json')
  
        # returns JSON object as 
        # a dictionary
        data = json.load(f)
        
        # Iterating through the json
        # list
        print(data[str(roi_classes[0])]['size_x'])
  

        return [data[str(roi_classes[0])]['size_x'], data[str(roi_classes[0])]['size_y'], data[str(roi_classes[0])]['size_z']]
    
    def estimate_pose(req):
        print("request detection...")

        # === IN ===
        # --- rgb
        detection = req.det
        rgb = req.rgb
        depth = req.depth

        width, height = rgb.width, rgb.height
        assert width == 640 and height == 480

        try:
            image = CvBridge().imgmsg_to_cv2(rgb, "bgr8")
        except CvBridgeError as e:
            print(e)

        roi_classes = [int(detection.name)]

        im_H, im_W = image_shape = image.shape[:2]
        coord_2d = get_2d_coord_np(im_W, im_H, low=0, high=1).transpose(1, 2, 0)
        print(coord_2d)
        x1, y1, x2, y2 = detection.bbox.xmin, detection.bbox.ymin, detection.bbox.xmax, detection.bbox.ymax
        bbox_center = np.array([0.5 * (x1 + x2), 0.5 * (y1 + y2)])
        bw = max(x2 - x1, 1)
        bh = max(y2 - y1, 1)
        scale = max(bh, bw) * cfg.INPUT.DZI_PAD_SCALE
        scale = min(scale, max(im_H, im_W)) * 1.0

        input_res = cfg.MODEL.CDPN.BACKBONE.INPUT_RES
        out_res = cfg.MODEL.CDPN.BACKBONE.OUTPUT_RES

        roi_img = crop_resize_by_warp_affine(
            image, bbox_center, scale, input_res, interpolation=cv2.INTER_LINEAR
        ).transpose(2, 0, 1)      

        roi_img = normalize_image(cfg, roi_img)

        roi_coord_2d = crop_resize_by_warp_affine(
                coord_2d, bbox_center, scale, out_res, interpolation=cv2.INTER_LINEAR
            ).transpose(
                2, 0, 1
            )  # HWC -> CHW
        roi_extents = get_extents(cfg, roi_classes)
        roi_img = torch.as_tensor(np.array(roi_img)).contiguous()
        roi_wh = np.array([bw, bh], dtype=np.float32)
        print(int(detection.name))

        #YCBV Cam: [1066.778, 0.0, 312.9869079589844, 0.0, 1067.487, 241.3108977675438, 0.0, 0.0, 1.0]
        #Intel RealSense D435 from /camera/color/camera_info    [606.6173706054688, 0.0, 322.375, 0.0, 605.2778930664062, 232.67811584472656, 0.0, 0.0, 1.0]
        roi_cam = [[[606.6173706054688, 0.0, 322.375], [0.0, 605.2778930664062, 232.67811584472656], [0.0, 0.0, 1.0]]]

        roi_center = bbox_center.astype("float32")
        resize_ratio = out_res / scale
        roi_coord_2d = roi_coord_2d.astype("float32")
        estimates = []
        estimate = PoseWithConfidence()
        estimate.name = detection.name
        estimate.confidence = detection.score

        # ------------------------------------------------------------------------------------#
        print("roi_img: ", roi_img)
        print("roi_classes: ", roi_classes)
        print("roi_cam: ", roi_cam)
        print("roi_wh: ", roi_wh)
        print("roi_center: ", roi_center)
        print("resize_ratios: ", resize_ratio)
        print("roi_coord_2d: ", roi_coord_2d)
        print("roi_extents: ", roi_extents)
        # print("roi_img: ", batch["roi_img"].cpu().numpy().shape)
        # print("roi_classes: ", batch["roi_cls"].cpu().numpy().shape)
        # print("roi_cam: ", batch["roi_cam"].cpu().numpy().shape)
        # print("roi_wh: ", batch["roi_wh"].cpu().numpy().shape)
        # print("roi_centers: ", batch["roi_center"].cpu().numpy().shape)
        # print("resize_ratios: ", batch["resize_ratio"].cpu().numpy().shape)
        # print("roi_coord_2d: ", batch.get("roi_coord_2d", None).cpu().numpy().shape)
        # print("roi_extents: ", batch.get("roi_extent", None).cpu().numpy().shape)
        
        # ------------------------------------------------------------------------------------#
        # estimate.pose = Pose()
        # estimate.pose.position.x = 0.5
        # estimate.pose.position.y = -0.1
        # estimate.pose.position.z = 1.0
        # # Make sure the quaternion is valid and normalized
        # estimate.pose.orientation.x = 0.0
        # estimate.pose.orientation.y = 0.0
        # estimate.pose.orientation.z = 0.0
        # estimate.pose.orientation.w = 1.0
        estimates.append(estimate)
        response = estimate_posesResponse()
        response.poses = estimates

        return response

    rospy.init_node("gdrn_estimation")
    s = rospy.Service("estimate_pose_gdrn", estimate_poses, estimate_pose)
    print("Pose Estimation with GDRNet is ready.")

    rospy.spin()
