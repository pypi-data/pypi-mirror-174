#!/usr/bin/env python
# -*- coding: utf-8 -*-

##############################################
# Copyright (C) 2014 by haogooder
##############################################

"""
Some snippets of opencv2

## Resize image
ref: <http://docs.opencv.org/modules/imgproc/doc/geometric_transformations.html#void
resize(InputArray src, OutputArray dst, Size dsize, double fx, double fy, int interpolation)>

    # half width and height
    small = cv2.resize(image, (0, 0), fx=0.5, fy=0.5)

    # to fixed Size
    small = cv2.resize(image, (100, 50))

## Constant
    1: cv2.IMREAD_COLOR
    0: cv2.IMREAD_GRAYSCALE
    -1: cv2.IMREAD_UNCHANGED

## Show image
    cv2.imshow('image title',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

## Generate a blank image
    size = (height, width, channels) = (512, 256, 3)
    img = np.zeros(size, np.uint8)

## Sort points
    pts = [(0, 7), (3, 5), (2, 6)]

    sorted(pts, key=lambda p: p[0]) # sort by point x row, expect [(0, 7), (2, 6), (3, 5)]

## Crop image
    croped = img[y0:y1, x0:x1]

"""
from typing import Any, Union, Optional, Tuple, List, Dict, Sequence, Mapping

import cv2
import numpy as np

__version__ = "0.1.x"  # 0.1.5 laster, version managed by pbr(tags) now
__project_url__ = ""

DEBUG = False
FEATURE_DEFAULT_THRESHOLD = 0.4


# def crop(img, (x0, y0), end=(0, 0), rect=(0, 0)):
#    ''' Crop image '''
#    (h, w) = img.shape[:2]
#    (x1, y1) = (w, h)
#    if end != (0, 0):
#        (x1, y1) = end
#    if rect != (0, 0):
#        (x1, y1) = (x0+rect[0], y0+rect[1])
#    (x1, y1) = min(max(x0, x1), w), min(max(y0, y1), h)
#    return img[y0:y1, x0:x1]

class MatchInfo:
    def __init__(self,
                 middle_point: Tuple[float, float],
                 confidence: float,
                 rectangle: Tuple[Tuple, ...] = None,):
        self.middle_point: Tuple[float, float] = middle_point
        self.rectangle: Tuple[Tuple, ...] = rectangle
        self.confidence: float = confidence

    def __str__(self):
        return str({
            "result": self.middle_point,
            "confidence": self.confidence
        })

    def __repr__(self):
        return str({
            "result": self.middle_point,
            "confidence": self.confidence
        })


# ======================================================================
# 模板匹配
# ======================================================================

def find_template(im_source, im_search, threshold=0.5, rgb=False, bgremove=False) -> MatchInfo:
    """
    @return find location
    if not found; return None

    :param im_source:
    :param im_search:
    :param threshold:
    :param rgb:
    :param bgremove:
    :return:
    """
    result = find_all_template(im_source, im_search, threshold, 1, rgb, bgremove)
    return result[0] if result else None


