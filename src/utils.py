import math


def line_intersec(l1, l2):
    xdiff = (l1[0][0] - l1[1][0], l2[0][0] - l2[1][0])
    ydiff = (l1[0][1] - l1[1][1], l2[0][1] - l2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]
    div = det(xdiff, ydiff)
    if div == 0:
        return None
    d = (det(*l1), det(*l2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    x = round(x)
    y = round(y)
    if x >= min(l1[0][0], l1[1][0])-1 and x <= max(l1[0][0], l1[1][0])+1 \
            and y >= min(l1[0][1], l1[1][1])-1 and y <= max(l1[0][1], l1[1][1])+1 \
            and x >= min(l2[0][0], l2[1][0])-1 and x <= max(l2[0][0], l2[1][0])+1 \
            and y >= min(l2[0][1], l2[1][1])-1 and y <= max(l2[0][1], l2[1][1])+1:
        return [x, y]
    else:
        return None


def dist(p1, p2):
    return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)
