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

r'''Classes for collective communication.
'''

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from tensorflow.python.framework import dtypes
from tensorflow.python.framework import ops
from tensorflow.python.framework import tensor_shape
from tensorflow.python.ops import array_ops
from tensorflow.python.ops import custom_gradient

from hybridbackend.tensorflow.distribute.ops import CollectiveOps
from hybridbackend.tensorflow.distribute.pubsub import PubSub
from hybridbackend.tensorflow.framework.context import Context
from hybridbackend.tensorflow.framework.view import op_like_view
from hybridbackend.tensorflow.framework.view import tensor_like_view
from hybridbackend.tensorflow.framework.view import tensors_like_view


class Collective(object):  # pylint: disable=useless-object-inheritance
  r'''Resource for collective communication.
  '''
  def __init__(self, shared_name, handle, create_op, is_initialized_op):
    r'''Constructs an instance for collective communication.

    Args:
      shared_name: shared name for collective communication.
      handle: Handle to the resource.
      create_op: Operation to create the resource.
      is_initialized_op: Operation to check if the reousrce is initialized.
    '''
    self._shared_name = shared_name
    self._handle = handle
    self._create_op = create_op
    self._is_initialized_op = is_initialized_op

  @classmethod
  def _resource_handle(cls, shared_name):
    r'''Resource handle op.
    '''
    return tensor_like_view(
      dtypes.resource, tensor_shape.TensorShape({}),
      'HbCollectiveHandleOp',
      shared_name=shared_name)

  @classmethod
  def _resource_get_id(cls, dtype, shape):
    r'''Resource get_id op.
    '''
    return tensor_like_view(dtype, shape, 'HbGetCollectiveId')

  @classmethod
  def _resource_create(cls, handle, collective_id, shared_name):
    r'''Resource get_id op.
    '''
    return op_like_view(
      'HbCreateCollective',
      handle,
      collective_id,
      size=Context.get().world_size,
      rank=Context.get().rank,
      shared_name=shared_name)

  @classmethod
  def _resource_is_initialized(cls, handle):
    r'''Resource is_initialized op.
    '''
    return tensor_like_view(
      dtypes.bool, tensor_shape.TensorShape({}),
      'HbIsCollectiveInitialized',
      handle)

  @classmethod
  def get(cls):
    r'''Get or create an instance.
    '''
    ctx = Context.get()
    if ctx.world_size == 1:
      return cls('', None, None, None)

    collective_resources = ops.get_collection_ref(cls.__name__)
    if collective_resources:
      return collective_resources[0]

    shared_name = ops.get_default_graph().unique_name('collective')
    with ops.name_scope(f'{shared_name}/replicas/{ctx.rank}/'):
      with ops.control_dependencies(None):
        handle = cls._resource_handle(shared_name)
        collective_id_dtype = dtypes.int64
        collective_id_shape = tensor_shape.TensorShape([16])  # 128 / 8
        collective_id = PubSub(ctx.devices)(
          lambda: cls._resource_get_id(
            collective_id_dtype, collective_id_shape),
          collective_id_dtype, collective_id_shape,
          name=f'{shared_name}/collective_id')
        create_op = cls._resource_create(handle, collective_id, shared_name)
        is_initialized_op = cls._resource_is_initialized(handle)
        coll = cls(shared_name, handle, create_op, is_initialized_op)
        ops.add_to_collection(ops.GraphKeys.LOCAL_RESOURCES, coll)
        collective_resources.append(coll)
        return coll

  @property
  def shared_name(self):
    r'''Shared name of the communicator.
    '''
    return self._shared_name

  @property
  def name(self):
    r'''Name of the communicator instance.
    '''
    return f'{self.shared_name}/replicas/{Context.get().rank}'

  @property
  def handle(self):
    r'''Handle op to the communicator instance.
    '''
    return self._handle.op

  @property
  def create(self):
    r'''Resource creation op of the communicator.
    '''
    return self._create_op  # pylint: disable=protected-access

  @property
  def is_initialized(self):
    r'''Resource creation check op of the communicator.
    '''
    return self._is_initialized_op  # pylint: disable=protected-access

  # Data reduction and movements with gradients

  def _allreduce(self, value, reduce_op, name):
    r'''Reduce values across devices.

    Args:
      value: Value to be allreduced.
      reduce_op: Reduction ops: SUM, PROD, MAX or MIN.
      name: Name of the op.

    Returns:
      Allreduced value.
    '''
    if Context.get().world_size == 1:
      return value

    with ops.device(value.device):
      with ops.name_scope(self.name):
        return tensor_like_view(
          value.dtype, value.shape,
          'HbCollectiveAllreduce',
          self._handle,
          value,
          reduce_op=reduce_op,
          name=name)

  def allreduce(self, value, reduce_op=None, name=None):
    r'''Reduce values across devices.

    Args:
      value: Value to be allreduced.
      reduce_op: Reduction ops: SUM, PROD, MAX or MIN.
      name: Name of the op.

    Returns:
      Allreduced value.
    '''
    if reduce_op is None:
      reduce_op = CollectiveOps.SUM

    @custom_gradient.custom_gradient
    def allreduce_fn(value):
      reduced = self._allreduce(
        value, reduce_op=reduce_op, name=name)

      def grad_fn(value_grad):
        r'''Gradient function for fn.
        '''
        if reduce_op != CollectiveOps.SUM:
          raise NotImplementedError(
            'Only reduce_op=SUM is supported for gradients computation.')
        with ops.control_dependencies(reduced):
          grad_out = self._allreduce(
            value_grad, reduce_op=reduce_op, name=f'gradients/{name}')
        return None, grad_out
      return reduced, grad_fn

    return allreduce_fn(value)

  def _alltoall(self, value, wire_dtype, name):
    r'''Shuffle value partitions across devices.

    Args:
      value: Value to be sent to other devices.
      wire_dtype: Data type for communication if possible.
      name: Name of the op.

    Returns:
      received value partitions from other devices.
    '''
    if Context.get().world_size == 1:
      return value

    with ops.device(value.device):
      with ops.name_scope(self.name):
        return tensor_like_view(
          value.dtype, value.shape,
          'HbCollectiveAlltoall',
          self._handle,
          value,
          wire_dtype=wire_dtype,
          name=name)

  def alltoall(self, value, wire_dtype=None, name=None):
    r'''Shuffle value partitions across devices.

    Args:
      value: Value to be sent to other devices.
      wire_dtype: Data type for communication if possible.
      name: Name of the op.

    Returns:
      received value partitions from other devices.
    '''
    if wire_dtype is None:
      wire_dtype = dtypes.float32

    @custom_gradient.custom_gradient
    def alltoall_fn(value):
      exchanged = self._alltoall(
        value, wire_dtype=wire_dtype, name=name)

      def grad_fn(value_grad):
        r'''Gradient function for fn.
        '''
        with ops.control_dependencies(exchanged):
          grad_out = self._alltoall(
            value_grad, wire_dtype=wire_dtype, name=f'gradients/{name}')
        return None, grad_out
      return exchanged, grad_fn

    return alltoall_fn(value)

  def _alltoallv(self, value, sizes, wire_dtype, common_shape, name):
    r'''Shuffle value partitions across devices.

    Args:
      value: Value to be sent to other devices.
      wire_dtype: Data type for communication if possible.
      name: Name of the op.

    Returns:
      received value partitions from other devices.
    '''
    if Context.get().world_size == 1:
      return value

    with ops.device(value.device):
      with ops.name_scope(self.name):
        return tensors_like_view(
          [(value.dtype, value.shape), (sizes.dtype, sizes.shape)],
          'HbCollectiveAlltoallv',
          self._handle,
          value,
          sizes,
          wire_dtype=wire_dtype,
          common_shape=common_shape,
          name=name)

  def alltoallv(
      self, value, sizes,
      wire_dtype=None,
      common_shape=None,
      name=None):
    r'''Shuffle value partitions with varying sizes across devices.

    Args:
      value: Value to be sent to other devices.
      wire_dtype: Data type for communication if possible.
      common_shape: common shape of tensors in value.
      name: Name of the op.

    Returns:
      received value partitions from other devices.
    '''
    if wire_dtype is None:
      wire_dtype = dtypes.float32

    if common_shape is None:
      common_shape = {}

    @custom_gradient.custom_gradient
    def alltoallv_fn(value, sizes):
      exchanged = self._alltoallv(
        value, sizes,
        wire_dtype=wire_dtype,
        common_shape=common_shape,
        name=name)

      def grad_fn(value_grad):
        r'''Gradient function for fn.
        '''
        with ops.control_dependencies(exchanged):
          grad_out = self._alltoallv(
            value_grad, sizes,
            wire_dtype=wire_dtype,
            common_shape=common_shape,
            name=f'gradients/{name}')
        return None, grad_out
      return exchanged, grad_fn

    return alltoallv_fn(value, sizes)

  # Data reduction and movements without gradients

  def _broadcast(self, value, root_rank, name):
    r'''Broadcast value across devices.

    Args:
      value: Value to broadcast.
      root_rank: Rank of broadcast root.
      name: Name of the op.

    Returns:
      Broadcasted value.
    '''
    if Context.get().world_size == 1:
      return value

    with ops.device(value.device):
      with ops.name_scope(self.name):
        return tensor_like_view(
          value.dtype, value.shape,
          'HbCollectiveBroadcast',
          self._handle,
          value,
          root_rank=root_rank,
          name=name)

  def broadcast(self, value, root_rank=0, name=None):
    r'''Broadcast value across devices.

    Args:
      value: Value to broadcast.
      root_rank: Rank of broadcast root.
      name: Name of the op.

    Returns:
      Broadcasted value.
    '''
    return array_ops.stop_gradient(
      self._broadcast(value, root_rank=root_rank, name=name))

  def _allgather(self, value, name):
    r'''Gather all values across devices to all devices.

    Args:
      value: Value on current device to be gathered.
      varying_size: Supposing all value sizes on devices are not equal.
      name: Name of the op.

    Returns:
      Gathered value.
    '''
    if Context.get().world_size == 1:
      return value

    with ops.device(value.device):
      with ops.name_scope(self.name):
        return tensor_like_view(
          value.dtype, value.shape,
          'HbCollectiveAllgather',
          self._handle,
          value,
          name=name)

  def allgather(self, value, name=None):
    r'''Gather all values across devices to all devices.

    Args:
      value: Value on current device to be gathered.
      varying_size: Supposing all value sizes on devices are not equal.
      name: Name of the op.

    Returns:
      Gathered value.
    '''
    return array_ops.stop_gradient(
      self._allgather(value, name=name))

  def _allgatherv(self, value, name):
    r'''Gather all values across devices to all devices.

    Args:
      value: Value on current device to be gathered.
      varying_size: Supposing all value sizes on devices are not equal.
      name: Name of the op.

    Returns:
      Gathered value.
    '''
    if Context.get().world_size == 1:
      return value

    with ops.device(value.device):
      with ops.name_scope(self.name):
        return tensor_like_view(
          value.dtype,
          tensor_shape.TensorShape(None).merge_with(value.shape[1:]),
          'HbCollectiveAllgatherv',
          self._handle,
          value,
          name=name)

  def allgatherv(self, value, name=None):
    r'''Gather all values across devices to all devices.

    Args:
      value: Value on current device to be gathered.
      varying_size: Supposing all value sizes on devices are not equal.
      name: Name of the op.

    Returns:
      Gathered value.
    '''
    return array_ops.stop_gradient(
      self._allgatherv(value, name=name))