# noinspection PyUnresolvedReferences
def find_all_template(im_source: np.ndarray, im_search: np.ndarray, threshold: float = 0.5, max_cnt: int = 0,
                      rgb: bool = False, bg_remove: bool = False) -> List[MatchInfo]:
    """
    Locate image position with cv2.templateFind

    Use pixel match to find pictures.

    Args:
        im_source(string): 图像、素材
        im_search(string): 需要查找的图片
        threshold: 阈值，当相识度小于该阈值的时候，就忽略掉

    Returns:
        A tuple of found [(point, score), ...]

    Raises:
        IOError: when file read error

    :param im_source:
    :param im_search:
    :param threshold:
    :param max_cnt:
    :param rgb:
    :param bg_remove:
    :return:
    """
    # method = cv2.TM_CCORR_NORMED
    # method = cv2.TM_SQDIFF_NORMED
    method = cv2.TM_CCOEFF_NORMED

    if rgb:
        # Blue Green Red
        search_bgr = cv2.split(im_search)
        source_bgr = cv2.split(im_source)
        # 权重设置，几乎为三等分
        weight = (0.3, 0.3, 0.4)
        #
        rlt_bgr = [0, 0, 0]
        for i in range(3):
            rlt_bgr[i] = cv2.matchTemplate(source_bgr[i], search_bgr[i], method)
        rlt = rlt_bgr[0] * weight[0] + rlt_bgr[1] * weight[1] + rlt_bgr[2] * weight[2]
    else:
        search_gray = cv2.cvtColor(im_search, cv2.COLOR_BGR2GRAY)
        source_gray = cv2.cvtColor(im_source, cv2.COLOR_BGR2GRAY)
        # 边界提取(实现背景去除的功能)
        if bg_remove:
            search_gray = cv2.Canny(search_gray, 100, 200)
            source_gray = cv2.Canny(source_gray, 100, 200)

        rlt = cv2.matchTemplate(source_gray, search_gray, method)
    h, w = im_search.shape[:2]

    result = []
    while True:
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(rlt)
        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc
        if DEBUG:
            print('templmatch_value(thresh:%.1f) = %.3f' % (threshold, max_val))  # not show debug
        if max_val < threshold:
            break
        # 计算中点 calculator middle point
        middle_point = (top_left[0] + w / 2, top_left[1] + h / 2)
        # result.append(dict(
        #     result=middle_point,
        #     rectangle=(top_left, (top_left[0], top_left[1] + h), (top_left[0] + w, top_left[1]),
        #                (top_left[0] + w, top_left[1] + h)),
        #     confidence=max_val
        # ))
        rect = (top_left, (top_left[0], top_left[1] + h), (top_left[0] + w, top_left[1]),
                (top_left[0] + w, top_left[1] + h))
        result.append(MatchInfo(
            middle_point=middle_point,
            rectangle=rect,
            confidence=max_val
        ))
        if max_cnt and len(result) >= max_cnt:
            break
        # 淹没已发现的区域 floodfill the already found area
        cv2.floodFill(rlt, None, max_loc, (-1000,), max_val - threshold + 0.1, 1, flags=cv2.FLOODFILL_FIXED_RANGE)
    return result


# ======================================================================
# 特征匹配
# ======================================================================

# noinspection PyUnresolvedReferences
def _sift_instance(edge_threshold=100):
    # if hasattr(cv2, 'SIFT'):
    #     return cv2.SIFT(edgeThreshold=edge_threshold)
    return cv2.SIFT_create(edgeThreshold=edge_threshold)


def sift_count(img):
    sift = _sift_instance()
    key_points = sift.detect(img, None)
    key_points, desc = sift.compute(img, key_points)
    return len(key_points)


def find_sift(im_source, im_search, min_match_count=4):
    """
    SIFT特征点匹配
    """
    rlt = find_all_sift(im_source, im_search, min_match_count, max_cnt=1)
    if not rlt:
        return None
    return rlt[0]


FLANN_INDEX_KDTREE = 0


