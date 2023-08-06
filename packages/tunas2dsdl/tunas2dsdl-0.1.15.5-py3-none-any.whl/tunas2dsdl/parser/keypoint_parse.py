from ..general import Field, Struct, DataSample, Util, ClassDomain, Label
from tqdm import tqdm
from .base_parse import BaseParse
from ..io import FileIO
from collections import defaultdict


class KeyPoint2DParse(BaseParse):

    def parse_class_domain(self):

        label_domain_info = dict()  # {task_uid: class_domain}
        keypoint_domain_info = defaultdict(dict)  # {task_uid: {category_id: class_domain}}
        raw_task_info = defaultdict(dict)  # {task_uid: {category_id: category_info_dic}}
        parent_class_domain = ClassDomain(FileIO.clean(f"{self._dataset_name}{self.PARENT_PATTERN}ClassDom"))
        for task in tqdm(self._data_info["tasks"], desc="parsing class domain..."):
            task_name, task_type, task_source, catalog = task['name'], task["type"], task['source'], task["catalog"]
            task_uid = f"{task_type}${task_name}${task_source}"
            if task_type not in (self.KEYPOINT2D_ANN_TYPE, self.DETECTION_ANN_TYPE, self.INSTANCE_SEG_ANN_TYPE):
                # keypoint 任务内只考虑 keypoint2d, box2d, polygon三种标注内容
                continue
            # this_class_domain只用来保存当前task表示的domain
            this_class_domain = ClassDomain(self.parse_domain_name(task_uid)[0])
            label_domain_info[task_uid] = this_class_domain
            for category_info in catalog:
                # 每个category可能包含一个keypoint class domain
                category_id, category_name = category_info["category_id"], category_info["category_name"]
                raw_task_info[task_uid][category_id] = category_info
                supercategories = category_info.get("supercategories", [])
                this_label = Label(category_name)
                this_class_domain.add_label(this_label, ori_id=category_id)

                for super_cat in supercategories:
                    super_label = Label(super_cat)
                    parent_class_domain.add_label(super_label)
                    this_label.add_supercategory(super_label)
                    this_class_domain.set_parent(parent_class_domain)

                if category_info.get("point_names") and category_info.get("skeleton"):
                    # 如果是keypoint任务
                    points_names, skeleton = category_info["point_names"], category_info["skeleton"]
                    domain_name = f"KeyPoint_{category_name}_ClassDom"
                    this_point_domain = ClassDomain(domain_name)
                    this_point_domain.set_parent(this_class_domain)
                    keypoint_domain_info[task_uid][category_id] = this_point_domain
                    for point_ind, point_name in enumerate(points_names, start=1):
                        this_point_label = Label(point_name)
                        this_point_label.add_supercategory(this_label)
                        this_point_domain.add_label(this_point_label, ori_id=point_ind)
                    this_point_domain.set_attributes("skeleton", skeleton)
        return parent_class_domain, (label_domain_info, keypoint_domain_info), raw_task_info, None

    def parse_ann_info(self):
        samples = self._annotation_info["samples"]
        sample_struct = Struct("KeyPointSample")  # 样本 struct
        object_struct = Struct("KeyPointLocalObject")  # 目标struct
        media_field = Field("media", field_type="media")  # 图像 field
        sample_struct.add_field(media_field)  # 添加图像field
        sample_container = DataSample(sample_struct, None)  # 暂时不添加 class domain
        domain_info = {}  # true_task_uid: domain
        parent_domain_info = {} # true_task_uid: parent_domain
        field_args = {}  # true_task_uid: arg
        for sample in tqdm(samples, desc="parsing samples ...."):
            sample_item = {}  # 存储当前样本信息
            media_info = sample["media"]
            img_path = media_info.pop("path")
            sample_item["media"] = img_path  # 添加图像样本信息
            for k, v in media_info.items():  # 添加图像相关的attributes
                this_field = Field(k, field_value=v, is_attr=True)
                sample_struct.add_field(this_field)
                sample_item[k] = v

            if "ground_truth" in sample:
                gt_info = sample["ground_truth"]
            else:
                gt_info = []
                # sample_struct.set_optional("annotations")
            gt_info_dic = {}  # ann_id: {gt}
            for gt in gt_info:
                # 获取ann_id
                task_type, task_name, ann_source = gt.pop("type"), gt.pop("name"), gt.pop("source")
                if task_type not in (self.INSTANCE_SEG_ANN_TYPE, self.DETECTION_ANN_TYPE, self.KEYPOINT2D_ANN_TYPE):
                    continue

                ann_id = gt.pop("ann_id")
                ann_id = gt.pop("ref_ann_id", ann_id)
                gt_info_dic.setdefault(ann_id, {})
                gt_item = gt_info_dic[ann_id]
                task_uid = f"{task_type}${task_name}${ann_source}"

                # 写attributes
                attributes = gt.pop("attributes", {})
                for attr_k, attr_v in attributes.items():
                    attr_k = Util.clean(attr_k)
                    attr_field = Field(attr_k, field_value=attr_v, is_attr=True)
                    object_struct.add_field(attr_field, optional=True)
                    gt_item[attr_k] = attr_v

                if task_type == self.KEYPOINT2D_ANN_TYPE:

                    category_id = gt.pop("category_id")
                    domain_uid = f"{task_uid}_{category_id}"
                    this_domain = self._class_domain[1][task_uid][category_id]
                    this_parent_domain = self._class_domain[0][task_uid]
                    parent_domain_uid = f"parent_{domain_uid}"
                    arg = None
                    for _k, _d in domain_info.items():
                        if this_domain == _d:
                            arg = field_args[_k]
                    if arg is None:
                        arg = f"cdom{len(field_args)}"
                        domain_info[domain_uid] = this_domain
                        field_args[domain_uid] = arg
                        parent_domain_info[parent_domain_uid] = this_parent_domain

                    keypoint_field = Field("keypoints", field_type="keypoint", param=f"${arg}")
                    gt_item["keypoints"] = gt.pop("points")
                    object_struct.add_field(keypoint_field)

                elif task_type in (self.DETECTION_ANN_TYPE, self.INSTANCE_SEG_ANN_TYPE):
                    if 'categories' in gt and len(gt['categories']) > 0:
                        ori_category_id = gt.pop("categories")[0]["category_id"]
                        this_domain = self._class_domain[0][task_uid]
                        category_name = this_domain.index_by_ori_id(ori_category_id).name
                        gt_item["category"] = this_domain.index(category_name)
                        arg = None
                        for _k, _d in domain_info.items():
                            if _d == this_domain:  # 如果domain中所有的类别名称都一样则认为是一样的
                                arg = field_args[_k]
                        if arg is None:
                            arg = f"cdom{len(field_args)}"
                            domain_info[task_uid] = this_domain
                            field_args[task_uid] = arg

                        label_field = Field("category", field_type="category", param=f"${arg}")
                        object_struct.add_field(label_field)
                    else:
                        gt.pop("categories", [])

                    if task_type == self.DETECTION_ANN_TYPE:
                        bbox_field = Field("bbox", field_type="bbox")
                        object_struct.add_field(bbox_field)
                        gt_item["bbox"] = gt.pop("bbox")
                    else:
                        ins_field = Field("points", field_type="points")
                        object_struct.add_field(ins_field)
                        gt_item["points"] = gt.pop("points")

            annotations = list(gt_info_dic.values())
            if annotations:
                sample_item["annotations"] = annotations

            sample_container.add_item(sample_item, not self.separate_flag)

        args = []
        domains = []
        for uid in field_args:
            domains.append(domain_info[uid])
            args.append(field_args[uid])

        if len(object_struct.fields):  # 如果有 object field的话
            if args:
                object_struct.set_arg(args)
                sample_struct.set_arg(args)
                sample_container.set_domain(domains)
            annotation_field = Field("annotations", field_type="list",
                                     param=object_struct.as_others_param(sample_struct))
            sample_struct.add_field(annotation_field)
            class_domains = list(domain_info.values())
            parent_class_domains = list(parent_domain_info.values())
            return (object_struct, sample_struct), [self._parent_class_domain] + parent_class_domains + class_domains, sample_container
        return (sample_struct,), [], sample_container
