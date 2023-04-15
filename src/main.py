import cv2
import numpy as np
import open3d as o3d
import pandas as pd
from matplotlib import pyplot as plt

from src.project_on_image import project_on_image


def it(image_name):
    # image = cv2.imread("C:\\Users\\dimen\\point-classifier\\data\\images\\pano_000006_000070.jpg")
    image = cv2.cvtColor(
        cv2.imread(f"C:\\Users\\dimen\\point-classifier-clear\\data\\images\\{image_name}.jpg"), cv2.COLOR_BGR2RGB
    )
    colorless_point_cloud = o3d.io.read_point_cloud(
        "C:\\Users\\dimen\\point-classifier-clear\\data\\point-clouds\\lamp_post.ply"
    )
    df = pd.read_csv("C:\\Users\\dimen\\cv\\HazzaStad-09-06-2020\\panorama\\reference.csv", sep="\t")
    df = df.loc[df["file_name"] == image_name]
    cx, cy, cz = df["projectedX[m]"].values[0], df["projectedY[m]"].values[0], df["projectedZ[m]"].values[0]
    roll, pitch, heading = df["roll[deg]"].values[0], df["pitch[deg]"].values[0], df["heading[deg]"].values[0]
    # image[0:4000, 0:8000] = [0, 0, 0]
    points = []
    for point in colorless_point_cloud.points:
        projected_point = project_on_image(point, np.array([cx, cy, cz]), np.array([roll, pitch, heading]))
        points.append(projected_point)
    points = np.array([(point[0], point[1]) for point in points])
    for point1, point2 in zip(points, points[1:]):
        cv2.line(image, point1, point2, [255, 0, 0], 2)
    # image = cv2.resize(image, (800, 400))
    # cv2.imshow("img", image)
    # cv2.waitKey()
    # cv2.destroyAllWindows()
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    cv2.imwrite(f"C:\\Users\\dimen\\point-classifier-clear\\data\\projected_images\\{image_name}_projected.jpg", image)


if __name__ == "__main__":
    for i in range(60, 86):
        it(f"pano_000006_0000{i}")
