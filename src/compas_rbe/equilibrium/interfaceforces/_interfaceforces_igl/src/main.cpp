// g++ -shared -fPIC src/main.cpp -o iforces.so
// g++ -shared -fPIC -I/opt/local/eigen -I/opt/local/libigl/include src/main.cpp -o iforces.so
// or use export CPLUS_INCLUDE_PATH=/opt/local/eigen:/opt/local/libigl/include

#include <igl/cotmatrix.h>
#include <Eigen/Dense>
#include <Eigen/Sparse>
#include <iostream>

extern "C" int compute_iforces();

int compute_iforces()
{
    Eigen::MatrixXd V(4,2);
    V<<0,0,
       1,0,
       1,1,
       0,1;

    Eigen::MatrixXi F(2,3);
    F<<0,1,2,
       0,2,3;

    Eigen::SparseMatrix<double> L;

    igl::cotmatrix(V,F,L);

    std::cout<<"Hello, mesh: "<<std::endl<<L*V<<std::endl;

    return 0;
}
