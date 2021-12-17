#include <fstream>
#include <iostream>
#include <string>
#include <vector>
#include <map>

using std::cout;   using std::ifstream;
using std::map;    using std::string;
using std::vector; using std::pair;

vector<string> read_input(const char* filepath)
{
  ifstream       in_f(filepath);
  string         line;
  vector<string> ret;

  while(std::getline(in_f, line))
    ret.push_back(line);

  return ret;
}

vector<int> valid_x_at_time(int t, const pair<int,int> &x)
{
  vector<int> ret;

  if(t == 1)
  {
    for(int i = x.first; i != x.second + 1; ++i)
      ret.push_back(i);
    return ret;
  }

  for(int start_x = 0; start_x != x.first; ++start_x)
  {
    int pos = t >= start_x ? start_x * (start_x + 1) / 2 :
                             t * ((start_x - t + 1) + start_x) / 2;

    if(pos >= x.first && pos <= x.second)
      ret.push_back(start_x);
  }

  return ret;
}

int y_pos(int start, int t)
{
  int ret = 0;

  for(size_t i = 0; i != t; ++i)
  {
    ret += start;
    --start;
  }

  return ret;
}

pair<int,int> solve(const pair<int,int> &x, const pair<int,int> &y)
{
  int high  = 0;
  map<pair<int,int>,int> valid;

  for(int i = -200; i != 200; ++i)
  {
    for(int t = 0; true; ++t)
    {
      int pos = y_pos(i, t);

      if(pos >= y.first && pos <= y.second)
      {
        for(const auto &v : valid_x_at_time(t, x))
          ++valid[pair<int,int>(v, i)];

        high = i > high ? i : high;
      } else if(pos < y.first) {
        break;
      }
    }
  }

  return pair<int,int>(high * (high + 1) / 2, valid.size());
}

int main()
{
  vector<string> input = read_input("inputs/d17.txt");

  // Parse input
  pair<int,int> x_lims, y_lims;
  auto s = input[0];
  auto comma_pos = s.find(",");
  auto x_string = s.substr(s.find("=") + 1, comma_pos);
  auto y_string = s.substr(s.find("=", comma_pos) + 1, s.length() - 1);
  x_lims.first = std::stoi(x_string.substr(0, x_string.find("..")));
  x_lims.second = std::stoi(x_string.substr(x_string.find("..") + 2,
                                            x_string.length() - 1));
  y_lims.first = std::stoi(y_string.substr(0, y_string.find("..")));
  y_lims.second = std::stoi(y_string.substr(y_string.find("..") + 2,
                                            y_string.length() - 1));

  // Get results
  auto p = solve(x_lims, y_lims);
  // Silver
  cout << p.first << "\n";
  // Gold
  cout << p.second << "\n";

  return 0;
}
