#include <fstream>
#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include <sstream>

using std::cout;    using std::ifstream;
using std::vector;  using std::pair;
using std::string;

vector<string> read_input(const char* filepath)
{
  ifstream       in_f(filepath);
  string         line;
  vector<string> ret;

  while(std::getline(in_f, line))
    ret.push_back(line);

  return ret;
}

struct packet
{
  unsigned long version, id, lit, l_id, l_sub;
  vector<packet> subs;
};

unsigned long bit_to_int(const vector<bool> &b, size_t i, size_t l)
{
  unsigned long ret = 0;
  for(size_t j = 0, s = l - 1; j != l; ++j, --s)
    ret += b[i + j] << s;
  return ret;
}

// Returns how many bits were parsed for the packet at b[i],
// packet gets pushed into r, v is running version sum
size_t parse_packet(const vector<bool>& b, size_t i, vector<packet> &r,
  unsigned long &v)
{
  packet p;
  p.version = bit_to_int(b, i, 3);
  p.id = bit_to_int(b, i + 3, 3);
  size_t parsed = 6;

  switch(p.id)
  {
    // Literal
    case 4:
    {
      size_t counter = i + 6;
      unsigned long val = 0;

      while(b[counter])
      {
        val += bit_to_int(b, counter + 1, 4);
        val <<= 4;
        counter += 5;
        parsed += 5;
      }

      val += bit_to_int(b, counter + 1, 4);
      parsed += 5;
      p.lit = val;
      break;
    }

    // Operator
    default:
      p.l_id = bit_to_int(b, i + 6, 1);
      parsed += 1;

      // Change parsing based on length id
      size_t sub_parsed = 0;
      if(p.l_id)
      {
        p.l_sub = bit_to_int(b, i + 7, 11);
        parsed += 11;

        // Keep reading until we parse n packets
        for(size_t c = 0; c != p.l_sub; ++c)
          sub_parsed += parse_packet(b, i + 18 + sub_parsed, p.subs, v);
      } else {
        p.l_sub = bit_to_int(b, i + 7, 15);
        parsed += 15;

        // Keep reading until we parse n bits
        while(sub_parsed < p.l_sub)
          sub_parsed += parse_packet(b, i + 22 + sub_parsed, p.subs, v);
      }

      parsed += sub_parsed;
  }

  r.push_back(p);
  v += p.version;
  return parsed;
}

packet parse_bitstring(const vector<bool> &b, unsigned long &v)
{
  vector<packet> ret;
  parse_packet(b, 0, ret, v);
  return ret[0];
}

unsigned long calculate(const packet &packet)
{
  unsigned long ret = 0;

  switch(packet.id)
  {
    // Lit
    case 4:
      ret = packet.lit;
      break;
    // Sum
    case 0:
      for(auto const &p : packet.subs)
        ret += calculate(p);
      break;
    // Prod
    case 1:
      ret = 1;
      for(auto const &p : packet.subs)
        ret *= calculate(p);
      break;
    // Min
    case 2:
      ret -= 1;
      for(auto const &p : packet.subs)
      {
        auto val = calculate(p);
        if(val < ret)
          ret = val;
      }
      break;
    // Max
    case 3:
      for(auto const &p : packet.subs)
      {
        auto val = calculate(p);
        if(val > ret)
          ret = val;
      }
      break;
    // GT
    case 5:
      ret = calculate(packet.subs[0]) > calculate(packet.subs[1]);
      break;
    // LT
    case 6:
      ret = calculate(packet.subs[0]) < calculate(packet.subs[1]);
      break;
    // EQ
    case 7:
      ret = calculate(packet.subs[0]) == calculate(packet.subs[1]);
  }

  return ret;
}

int main()
{
  vector<string> input = read_input("inputs/d16.txt");

  // Parse input into bitstring
  vector<bool> bitstring;
  for(auto it = input[0].crbegin(); it != input[0].crend(); ++it)
  {
    string hexed = "0x";
    hexed.push_back(*it);
    std::stringstream ss;
    ss << std::hex << hexed;
    unsigned long num;
    ss >> num;

    for(size_t i = 0; i != 4; ++i)
    {
      bitstring.push_back(num & 1);
      num >>= 1;
    }
  }

  std::reverse(bitstring.begin(), bitstring.end());

  // Parse the bitstring
  unsigned long v_sum = 0;
  auto packet = parse_bitstring(bitstring, v_sum);

  // Silver
  cout << v_sum << "\n";

  // Gold
  cout << calculate(packet) << "\n";

  return 0;
}
