#include <Eigen/Dense>
#include <Eigen/Sparse>
#include <iostream>

extern "C" int compute_iforces(int v, double **vertices);

int compute_iforces(int v, double **vertices)
{
	int i;
	double sum;

	for (i = 0; i < v; i++) {
		sum = vertices[i][0] + vertices[i][1] + vertices[i][2];

	    std::cout << "sum coods vertex i: " << sum << std::endl;
	}

	return 0;
}
