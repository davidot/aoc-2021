#include <iostream>
#include <fstream>
#include <vector>
#include <cmath>
#include <algorithm>
#include <numeric>
#include <sstream>
#include <iomanip>

void solve(char* input_path) {
    std::ifstream file;
    file.open(input_path);
    if (!file.is_open()) {
        std::cout << "Could not open file:" << input_path << '\n';
        return;
    }


    std::vector<std::vector<int>> heightmap;

    {
      std::string line;
      while (std::getline(file, line)) {
        if (line.empty() || line == "\n") {
          continue;
        }
        auto& row = heightmap.emplace_back();
        for (char c : line) {
          row.push_back(static_cast<int>(c - '0'));
        }
      }
    }

    if (heightmap.empty()) {
      std::cout << "no input\n";
      return;
    }

    int width = heightmap[0].size();
    int height = heightmap.size();

//    for (auto& a : heightmap) {
//      for (auto& c : a) {
//        std::cout << static_cast<int>(c);
//      }
//      std::cout << '\n';
//    }

//    std::cout << "Read " << heightmap.size() << " lines with " << heightmap[0].size() << " chars? \n";



    auto val_at = [&](int x, int y, int default_val) {
      if (x < 0 || x >= height || y < 0 || y >= width)
        return default_val;
      return heightmap[x][y];
    };


    uint64_t lowpoints_score = 0;
    struct Coord {
      Coord(int x_, int y_)
          : x(x_), y(y_) {}
      int x = -1;
      int y = -1;
      int val = 100;
    };

    std::vector<Coord> lowpoints;

    std::array<std::pair<int, int>, 4> offsets {{
        {-1, 0},
        {1, 0},
        {0, -1},
        {0, 1},
    }};

    int nines =0;

    for (int x = 0; x < height; x++) {
      for (int y = 0; y < width; y++) {
        if (heightmap[x][y] == 9)
          nines++;

        int min_neighbor = 10;

        for (auto& [xx, yy] : offsets) {
          int i = x + xx;
          int j = y + yy;
          auto val = val_at(i, j, 10);
          min_neighbor = std::min(min_neighbor, val);
        }

//        for (int i = x - 1; i <= x+1; i++) {
//          for (int j = y - 1; j <= y+1; j++) {
//            if (i == x && j == y)
//              continue;
//            auto val = val_at(i, j, 10);
//            min_neighbor = std::min(min_neighbor, val);
//          }
//        }

        auto val = val_at(x, y, 10);
        if (min_neighbor > val) {
          lowpoints_score += 1 + val;
          auto& pt = lowpoints.emplace_back(x, y);
          pt.val = val;
        }

      }
    }

    std::cout << "#PART 1 Lowpoints: " << lowpoints_score << '\n';


//    std::vector<int> basin_sizes;

    std::vector<std::vector<int>> done{(size_t)height, std::vector<int>((size_t)width, 0)};
    int next_basin = 1;



    auto val = [&](Coord c) {
      return val_at(c.x, c.y, 11);
    };

    auto val_xy = [&](int x, int y) {
      return val_at(x, y, 11);
    };

    std::vector<Coord> list;
    list.reserve(64);

    std::sort(lowpoints.begin(), lowpoints.end(), [](auto& a, auto& b) {
      return a.val < b.val;
    });

    for (auto& [x, y, _] : lowpoints) {
      if (done[x][y] != 0)
        continue;

      if (heightmap[x][y] >= 9)
        continue;



      list.emplace_back(x, y);

      int basin_size = 0;

      while (!list.empty()) {
        auto curr = list.back();
        list.pop_back();
        done[curr.x][curr.y] = next_basin;

//        auto curr_val = val(curr);

        for (auto& [xx, yy] : offsets) {
          int i = curr.x + xx;
          int j = curr.y + yy;

          auto neigh_val = val_xy(i, j);

          if (neigh_val >= 9)
            continue;

          if (done[i][j] != 0)
            continue;

//          if (neigh_val > curr_val)
          list.emplace_back(i, j);
          done[i][j] = next_basin;
        }


//        for (int i = curr.x - 1; i <= curr.x+1; i++) {
//          for (int j = curr.y - 1; j <= curr.y + 1; j++) {
//            if (i == curr.x && j == curr.y)
//              continue;


//            auto neigh_val = val_xy(i, j);
//
//            if (neigh_val >= 9)
//              continue;
//
//            if (done[i][j] != 0)
//              continue;
//
//            if (neigh_val > curr_val)
//              list.emplace_back(i, j);
//
//          }
//        }


        ++basin_size;
      }


      std::cout << std::setfill('0') << std::setw(2) << std::hex << next_basin << " Was of size: " << std::dec << basin_size << '\n';
//      basin_sizes.push_back(basin_size);
      next_basin++;
    }

    std::vector<int> basin_sizes(next_basin, 0);

    std::cout << std::hex;
    for (auto& a : done) {
      for (auto& c : a) {
        if (c != 0)
          basin_sizes[c]++;
        std::cout << std::setfill('0') << std::setw(2) << c << ' ';
      }
      std::cout << '\n';
    }


    for (size_t i = 0; i < basin_sizes.size(); i++) {
      std::cout << std::setfill('0') << std::setw(2) << std::hex << i << " Was of size: " << std::dec << basin_sizes[i] << '\n';
    }

//    std::cout << std::hex;
//    int x = 0;
//    for (auto& a : heightmap) {
//      int y = 0;
//      for (auto& c : a) {
//        std::cout << std::setfill('0') << std::setw(2) << c;
//        if (std::find_if(lowpoints.begin(), lowpoints.end(), [&](Coord const& c) {
//              return c.x == x && c.y == y;
//            }) != lowpoints.end())
//          std::cout << '*';
//        else
//          std::cout << ' ';
//
//        y++;
//      }
//      x++;
//      std::cout << '\n';
//    }

    std::cout << std::dec;

    std::cout << "Have " << basin_sizes.size() << " basisn\n";

    std::sort(basin_sizes.begin(), basin_sizes.end(), std::greater());
//    std::reverse(basin_sizes.begin(), basin_sizes.end());

    if (basin_sizes.size() < 3) {
      std::cout << "Less than 3 basins\n";
    } else {
      std::cout << "Top 3 sizes: " << basin_sizes[0] << ", " << basin_sizes[1] << ", " << basin_sizes[2] << '\n';
      std::cout << "#PART 2 Product: " << (basin_sizes[0] * basin_sizes[1] * basin_sizes[2]) << '\n';
    }

    auto sum = std::accumulate(basin_sizes.begin(), basin_sizes.end(), 0);
    std::cout << "Total " << sum << " nines " << nines << " size: " << (width * height) << " vs" << sum + nines << '\n';




//    std::vector<std::vector<char>> visited{(size_t)height, std::vector<char>((size_t)width, 0)};
//
//    for (int x = 0; x < height; x++) {
//      for (int y = 0; y < width; y++) {
//        if (visited[x][y] != 0)
//          continue;
//
//        if (val[x][y] >= 9)
//          continue;
//
//        list.emplace_back(x, y);
//
//        int basin_size = 0;
//
//        while (!list.empty()) {
//          auto curr = list.back();
//          list.pop_back();
//
//          for (auto &[xx, yy] : offsets) {
//            int i = curr.x + xx;
//            int j = curr.y + yy;
//
//            auto neigh_val = val_xy(i, j);
//
//            if (neigh_val >= 9)
//              continue;
//
//            if (visited[i][j] != 0)
//              continue;
//
//            list.emplace_back(i, j);
//          }
//        }
//
//        visited[x][y] = 1;
//        std::cout << std::setfill('0') << std::setw(2) << std::hex << next_basin << " Was of size: " << std::dec << basin_size << '\n';
//        basin_sizes.push_back(basin_size);
//        next_basin++;
//      }
//    }
//
//
//    std::cout << std::dec;
//
//    std::cout << "Have " << basin_sizes.size() << " basisn\n";
//
//    std::sort(basin_sizes.begin(), basin_sizes.end(), std::greater());
//    //    std::reverse(basin_sizes.begin(), basin_sizes.end());
//
//    if (basin_sizes.size() < 3) {
//      std::cout << "Less than 3 basins\n";
//    } else {
//      std::cout << "Top 3 sizes: " << basin_sizes[0] << ", " << basin_sizes[1] << ", " << basin_sizes[2] << '\n';
//      std::cout << "#PART 2 Product: " << (basin_sizes[0] * basin_sizes[1] * basin_sizes[2]) << '\n';
//    }



}



int main(int argc, char** argv) {
    if (argc < 2) {
        std::cout << "Give file to run on like: " << argv[0] << " sample.txt\n";
        return -1;
    }
    
    solve(argv[1]);
}
