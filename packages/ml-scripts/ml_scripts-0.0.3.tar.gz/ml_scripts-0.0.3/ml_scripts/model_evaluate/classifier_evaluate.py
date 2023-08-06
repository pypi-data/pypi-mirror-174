#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2022/9/23 14:13
# @Author  : zhangbc0315@outlook.com
# @File    : classifier_evaluate.py
# @Software: PyCharm

import os

import numpy as np
import pandas as pd
from tqdm import tqdm


class ClassifierEvaluate:

    def __init__(self, pred_prob_vectors: [[float]], real_idxes: [int]):
        self._check_pred_and_real(pred_prob_vectors, real_idxes)
        self._pred_prob_vectors = pred_prob_vectors
        self._real_idxes = real_idxes

    @classmethod
    def _check_pred_and_real(cls, pred_prob_vectors: [[float]], real_idxes: [int]):
        if len(pred_prob_vectors) != len(real_idxes):
            raise ValueError(f"length of pred and real must be same, "
                             f"but get {len(pred_prob_vectors)} and {len(real_idxes)}")
        lens = set(len(p) for p in pred_prob_vectors)
        if len(lens) > 1:
            raise ValueError(f"length of each predict probabilities vector must be same, but get f{lens}")

    def extend_pred_and_real(self, pred_prob_vectors: [[float]], real_idxes: [int]):
        self._check_pred_and_real(pred_prob_vectors, real_idxes)
        self._pred_prob_vectors.extend(pred_prob_vectors)
        self._real_idxes.extend(real_idxes)

    @classmethod
    def _get_topk_acc_num(cls, k, pred_prob_vectors: np.ndarray, real_idxes: np.ndarray) -> int:
        pred_sorted_idxes = np.argsort(-pred_prob_vectors, axis=-1)
        sub = (pred_sorted_idxes.transpose() - real_idxes).transpose()
        pred_true_ids = np.argwhere(sub == 0)[:, -1]
        num_right = np.sum(pred_true_ids < k)
        return int(num_right)

    def get_topk_acc(self, k: int) -> float:
        np_pred_prob_vectors = np.array(self._pred_prob_vectors)
        np_real_idxes = np.array(self._real_idxes)
        return self._get_topk_acc_num(k, np_pred_prob_vectors, np_real_idxes) / len(np_real_idxes)

    def get_topk_tp_fn_fp_tn_for_idxes(self, k: int) -> {int: (int, int, int, int)}:
        np_pred_prob_vectors = np.array(self._pred_prob_vectors)
        np_real_idxes = np.array(self._real_idxes)
        all_idxes = set(self._real_idxes)
        idx_to_topk_tp_fn_fp_tn = {}
        with tqdm(total=len(all_idxes))as pbar:
            pbar.set_description("get tp fn fp tn")
            for idx in all_idxes:
                pbar.update(1)
                ids_for_real_idx = np.argwhere(np_real_idxes == idx)[:, -1]
                real_idxes = np_real_idxes[ids_for_real_idx]
                pred_prob_vectors = np_pred_prob_vectors[ids_for_real_idx]
                tp = self._get_topk_acc_num(k, pred_prob_vectors, real_idxes)
                fn = len(real_idxes) - tp

                ids_for_real_idx = np.argwhere(np_real_idxes != idx)[:, -1]
                real_idxes = np.array([idx] * len(ids_for_real_idx))
                pred_prob_vectors = np_pred_prob_vectors[ids_for_real_idx]
                fp = self._get_topk_acc_num(k, pred_prob_vectors, real_idxes)
                tn = len(real_idxes) - fp

                idx_to_topk_tp_fn_fp_tn[idx] = (tp, fn, fp, tn)

        return idx_to_topk_tp_fn_fp_tn

    @classmethod
    def get_pre_rec_acc(cls, tp: int, fn: int, fp: int, tn: int) -> (float, float):
        return tp / (tp + fp), tp / (tp + fn), (tp + tn) / (tp + fn + fp + tn)

    # region ===== save =====

    @classmethod
    def _get_tp_fn_fp_tn_df_for_k(cls, idx_to_tp_fn_fp_tn: {}):
        dic = {'idx': [], 'precision': [], 'recall': [], 'accuracy': [],
               'tp': [], 'tn': [], 'fp': [], 'fn': []}
        for idx, (tp, fn, fp, tn) in idx_to_tp_fn_fp_tn.items():
            pre, rec, acc = cls.get_pre_rec_acc(tp, fn, fp, tn)
            dic['idx'].append(idx)
            dic['precision'].append(pre)
            dic['recall'].append(rec)
            dic['accuracy'].append(acc)
            dic['tp'].append(tp)
            dic['tn'].append(tn)
            dic['fp'].append(fp)
            dic['fn'].append(fn)
        return pd.DataFrame(dic)

    def save_result(self, max_k: int, result_dp: str):
        if not os.path.exists(result_dp):
            os.mkdir(result_dp)
        topk_acc_fp = os.path.join(result_dp, 'topk_accuracies.tsv')

        topk_acc_df = pd.DataFrame(columns=['k', 'accuracy'])
        with tqdm(total=max_k)as pbar:
            pbar.set_description(f"save results")
            for _k in range(max_k):
                pbar.set_postfix_str(f"k: {_k}")
                pbar.update(1)
                k = _k + 1
                acc = self.get_topk_acc(k)
                topk_acc_df = topk_acc_df.append({'k': k, 'accuracy': acc}, ignore_index=True)
                idx_to_tp_fn_fp_tn = self.get_topk_tp_fn_fp_tn_for_idxes(k)
                idx_to_eva_df = self._get_tp_fn_fp_tn_df_for_k(idx_to_tp_fn_fp_tn)
                idx_to_eva_df.to_csv(os.path.join(result_dp, f'idx_eva_for_k.tsv'),
                                     sep='\t', encoding='utf-8', index=False)

        topk_acc_df.to_csv(topk_acc_fp, sep='\t', encoding='utf-8', index=False)

    # endregion


if __name__ == "__main__":
    pass
