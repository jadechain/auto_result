def compute_iou(rec1, rec2):
    """
    computing IoU
    :param rec1: (y0, x0, y1, x1), which reflects
            (top, left, bottom, right)
    :param rec2: (y0, x0, y1, x1)
    :return: scala value of IoU
    """
    # computing area of each rectangles
    S_rec1 = (rec1[2] - rec1[0]) * (rec1[3] - rec1[1])
    S_rec2 = (rec2[2] - rec2[0]) * (rec2[3] - rec2[1])

    # computing the sum_area
    sum_area = S_rec1 + S_rec2

    # find the each edge of intersect rectangle
    left_line = max(rec1[1], rec2[1])
    right_line = min(rec1[3], rec2[3])
    top_line = max(rec1[0], rec2[0])
    bottom_line = min(rec1[2], rec2[2])

    # judge if there is an intersect
    if left_line >= right_line or top_line >= bottom_line:
        return 0
    else:
        intersect = (right_line - left_line) * (bottom_line - top_line)
        return (intersect / (sum_area - intersect)) * 1.0


def compute_iou2(rec1, rec2):
    areas1 = (int(rec1[3]) - int(rec1[1])) * (int(rec1[2]) - int(rec1[0]))
    areas2 = (int(rec2[3]) - int(rec2[1])) * (int(rec2[2]) - int(rec2[0]))
    left = max(int(rec1[1]), int(rec2[1]))
    right = min(int(rec1[3]), int(rec2[3]))
    top = max(int(rec1[0]), int(rec2[0]))
    bottom = min(int(rec1[2]), int(rec2[2]))
    w = max(0, right - left)
    h = max(0, bottom - top)
    return w * h / (areas2 + areas1 - w * h)


if __name__ == '__main__':
    rect1 = [182, 120, 1041, 476]
    # (top, left, bottom, right)
    rect2 = [182, 180, 1041, 476]

    iou = compute_iou(rect2, rect1)
    print(iou)
    print(compute_iou2(rect1, rect2))
