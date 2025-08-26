#include <iostream>
using namespace std;

int countDigits(int n) {
    if (n == 0) return 1; // Special case for 0
    int count = 0;
    while (n != 0) {
        n /= 10;
        count++;
    }
    return count;
}

int main() {
    int n;
    cin >> n;
    cout << countDigits(n) << endl;
    return 0;
}
