"""Performance-curve charts: read axes, digitise curves, compare with the table, redraw curves
as smooth Bezier paths through the table points (same colour / width / object).

    ch = Chart.from_ticks(xticks=[(0, 210.56), (4, 273.0), ...], yticks=[(0, 101.3), (30, 156.7), ...])
    # or: ch = Chart.from_labels(T, pi, plot_rect)   (T = OutlineText; reads the numbers on the axes)
    cur = curve_objects(E.page(pi), plot_rect, color=(0.133, 0.365, 0.635))
    pts = ch.to_data(sample_path(E.page(pi).object_pagepath(oi)))
    dev = ch.compare(oi_points, table_points)
    path = ch.smooth_path(table_points)          # [(op, [(x, y), ...]), ...] page coordinates
    E.replace_path(pi, oi, path)                 # same paint object -> same colour/width
"""
import math

import numpy as np

try:
    from scipy.interpolate import CubicSpline, PchipInterpolator
except Exception:  # pragma: no cover
    CubicSpline = PchipInterpolator = None


# ------------------------------------------------------------------ geometry
def bezier(p0, p1, p2, p3, n=24):
    t = np.linspace(0, 1, n)[:, None]
    return (1 - t) ** 3 * p0 + 3 * (1 - t) ** 2 * t * p1 + 3 * (1 - t) * t ** 2 * p2 + t ** 3 * p3


