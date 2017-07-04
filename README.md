# ImageClassifier
- 사용자가 찾고싶은 유사한 패션 이미지나, 같은 카테고리의 이미지들을 찾아주는 웹 어플리케이션입니다. 

- CNN을 이용한 Machine Learning, HOG Feature Descriptor를 이용한 특징점 추출, Color Histogram 비교를 통한 유사색상추출 등의 알고리즘을 활용하여 이미지를 추천 및 검색해줍니다. 

- 모델 학습은 약 10000여개의 이미지와 30여개의 클래스로 진행했으며, 검색 알고리즘의 효율성을 위해 CNN, HOG Descriptor, Color Histogram Extract의 과정을 순차적으로 진행하고, 각 단계에서의 랭킹을 매긴 후 정렬하였습니다.

## Using
- 개발 Framework : Python, AWS Django, SQL DB, Tensorflow, 
- Algorithm : CNN, HOG discriptor, Color Histogram dist

## Project Goal
- 사용자가 찾고자 하는 유사한 이미지를 분류 및 검색해주고, 더 나아가 추천해줍니다.

## P.S
- 시연 동영상 주소 : https://youtu.be/p7VElDb3Quo