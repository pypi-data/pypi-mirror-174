from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import os
import sys
__dir__ = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.abspath(os.path.join(__dir__, './')))

import numpy as np
import paddle
from paddle import nn

import ppcls.arch.backbone as paddleclas
from ppcls.utils.logger import init_logger

init_logger()





np_input = np.zeros((1, 3, 224, 224))
pd_input  = paddle.to_tensor(np_input, dtype="float32")


net = paddleclas.AlexNet()
print(net)
print(net.update_res(return_patterns=["_conv1", "_conv2", "_conv3", "_conv4"]))
output = net(pd_input)
print(output.keys())

# net = paddleclas.MobileNetV1(pretrained=True, return_patterns=["blocks[1]", "blocks[3]"])
# net = paddleclas.MobileNetV1(pretrained=True, return_patterns=["blocks[1]", ""])
# net = paddleclas.MobileNetV1(pretrained=True)
# net = paddleclas.VGG11(pretrained=True)
# print(net.update_res(return_patterns=["blocks[-1]", "blocks[4].depthwise_conv"]))

# features = net.res_dict
# print(features.keys())

# output = net(pd_input)
# print(output.keys())

# print("-------------")
# print(net.update_res(return_patterns=["blocks[0]", "blocks[10].depthwise_conv"]))

# features = net.res_dict
# print(features.keys())

# output = net(pd_input)
# print(output.keys())


# tag = net.stop_after(stop_layer_name="avg_pool")
# tag = net.stop_after(stop_layer_name="blocks")
# tag = net.stop_after(stop_layer_name="blocks[3]")
# tag = net.stop_after(stop_layer_name="blocks[3].depthwise_conv")
# tag = net.stop_after(stop_layer_name="blocks[0].depthwise_conv.conv")
# tag = net.stop_after(stop_layer_name="blocks[0].depthwise_conv.bn")
# print(net)
# print(tag)


#def rep_func(sub_layer: nn.Layer, pattern: str):
#    new_layer = nn.Conv2D(
#        in_channels=sub_layer._in_channels,
#        out_channels=sub_layer._out_channels,
#        kernel_size=5,
#        padding=2
#    )
#    return new_layer
#
#res = net.layer_wrench(layer_name_pattern=["blocks[11].depthwise_conv.conv", "blocks[12].depthwise_conv.conv"], handle_func=rep_func)
#res = net.layer_wrench(layer_name_pattern=["blocks[11].depthwise_conv.conv", "block.depthwise_conv.conv"], handle_func=rep_func)
#print(net)
#print(res)


#from ppcls.arch.backbone.variant_models.vgg_variant import SigmoidSuffix
#
#def replace_function(origin_layer, pattern):
#    new_layer = SigmoidSuffix(origin_layer)
#    return new_layer
#
#model = paddleclas.VGG19()
#pattern = "fc2"
#model.upgrade_sublayer(pattern, replace_function)
#print(model)


# from ppcls.arch.backbone.legendary_models.resnet import MODEL_URLS, _load_pretrained
# from paddle.nn import Conv2D
# def replace_function(conv, pattern):
#     new_conv = Conv2D(
#         in_channels=conv._in_channels,
#         out_channels=conv._out_channels,
#         kernel_size=conv._kernel_size,
#         stride=1,
#         padding=conv._padding,
#         groups=conv._groups,
#         bias_attr=conv._bias_attr)
#     return new_conv
#
# pattern = ["blocks[13].conv1.conv", "blocks[13].short.conv"]
# model = paddleclas.ResNet50()
# model.upgrade_sublayer(pattern, replace_function)
# _load_pretrained(True, model, MODEL_URLS["ResNet50"], False)