def allreduce(value, reduce_op=None, name=None):
  r'''Reduce values across devices.

  Args:
    value: Value to be allreduced.
    reduce_op: Reduction ops: SUM, PROD, MAX or MIN.
    name: Name of the op.

  Returns:
    Allreduced value.
  '''
  return Collective.get().allreduce(
    value,
    reduce_op=reduce_op,
    name=name)


def alltoall(value, wire_dtype=None, name=None):
  r'''Shuffle value partitions across devices.

  Args:
    value: Value to be sent to other devices.
    wire_dtype: Data type for communication if possible.
    name: Name of the op.

  Returns:
    received value partitions from other devices.
  '''
  return Collective.get().alltoall(value, wire_dtype=wire_dtype, name=name)


def alltoallv(
    value, sizes,
    wire_dtype=None,
    common_shape=None,
    name=None):
  r'''Shuffle value partitions with varying sizes across devices.

  Args:
    value: Value to be sent to other devices.
    wire_dtype: Data type for communication if possible.
    common_shape: common shape of tensors in value.
    name: Name of the op.

  Returns:
    received value partitions from other devices.
  '''
  return Collective.get().alltoallv(
    value, sizes,
    wire_dtype=wire_dtype,
    common_shape=common_shape,
    name=name)


def broadcast(value, root_rank=0, name=None):
  r'''Broadcast value across devices.

  Args:
    value: Value to broadcast.
    root_rank: Rank of broadcast root.
    name: Name of the op.

  Returns:
    Broadcasted value.
  '''
  return Collective.get().broadcast(value, root_rank=root_rank, name=name)


def allgather(value, name=None):
  r'''Gather all values across devices to all devices.

  Args:
    value: Value on current device to be gathered.
    varying_size: Supposing all value sizes on devices are not equal.
    name: Name of the op.

  Returns:
    Gathered value.
  '''
  return Collective.get().allgather(value, name=name)


def allgatherv(value, name=None):
  r'''Gather all values across devices to all devices.

  Args:
    value: Value on current device to be gathered.
    varying_size: Supposing all value sizes on devices are not equal.
    name: Name of the op.

  Returns:
    Gathered value.
  '''
  return Collective.get().allgatherv(value, name=name)
