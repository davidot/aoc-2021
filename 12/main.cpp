#include <algorithm>
#include <cmath>
#include <deque>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <map>
#include <numeric>
#include <set>
#include <sstream>
#include <vector>

using namespace std;

static int next_num = 0;

struct Node {
  Node(string name_) : name(name_), id(next_num++), is_big(isupper(name_[0])) {}
  string name{};
  int id{-1};
  bool is_big{false};
  std::vector<int> edges{};
};

void solve(char *input_path) {
  std::ifstream file;
  file.open(input_path);
  if (!file.is_open()) {
    std::cout << "Could not open file:" << input_path << '\n';
    return;
  }
  next_num = 0;

  std::vector<Node> nodes{};
  nodes.reserve(10);

  const int start_num = nodes.emplace_back("start").id;
  const int end_num = nodes.emplace_back("end").id;

  if (start_num != 0) {
    cout << "Start is not 0?? " << start_num << "_\n";
    return;
  }

  {
    auto get_id = [&](string const &name) {
      auto nm = std::find_if(nodes.begin(), nodes.end(), [&](Node const &node) {
        return node.name == name;
      });
      if (nm != nodes.end())
        return nm->id;
      return nodes.emplace_back(name).id;
    };

    string from;
    string to;
    string line;
    line.reserve(100);
    while (getline(file, line)) {
      if (line.empty() || line == "\n") {
        continue;
      }

      auto split = line.find('-');
      if (split == string::npos) {
        cout << "No - to split on?? _" << line << "_\n";
        return;
      }

      from = line.substr(0, split);
      to = line.substr(split + 1);

      int from_id = get_id(from);
      int to_id = get_id(to);

      nodes[from_id].edges.push_back(to_id);
      nodes[to_id].edges.push_back(from_id);
    }
  }

#if 0
    for (auto& n : nodes) {
      cout << '[' << n.id << (n.is_big ? "BIG" : "   ") << "] : ";
      for (auto d : n.edges) {
        cout << d << ", ";
      }
      cout << '\n';
    }
#endif

  struct Path {
    Path() : curr(0) { path.push_back(0); }
    Path(bool) : curr(0) {
      path.push_back(0);
    }
    Path(Path &before, int step) : path(before.path), curr(step) {
      path.push_back(curr);
    }

    Path(Path &before, int step, bool has_double_) : path(before.path), curr(step), has_double(has_double_) {
      path.push_back(curr);
    }

    vector<int> path{};
    int curr = -1;
    bool has_double = false;

    bool has_id1(Node &node) const {
      if (node.is_big)
        return false;
      return std::find(path.begin(), path.end(), node.id) != path.end();
    }

    bool has_id2(Node &node) const {
      if (node.is_big)
        return false;
      if (!has_double)
        return false; // we assume no start here!

      return std::find(path.begin(), path.end(), node.id) != path.end();
    }

    Path step1(int next) { return Path(*this, next); }

    Path step2(int next, vector<Node>& nodes) {
      if (!nodes[next].is_big && has_id1(nodes[next])) {
        if (has_double)
          cout << "Double double??\n";
        return Path(*this, next, true);
      }
      return Path(*this, next, has_double);
    }
  };

  std::deque<Path> paths;
  paths.emplace_back();

  size_t finished_paths1 = 0;

  while (!paths.empty()) {
    auto front = move(paths.front());
    paths.pop_front();

    for (int next : nodes[front.curr].edges) {
      if (next == start_num)
        continue;
      if (next == end_num) {
        finished_paths1++;
        continue;
      }
      if (front.has_id1(nodes[next]))
        continue;

      paths.push_back(front.step1(next));
    }
  }

  cout << "Visiting small caves at most once: Total paths: " << finished_paths1
       << '\n';

  size_t finished_paths2 = 0;
  paths.emplace_back(true);

  while (!paths.empty()) {
    auto front = move(paths.front());
    paths.pop_front();

    for (int next : nodes[front.curr].edges) {
      if (next == start_num)
        continue;
      if (next == end_num) {
        finished_paths2++;
//        for (auto& i : front.path) {
//          cout << nodes[i].name << ",";
//        }
//        cout << "end\n";
        continue;
      }
      if (front.has_id2(nodes[next]))
        continue;

      paths.push_back(front.step2(next, nodes));
    }
  }

  cout << "Visiting one! small caves at most twice: Total paths: " << finished_paths2
       << '\n';
}

int main(int argc, char **argv) {
  if (argc < 2) {
    std::cout << "Give file to run on like: " << argv[0] << " sample.txt\n";
    return -1;
  }

  for (int i = 1; i < argc; i++) {
    std::cout << "-----------[ " << argv[i] << " ]---------------\n";
    solve(argv[i]);
  }
}
