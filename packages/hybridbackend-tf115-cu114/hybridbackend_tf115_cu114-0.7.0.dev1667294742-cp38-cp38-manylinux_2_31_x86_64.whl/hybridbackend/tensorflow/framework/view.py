# Copyright 2021 Alibaba Group Holding Limited. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =============================================================================

r'''View of computed tensors.
'''

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from tensorflow.core.framework import attr_value_pb2
from tensorflow.python.framework import dtypes
from tensorflow.python.framework import ops
from tensorflow.python.framework import tensor_shape
from tensorflow.python.ops import array_ops
from tensorflow.python.ops import control_flow_ops
from tensorflow.python.util import compat


def tensors_like_view(dtypes_and_shapes, op_view_name, *args, **kwargs):
  r'''Declares view for multiple tensors computed by specific function.
  '''
  name = kwargs.pop('name', None)
  if name is None:
    name = ops.get_default_graph().unique_name(op_view_name)
  attrs = {}
  for k, v in kwargs.items():
    attr_key = f'{op_view_name}_{k}'
    if isinstance(v, str):
      attrs[attr_key] = attr_value_pb2.AttrValue(s=compat.as_bytes(v))
    elif isinstance(v, int):
      attrs[attr_key] = attr_value_pb2.AttrValue(i=v)
    elif isinstance(v, bool):
      attrs[attr_key] = attr_value_pb2.AttrValue(b=v)
    elif isinstance(v, dtypes.DType):
      attrs[attr_key] = attr_value_pb2.AttrValue(type=v)
    elif isinstance(v, tensor_shape.TensorShape):
      attrs[attr_key] = attr_value_pb2.AttrValue(shape=v)
    else:
      attrs[attr_key] = v
  if args:
    with ops.get_default_graph()._attr_scope({  # pylint: disable=protected-access
        f'{op_view_name}_input_proxy': attr_value_pb2.AttrValue(b=True)}):
      proxied_inputs = array_ops.identity_n(args, name=f'{name}_input_proxy')
    if dtypes_and_shapes:
      placeholders = [
        array_ops.placeholder(*o, name=f'{name}_placeholder{i}')
        for i, o in enumerate(dtypes_and_shapes)]
      with ops.control_dependencies(proxied_inputs):
        with ops.get_default_graph()._attr_scope(  # pylint: disable=protected-access
            {op_view_name: attr_value_pb2.AttrValue(b=True), **attrs}):
          return array_ops.identity_n(placeholders, name=name)
    with ops.control_dependencies(proxied_inputs):
      with ops.get_default_graph()._attr_scope(  # pylint: disable=protected-access
          {op_view_name: attr_value_pb2.AttrValue(b=True), **attrs}):
        return control_flow_ops.no_op(name=name)
  if dtypes_and_shapes:
    placeholders = [
      array_ops.placeholder(*o, name=f'{name}_placeholder{i}')
      for i, o in enumerate(dtypes_and_shapes)]
    with ops.get_default_graph()._attr_scope(  # pylint: disable=protected-access
        {op_view_name: attr_value_pb2.AttrValue(b=True), **attrs}):  # pylint: disable=protected-access
      return array_ops.identity_n(placeholders, name=name)
  with ops.get_default_graph()._attr_scope(  # pylint: disable=protected-access
      {op_view_name: attr_value_pb2.AttrValue(b=True), **attrs}):  # pylint: disable=protected-access
    return control_flow_ops.no_op(name=name)


def tensor_like_view(output_dtype, output_shape, op_view_name, *args, **kwargs):
  r'''Declares a tensor computed by specific function.
  '''
  return tensors_like_view(
    [(output_dtype, output_shape)], op_view_name, *args, **kwargs)[0]


def op_like_view(op_view_name, *args, **kwargs):
  r'''Declares an op computed by specific function.
  '''
  return tensors_like_view([], op_view_name, *args, **kwargs)
