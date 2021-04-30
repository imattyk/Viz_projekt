import numpy as np
import cv2
import math

def rgb2gray(rgb):
    return np.dot(rgb[..., :3], [0.299, 0.587, 0.114]).astype(np.uint8)


def hough_line(img, angle_step=1, lines_are_white=True, value_threshold=5):

    # Rhocka a Thety
    thetas = np.deg2rad(np.arange(-90.0, 90.0, angle_step))
    width, height = img.shape
    diag_len = int(round(math.sqrt(width * width + height * height)))
    rhos = np.linspace(-diag_len, diag_len, diag_len * 2)

    # Vytvorenie matice co drzi hough space
    num_thetas = len(thetas)
    accumulator = np.zeros((2 * diag_len, num_thetas), dtype=np.uint8)
    # indexy ku krajom
    are_edges = img > value_threshold if lines_are_white else img < value_threshold
    y_idxs, x_idxs = np.nonzero(are_edges)

    # pocet priesecnikov pre kazdy edge pixel
    for i in range(len(x_idxs)):
        x = x_idxs[i]
        y = y_idxs[i]

        for t_idx in range(num_thetas):
            # diag len pridame aby sme boli len v kladnych indexoch
            rho = diag_len + int(round(x * np.cos(thetas[t_idx]) + y * np.sin(thetas[t_idx])))
            accumulator[rho, t_idx] += 1

    return accumulator, thetas, rhos


def show_hough_line(img, accumulator, thetas, rhos, save_path=None):
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(1, 2, figsize=(10, 10))

    ax[0].imshow(img, cmap=plt.cm.gray)
    ax[0].set_title('Input image')
    ax[0].axis('image')

    ax[1].imshow(
        accumulator, cmap='jet',
        extent=[np.rad2deg(thetas[-1]), np.rad2deg(thetas[0]), rhos[-1], rhos[0]])
    ax[1].set_aspect('equal', adjustable='box')
    ax[1].set_title('Hough transform')
    ax[1].set_xlabel('Thety')
    ax[1].set_ylabel('Vzdialenost')
    ax[1].axis('image')

    # plt.axis('off')
    if save_path is not None:
        plt.savefig(save_path, bbox_inches='tight')
    plt.show()

def peak_votes(accumulator, thetas, rhos):
    """ Finds the max number of votes in the hough accumulator """
    idx = np.argmax(accumulator)
    #accumulator[idx] = 0
    rho_theta = np.unravel_index(idx, accumulator.shape)
    rho = rhos[rho_theta[0]]
    theta = thetas[rho_theta[1]]

    return idx, theta, rho

def theta2gradient(theta):
    return np.cos(theta) / np.sin(theta)

def rho2intercept(theta, rho):
    return rho / np.sin(theta)



if __name__ == '__main__':
    imgpath = 'imgs/vstup2.png'
    img = cv2.imread(imgpath)
    #img = imageio.imread(imgpath)
    img = rgb2gray(img)
    accumulator, thetas, rhos = hough_line(img)
    show_hough_line(img, accumulator, thetas, rhos, save_path='imgs/output.png')

    img_copy = cv2.imread(imgpath)
    for i in range(30):
        idx, theta, rho = peak_votes(accumulator, thetas, rhos)
        unraveled = np.unravel_index(idx, accumulator.shape)
        accumulator[unraveled[0]][unraveled[1]] = 0
        print(accumulator[unraveled[0]])

        a = math.cos(theta)
        b = math.sin(theta)
        x = a * rho
        y = b * rho

        point1 = (int(x + 1000*(-b)), int(y + 1000*(a)))
        point2 = (int(x - 1000*(-b)), int(y - 1000*(a)))
        cv2.line(img_copy, point1, point2, (0,255,0), 2)

    cv2.imshow('lines',img_copy)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
