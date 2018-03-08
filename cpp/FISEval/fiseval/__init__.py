import ctypes as C
import os
from collections import OrderedDict

import numpy as np
from numpy.ctypeslib import ndpointer

from evo.helpers.ifs_utils import IFSUtils

np.set_printoptions(precision=2, suppress=True)

PARENT_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

_fiseval_wrapper = C.cdll.LoadLibrary(
    os.path.join(PARENT_DIR, "cpp/build/fiseval_wrapper.so"))


def run_func_in_c():
    return _fiseval_wrapper.cffi_hello()


def mul_np_array(arr, scaler):
    f = _fiseval_wrapper.c_mul_np_array

    f.argtypes = [
        ndpointer(dtype=np.float64, ndim=1, flags='C_CONTIGUOUS'),
        C.c_int, C.c_int]

    f(arr, arr.shape[0], scaler)

    return arr


def _get_np_array_2d_ptr(arr, ctype_type):
    ptr_type = C.POINTER(ctype_type)
    n_rows = len(arr)
    return (ptr_type * n_rows)(*[row.ctypes.data_as(ptr_type) for row in arr])


def _get_np_array_1d_ptr(arr, ctype_type):
    # return _get_np_array_2d_ptr(arr, ctype_type)
    return _get_array_1d_ptr(arr, ctype_type)


def _get_array_1d_ptr(arr, ctype_type):
    return (ctype_type * len(arr))(*arr)


def _get_c_array_from_np(arr, ctype_type):
    return arr.ctypes.data_as(C.POINTER(ctype_type))


def predict_native(ind, observations, n_rules, max_vars_per_rule, n_labels,
                   n_consequents, default_rule_cons, vars_ranges,
                   labels_weights,
                   dc_idx):
    f = _fiseval_wrapper.c_predict

    # observations = np.arange(6).reshape(3, 2).astype(np.float64)
    # print(observations)

    # kwargs = OrderedDict([
    #     ("ind", C.POINTER(C.c_float)),
    #     ("ind_n", C.c_int),
    #     ("observations", ndpointer(dtype=np.float64, ndim=2, flags='C')),
    #     ("observations_n", C.c_int),
    #     ("observations_m", C.c_int),
    # ])

    # f.argtypes = kwargs.values()

    # kwargs = OrderedDict([
    #     ("ind", C.POINTER(C.c_float)),
    #     ("ind_n", C.c_int),
    #     ("observations", ndpointer(dtype=np.float64, ndim=2, flags='C')),
    #     ("observations_n", C.c_int),
    #     ("observations_m", C.c_int),
    #     ("n_rules", C.c_int),
    #     ("max_vars_per_rules", C.c_int),
    #     ("n_labels", C.c_int),
    #     ("n_consequents", C.c_int),
    #     ("default_rule_cons", ndpointer(dtype=np.float64, ndim=1, flags='C')),
    #     ("default_rule_cons_n", C.c_int),
    #     ("vars_range", ndpointer(dtype=np.float64, ndim=2, flags='C')),
    #     ("vars_range_n", C.c_int),
    #     ("vars_range_m", C.c_int),
    #     ("labels_weights", ndpointer(dtype=np.float64, ndim=1, flags='C')),
    #     ("labels_weights_n", C.c_int),  # FIXME: same as n_labels ?
    #     ("dc_idx", C.c_int)
    # ])
    # f.argtypes = kwargs.values()
    f.restype = C.c_float
    # f(ind,
    #   len(ind),
    #   observations,
    #   observations.shape[0],
    #   observations.shape[1],
    #   n_rules,
    #   max_vars_per_rule,
    #   n_labels,
    #   n_consequents,
    #   default_rule_cons,
    #   len(default_rule_cons),
    #   vars_ranges,
    #   vars_ranges.shape[0],
    #   vars_ranges.shape[1],
    #   labels_weights,
    #   len(labels_weights),
    #   dc_idx
    #   )

    kwargs = OrderedDict([
        ("ind", _get_array_1d_ptr(ind, C.c_float)),
        ("ind_n", len(ind)),
        ("observations", (_get_c_array_from_np(observations, C.c_double))),
        # _get_c_array_from_np(observations, C.c_double)),
        ("observations_n", observations.shape[0]),
        ("observations_m", observations.shape[1]),
        ("n_rules", n_rules),
        ("max_vars_per_rules", max_vars_per_rule),
        ("n_labels", n_labels),
        ("n_consequents", n_consequents),
        ("default_rule_cons", _get_np_array_1d_ptr(default_rule_cons, C.c_int)),
        ("default_rule_cons_n", len(default_rule_cons)),
        ("vars_range", _get_c_array_from_np(vars_ranges, C.c_double)),
        ("vars_range_n", vars_ranges.shape[0]),
        ("vars_range_m", vars_ranges.shape[1]),
        ("labels_weights", _get_np_array_1d_ptr(labels_weights, C.c_double)),
        ("labels_weights_n", len(labels_weights)),  # FIXME: same as n_labels ?
        ("dc_idx", dc_idx)
    ])

    # print("ind", ind)
    print("observations")
    print(observations[:2])
    # print("n_rules", n_rules)
    # print("max_vars_per_rule", max_vars_per_rule)
    # print("n_labels", n_labels)
    # print("n_consequents", n_consequents)
    # print("default_rule_cons", default_rule_cons)
    # print("vars_ranges\n", vars_ranges)
    # print("labels_weights", labels_weights)
    # print("dc_idx", dc_idx)

    print("shape", observations.shape)
    # res = f(c_ind, len(ind))

    f.restype = C.c_float
    res = f(*kwargs.values())  # cannot pass keyword args to native function
    print("res", res)

    # print("py res", np.sum(observations[:, 0]))

    n_obs = observations.shape[0]
    n_vars = observations.shape[1]
    _, evo_ants, _ = IFSUtils.extract_ind_new(ind, n_vars, n_labels, n_rules,
                                              n_consequents)
    # print("evo_ants shape", evo_ants.shape)
    # print("evo_ants", evo_ants)

    from time import sleep
    sleep(0.1)
    assert False, "trololo"

    predicted_outputs = np.array([])
    return predicted_outputs
