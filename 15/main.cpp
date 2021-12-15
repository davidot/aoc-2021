#include <iostream>
#include <fstream>
#include <vector>
#include <cmath>
#include <algorithm>
#include <numeric>
#include <sstream>
#include <iomanip>
#include <deque>
#include <queue>

using namespace std;

int best_path(vector<vector<int>> const& grid) {

  int width = grid[0].size();
  int height = grid.size();

  cout << "width: " << width << ", " << height << '\n';

  struct Coord {
    Coord(int x_, int y_) : x(x_), y(y_) {}
    int x;
    int y;
  };


  if (width != height) {
    cout << "Can only do squares!\n";
    return -1;
  }

  std::vector<std::vector<int>> best(height, vector<int>(width, 1000000));
  std::vector<std::vector<char>> visited(height, vector<char>(width, 0));
  best[0][0] = 0;

  size_t visited_count = 0;

  std::array<std::pair<int, int>, 4> offsets {{
      {-1, 0},
      {1, 0},
      {0, -1},
      {0, 1},
  }};

  auto min_non_visited = [&] {
    int xx = -1;
    int yy = 0;
    int min_score = 10000000;

    for (int x = 0; x < width; x++) {
      for (int y = 0; y < width; y++) {
        if (visited[x][y] != 0)
          continue;

        if (best[x][y] < min_score) {
          min_score = best[x][y];
          xx = x;
          yy = y;
        }
      }
    }

    return std::make_pair(xx, yy);
  };


  while (visited[width - 1][width -1] == 0) {
    auto [x, y] = min_non_visited();

    for (auto& off : offsets) {
      int xx = x + off.first;
      int yy = y + off.second;
      if (xx < 0 || xx >= height || yy < 0 || yy >= width)
        continue;
      if (visited[xx][yy] != 0)
        continue;
      best[xx][yy] = min(best[xx][yy], best[x][y] + grid[xx][yy]);
    }

    visited[x][y] = 1;
//    visited_count++;
//    if (visited_count % 500 == 500) cout << " visited: " << visited_count << '\n';
  }


//  for (int x = 0; x < width; x++) {
//    for (int y = 0; y < width; y++) {
//      cout << setw(3) << min(best[x][y], 999) << ' ';
//    }
//    cout << '\n';
//  }

  return best[width - 1][height - 1];
}

void solve(char* input_path) {
    std::ifstream file;
    file.open(input_path);
    if (!file.is_open()) {
        std::cout << "Could not open file:" << input_path << '\n';
        return;
    }


    std::vector<std::vector<int>> grid;

    {
      std::string line;
      while (std::getline(file, line)) {
        if (line.empty() || line == "\n") {
          continue;
        }
        auto& row = grid.emplace_back();
        for (char c : line) {
          row.push_back(static_cast<int>(c - '0'));
        }
      }
    }

    if (grid.empty()) {
      std::cout << "no input\n";
      return;
    }


    std::cout << "PART 1: Best score: " << best_path(grid) << '\n';

    vector<vector<int>> grid2 {grid.size() * 5, std::vector<int>(grid.size() * 5, -1)};

    for (int i = 0; i < 5; i++) {
      for (int j = 0; j < 5; j++) {

        int add = i + j;
        size_t baseX = i * grid.size();
        size_t baseY = j * grid.size();

        for (size_t x = 0; x < grid.size(); x++) {
          for (size_t y = 0; y < grid.size(); y++) {
            grid2[baseX + x][baseY + y] = (((grid[x][y] - 1) + add) % 9) + 1;
          }
        }
      }
    }

//    for (size_t x = 0; x < grid.size(); x++) {
//      for (size_t y = 0; y < grid.size(); y++) {
//        for (size_t i = 0; i < 5; i++) {
//          size_t yy = y + i * grid.size();
//          grid2[x][yy] = (((grid[x][y] - 1) + i) % 9) + 1;
//        }
//      }
//    }

//    for (size_t x = 0; x < grid2.size(); x++) {
//      for (size_t y = 0; y < grid2.size(); y++) {
//        cout << grid2[x][y];
//      }
//      cout << '\n';
//    }

    std::cout << "PART 2: Best score: " << best_path(grid2) << '\n';
}



int main(int argc, char** argv) {
    if (argc < 2) {
        std::cout << "Give file to run on like: " << argv[0] << " sample.txt\n";
        return -1;
    }
    
    solve(argv[1]);
}
