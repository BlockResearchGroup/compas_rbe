#include <igl/active_set.h>
#include <igl/invert_diag.h>
#include <Eigen/Sparse>
#include <iostream>
  

int main()
{
    // mininimse  0.5 * zT * Q * z + zTB + constant
    // such that  zb = zbc and Aeq * z = Beq

    // Q   : n x n positive semi-definite matrix of quadratic coefficients
    // B   : n x 1 vector of linear coefficients
    // zb  : b x 1 portion of z corresponding to fixed vertices
    // zbc : b x 1 vector of known values corresponding to zb
    // Aeq : m x n matrix of linear equality constraint coefficients (one per row constraint)
    // Beq : m x 1 vector of linear equality constraint RHS values


    Eigen::VectorXi zb;
    Eigen::VectorXd B, zbc, lx, ux, Beq, Bieq, Z;

    Eigen::SparseMatrix<double> Q, Aeq, Aieq;

    // Eigen::MatrixXd V;
    // Eigen::MatrixXi F;

    // igl::readOFF(TUTORIAL_SHARED_PATH "/cheburashka.off",V,F);

    // // One fixed point
    // b.resize(1,1);
    // b<<2556;

    // bc.resize(1,1);
    // bc<<1;

    // // Construct Laplacian and mass matrix
    // Eigen::SparseMatrix<double> L,M,Minv;

    // igl::cotmatrix(V,F,L);
    // igl::massmatrix(V,F,igl::MASSMATRIX_TYPE_VORONOI,M);

    // // M = (M/M.diagonal().maxCoeff()).eval();
    // igl::invert_diag(M,Minv);

    // // Bi-Laplacian
    // Q = L.transpose() * (Minv * L);

    // // Zero linear term
    // B = VectorXd::Zero(V.rows(),1);

    // // Lower and upper bound
    // lx = VectorXd::Zero(V.rows(),1);
    // ux = VectorXd::Ones(V.rows(),1);

    // // Equality constraint constrain solution to sum to 1
    // Beq.resize(1,1);
    // Beq(0) = 0.08;
    // Aeq = M.diagonal().sparseView().transpose();

    // Inequality constraints

    igl::active_set_params as;
    as.max_iter = 8;

    igl::active_set(Q, B, b, bc, Aeq, Beq, Aieq, Bieq, lx, ux, as, Z);

    return 0;
}
