#include <fstream>
#include <iostream>
#include <string>
#include <vector>
#include <limits>
#include <queue>

using std::cout;            using std::ifstream;
using std::priority_queue;  using std::string;
using std::vector;          using std::pair;

vector<string> read_input(const char* filepath)
{
  ifstream       in_f(filepath);
  string         line;
  vector<string> ret;

  while(std::getline(in_f, line))
    ret.push_back(line);

  return ret;
}

class node
{
  public:
  size_t x, y;
  int d;

  node(size_t x, size_t y, int d) : x(x), y(y), d(d) {}
  node() : node(0, 0, 0) {}

  bool operator <(const node& rhs) const { return d > rhs.d; }
};

void extend_map(vector<vector<int>> &d)
{
  vector<vector<int>> big;

  for(size_t i = 0; i != d.size() * 5; ++i)
    big.push_back(vector<int>(d[0].size() * 5,
      std::numeric_limits<int>::max()));

  d = big;
}

int smart_get(const vector<vector<int>> &r, size_t x, size_t y)
{
  auto ret = r[x % (r.size())][y % (r[0].size())];
  ret += x / r.size() + y / r[0].size();

  if(ret > 9)
    ret = (ret % 10) + 1;

  return ret;
}

vector<pair<size_t,size_t>> get_neighbors(size_t x, size_t y,
  size_t lim_x, size_t lim_y)
{
  vector<pair<size_t,size_t>> ret;

  if(x != 0) { ret.push_back(pair(x - 1, y)); }
  if(x != lim_x - 1) { ret.push_back(pair(x + 1, y)); }
  if(y != 0) { ret.push_back(pair(x, y - 1)); }
  if(y != lim_y - 1) { ret.push_back(pair(x, y + 1)); }

  return ret;
}

int dijkstra(vector<vector<int>> &d, const vector<vector<int>> &r)
{
  priority_queue<node> q;
  q.push(node(0, 0, 0));
  d[0][0] = 0;

  while(!q.empty())
  {
    auto n      = q.top();
    auto curr_d = d[n.x][n.y];
    q.pop();

    for(auto const &p : get_neighbors(n.x, n.y, d.size(), d[0].size()))
    {
      auto risk  = smart_get(r, p.first, p.second);
      auto new_d = curr_d + risk;

      if(new_d < d[p.first][p.second])
      {
        d[p.first][p.second] = new_d;
        q.push(node(p.first, p.second, new_d));
      }
    }
  }

  return d[d.size() - 1][d[0].size() - 1];
}

int main()
{
  vector<string> input = read_input("inputs/d15.txt");

  // Parse input
  vector<vector<int>> dist;
  vector<vector<int>> risk;
  for(auto const &s : input)
  {
    vector<int> new_r;

    for(size_t j = 0; j != s.length(); ++j)
      new_r.push_back(s[j] - '0');

    risk.push_back(new_r);
    dist.push_back(vector<int>(s.length(), std::numeric_limits<int>::max()));
  }

  // Silver
  cout << dijkstra(dist, risk) << "\n";

  // Gold
  extend_map(dist);
  cout << dijkstra(dist, risk) << "\n";

  return 0;
}
