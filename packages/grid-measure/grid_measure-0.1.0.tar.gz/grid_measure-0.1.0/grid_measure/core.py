import numpy as np
import skimage
import skimage.io
import skimage.transform
import skimage.color
import numpy, scipy.optimize
import scipy
import scipy.ndimage
from deskew import determine_skew
import cv2


def enhance_img(img, is_BRG=False):

    if not is_BRG:
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    # converting to LAB color space
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)

    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    lab[:, :, 0] = clahe.apply(lab[:, :, 0])

    enhanced_img = cv2.cvtColor(lab, cv2.COLOR_Lab2RGB)

    return enhanced_img


# https://stackoverflow.com/a/42322656/5665958
def fit_sin(tt, yy):
    '''Fit sin to the input time sequence, and return fitting parameters "amp", "omega", "phase", "offset", "freq", "period" and "fitfunc"'''
    tt = numpy.array(tt)
    yy = numpy.array(yy)
    ff = numpy.fft.fftfreq(len(tt), (tt[1] - tt[0]))  # assume uniform spacing
    Fyy = abs(numpy.fft.fft(yy))
    guess_freq = abs(
        ff[numpy.argmax(Fyy[1:]) + 1]
    )  # excluding the zero frequency "peak", which is related to offset
    guess_amp = numpy.std(yy) * 2.0**0.5
    guess_offset = numpy.mean(yy)
    guess = numpy.array([guess_amp, 2.0 * numpy.pi * guess_freq, 0.0, guess_offset])

    def sinfunc(t, A, w, p, c):
        return A * numpy.sin(w * t + p) + c

    popt, pcov = scipy.optimize.curve_fit(sinfunc, tt, yy, p0=guess)
    A, w, p, c = popt
    f = w / (2.0 * numpy.pi)
    fitfunc = lambda t: A * numpy.sin(w * t + p) + c
    return {
        "amp": A,
        "omega": w,
        "phase": p,
        "offset": c,
        "freq": f,
        "period": 1.0 / f,
        "fitfunc": fitfunc,
        "maxcov": numpy.max(pcov),
        "rawres": (guess, popt, pcov),
    }


def get_scale_mm(img, th=0.5):
    img = enhance_img(img)
    angle = determine_skew(img)
    img = skimage.transform.rotate(img, angle)
    img_gray = skimage.color.rgb2gray(img)
    img_bin = img_gray <= th

    y = img_bin.sum(1)
    y = scipy.ndimage.gaussian_filter1d(y, 10)
    y -= scipy.ndimage.gaussian_filter1d(y, 10)

    r = fit_sin(np.arange(len(y)), y)
    scale = r["period"]

    return scale
