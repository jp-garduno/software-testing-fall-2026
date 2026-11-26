#include <iostream>

int main() {
  int n = 3;
  // std::cin>>n;
  int m[3][3] = {{1, -2, 4}, {3, 8, -6}, {5, 1, -10}};
  for (int e = 0; e < n; e++) {
    for (int f = 0; f < n; f++) {
      std::cout << m[e][f] << " ";
    }
    std::cout << std::endl;
  }
}
