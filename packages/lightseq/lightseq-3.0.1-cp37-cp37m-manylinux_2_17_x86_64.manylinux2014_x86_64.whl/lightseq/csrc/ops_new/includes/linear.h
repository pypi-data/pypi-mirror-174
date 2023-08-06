#pragma once
#include "declaration.h"
#include "node.h"
#include "kernels.h"
#include "cublas_wrappers.h"

namespace lightseq {

template <typename T1, typename T2>
class LinearOp : public Operator {
 private:
  int _output_size;
  int _input_size;
  int _max_batch_tokens;
  int _batch_tokens;
  std::array<int, 3> _gemm_algos;

 public:
  LinearOp(int max_batch_tokens, int output_size, int input_size)
      : Operator("LinearOp"),
        _max_batch_tokens(max_batch_tokens),
        _output_size(output_size),
        _input_size(input_size),
        _gemm_algos(std::array<int, 3>({99, 99, 99})) {}

  ~LinearOp() {}

  Variable* operator()(Variable* inp, Variable* weight);

  void forward() override;

  void before_forward(int batch_tokens) { _batch_tokens = batch_tokens; }

  void backward() override;

  void before_backward() {}
};

}  // namespace lightseq
