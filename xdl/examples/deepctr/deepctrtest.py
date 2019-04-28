# Copyright (C) 2016-2018 Alibaba Group Holding Limited
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
# ==============================================================================

import tensorflow as tf
import xdl

reader = xdl.DataReader("r1", # name of reader
                        paths=["./data.txt"], # file paths
                        enable_state=False) # enable reader state

reader.epochs(300).threads(1).batch_size(1024).label_count(1)
reader.feature(name='sparse0', type=xdl.features.sparse)\
    .feature(name='sparse1', type=xdl.features.sparse)\
    .feature(name='deep0', type=xdl.features.dense, nvec=256)
reader.startup()

def train():
    batch = reader.read()
    sess = xdl.TrainSession()
    # emb1 = xdl.embedding('emb1', batch['sparse0'], xdl.TruncatedNormal(stddev=0.001), 128, 1024, vtype='hash')
    # emb2 = xdl.embedding('emb2', batch['sparse1'], xdl.TruncatedNormal(stddev=0.001), 128, 1024, vtype='hash')
    emb1 = xdl.embedding('emb1', batch['sparse0'], xdl.Constant(0.1), 128, 1024, vtype='hash')
    emb2 = xdl.embedding('emb2', batch['sparse1'], xdl.Constant(0.1), 128, 1024, vtype='hash')
    # loss = model(batch['deep0'], [emb1, emb2], batch['label'])
    # train_op = xdl.SGD(0.5).optimize()
    # log_hook = xdl.LoggerHook(loss, "loss:{0}", 10)
    # sess = xdl.TrainSession(hooks=[log_hook])
    sess = xdl.TrainSession()
    cnt = 0
    while not sess.should_stop():
        # sess.run(train_op)
        input1, input2 = sess.run([emb1, emb2])
        # bt0, bt1 = sess.run([batch['sparse0'].ids, batch['sparse1'].ids])
        if cnt % 10 == 0:
            print(cnt)
            print(len(input1), len(input2))
            print(input1, input2)
        cnt += 1

@xdl.tf_wrapper()
def model(deep, embeddings, labels):
    input = tf.concat([deep] + embeddings, 1)
    y = tf.layers.dense(
        input, 1, kernel_initializer=tf.truncated_normal_initializer(
            stddev=0.001, dtype=tf.float32))
    loss = tf.losses.sigmoid_cross_entropy(labels, y)
    return loss

train()        

