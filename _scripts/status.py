from globox import AnnotationSet


yolo = AnnotationSet.from_yolo_v5(
    folder="/gpfs/scratch/rayen/YOLOv8/datasets/wood/labels/train/",
    image_folder="/gpfs/scratch/rayen/YOLOv8/datasets/wood/images/train/"
)

yolo.show_stats()