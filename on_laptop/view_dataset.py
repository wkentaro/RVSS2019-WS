#!/usr/bin/env python

from steer_net.steerDS import SteerDataSet

import cv2


dataset = SteerDataSet('dev_data/training_data', '.jpg')
print(f'Datset Size: {len(dataset)}')
for index, data in enumerate(dataset):
    print(f"Index: {index}, Steering: {data['steering']:.3f}, "
          f"Class: {data['steering_class']}, Image: {data['image'].shape}")
    cv2.imshow(__file__, data['image'].numpy().transpose(1, 2, 0))
    if cv2.waitKey(0) == ord('q'):
        break
