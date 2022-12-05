# YOLOP-TL-AIHub
YOLOP model fine-tuned with AIHub traffic light data.
unofficial adoptation of [YOLOP](https://github.com/hustvl/YOLOP).

# 프로젝트 선정 이유와 목적
최근 자율주행에 대한 연구가 multi-camera와 Lidar 센서, 객체인식과 segmentation 등 여러 방면에서 활발히 이루어지면서 차량 감지만이 아닌 차선, 경로 예측 등 주행에 직간접적으로 도움을 줄 수 있는 요소들을 모델에 접목시키기 위한 다양한 시도를 하고 있음. </br>

이번 프로젝트는 신호등을 감지함으로써 향후 더 안정적인 주행을 하는 모델을 만드는 데에 도움이 될 수 있도록 기존의 모델을 튜닝하는 것을 목표로 함. </br>

# 데이터 전처리
구(등)수 3구이상의 일반 신호등으로 학습 진행 </br>
상태 세부 속성을 좌회전, 초록불, 노란불, 빨간불, 꺼짐 상태로 입력 받도록 함. </br>
너무 멀리 있는 신호등은 식별하는데 어려움이 있어
가로 5, 세로 5 픽셀 이상의 신호등을 인지하도록 함. </br>

![image](https://user-images.githubusercontent.com/110019752/205637769-5d3635ce-0a8d-4805-9d55-4ee46cd5b5a7.png)
 </br>


### Requirements
basic requirements can be found at original [repo](https://github.com/hustvl/YOLOP).

### Tested environment
```bash
ubuntu 20.04
ros-galactic
CUDA 11.4
```

![image](https://user-images.githubusercontent.com/110019752/205632751-8f5ef416-2055-47ab-b5a2-669bc1b23414.png)
