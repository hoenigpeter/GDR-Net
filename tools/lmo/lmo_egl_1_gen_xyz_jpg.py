import os

os.environ["PYOPENGL_PLATFORM"] = "egl"
import os.path as osp
import sys

import mmcv
import numpy as np
from tqdm import tqdm

cur_dir = osp.abspath(osp.dirname(__file__))
PROJ_ROOT = osp.join(cur_dir, "../..")
sys.path.insert(0, PROJ_ROOT)
from lib.egl_renderer.egl_renderer_v3 import EGLRenderer
from lib.vis_utils.image import grid_show
from lib.pysixd import misc
from lib.utils.mask_utils import cocosegm2mask

import cv2

idx2class = {
    1: "ape",
    #  2: 'benchvise',
    #  3: 'bowl',
    #  4: 'camera',
    5: "can",
    6: "cat",
    #  7: 'cup',
    8: "driller",
    9: "duck",
    10: "eggbox",
    11: "glue",
    12: "holepuncher",
    #  13: 'iron',
    #  14: 'lamp',
    #  15: 'phone'
}
class2idx = {_name: _id for _id, _name in idx2class.items()}

classes = idx2class.values()
classes = sorted(classes)

# DEPTH_FACTOR = 1000.
IM_H = 480
IM_W = 640
near = 0.01
far = 6.5

data_dir = osp.normpath(osp.join(PROJ_ROOT, "datasets/BOP_DATASETS/lmo/test"))

scene_id = 2
scenes = [f"{scene_id:06d}"]
print(scenes)

cls_indexes = [_idx for _idx in sorted(idx2class.keys())]
cls_names = [idx2class[cls_idx] for cls_idx in cls_indexes]
lmo_model_dir = osp.normpath(osp.join(PROJ_ROOT, "datasets/BOP_DATASETS/lmo/models"))
model_paths = [osp.join(lmo_model_dir, f"obj_{cls_idx:06d}.ply") for cls_idx in cls_indexes]
texture_paths = None

K = np.array([[572.411363389757, 0, 325.2611083984375], [0, 573.5704328585578, 242.04899588216654], [0, 0, 1]])

xyz_root = osp.normpath(osp.join(data_dir, "xyz_crop"))
def normalize_to_01(img):
    if img.max() != img.min():
        return (img - img.min()) / (img.max() - img.min())
    else:
        return img


def get_emb_show(bbox_emb):
    show_emb = bbox_emb.copy()
    show_emb = normalize_to_01(bbox_emb)
    return show_emb


class XyzGen(object):
    def __init__(self):
        self.renderer = None

    def get_renderer(self):
        if self.renderer is None:
            self.renderer = EGLRenderer(
                model_paths,
                texture_paths=texture_paths,
                vertex_scale=0.001,
                height=IM_H,
                width=IM_W,
                znear=near,
                zfar=far,
                use_cache=True,
                gpu_id=int(args.gpu),
            )
            self.image_tensor = torch.cuda.FloatTensor(height, width, 4, device=device).detach()
            self.seg_tensor = torch.cuda.FloatTensor(height, width, 4, device=device).detach()
            self.pc_obj_tensor = torch.cuda.FloatTensor(height, width, 4, device=device).detach()
            self.pc_cam_tensor = torch.cuda.FloatTensor(height, width, 4, device=device).detach()
        return self.renderer

    def main(self, scene):
        gt_path = osp.join(data_dir, str(scene))
        gt_path = osp.join(gt_path, "scene_gt.json")
        mmcv.mkdir_or_exist(osp.dirname(gt_path))
        print(gt_path)
        assert osp.exists(gt_path)

        gt_dict = mmcv.load(gt_path)

        for target_obj_id in cls_indexes:
            for str_im_id, annos in tqdm(gt_dict.items()):
                int_im_id = int(str_im_id)
                im_path = osp.join(data_dir, f"rgb/{int_im_id:06d}.png")
                print(im_path)

                for anno_i, anno in enumerate(annos):
                    obj_id = anno["obj_id"]
                    if obj_id in cls_indexes and obj_id == target_obj_id:
                        # read Pose
                        #pose = np.array(anno["pose"])
                        save_path_temp = osp.join(xyz_root, str(obj_id))
                        mmcv.mkdir_or_exist(osp.dirname(save_path_temp))
                        save_path = osp.join(save_path_temp, f"{int_im_id:06d}.npy")
                        jpg_path = osp.join(save_path_temp, f"{int_im_id:06d}.jpg")
                        # if osp.exists(save_path) and osp.getsize(save_path) > 0:
                        #     continue
                        R = np.array(anno["cam_R_m2c"], dtype="float32").reshape(3, 3)
                        t = np.array(anno["cam_t_m2c"], dtype="float32") / 1000.0
                        pose = np.hstack([R, t.reshape(3, 1)])

                        K_th = torch.tensor(K, dtype=torch.float32, device=device)
                        R_th = torch.tensor(R, dtype=torch.float32, device=device)
                        t_th = torch.tensor(t, dtype=torch.float32, device=device)

                        cls_name = idx2class[obj_id]
                        render_obj_id = cls_indexes.index(obj_id)
                        self.get_renderer().render(
                            [render_obj_id],
                            pose,
                            K=K,
                            image_tensor=self.image_tensor,
                            seg_tensor=self.seg_tensor,
                            # pc_obj_tensor=self.pc_obj_tensor,
                            pc_cam_tensor=self.pc_cam_tensor,
                        )

                        mask = (self.seg_tensor[:, :, 0] > 0).to(torch.uint8)

                        if mask.sum() == 0:
                            imName = osp.basename(im_path)
                            print(f"not visible, cls {cls_name}, im {imName} obj {idx2class[obj_id]} {obj_id}")
                            xyz_info = {
                                "xyz_crop": np.zeros((IM_H, IM_W, 3), dtype=np.float16),
                                "xyxy": [0, 0, IM_W - 1, IM_H - 1],
                            }
                        else:
                            ys_xs = mask.nonzero(as_tuple=False)
                            ys, xs = ys_xs[:, 0], ys_xs[:, 1]
                            x1, y1 = [xs.min().item(), ys.min().item()]
                            x2, y2 = [xs.max().item(), ys.max().item()]

                            depth_th = self.pc_cam_tensor[:, :, 2].detach()
                            xyz_th = misc.calc_xyz_bp_torch(depth_th, R_th, t_th, K_th)
                            xyz_crop = xyz_th[y1 : y2 + 1, x1 : x2 + 1].cpu().numpy()

                            if xyz_crop.shape[0] > 15 and xyz_crop.shape[1] > 15:
                                xyz_info = {
                                    "xyz_crop": xyz_crop.astype("float16"),
                                    "xyxy": [x1, y1, x2, y2],
                                }

                                mmcv.mkdir_or_exist(osp.dirname(save_path))
                                xyz_crop_normalized = get_emb_show(xyz_crop)

                                scaled_image = xyz_crop_normalized * 255
                                
                                scaled_image = np.uint8(scaled_image)
                                cv2.imwrite(jpg_path, scaled_image)

                                np.save(save_path, xyz_crop)
                            
        if self.renderer is not None:
            self.renderer.close()


if __name__ == "__main__":
    import argparse
    import time

    import setproctitle
    import torch

    parser = argparse.ArgumentParser(description="gen lmo egl xyz")
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
        setproctitle.setproctitle("gen_xyz_lmo_egl")
        xyz_gen = XyzGen()
        xyz_gen.main(scene)
        T_end = time.perf_counter() - T_begin
        print("total time: ", T_end)
