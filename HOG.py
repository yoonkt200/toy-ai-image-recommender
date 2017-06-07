# import cv2
# from skimage.feature import hog
# from skimage import data, color, exposure
# import numpy as np
#
# inputimg = cv2.imread('/Users/yoon/Documents/clothes/outer/image_input.jpg')
# image = color.rgb2gray(inputimg)
# image = cv2.resize(image, (256, 256))
# fd, hog_image = hog(image, orientations=8, pixels_per_cell=(16, 16), cells_per_block=(1, 1), block_norm="L2-Hys", visualise=True)
# hog_image = np.float32(hog_image)
# fd = np.float32(fd)
# result_array = []
#
# def getKey(item):
#     return item[0]
#
# for i in range (0,100):
#     inputimg2 = cv2.imread('/Users/yoon/Documents/clothes/outer/image_outer_' + str(i + 1) + '.jpg')
#     image2 = color.rgb2gray(inputimg2)
#     image2 = cv2.resize(image2, (256, 256))
#
#     fd2, hog_image2 = hog(image2, orientations=8, pixels_per_cell=(16, 16), cells_per_block=(1, 1), block_norm="L2-Hys", visualise=True)
#
#     hog_image2 = np.float32(hog_image2)
#     fd2 = np.float32(fd2)
#     hog_result = [cv2.compareHist(fd, fd2, 0), str(i + 1)]
#     result_array.append(hog_result)
#
# result_array = sorted(result_array, key=getKey)
# for x in result_array:
#     print (x)
#
#
#
# # class LocalBinaryPatterns:
# #     def __init__(self, numPoints, radius):
# #         # store the number of points and radius
# #         self.numPoints = numPoints
# #         self.radius = radius
# #
# #     def describe(self, image, eps=1e-7):
# #         # compute the Local Binary Pattern representation
# #         # of the image, and then use the LBP representation
# #         # to build the histogram of patterns
# #         lbp = feature.local_binary_pattern(image, self.numPoints,
# #                                            self.radius, method="uniform")
# #         (hist, _) = np.histogram(lbp.ravel(),
# #                                  bins=np.arange(0, self.numPoints + 3),
# #                                  range=(0, self.numPoints + 2))
# #
# #         # normalize the histogram
# #         hist = hist.astype("float")
# #         hist /= (hist.sum() + eps)
# #
# #         # return the histogram of Local Binary Patterns
# #         return hist
# #
# # start_time = time.time()
# # desc = LocalBinaryPatterns(24, 8)
# #
# # imgs = []
# # histHOG = []
# #
# # compare = []
# # rank = []
# #
# # input_img = cv2.imread('/Users/yoon/Documents/clothes/outer/image_input.jpg');
# # image = cv2.cvtColor(input_img, cv2.COLOR_BGR2GRAY)
# # input_histHOG = desc.describe(image)
# # input_histHOG = np.float32(input_histHOG)
# #
# # for i in range(0, 100):
# #     img = cv2.imread('/Users/yoon/Documents/clothes/outer/image_outer_' + str(i + 1) + '.jpg')
# #     img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# #     imgs.append(img)
# #
# # for i in range(0, 100):
# #     hog_image = desc.describe(imgs[i])
# #     hog_image = np.float32(hog_image)
# #     histHOG.append(hog_image)
# #
# # for i in range(0, 100):
# #     compHOG = cv2.compareHist(histHOG[i], input_histHOG, 0)
# #
# #     if len(compare) == 0:
# #         compare.append(compHOG)
# #         rank.append(i)
# #     else:
# #         j = 0
# #         while j != i and compare[j] < compHOG:
# #             j = j + 1
# #
# #         if j == i:
# #             compare.append(compHOG)
# #             rank.append(i)
# #         else:
# #             compare.insert(j, compHOG)
# #             rank.insert(j, i)
# #
# # for i in range(0, 100):
# #     print(str(i + 1) + "등 : image_" + str(rank[i] + 1))
# #     print (str(compare[i] + 1))
# #
# # print("time:" + str(time.time() - start_time))
#
#
#
# # start_time = time.time();
# #
# # imgs = []
# # histHOG = []
# #
# # compare = []
# # rank =[]
# #
# # input_img = cv2.imread('/Users/yoon/Documents/clothes/outer/image_input.jpg');
# # image = cv2.cvtColor(input_img, cv2.COLOR_BGR2GRAY)
# # image = cv2.resize(image, (256, 256))
# #
# # fd, input_histHOGg = hog(image, orientations=8, pixels_per_cell=(16, 16), cells_per_block=(1, 1), block_norm="L2-Hys", visualise=True)
# # fd = np.float32(fd)
# # # input_histHOG = exposure.rescale_intensity(fd, out_range=(0, 255))
# # # hogImage = hogImage.astype("uint8")
# #
# # for i in range(0,100):
# #     img = cv2.imread('/Users/yoon/Documents/clothes/outer/image_outer_' + str(i + 1) + '.jpg')
# #     img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# #     img = cv2.resize(img, (256, 256))
# #     imgs.append(img)
# #
# # for i in range(0,100):
# #     fd1, hog_image = hog(imgs[i], orientations=8, pixels_per_cell=(16, 16), cells_per_block=(1, 1), block_norm="L2-Hys",
# #                         visualise=True)
# #     fd1 = np.float32(fd1)
# #     fd1 = exposure.rescale_intensity(fd1, out_range=(0, 255))
# #     histHOG.append(fd1)
# #
# # for i in range(0,100):
# #     compHOG = cv2.compareHist(histHOG[i], fd, 0)
# #
# #     if len(compare) == 0:
# #         compare.append(compHOG)
# #         rank.append(i)
# #     else:
# #         j=0
# #         while j != i and compare[j] < compHOG:
# #             j = j + 1
# #
# #         if j == i:
# #             compare.append(compHOG)
# #             rank.append(i)
# #         else :
# #             compare.insert(j, compHOG)
# #             rank.insert(j,i)
# #
# # for i in range(0,100):
# #     print(str(i+1) + "등 : image_" + str(rank[i]+1))
# #     print (str(compare[i]+1))
# #
# # print("time:" + str(time.time() - start_time))
#
#
#
# 'import cv2
# import time
#
# start_time = time.time();
#
# WEIGHT_1 = 0.5
# WEIGHT_2 = 0.3
# WEIGHT_3 = 0.2
#
# weightR = 0;
# weightG = 0;
# weightB = 0;
#
# imgs = [];
# histsR = [];
# histsG = [];
# histsB = [];
# hists = [];
#
# compare = [];
# rank =[];
#
# input_img = cv2.imread('image_input.jpg',cv2.IMREAD_COLOR);
#
# input_hist = cv2.calcHist([input_img], [0,1,2], None, [8,8,8], [0, 256,0, 256,0, 256]);
# input_hist = cv2.normalize(input_hist,input_hist)
#
#
# for i in range(0,100):
#     img = cv2.imread('image_outer_' + str(i+1) + '.jpg',cv2.IMREAD_COLOR);
#     imgs.append(img);
#
#
# for i in range(0,100):
#     hist = cv2.calcHist([imgs[i]], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
#     hist = cv2.normalize(hist,hist)
#     hists.append(hist);
#
# for i in range(0,100):
#     compHist = cv2.compareHist(hists[i], input_hist, 2)
#     if len(compare) == 0:
#         compare.append(compHist);
#         rank.append(i);
#     else:
#         j=0;
#         while j != i and compare[j]>compHist:
#             j = j + 1;
#
#         if j == i:
#             compare.append(compHist);
#             rank.append(i)
#         else :
#             compare.insert(j, compHist);
#             rank.insert(j,i);
#
# for i in range(0,100):
#     print(str(i+1) + "등 : image_" + str(rank[i]+1));
#
# print("time:" + str(time.time() - start_time));
#
# cv2.imshow("1",imgs[rank[0]]);
# cv2.imshow("2",imgs[rank[1]]);
# cv2.imshow("3",imgs[rank[2]]);
# cv2.imshow("input_img",input_img);
# cv2.waitKey(0)
# cv2.destroyAllWindows()