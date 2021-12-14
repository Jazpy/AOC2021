#include <fstream>
#include <iostream>
#include <string>
#include <vector>
#include <map>

using std::cout;   using std::ifstream;
using std::stoi;   using std::string;
using std::vector; using std::map;

vector<string> read_input(const char* filepath)
{
  ifstream       in_f(filepath);
  string         line;
  vector<string> ret;

  while(std::getline(in_f, line))
    ret.push_back(line);

  return ret;
}

void apply_rules(map<string,size_t> &b, const map<string,string> &r)
{
  map<string,size_t> delta_map;
  for(auto const& p : r)
  {
    if(b.find(p.first) == b.end())
      continue;

    delta_map[p.first[0] + p.second] += b[p.first];
    delta_map[p.second + p.first[1]] += b[p.first];
    b[p.first] = 0;
  }

  for(auto const &p : delta_map)
    b[p.first] += p.second;
}

int main()
{
  vector<string> input = read_input("inputs/d14.txt");

  // Parse input
  auto formula = input[0];
  map<string,size_t>    bigrams;
  map<string,string> rules;
  for(auto const &s : input)
  {
    if(s.find("-") == string::npos)
      continue;

    rules[s.substr(0, 2)] = s.substr(6, 7);
  }

  for(size_t i = 0; i != formula.length() - 1; ++i)
    ++bigrams[formula.substr(i, 2)];
  ++bigrams[formula.substr(formula.length() - 1, 1)];

  // Do 40 steps of the formula
  for(size_t i = 0; i != 40; ++i)
    apply_rules(bigrams, rules);

  // Get counts
  map<char,size_t> counts;
  for(auto const &p : bigrams)
    counts[p.first[0]] += p.second;

  size_t max = 0;
  size_t min = (size_t) - 1;

  for(auto const &p : counts)
  {
    max = p.second > max ? p.second : max;
    min = p.second < min ? p.second : min;
  }

  cout << max - min << "\n";

  return 0;
}
