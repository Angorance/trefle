#ifndef FIS_H
#define FIS_H

#include "../hpp/custom_eigen_td.h"
#include <Eigen/Core>
#include <iostream>

using namespace Eigen;
using namespace std;

void mul_np_array(double *arr, int arr_n, int scaler);

float predict(float *ind, int ind_n, double *observations, int observations_r,
              int observations_c, int n_rules, int max_vars_per_rules,
              int n_labels, int n_consequents, int *default_rule_cons,
              int default_rule_cons_n, double *vars_range, int vars_range_r,
              int vars_range_c, double *labels_weights, int labels_weights_n,
              int dc_idx);

double omp_sum(double **arr, int arr_n);
void extract_mfs_from_ind(float *ind, double **evo_mfs, int n_vars,
                          int n_labels);

void extract_ants_from_ind(float *ind, double **evo_ants, int n_vars,
                           int n_labels);

MatrixXi evo_ants1ifs_ants(const Map<MatXf> &evo_ants,
                           Map<RowVectorXd> &vec_labels_weights);

MatrixXd evo_mfs2ifs_mfs(const Map<MatXf> &evo_mfs, Map<MatXd> &m_vars_range);

int unitfloat2idx(float flt, Map<RowVectorXd> &weights);

template <typename T, typename U>
void array1d_to_2d(T *in, U **out, int n, int m);
#endif