# noinspection PyUnresolvedReferences
def find_all_sift(img_source: np.ndarray, img_search: np.ndarray,
                  min_match_count: int = 4, max_cnt: int = 0,
                  thresold: float = FEATURE_DEFAULT_THRESHOLD) -> List[MatchInfo]:
    """
    使用sift算法进行多个相同元素的查找
    Args:
        im_source(string): 图像、素材
        im_search(string): 需要查找的图片
        threshold: 阈值，当相识度小于该阈值的时候，就忽略掉
        max_cnt: 限制匹配的数量

    Returns:
        A tuple of found [(point, rectangle), ...]
        A tuple of found [{"point": point, "rectangle": rectangle, "confidence": 0.76}, ...]
        rectangle is a 4 points list

    :param thresold:
    :param img_source:
    :param img_search:
    :param min_match_count:
    :param max_cnt:
    :return:
    """
    sift = _sift_instance()
    flann = cv2.FlannBasedMatcher({'algorithm': FLANN_INDEX_KDTREE, 'trees': 5}, dict(checks=50))

    # key_point description
    key_points = sift.detect(img_search, None)
    kp_sch, desc_sch = sift.compute(img_search, key_points)
    if len(kp_sch) < min_match_count:
        return []

    # key_point description
    key_points = sift.detect(img_source, None)
    kp_src, desc_src = sift.compute(img_source, key_points)
    if len(kp_src) < min_match_count:
        return []

    # h, w = img_search.shape[:2]

    result = []
    while True:
        # 匹配两个图片中的特征点，k=2表示每个特征点取2个最匹配的点
        matches = flann.knnMatch(desc_sch, desc_src, k=2)
        good = []
        for m, n in matches:
            # 剔除掉跟第二匹配太接近的特征点
            if m.distance < thresold * n.distance:
                good.append(m)

        if len(good) < min_match_count:
            break

        sch_pts = np.float32([kp_sch[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
        img_pts = np.float32([kp_src[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

        # M是转化矩阵
        M, mask = cv2.findHomography(sch_pts, img_pts, cv2.RANSAC, 5.0)
        matches_mask = mask.ravel().tolist()

        # 计算四个角矩阵变换后的坐标，也就是在大图中的坐标
        h, w = img_search.shape[:2]
        pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
        dst = cv2.perspectiveTransform(pts, M)

        # trans numpy arrary to python list
        # [(a, b), (a1, b1), ...]
        pypts = []
        for npt in dst.astype(int).tolist():
            pypts.append(tuple(npt[0]))

        lt, br = pypts[0], pypts[2]
        middle_point = (lt[0] + br[0]) / 2, (lt[1] + br[1]) / 2

        result.append(MatchInfo(
            middle_point=middle_point,
            rectangle=tuple(pypts),
            confidence=matches_mask.count(1) / len(good),
        ))

        if max_cnt and len(result) >= max_cnt:
            break

        # 从特征点中删掉那些已经匹配过的, 用于寻找多个目标
        qindexes, tindexes = [], []
        for m in good:
            qindexes.append(m.queryIdx)  # need to remove from kp_sch
            tindexes.append(m.trainIdx)  # need to remove from kp_src

        def filter_kp_index(indexes, arr):
            r = []
            for i, item in enumerate(arr):
                if i not in indexes:
                    r.append(item)
            return tuple(r)

        def filter_desc_index(indexes, arr):
            r = []
            for i, item in enumerate(arr):
                if i not in indexes:
                    r.append(item)
            return np.array(r)

        kp_src = filter_kp_index(tindexes, kp_src)
        desc_src = filter_desc_index(tindexes, desc_src)

    return result

# ======================================================================
# 入口函数
# ======================================================================


def find_all(im_source: np.ndarray, im_search: np.ndarray,
             max_cnt: int = 0, use_type: int = -1) -> List[MatchInfo]:
    """
    优先Template，之后Sift
    @ return [(x,y), ...]

    :param use_type:
    :param im_source:
    :param im_search:
    :param max_cnt:
    :return:
    """
    if use_type == 1:
        # 1
        result = find_all_template(im_source, im_search, max_cnt=max_cnt)
    elif use_type == 0:
        # 0
        result = find_all_sift(im_source, im_search, max_cnt=max_cnt)
    else:
        # -1 或者 default
        result = []
        result.extend(find_all_sift(im_source, im_search, max_cnt=max_cnt))
        result.extend(find_all_template(im_source, im_search, max_cnt=max_cnt))
    if not result:
        return []
    return result


def find(im_source: np.ndarray, im_search: np.ndarray) -> Optional[MatchInfo]:
    """
    Only find maximum one object
    """
    result = []
    result.extend(find_all_sift(im_source, im_search, max_cnt=1))
    result.extend(find_all_template(im_source, im_search, max_cnt=1))
    if not result:
        return None
    confidence_max = 0
    cur = None
    for i in result:
        if i.confidence > confidence_max:
            confidence_max = i.confidence
            cur = i.middle_point
    return MatchInfo(middle_point=cur, confidence=confidence_max)


# ======================================================================
# 工具函数
# ======================================================================
# noinspection PyUnresolvedReferences
def show(img: np.ndarray):
    """ 显示一个图片 """
    cv2.imshow('image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# noinspection PyUnresolvedReferences
def mark_point(img: np.ndarray, pt: Sequence):
    """ 调试用的: 标记一个点 """
    x, y = int(pt[0]), int(pt[1])
    # cv2.rectangle(img, (x, y), (x+10, y+10), 255, 1, lineType=cv2.CV_AA)
    radius = 6
    cv2.circle(img, (x, y), radius, 255, thickness=2)
    # cv2.line(img, (x - radius, y), (x + radius, y), 100)  # x line
    # cv2.line(img, (x, y - radius), (x, y + radius), 100)  # y line
    return img


# noinspection PyUnresolvedReferences
def imread(filename: str) -> np.ndarray:
    """
    Like cv2.imread
    This function will make sure filename exists
    """
    im = cv2.imread(filename)
    if im is None:
        raise RuntimeError("file: '%s' not exists" % filename)
    return im


# noinspection PyUnresolvedReferences
def brightness(im: np.ndarray):
    """
    获取图片亮度
    Return the brightness of an image
    Args:
        im(numpy): image

    Returns:
        float, average brightness of an image
    """
    im_hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(im_hsv)
    height, weight = v.shape[:2]
    total_bright = 0
    for i in v:
        total_bright = total_bright + sum(i)
    return float(total_bright) / (height * weight)


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    def main():
        # noinspection PyUnresolvedReferences
        def mark_point(img, pt):
            """ 调试用的: 标记一个点 """
            x, y = int(pt[0]), int(pt[1])
            # cv2.rectangle(img, (x, y), (x+10, y+10), 255, 1, lineType=cv2.CV_AA)
            radius = 10
            cv2.circle(img, (x, y), radius, 255, thickness=2)
            # cv2.line(img, (x - radius, y), (x + radius, y), 100)  # x line
            # cv2.line(img, (x, y - radius), (x, y + radius), 100)  # y line
            return img

        print(cv2.IMREAD_COLOR)
        print(cv2.IMREAD_GRAYSCALE)
        print(cv2.IMREAD_UNCHANGED)
        imsrc = imread('../tests/testdata/1s-rotate.png')
        imsch = imread('../tests/testdata/1t.png')
        print(brightness(imsrc))
        print(brightness(imsch))
        pt = find(imsrc, imsch)
        print(pt)
        imsrc = mark_point(imsrc, pt.middle_point)
        show(imsrc)

        imsrc = imread('../tests/testdata/2s.png')
        imsch = imread('../tests/testdata/2t.png')
        result = find_all_template(imsrc, imsch)
        print(result)
        pts = []
        for match in result:
            pt = match.middle_point
            imsrc = mark_point(imsrc, pt)
            pts.append(pt)
        # pts.sort()
        show(imsrc)
        # print pts
        # print sorted(pts, key=lambda p: p[0])

        imsrc = imread('../tests/testdata/1s-rotate.png')
        imsch = imread('../tests/testdata/1t.png')
        print('SIFT count=', sift_count(imsch))
        print(find_sift(imsrc, imsch))
        print("")
        print(find_all_sift(imsrc, imsch))
        print(find_all_template(imsrc, imsch))
        print(find_all(imsrc, imsch))
        for pt in find_all(imsrc, imsch):
            imsrc = mark_point(imsrc, pt.middle_point)
        show(imsrc)


    main()
