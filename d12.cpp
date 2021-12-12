#include <fstream>
#include <iostream>
#include <string>
#include <vector>
#include <set>
#include <map>
#include <algorithm>

using std::cout;   using std::ifstream;
using std::set;    using std::map;
using std::string; using std::vector;

vector<string> read_input(const char* filepath)
{
  ifstream in_f(filepath);
  string line;
  vector<string> ret;

  while(std::getline(in_f, line))
    ret.push_back(line);

  return ret;
}

// Just store the Node's id, neighbors, and if it's big or not
class node
{
  public:

  string         id;
  bool           is_big;
  vector<string> neighbors;

  node(const string &id) : id(id)
  {
    is_big = std::all_of(id.begin(), id.end(),
      [](unsigned char c){ return std::isupper(c); });
  }
  node() : node("") {}

  void add_neighbor(const string &s) { neighbors.push_back(s); }
  bool can_repeat() const { return !is_big and id != "start" and id != "end"; }
  bool operator <(const node &rhs) const { return id < rhs.id; }
};

void find_paths(const node &curr, string path, map<string, node> nodes,
  set<string> &paths, map<string, size_t> &visited, const string& repeat)
{
  auto updated_path = path + curr.id + ",";

  if(curr.id == "end")
  {
    paths.emplace(updated_path);
    return;
  }

  ++visited[curr.id];

  for(const auto &s : curr.neighbors)
  {
    auto n = nodes[s];
    if((!n.is_big && visited[s] > 0 && s != repeat) ||
       (s == repeat && visited[s] > 1))
      continue;

    find_paths(n, updated_path, nodes, paths, visited, repeat);
  }

  --visited[curr.id];
}

int main()
{
  vector<string> input = read_input("inputs/d12.txt");

  // Build "graph"
  map<string, node> nodes;
  map<string, size_t>   visited;
  for(const auto &s : input)
  {
    auto dash = s.find("-");
    auto s0 = s.substr(0, dash);
    auto s1 = s.substr(dash + 1, s.length());

    if(nodes.find(s0) == nodes.end())
      nodes[s0] = node(s0);
    if(nodes.find(s1) == nodes.end())
      nodes[s1] = node(s1);

    nodes[s0].add_neighbor(s1);
    nodes[s1].add_neighbor(s0);
    visited[s0] = 0;
    visited[s1] = 0;
  }

  // Output silver
  set<string> paths;
  find_paths(nodes["start"], "", nodes, paths, visited, "");
  cout << paths.size() << "\n";

  // Output gold
  set<string> gold_paths;
  for(const auto &p : nodes)
  {
    if(!p.second.can_repeat())
      continue;

    find_paths(nodes["start"], "", nodes, gold_paths, visited, p.first);
  }
  cout << gold_paths.size() << "\n";

  return 0;
}
