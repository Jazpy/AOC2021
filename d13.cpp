#include <fstream>
#include <iostream>
#include <string>
#include <vector>
#include <set>
#include <array>

using std::cout;   using std::ifstream;
using std::stoi;   using std::set;
using std::string; using std::vector;
using std::pair;   using std::array;

vector<string> read_input(const char* filepath)
{
  ifstream       in_f(filepath);
  string         line;
  vector<string> ret;

  while(std::getline(in_f, line))
    ret.push_back(line);

  return ret;
}

pair<int,int> fold(pair<int,int> const &p, int line, bool along_x)
{
  pair<int,int> ret;

  if(along_x && p.first > line)
  {
    ret.first = line - (p.first - line);
    ret.second = p.second;
  } else if(!along_x && p.second > line) {
    ret.second = line - (p.second - line);
    ret.first = p.first;
  } else {
    ret.first = p.first;
    ret.second = p.second;
  }

  return ret;
}

int main()
{
  vector<string> input = read_input("inputs/d13.txt");

  // Parse input
  set<pair<int,int>> dots;
  vector<string>     instructions;
  for(auto const &s : input)
  {
    auto comma = s.find(",");

    if(comma != string::npos)
      dots.emplace(pair(stoi(s.substr(0, comma)),
                        stoi(s.substr(comma + 1, s.length()))));
    else if(s.length())
      instructions.push_back(s);
  }

  // Do the folds
  size_t inst_count = 0;
  for(auto const &inst : instructions)
  {
    bool along_x = inst.find("x") != string::npos;
    int  val = stoi(inst.substr(inst.find("=") + 1, inst.length()));

    set<pair<int,int>> new_dots;
    for(auto const &d : dots)
      new_dots.emplace(fold(d, val, along_x));
    dots = new_dots;

    // Silver star
    if(!inst_count)
      cout << dots.size() << "\n";
    ++inst_count;
  }

  // Gold star
  array<array<int, 40>, 6> arr{};
  for(auto const &d : dots)
    arr[d.second][d.first] = 1;

  for(auto const &r : arr)
  {
    for(auto const &c : r)
      cout << c;
    cout << "\n";
  }

  return 0;
}
