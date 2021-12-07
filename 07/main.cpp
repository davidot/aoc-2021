#include <iostream>
#include <fstream>
#include <vector>
#include <cmath>
#include <algorithm>
#include <numeric>

void solve(char* input_path) {
    std::ifstream file;
    file.open(input_path);
    if (!file.is_open()) {
        std::cout << "Could not open file:" << input_path << '\n';
        return;
    }
    
    std::vector<int64_t> numbers;
    numbers.reserve(1024);
    
    int64_t num;
    char c;
    while (file >> num >> c) {
        //std::cout << "Got number: _" << num << "_\n";
        numbers.push_back(num);
        if (c != ',')
            std::cout << "Read non comma!\n";
    }
    
    if (numbers.empty()) {
        std::cout << "Could not read a number??\n";
        return;
    }
    
    numbers.push_back(num);
    

    std::sort(numbers.begin(), numbers.end());
    
    int64_t minn = numbers[0];
    int64_t maxx = numbers[numbers.size() - 1];
    
    
    uint64_t least_sum = std::numeric_limits<uint64_t>::max();
    int64_t index = -1;
    
    for (int64_t i = minn; i <= maxx; i++) {
        uint64_t cost = std::accumulate(
            numbers.begin(), numbers.end(), 0ul,
            [i](uint64_t curr, int64_t val) {
                if (val == i)
                    return curr;
                if (val < i)
                    return curr + (i - val);
                return curr + (val - i);            
            });
        if (cost < least_sum) {
            least_sum = cost;
            index = i;
        }
    }
    
    std::cout << "#PART 1: Min cost: " << least_sum << " at " << index << '\n';

    double sum = std::accumulate(numbers.begin(), numbers.end(), 0.0);
    std::cout << "The sum is " << sum << '\n';
    sum /= numbers.size();
    int64_t val = std::llround(sum);
    std::cout << "Going to mean " << val << '\n';
    
    uint64_t least_sum2 = std::numeric_limits<uint64_t>::max();
    int64_t index2 = -1;
    
    
    for (int64_t i = minn; i <= maxx; i++) {
        uint64_t cost = std::accumulate(
            numbers.begin(), numbers.end(), 0ul,
            [i](uint64_t curr, int64_t val) {
                if (val == i)
                    return curr;
                uint64_t distance = val < i ? (i - val) : (val - i);
                return curr + ((distance * (distance + 1)) / 2);
            });
        if (cost < least_sum2) {
            least_sum2 = cost;
            index2 = i;
        }
    }

    std::cout << "#PART 2: Min cost: " << least_sum2 << " at " << index2 << '\n';

}



int main(int argc, char** argv) {
    if (argc < 2) {
        std::cout << "Give file to run on like: " << argv[0] << " sample.txt\n";
        return -1;
    }
    
    solve(argv[1]);
}

