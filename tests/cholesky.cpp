#include <iostream>
#include <Eigen/Sparse>
#include <Eigen/CholmodSupport>

int main() {
    // Ax = b
    Eigen::SparseMatrix<double> A(4, 4); // Semi-Positive Definite
    Eigen::VectorXd b(4);

    std::vector<Eigen::Triplet<double>> triplets;

    triplets.push_back({0, 0, 4});
    triplets.push_back({1, 1, 5});
    triplets.push_back({2, 2, 6});
    triplets.push_back({3, 3, 7});
    triplets.push_back({0, 1, 1});
    triplets.push_back({1, 0, 1});
    triplets.push_back({1, 2, 1});
    triplets.push_back({2, 1, 1});
    triplets.push_back({2, 3, 1});
    triplets.push_back({3, 2, 1});

    A.setFromTriplets(triplets.begin(), triplets.end());

    b << 1, 2, 3, 4;

    // sparse Cholesky
    Eigen::SimplicialLLT<Eigen::SparseMatrix<double>> solver;
    solver.compute(A);

    if (solver.info() != Eigen::Success) {
        std::cerr << "Decomposition failed" << std::endl;
        return -1;
    }

    Eigen::VectorXd x = solver.solve(b);

    std::cout << "Solution x:\n" << x << std::endl;

    return 0;
}

// Learn Lu, QR, Cholesky, bundle adjustment/slam, QP/LP, Sparse Regression (lasso)