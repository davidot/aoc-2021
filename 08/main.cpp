#include <iostream>
#include <fstream>
#include <vector>
#include <cmath>
#include <algorithm>
#include <numeric>
#include <sstream>

void solve(char* input_path) {
    std::ifstream file;
    file.open(input_path);
    if (!file.is_open()) {
        std::cout << "Could not open file:" << input_path << '\n';
        return;
    }


    struct Line {
      Line() {
        words.reserve(10);
        outputs.reserve(4);
      }
      std::vector<std::string> words;
      std::vector<std::string> outputs;
    };

    std::vector<Line> inputs;
    inputs.reserve(200);

    {
      std::string line;
      while (std::getline(file, line)) {
        if (line.size() <= 1 || line[0] == '\n')
          break;
        std::istringstream line_stream{line};
        std::string word;

        Line l;

        bool pre_bar = true;

        while (line_stream) {
          line_stream >> word;
          if (word == "|") {
            pre_bar = false;
            continue;
          }

          if (word.empty())
            continue;

          if (pre_bar)
            l.words.push_back(move(word));
          else
            l.outputs.push_back(move(word));
        }

        inputs.push_back(l);
      }
    }

    std::cout << "Have " << inputs.size() << " inputs!\n";

    std::array<uint32_t, 10> counts = {
        6, 2, 5, 5, 4, 5, 6, 3, 7, 6
    };


    std::array<uint32_t, 4> unique_counts = {
        2, 4, 3, 7
    };

    int64_t one_four_seven_eight_count = 0;

    for (auto& line : inputs) {
      for (auto& digit : line.outputs) {
//        std::cout << " _" << digit << "_ ";
        if (digit.size() <= 4 || digit.size() == 7)
          one_four_seven_eight_count++;
      }
//      std::cout << "    -> " << one_four_seven_eight_count << '\n';
    }

    std::cout << "Got " << one_four_seven_eight_count << " 1,4,7 and 8's\n";


    uint64_t sum = 0;

    const size_t a = 0;
    const size_t b = 1;
    const size_t c = 2;
    const size_t d = 3;
    const size_t e = 4;
    const size_t f = 5;
    const size_t g = 6;

    for (auto& line : inputs) {
      std::string perm = "abcdefg";

      std::string needed;
      needed.reserve(8);

      auto is_valid =[&](std::string const& input)  {
        auto check_perm = [&] {
          bool is_perm = std::is_permutation(needed.begin(), needed.end(), input.begin());
          needed.clear();
          return is_perm;
        };

        if (input.size() <= 4 || input.size() == 7) {

          switch (input.size()) {
            case 2:
              // 1
              needed.push_back(perm[c]);
              needed.push_back(perm[f]);
              break;
            case 3:
              // 7
              needed.push_back(perm[a]);
              needed.push_back(perm[c]);
              needed.push_back(perm[f]);
              break;
            case 4:
              // 4
              needed.push_back(perm[b]);
              needed.push_back(perm[c]);
              needed.push_back(perm[d]);
              needed.push_back(perm[f]);
              break;
            case 7:
              // 8
              needed.append("abcdefg");
              break;
            default:
              std::cout << "WJAT???\n";
              std::terminate();
              break;
          }

          return check_perm();
        }

        if (input.size() == 6) {
          {
            // 0
            needed.push_back(perm[a]);
            needed.push_back(perm[b]);
            needed.push_back(perm[c]);
            needed.push_back(perm[e]);
            needed.push_back(perm[f]);
            needed.push_back(perm[g]);
            if (check_perm())
              return true;
          }

          {
            // 6
            needed.push_back(perm[a]);
            needed.push_back(perm[b]);
            needed.push_back(perm[d]);
            needed.push_back(perm[e]);
            needed.push_back(perm[f]);
            needed.push_back(perm[g]);
            if (check_perm())
              return true;
          }

          {
            // 9
            needed.push_back(perm[a]);
            needed.push_back(perm[b]);
            needed.push_back(perm[c]);
            needed.push_back(perm[d]);
            needed.push_back(perm[f]);
            needed.push_back(perm[g]);
            if (check_perm())
              return true;
          }

          return false;
        }

        {
          // 2
          needed.push_back(perm[a]);
          needed.push_back(perm[c]);
          needed.push_back(perm[d]);
          needed.push_back(perm[e]);
          needed.push_back(perm[g]);
          if (check_perm())
            return true;
        }

        {
          // 3
          needed.push_back(perm[a]);
          needed.push_back(perm[c]);
          needed.push_back(perm[d]);
          needed.push_back(perm[f]);
          needed.push_back(perm[g]);
          if (check_perm())
            return true;
        }

        {
          // 5
          needed.push_back(perm[a]);
          needed.push_back(perm[b]);
          needed.push_back(perm[d]);
          needed.push_back(perm[f]);
          needed.push_back(perm[g]);
          if (check_perm())
            return true;
        }

        return false;
      };

      auto all_valid = [&] {
        for (auto& digit : line.words) {
          if (!is_valid(digit))
            return false;
        }

        for (auto& digit : line.outputs) {
          if (!is_valid(digit))
            return false;
        }

        return true;
      };


      while (!all_valid()) {
        if (!std::next_permutation(perm.begin(), perm.end())) {
          std::cout << "Wrapped!!!\n";
          break;
        }
      }

//      std::cout << "Got permutation " << perm << '\n';

      auto to_digit = [&perm](std::string const& digit) {
        switch (digit.size()) {
          case 2:
            return 1;
          case 3:
            return 7;
          case 4:
            return 4;
          case 7:
            return 8;
          case 6: {
            // 0, 6, 9
            if (digit.find(perm[d]) == std::string::npos) {
              return 0;
            }
            if (digit.find(perm[c]) == std::string::npos) {
              return 6;
            }

            return 9;
          }
          case 5: {
            // 2, 3, 5
            if (digit.find(perm[c]) == std::string::npos)
              return 5;
            if (digit.find(perm[e]) == std::string::npos)
              return 3;
            return 2;
          }
          default:
            break;
        }

        std::cout << "Cannot convert to digit??\n";
        std::terminate();
        return -1;
      };

      int64_t output = 0;
      int64_t multiplier = 1000;

      for (auto& out : line.outputs) {
        output += multiplier * to_digit(out);
        multiplier /= 10;
      }

      sum += output;
    }

    std::cout << "#PART 2 Got total sum value:" << sum << '\n';
}



int main(int argc, char** argv) {
    if (argc < 2) {
        std::cout << "Give file to run on like: " << argv[0] << " sample.txt\n";
        return -1;
    }
    
    solve(argv[1]);
}
