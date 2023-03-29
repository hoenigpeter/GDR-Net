import os.path as osp
import random
import sys

import cv2
import mmcv
import numpy as np
from tqdm import tqdm

cur_dir = osp.abspath(osp.dirname(__file__))
PROJ_ROOT = osp.join(cur_dir, "../..")
sys.path.insert(0, PROJ_ROOT)
from core.utils.data_utils import get_2d_coord_np
from lib.pysixd import inout, misc
from lib.pysixd.pose_error import calc_rt_dist_m
from lib.utils import logger
from lib.vis_utils.image import grid_show
from lib.utils.mask_utils import cocosegm2mask


random.seed(2333)

idx2class = {
    1: "ape",
    2: "benchvise",
    3: "bowl",
    4: "camera",
    5: "can",
    6: "cat",
    7: "cup",
    8: "driller",
    9: "duck",
    10: "eggbox",
    11: "glue",
    12: "holepuncher",
    13: "iron",
    14: "lamp",
    15: "phone",
}

class2idx = {_name: _id for _id, _name in idx2class.items()}

classes = idx2class.values()
classes = sorted(classes)

# DEPTH_FACTOR = 1000.
IM_H = 480
IM_W = 640
near = 0.01
far = 6.5

data_dir = osp.normpath(osp.join(PROJ_ROOT, "datasets/BOP_DATASETS/lmo/train_pbr"))

scenes = [f"{i:06d}" for i in range(50)]
print(scenes)

cls_indexes = [_idx for _idx in sorted(idx2class.keys())]
cls_names = [idx2class[cls_idx] for cls_idx in cls_indexes]
lmo_model_dir = osp.normpath(osp.join(PROJ_ROOT, "datasets/BOP_DATASETS/lmo/models"))
model_paths = [osp.join(lmo_model_dir, f"obj_{cls_idx:06d}.ply") for cls_idx in cls_indexes]
texture_paths = None

xyz_root = osp.normpath(osp.join(data_dir, "xyz_crop"))
#gt_path = osp.join(data_dir, "gt.json")
#assert osp.exists(gt_path)

K = np.array([[572.4114, 0, 325.2611], [0, 573.57043, 242.04899], [0, 0, 1]])
DEPTH_FACTOR = 10000.0

coord2d = get_2d_coord_np(width=IM_W, height=IM_H, fmt="HWC")


def normalize_to_01(img):
    if img.max() != img.min():
        return (img - img.min()) / (img.max() - img.min())
    else:
        return img


def get_emb_show(bbox_emb):
    show_emb = bbox_emb.copy()
    show_emb = normalize_to_01(bbox_emb)
    return show_emb


def get_img_model_points_with_coords2d(mask_pred, xyz_pred, coord2d, im_H, im_W, max_num_points=-1, mask_thr=0.5):
    """
    from predicted crop_and_resized xyz, bbox top-left,
    get 2D-3D correspondences (image points, 3D model points)
    Args:
        mask_pred: HW, predicted mask in roi_size
        xyz_pred: HWC, predicted xyz in roi_size(eg. 64)
        coord2d: HW2 coords 2d in roi size
        im_H, im_W
        extent: size of x,y,z
    """
    coord2d = coord2d.copy()
    coord2d[:, :, 0] = coord2d[:, :, 0] * im_W
    coord2d[:, :, 1] = coord2d[:, :, 1] * im_H

    sel_mask = (
        (mask_pred > mask_thr)
        & (abs(xyz_pred[:, :, 0]) > 0.0001)
        & (abs(xyz_pred[:, :, 1]) > 0.0001)
        & (abs(xyz_pred[:, :, 2]) > 0.0001)
    )
    model_points = xyz_pred[sel_mask].reshape(-1, 3)
    image_points = coord2d[sel_mask].reshape(-1, 2)

    if max_num_points >= 4:
        num_points = len(image_points)
        max_keep = min(max_num_points, num_points)
        indices = [i for i in range(num_points)]
        random.shuffle(indices)
        model_points = model_points[indices[:max_keep]]
        image_points = image_points[indices[:max_keep]]
    return image_points, model_points