def sample_path(pagepath, n=24):
    """points along a path given as [(op, [(x, y), ...]), ...] (ops m l c v y h)."""
    out = []
    cur = None
    start = None
    for op, pts in pagepath:
        P = [np.array(p, float) for p in pts]
        if op == 'm':
            cur = P[0]
            start = cur
            out.append(cur)
        elif op == 'l':
            seg = np.linspace(cur, P[0], max(2, n // 4))
            out.extend(seg[1:])
            cur = P[0]
        elif op == 'c':
            out.extend(bezier(cur, P[0], P[1], P[2], n)[1:])
            cur = P[2]
        elif op == 'v':
            out.extend(bezier(cur, cur, P[0], P[1], n)[1:])
            cur = P[1]
        elif op == 'y':
            out.extend(bezier(cur, P[0], P[1], P[1], n)[1:])
            cur = P[1]
        elif op == 'h' and start is not None:
            out.append(start)
            cur = start
    return np.array(out)


def fit_axis(pairs):
    """pairs [(value, coord)] -> (a, b, max_residual) with coord = a * value + b."""
    v = np.array([p[0] for p in pairs], float)
    c = np.array([p[1] for p in pairs], float)
    A = np.vstack([v, np.ones_like(v)]).T
    (a, b), *_ = np.linalg.lstsq(A, c, rcond=None)
    res = float(np.abs(A @ np.array([a, b]) - c).max()) if len(v) else 0.0
    return float(a), float(b), res


def robust_ticks(pairs, max_res=0.6):
    """drop mis-read tick labels: keep the largest subset that lies on one straight line."""
    pairs = list(pairs)
    if len(pairs) <= 2:
        return pairs
    best = pairs
    best_n = 0
    for i in range(len(pairs)):
        for j in range(i + 1, len(pairs)):
            (v1, c1), (v2, c2) = pairs[i], pairs[j]
            if v1 == v2:
                continue
            a = (c2 - c1) / (v2 - v1)
            b = c1 - a * v1
            inl = [p for p in pairs if abs(a * p[0] + b - p[1]) <= max_res * 3]
            if len(inl) > best_n:
                best, best_n = inl, len(inl)
    return best


class Chart(object):
    def __init__(self, ax, bx, ay, by, xlog=False, ylog=False):
        self.ax, self.bx, self.ay, self.by = ax, bx, ay, by
        self.xlog, self.ylog = xlog, ylog

    @classmethod
    def from_ticks(cls, xticks, yticks, xlog=False, ylog=False, max_res=0.6):
        """xticks: [(value, page_x)], yticks: [(value, page_y)]  (log axes: value is real value)."""
        fx = [(math.log10(v) if xlog else v, c) for v, c in xticks]
        fy = [(math.log10(v) if ylog else v, c) for v, c in yticks]
        fx = robust_ticks(fx, max_res)
        fy = robust_ticks(fy, max_res)
        ax, bx, rx = fit_axis(fx)
        ay, by, ry = fit_axis(fy)
        ch = cls(ax, bx, ay, by, xlog, ylog)
        ch.residual = (rx, ry)
        if rx > max_res or ry > max_res:
            ch.warning = 'Trục không tuyến tính (sai số %.2f / %.2f pt) - kiểm tra nhãn trục' % (rx, ry)
        else:
            ch.warning = None
        return ch

    def to_page(self, Q, H):
        q = math.log10(Q) if self.xlog else Q
        h = math.log10(H) if self.ylog else H
        return (self.ax * q + self.bx, self.ay * h + self.by)

    def to_data(self, pts):
        pts = np.asarray(pts, float)
        q = (pts[..., 0] - self.bx) / self.ax
        h = (pts[..., 1] - self.by) / self.ay
        if self.xlog:
            q = 10 ** q
        if self.ylog:
            h = 10 ** h
        return np.stack([q, h], axis=-1)

    # -------------------------------------------------------------- curves
    @staticmethod
    def value_at(data_pts, Q):
        """head of a digitised curve at flow Q (linear interpolation); None if outside."""
        d = np.asarray(data_pts)
        order = np.argsort(d[:, 0])
        d = d[order]
        eps = 1e-6 * max(1.0, abs(d[-1, 0] - d[0, 0]))
        if Q < d[0, 0] - eps or Q > d[-1, 0] + eps:
            return None
        Q = min(max(Q, d[0, 0]), d[-1, 0])
        return float(np.interp(Q, d[:, 0], d[:, 1]))

    def compare(self, data_pts, table_pts, tol_abs=None, tol_rel=0.03):
        """deviation of curve vs table points -> list of dict(Q, H_table, H_curve, diff, ok)."""
        out = []
        Hs = [h for q, h in table_pts]
        span = (max(Hs) - min(Hs)) if Hs else 1.0
        for Q, H in table_pts:
            hc = self.value_at(data_pts, Q)
            if hc is None:
                out.append(dict(Q=Q, H_table=H, H_curve=None, diff=None, ok=False))
                continue
            tol = tol_abs if tol_abs is not None else max(0.5, tol_rel * max(abs(H), span * 0.1))
            out.append(dict(Q=Q, H_table=H, H_curve=round(hc, 2), diff=round(hc - H, 2), ok=abs(hc - H) <= tol))
        return out

    @staticmethod
    def fit_poly(Q, H, tol, degrees=(2, 3)):
        """lowest-degree polynomial H(Q) within tol of every point and monotone like the data."""
        Q = np.asarray(Q, float)
        H = np.asarray(H, float)
        dif = np.diff(H)
        dec = np.all(dif <= 0)
        inc = np.all(dif >= 0)
        for deg in degrees:
            if len(Q) <= deg:
                break
            c = np.polyfit(Q, H, deg)
            res = float(np.abs(np.polyval(c, Q) - H).max())
            qq = np.linspace(Q[0], Q[-1], 300)
            dh = np.diff(np.polyval(c, qq))
            mono = (not dec or np.all(dh <= 1e-9)) and (not inc or np.all(dh >= -1e-9))
            if res <= tol and mono:
                return c, deg, res
        return None

    def smooth_path(self, table_pts, method='auto', tol=None):
        """smooth path through data points [(Q, H), ...] -> page path [('m', [p]), ('c', [p1, p2, p3]), ...].
        method: 'spline' (natural cubic, C2) | 'pchip' (monotone, no overshoot) | 'auto' (spline unless it
        makes the curve non-monotone, then pchip).  The curve passes EXACTLY through every point."""
        pts = sorted((float(q), float(h)) for q, h in table_pts if h is not None)
        Q = np.array([p[0] for p in pts])
        H = np.array([p[1] for p in pts])
        if len(Q) < 2:
            raise ValueError('cần >= 2 điểm')
        if tol is None:
            tol = max(1.0, 0.02 * float(np.abs(H).max()))
        self.last_fit = None
        if method in ('auto', 'poly') and len(Q) >= 3:
            fp = self.fit_poly(Q, H, tol)
            if fp is not None:
                c, deg, res = fp
                dc = np.polyder(c)
                q0, q1 = Q[0], Q[-1]
                dq = q1 - q0
                h0, h1 = float(np.polyval(c, q0)), float(np.polyval(c, q1))
                d0, d1 = float(np.polyval(dc, q0)), float(np.polyval(dc, q1))
                c1 = (q0 + dq / 3.0, h0 + d0 * dq / 3.0)
                c2 = (q1 - dq / 3.0, h1 - d1 * dq / 3.0)
                self.last_method = 'poly%d' % deg
                self.last_fit = dict(method=self.last_method, max_dev=round(res, 3), tol=round(tol, 3))
                return [('m', [self.to_page(q0, h0)]), ('c', [self.to_page(*c1), self.to_page(*c2), self.to_page(q1, h1)])]
            if method == 'poly':
                raise ValueError('Không có đa thức bậc 2-3 nào đi sát mọi điểm (sai số > %.2f) - dùng method=pchip' % tol)
        if CubicSpline is None:
            method = 'linear'
        if len(Q) == 2:
            method = 'linear'
        if method in ('auto', 'spline'):
            f = CubicSpline(Q, H, bc_type='natural')
            if method == 'auto':
                qq = np.linspace(Q[0], Q[-1], 400)
                hh = f(qq)
                dif = np.diff(H)
                mono_dec = np.all(dif <= 0)
                mono_inc = np.all(dif >= 0)
                if (mono_dec and np.any(np.diff(hh) > 1e-9)) or (mono_inc and np.any(np.diff(hh) < -1e-9)):
                    f = PchipInterpolator(Q, H)
                    method = 'pchip'
                else:
                    method = 'spline'
        elif method == 'pchip':
            f = PchipInterpolator(Q, H)
        if method == 'linear':
            path = [('m', [self.to_page(Q[0], H[0])])]
            for q, h in zip(Q[1:], H[1:]):
                path.append(('l', [self.to_page(q, h)]))
            return path
        d = f.derivative()
        path = [('m', [self.to_page(Q[0], H[0])])]
        for i in range(len(Q) - 1):
            q0, q1 = Q[i], Q[i + 1]
            h0, h1 = float(f(q0)), float(f(q1))
            d0, d1 = float(d(q0)), float(d(q1))
            dq = q1 - q0
            # cubic Hermite -> Bezier (exact because the page map is affine per axis)
            c1 = (q0 + dq / 3.0, h0 + d0 * dq / 3.0)
            c2 = (q1 - dq / 3.0, h1 - d1 * dq / 3.0)
            path.append(('c', [self.to_page(*c1), self.to_page(*c2), self.to_page(q1, h1)]))
        self.last_method = method
        return path


# ------------------------------------------------------------------ finding chart parts (vector)
def curve_objects(P, rect, color=None, tol=0.02, ops=('S', 's'), min_span=20.0):
    """stroke objects inside rect that look like curves (long, not straight horizontal/vertical)."""
    out = []
    for oi in P.objects_in(rect):
        o = P.objs[oi]
        if o['op'] not in ops:
            continue
        b = o['bbox']
        if (b[2] - b[0]) < min_span and (b[3] - b[1]) < min_span:
            continue
        if (b[3] - b[1]) < 0.5 or (b[2] - b[0]) < 0.5:
            continue   # straight grid line
        if color is not None:
            c = P.color_of(oi, 'stroke')
            if c is None or max(abs(a - b_) for a, b_ in zip(c, color)) > tol:
                continue
        out.append(oi)
    return out


def gridlines(P, rect, ops=('S', 's'), tol=0.3):
    """x positions of vertical and y positions of horizontal straight lines inside rect."""
    xs, ys = [], []
    for oi in P.objects_in(rect):
        o = P.objs[oi]
        if o['op'] not in ops:
            continue
        for s in o['subs']:
            b = s['bbox']
            if b[2] - b[0] < tol and b[3] - b[1] > 5:
                xs.append(round((b[0] + b[2]) / 2, 3))
            elif b[3] - b[1] < tol and b[2] - b[0] > 5:
                ys.append(round((b[1] + b[3]) / 2, 3))
    return sorted(set(xs)), sorted(set(ys))


def ticks_from_labels(T, key, rect, axis):
    """numbers printed along an axis -> [(value, centre coordinate)].
    T: OutlineText (learned).  axis 'x' -> centre x of each number;  'y' -> centre y."""
    out = []
    for text, ln in T.text_lines(key, rect):
        t = text.replace(' ', '')
        try:
            v = float(t)
        except ValueError:
            continue
        b = (min(g.bbox[0] for g in ln), min(g.bbox[1] for g in ln), max(g.bbox[2] for g in ln), max(g.bbox[3] for g in ln))
        out.append((v, (b[0] + b[2]) / 2.0 if axis == 'x' else (b[1] + b[3]) / 2.0))
    return sorted(out)


def snap_ticks(ticks, lines, max_dist=4.0):
    """replace label centres by the nearest grid line position (more exact)."""
    out = []
    for v, c in ticks:
        if lines:
            k = min(lines, key=lambda L: abs(L - c))
            out.append((v, k if abs(k - c) <= max_dist else c))
        else:
            out.append((v, c))
    return out


# ------------------------------------------------------------------ raster helpers
def draw_polyline(cv, page_pts, color, width_px, ss=4):
    """anti-aliased polyline on a raster canvas (supersampled). page_pts in page coords."""
    from PIL import Image, ImageDraw
    H, W = cv.work.shape[:2]
    px = [cv.to_px(x, y) for x, y in page_pts]
    u0 = max(0, int(min(p[0] for p in px) - width_px * 2 - 2))
    v0 = max(0, int(min(p[1] for p in px) - width_px * 2 - 2))
    u1 = min(W, int(max(p[0] for p in px) + width_px * 2 + 3))
    v1 = min(H, int(max(p[1] for p in px) + width_px * 2 + 3))
    w, h = u1 - u0, v1 - v0
    mask = Image.new('L', (w * ss, h * ss), 0)
    dr = ImageDraw.Draw(mask)
    pts = [((p[0] - u0) * ss, (p[1] - v0) * ss) for p in px]
    dr.line(pts, fill=255, width=max(1, int(round(width_px * ss))), joint='curve')
    al = np.asarray(mask.resize((w, h), Image.LANCZOS)).astype(np.float32) / 255.0
    col = np.asarray(color, np.float32)
    dst = cv.work[v0:v1, u0:u1].astype(np.float32)
    cv.work[v0:v1, u0:u1] = (dst * (1 - al[:, :, None]) + col[None, None, :] * al[:, :, None]).round().clip(0, 255).astype(np.uint8)
    return (u0, v0, u1, v1)


def color_mask(cv, box, color, tol=40):
    """bool mask of pixels close to `color` inside pixel box (for erasing an old raster curve)."""
    u0, v0, u1, v1 = box
    a = cv.work[v0:v1, u0:u1].astype(np.int32)
    d = np.abs(a - np.asarray(color, np.int32)[None, None, :]).max(axis=2)
    m = np.zeros(cv.work.shape[:2], bool)
    m[v0:v1, u0:u1] = d <= tol
    return m
