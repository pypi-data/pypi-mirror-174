# Machine Learning Kit (mlkit)

## INSTALL
```bash
pip install ml_scripts
```

## EXAMPLES

### 1. Model Evaluate

#### 1.1 Classifier Evaluate

* Add Data

```python
from ml_scripts.model_evaluate import ClassifierEvaluate

pred_probs_vectors = [[1, 3, 2, 7, 0],
                      [4, 7, 2, 8, 2],
                      [1, 3, 7, 4, 9]]  # normalization is not required
real_idxes = [2, 1, 3]
ce = ClassifierEvaluate(pred_probs_vectors, real_idxes)

more_pred_probs_vectors = [[7, 5, 3, 6, 1],
                           [1, 4, 6, 7, 9]]
more_real_idxes = [0, 4]
ce.extend_pred_and_real(more_pred_probs_vectors, more_real_idxes)
```

* Calculate Topk-Accuracies
```python
ce.get_topk_acc(1)
# 0.4

ce.get_topk_acc(2)  
# 0.6

ce.get_topk_acc(3)  
# 1.0
```
* Calculate Topk-Precision/Recall/Accuracies for each class
```python
ce.get_topk_tp_fn_fp_tn_for_idxes(1)
# {0: (1, 0, 0, 4),
#  1: (0, 1, 0, 4),
#  2: (0, 1, 0, 4),
#  3: (0, 1, 2, 2),
#  4: (1, 0, 1, 3)}

ce.get_topk_tp_fn_fp_tn_for_idxes(2)
# {0: (1, 0, 0, 4),
#  1: (1, 0, 1, 3),
#  2: (0, 1, 1, 3),
#  3: (0, 1, 4, 0),
#  4: (1, 0, 1, 3)}

```
* Save All Results of Evaluation
```python
ce.save_result(max_k=50, result_dp='[directory_path_to_save_result_of_evaluation]')
```