def get_pose_pnp_from_xyz_crop(emb_pred_, coord2d, im_H, im_W, K):
    # emb_pred_: emb_crop, HWC
    mask_pred = ((emb_pred_[:, :, 0] != 0) & (emb_pred_[:, :, 1] != 0) & (emb_pred_[:, :, 2] != 0)).astype("uint8")
    image_points, model_points = get_img_model_points_with_coords2d(mask_pred, emb_pred_, coord2d, im_H=im_H, im_W=im_W)
    pnp_method = cv2.SOLVEPNP_EPNP
    pose_est = misc.pnp_v2(
        model_points,
        image_points,
        K,
        method=pnp_method,
        ransac=True,
        ransac_reprojErr=3.0,
        ransac_iter=100,
    )
    return pose_est


class XyzVerify(object):
    def __init__(self):
        pass

    def main(self, scene):
        self.image_tensor = torch.cuda.FloatTensor(height, width, 4, device=device).detach()
        self.seg_tensor = torch.cuda.FloatTensor(height, width, 4, device=device).detach()
        self.pc_obj_tensor = torch.cuda.FloatTensor(height, width, 4, device=device).detach()
        self.pc_cam_tensor = torch.cuda.FloatTensor(height, width, 4, device=device).detach()
        
        gt_path = osp.join(data_dir, str(scene))
        gt_path = osp.join(gt_path, "scene_gt.json")
        mmcv.mkdir_or_exist(osp.dirname(gt_path))
        print(gt_path)
        assert osp.exists(gt_path)

        gt_dict = mmcv.load(gt_path)
        r_errors = []
        t_errors = []
        for str_im_id, annos in tqdm(gt_dict.items()):
            int_im_id = int(str_im_id)
            im_path = osp.join(data_dir, f"rgb/{int_im_id:06d}.jpg")

            for anno_i, anno in enumerate(annos):
                obj_id = anno["obj_id"]
                #pose = np.array(anno["pose"])
                save_path_temp = osp.join(xyz_root, str(scene))
                mmcv.mkdir_or_exist(osp.dirname(save_path_temp))
                save_path = osp.join(save_path_temp, f"{int_im_id:06d}_{anno_i:06d}-xyz.pkl")

                R = np.array(anno["cam_R_m2c"], dtype="float32").reshape(3, 3)
                t = np.array(anno["cam_t_m2c"], dtype="float32") / 1000.0
                pose = np.hstack([R, t.reshape(3, 1)])

                K_th = torch.tensor(K, dtype=torch.float32, device=device)
                R_th = torch.tensor(R, dtype=torch.float32, device=device)
                t_th = torch.tensor(t, dtype=torch.float32, device=device)

                #mask = cocosegm2mask(anno["mask_full"], IM_H, IM_W)
                #area = mask.sum()
                #if area < 4:  # NOTE: pnp need at least 4 points
                #    continue

                #save_path = osp.join(xyz_root, f"{int_im_id:06d}_{anno_i:06d}-xyz.pkl")
                assert osp.exists(save_path), save_path
                xyz = np.zeros((height, width, 3), dtype=np.float32)
                xyz_info = mmcv.load(save_path)
                x1, y1, x2, y2 = xyz_info["xyxy"]
                w = x2 - x1 + 1
                h = y2 - y1 + 1
                bbox_area = w * h
                xyz[y1 : y2 + 1, x1 : x2 + 1, :] = xyz_info["xyz_crop"]
                num_xyz_point = (abs(xyz) > 1e-6).sum()
                if num_xyz_point < 4 or bbox_area < 4:
                    #logger.warn(f"{save_path} num xyz point: {num_xyz_point} bbox_area: {bbox_area} mask_area: {area}")
                    logger.warn(f"{save_path} num xyz point: {num_xyz_point} bbox_area: {bbox_area}")
                    continue

                coord2d_crop = coord2d[y1 : y2 + 1, x1 : x2 + 1, :]
                try:
                    pose_est = get_pose_pnp_from_xyz_crop(
                        xyz_info["xyz_crop"].astype("float32"),
                        coord2d_crop,
                        im_H=IM_H,
                        im_W=IM_W,
                        K=K,
                    )
                except:
                    pose_est = get_pose_pnp_from_xyz_crop(
                        xyz_info["xyz_crop"].astype("float32"),
                        coord2d_crop,
                        im_H=IM_H,
                        im_W=IM_W,
                        K=K,
                    )
                    logger.warn(f"{save_path} num xyz point: {num_xyz_point} class: {idx2class[obj_id]} {obj_id}")

                    bgr = mmcv.imread(im_path, "color")

                    print(f"xyz min {xyz.min()} max {xyz.max()}")
                    print(xyz_info["xyz_crop"].shape, xyz_info["xyxy"])
                    show_ims = [
                        bgr[:, :, [2, 1, 0]],
                        get_emb_show(xyz),
                        get_emb_show(xyz_info["xyz_crop"].astype("float32")),
                        #mask,
                    ]

                    #show_titles = ["color", "xyz", "xyz_crop", "mask"]
                    show_titles = ["color", "xyz", "xyz_crop"]
                    grid_show(show_ims, show_titles, row=2, col=2)
                    raise
                re, te = calc_rt_dist_m(pose_est, pose)
                r_errors.append(re)
                t_errors.append(te)

                # CUSTOM STUFFI 
                bgr_gl = (self.image_tensor[:, :, :3].cpu().numpy() + 0.5).astype(np.uint8)
                mask = (self.seg_tensor[:, :, 0] > 0).to(torch.uint8)
                ys_xs = mask.nonzero(as_tuple=False)
                ys, xs = ys_xs[:, 0], ys_xs[:, 1]
                x1, y1 = [xs.min().item(), ys.min().item()]
                x2, y2 = [xs.max().item(), ys.max().item()]

                # xyz_th = self.pc_obj_tensor[:, :, :3].detach()
                depth_th = self.pc_cam_tensor[:, :, 2].detach()
                xyz_th = misc.calc_xyz_bp_torch(depth_th, R_th, t_th, K_th)
                xyz_crop = xyz_th[y1 : y2 + 1, x1 : x2 + 1].cpu().numpy()
                xyz_info = {
                    "xyz_crop": xyz_crop.astype("float16"),
                    "xyxy": [x1, y1, x2, y2],
                }

                if VIS:
                    xyz_th_cpu = xyz_th.cpu().numpy()
                    print(f"xyz min {xyz_th_cpu.min()} max {xyz_th_cpu.max()}")
                    show_ims = [
                        bgr_gl[:, :, [2, 1, 0]],
                        get_emb_show(xyz_th_cpu),
                        get_emb_show(xyz_crop),
                    ]
                    show_titles = ["bgr_gl", "xyz", "xyz_crop"]
                    grid_show(show_ims, show_titles, row=1, col=3)

                if not (re < 5 and te < 0.05):
                    #logger.warn(f"{save_path} re: {re}, te: {te} class: {idx2class[obj_id]} {obj_id} mask area: {area}")
                    logger.warn(f"{save_path} re: {re}, te: {te} class: {idx2class[obj_id]} {obj_id}")
        # stat results for this scene
        r_errors = np.array(r_errors)
        t_errors = np.array(t_errors)
        logger.info(f"r errors: min {r_errors.min()} max {r_errors.max()} mean {r_errors.mean()} std {r_errors.std()}")
        logger.info(f"t errors: min {t_errors.min()} max {t_errors.max()} mean {t_errors.mean()} std {t_errors.std()}")


if __name__ == "__main__":
    import argparse
    import time

    import setproctitle

    import torch

    parser = argparse.ArgumentParser(description="verify lmo_egl xyz")
    parser.add_argument("--gpu", type=str, default="0", help="gpu")
    parser.add_argument("--vis", default=False, action="store_true", help="vis")
    args = parser.parse_args()

    height = IM_H
    width = IM_W

    VIS = args.vis

    device = torch.device(int(args.gpu))
    dtype = torch.float32
    tensor_kwargs = {"device": device, "dtype": dtype}

    for scene in scenes:
        T_begin = time.perf_counter()
        setproctitle.setproctitle("verify xyz egl")
        xyz_gen = XyzVerify()
        xyz_gen.main(scene)
        T_end = time.perf_counter() - T_begin
        print("total time: ", T_end)
