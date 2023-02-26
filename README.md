# YOLOP-TL-AIHub
## YOLOP model fine-tuned with AIHub traffic light data. </br>
## unofficial adoptation of [YOLOP](https://github.com/hustvl/YOLOP).

# 프로젝트 선정 이유와 목적
최근 자율주행에 대한 연구가 multi-camera와 Lidar 센서, 객체인식과 segmentation 등 여러 방면에서 활발히 이루어지면서 차량 감지만이 아닌 차선, 경로 예측 등 주행에 직간접적으로 도움을 줄 수 있는 요소들을 모델에 접목시키기 위한 다양한 시도를 하고 있음. </br>

이번 프로젝트는 신호등을 감지함으로써 향후 더 안정적인 주행을 하는 모델을 만드는 데에 도움이 될 수 있도록 기존의 모델을 튜닝하는 것을 목표로 함. </br>

# 데이터 전처리
* 구(등)수 3구이상의 일반 신호등으로 학습 진행 </br>
* 상태 세부 속성을 좌회전, 초록불, 노란불, 빨간불, 꺼짐 상태로 입력 받도록 함. </br>
* 너무 멀리 있는 신호등은 식별하는데 어려움이 있어
가로 5, 세로 5 픽셀 이상의 신호등을 인지하도록 함. </br>

# 훈련 방법
훈련과정은 segmentation 부분 학습을 위해 BDD100K 데이터셋으로 전체 훈련을 진행한 뒤 segmentation 부분을 freeze하고 신호등 데이터로 detection 부분을 학습 </br>

# Result
![image](https://user-images.githubusercontent.com/110019752/205637769-5d3635ce-0a8d-4805-9d55-4ee46cd5b5a7.png) </br>

# 프로젝트 리뷰
* **Segmentation**: 논문에서 제시한 epoch(80)는 3일 이상 소요돼 더 적은 횟수로 segmentation 모델을 훈련함. BDD로만 훈련되어 BDD 데이터셋에 적용하면 높은 정확도를 보이지만, 한국 데이터에서는 정확도가 낮음. </br>
* 한국 도로로 구성된 훈련 가능한 데이터 셋이 있다면 시도해볼 만할 것으로 보임. </br>

* **Detection**: 더 많은 신호등 데이터가 필요할 것 같고, 자동차와 물체의 특성이 다르기 때문에 여러 하이퍼 파라미터들을 변경해가며 더 높은 정확도를 가질 수 있을 것으로 보임. </br>

* BDD100K 데이터셋에 있는 신호등 물체를 사용하여 훈련했지만, 원하는 정확도가 나오지 않음. 데이터셋 분석 결과 신호등 오브젝트가 굉장히 적었으며, Bbox도 부정확한 경우가 많은 것으로 판단돼 신호등 데이터가 적었다고 판단. </br>

* YOLOPv2가 22년 11월 기준 BDD100K 데이터셋 SOTA를 달성해서 사용하려 했으나, 훈련 방법이 공개되지 않아 YOLOP로 개발을 진행 향후 YOLOPv2의 추가적인 코드가 공개되면 쉽게 이식하여 훨씬 높은 정확도로 모델을 구축 가능할 것으로 보임. </br>

## 향후 계획

* **mAP(mean precision)** 게시

![image](https://user-images.githubusercontent.com/110019752/205632751-8f5ef416-2055-47ab-b5a2-669bc1b23414.png)
