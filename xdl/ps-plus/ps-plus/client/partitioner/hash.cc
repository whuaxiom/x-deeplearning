/* Copyright (C) 2016-2018 Alibaba Group Holding Limited

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
==============================================================================*/

#include "ps-plus/client/partitioner/hash.h"
#include "ps-plus/common/tensor_shape.h"
#include "ps-plus/common/types.h"
#include "ps-plus/common/hasher.h"

#include <cmath>

namespace ps {
namespace client {
namespace partitioner {

Status HashDataType::Split(PartitionerContext* ctx, Data* src, std::vector<Data*>* dst) {
  VariableInfo* info = ctx->GetVariableInfo();
  dst->clear();
  for (size_t i = 0; i < info->parts.size(); i++) {
    Data* d = new WrapperData<DataType>(info->datatype);
    ctx->AddDeleter(d);
    dst->push_back(d);
  }
  return Status::Ok();
}

Status HashShape::Split(PartitionerContext* ctx, Data* src, std::vector<Data*>* dst) {
  VariableInfo* info = ctx->GetVariableInfo();
  std::vector<size_t> dims(info->shape.begin(), info->shape.end());
  dst->clear();
  for (size_t i = 0; i < info->parts.size(); i++) {
    size_t k = info->parts[i].size * info->shape[0] / Hasher::kTargetRange;
    dims[0] = k + 10 * sqrt(k) + 10;
    Data* d = new WrapperData<TensorShape>(dims);
    ctx->AddDeleter(d);
    dst->push_back(d);
  }
  return Status::Ok();
}

}
}
}

