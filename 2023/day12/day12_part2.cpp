#include <stdlib.h>

#include <algorithm>
#include <bitset>
#include <cmath>
#include <cstdint>
#include <cstring>
#include <fstream>
#include <iostream>
#include <map>
#include <sstream>
#include <string>
#include <vector>
#include <numeric>
#include <ranges>

enum Type { OPERATIONAL, BROKEN, UNKNOWN };

std::map<char, Type> symbol_map = {
    {'#', BROKEN}, {'?', UNKNOWN}, {'.', OPERATIONAL}};

const unsigned int unfold_factor = 5;

typedef unsigned __int128 uint128_t;

class Hash {
    uint128_t bits = 0;
    unsigned int n_bits = 0;
   public:
    Hash(){};
    void load(std::string description, std::map<char, uint8_t> symbol_map) {
        n_bits = (description.length());

        uint8_t bit_counter = 0;
        for (char d : description) {
            bits |= ((uint128_t)symbol_map[d] << bit_counter);
            bit_counter++;
        }
    }

    Hash(std::string description, std::map<char, uint8_t> symbol_map) {
        load(description, symbol_map);
    }

    Hash(unsigned int N, unsigned int n_mask) {
        // Create a mask
        bits = 1;
        bits <<= (n_mask - 1);
        bits -= 1;

        n_bits = N;
    }

    Hash(unsigned int N, std::vector<unsigned int> positions, std::vector<unsigned int> counts) {
        n_bits = N;

        for (unsigned int i = 0; i < positions.size(); i++) {
            auto p = positions[i];
            auto c = counts[i];

            for (unsigned int k = p; k < p + c;k++) {
                bits |= (uint128_t)1 << (uint128_t)k;
            }
        }
    }

    

    std::string to_string() {
        std::string bits_string = std::bitset<128>(bits).to_string();
        std::reverse(bits_string.begin(), bits_string.end());
        return bits_string.substr(0, n_bits);
    }

    Hash invert() {
        uint128_t mask = 1;
        mask <<= (n_bits - 1);
        mask -= 1;
        Hash newHash;
        newHash.bits = ~bits & mask;
        newHash.n_bits = n_bits;
        return newHash;
    }

    bool any() {
        return bits > 0;
    }

    Hash operator&(const Hash& other) 
    { 
        //uint128_t mask = (1 << std::min((unsigned int)8*bytes_per_int, n_bits - i * (8*bytes_per_int))) - 1;
        Hash newHash;
        newHash.bits = bits & other.bits;
        newHash.n_bits = n_bits;
        return newHash;
    }

    unsigned int size() {
        return n_bits;
    }
};

class Line {
   public:
    
    Hash operational_hash;
    Hash broken_hash;
    std::vector<unsigned int> counts;

    Line(std::string line) {
        std::size_t separator_pos = line.find(' ');
        // Parse sequence (#.? etc...)
        std::string sequence = line.substr(0, separator_pos);

         
        std::string sequence_unfold;
        for (unsigned int i = 0;i < unfold_factor;i++) {
            sequence_unfold += sequence;
            if (i < unfold_factor - 1) {
                sequence_unfold += '?';
            }
        }

        operational_hash.load(sequence_unfold, {{'#', 0}, {'?', 0}, {'.', 1}});
        broken_hash.load(sequence_unfold, {{'#', 1}, {'?', 0}, {'.', 0}});
        // Parse counts
        std::string counts_str = line.substr(separator_pos + 1);

        std::vector<unsigned int> counts_single;

        std::stringstream ss(counts_str);

        for (int i; ss >> i;) {
            counts_single.push_back(i);
            if (ss.peek() == ',') ss.ignore();
        }

        for(unsigned i = 0;i<unfold_factor;i++) {
            counts.insert(counts.end(), counts_single.begin(), counts_single.end());
        }

    }

    unsigned long try_all(unsigned long N, std::vector<unsigned int> positions, std::vector<unsigned int> counts, unsigned int i=0) {
        static unsigned long hash_counter = 0;
        static unsigned long call_counter = 0;
        call_counter++;
        int _min, _max;
        std::string test;
        unsigned int counter = 0;
        bool _continue = false;

        
        if (i) {
            _min = positions.at(i-1) + counts.at(i-1) + 1;
        }
        else {
            _min = 0;
        }

        if (i == counts.size() - 1) {
            // Last one
            _max = N - counts.at(i);
        }
        else {
            _max = N - (std::accumulate(std::next(counts.begin(), i+1), counts.end(), decltype(counts)::value_type(0)) + (counts.size()-i));
            _max = std::max(_max, _min);
        }

        
        //std::cout << i << " " << _min << "->" << _max << std::endl;
        if (_max >= _min) {
            for (int k = _max;k >= _min;k--) {
                positions.at(i) = k;

                std::vector<unsigned int> positions_sublist;
                std::vector<unsigned int> counts_sublist;
                for (unsigned int j = 0;j < i + 1 && j < positions.size();j++) {
                    positions_sublist.push_back(positions[j]);
                    counts_sublist.push_back(counts[j]);
                }
                

                Hash new_hash(N, positions_sublist, counts_sublist);
                Hash mask(N, k + counts[i]);
                Hash tempHash = new_hash.invert();
                // std::cout << "operational hash : " << operational_hash.to_string() << std::endl;
                // std::cout << hash_counter++ << " new hash : " << new_hash.to_string() << std::endl;

                _continue = false;
                
                if (((broken_hash & new_hash.invert()) & mask).any()) {
                    // std::cout << " skip A" << std::endl;
                    _continue = true;
                }

                if (((operational_hash & new_hash) & mask).any() && _continue == false) {
                    // std::cout << " skip B" << std::endl;
                    _continue = true;
                }

                if (!_continue) {
                    // std::cout << " keep" << std::endl;
                }

                //std::cin >> test;
                if (_continue) {
                    continue;
                }

                if (i == positions.size() - 1) {
                    counter += 1;
                }
                else {
                    counter += try_all(N, positions, counts, i+1);
                }

            }
        }

        // std::cout << "Call counter : " << call_counter << std::endl;
        return counter;

    }

    unsigned long count_arangements() {
        std::vector<unsigned int> positions;
        unsigned int p = operational_hash.size() - std::accumulate(counts.begin(), counts.end(), decltype(counts)::value_type(0)) - counts.size() + 1;
        for (auto c : counts) {
            positions.push_back(p);
            p += c + 1;
        }
        return try_all(broken_hash.size(), positions, counts, 0);
    }
};


int main(int argc, char **argv) {
    std::cout << "Open file " << argv[1] << std::endl;
    std::ifstream inputFile(argv[1]);
    if (!inputFile.is_open()) {
        std::cerr << "Unable to open file!" << std::endl;
        return 1;
    }

    std::string line;
    unsigned int line_counter = 1;
    unsigned long total = 0;
    unsigned long n = 0;
    while (std::getline(inputFile, line)) {
        Line newLine(line);
        n = newLine.count_arangements();
        std::cout << "line " << line_counter++ << " : " << n << std::endl;
        total += n;
    }

    inputFile.close();
    return 0;
}
