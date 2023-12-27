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

class Hash {
    const unsigned int bytes_per_int = 8;
    std::vector<uint64_t> buffer;

   public:
    unsigned int n_bits = 0;
    Hash(){};
    void load(std::string description, std::map<char, uint8_t> symbol_map) {
        n_bits = (description.length());
        unsigned int n_ints = std::ceil(n_bits / 8 / bytes_per_int);

        uint8_t bit_counter = 0;

        uint64_t value = 0;
        for (char d : description) {
            if (bit_counter == bytes_per_int * 8) {
                // Add a new value
                buffer.push_back(value);
                value = 0;
            }
            value |= ((uint64_t)symbol_map[d] << bit_counter);
            bit_counter++;
        }
        buffer.push_back(value);
    }

    Hash(std::string description, std::map<char, uint8_t> symbol_map) {
        load(description, symbol_map);
    }

    Hash(unsigned int N, unsigned int n_mask) {
        // Create a mask
        uint8_t bit_counter = 0;
        n_bits = N;

        uint64_t value = 0;
        for (unsigned int i = 0;i < N;i++) {
            if (bit_counter == bytes_per_int * 8) {
                // Add a new value
                buffer.push_back(value);
                value = 0;
            }
            value |= (uint64_t)(i < n_mask ? 1 : 0) << bit_counter++;
        }
        buffer.push_back(value);
    }

    Hash(unsigned int N, std::vector<unsigned int> positions, std::vector<unsigned int> counts) {
        n_bits = N;
        unsigned int n_ints = std::ceil(n_bits / (8 * bytes_per_int));
        unsigned int bit_counter = 0;
        unsigned int byte_counter = 0;

        for (unsigned int i = 0;i < n_ints;i++) {
            buffer.push_back(0);
        }

        for (unsigned int i = 0; i < positions.size(); i++) {
            auto p = positions[i];
            auto c = counts[i];

            for (unsigned int k = p; k < p + c;k++) {
                bit_counter = k % (8 * bytes_per_int);
                byte_counter = (unsigned int)(k - bit_counter) / (8 * bytes_per_int);
                buffer.at(byte_counter) |= 1 << bit_counter;
            }
        }
    }

    Hash(std::vector<uint64_t> buffer, unsigned int n_nits) : buffer(buffer), n_bits(n_bits) {
    }

    std::string to_string() {
        std::string output;
        for (unsigned int i = 0; i < buffer.size(); i++) {
            unsigned int max_length = (unsigned int)8*bytes_per_int;
            unsigned int effective_length = (unsigned int)n_bits - i * (8*bytes_per_int);
            std::string bits = std::bitset<64>(buffer[i]).to_string().substr(0, std::min(max_length, effective_length));
            std::reverse(bits.begin(), bits.end());
            output.append(bits);
        }
        return output;
    }

    Hash invert() {
        std::vector<uint64_t> new_buffer;
        unsigned int i = 0;
        for (auto b : buffer) {
            uint64_t mask = (1 << std::min((unsigned int)8*bytes_per_int, n_bits - i * (8*bytes_per_int))) - 1;
            new_buffer.push_back(b & mask);
            i++;
        }
        return Hash(new_buffer, n_bits);
    }

    bool any() {
        for (auto b : buffer) {
            if (b) {
                return true;
            }
        }
        return false;
    }

    Hash operator&(const Hash& other) 
    { 
        std::vector<uint64_t> new_buffer;
        for (unsigned int i = 0;i < buffer.size();i++) {
            uint64_t mask = (1 << std::min((unsigned int)8*bytes_per_int, n_bits - i * (8*bytes_per_int))) - 1;
            new_buffer.push_back(buffer.at(i) & mask & other.buffer.at(i));
        }
        return Hash(new_buffer, n_bits);;
    } 
};

class Line {
   public:
    
    Hash operational_hash;
    Hash broken_hash;
    std::vector<unsigned int> counts;

    Line(std::string line) {
        std::cout << "Creating a new line..." << std::endl;
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

        std::cout << std::endl;
    }

    unsigned long try_all(unsigned long N, std::vector<unsigned int> positions, std::vector<unsigned int> counts, unsigned int i=0) {
        static unsigned long call_counter = 0;
        call_counter++;
        unsigned int _min, _max;
        std::string test;
        unsigned int counter = 0;

        
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

        
        if (i < 2) {
            std::cout << i << " " << _min << "->" << _max << std::endl;
            if (i > 0) {
                std::cout << "positions[i-1] : " << positions.at(i-1) << ", counts[i-1] : " << counts.at(i-1) << std::endl;
            }
            
        }
        if (_max >= _min) {
            for (unsigned int k = _max;k >= _min;k--) {
                std::cout << "Set positions[" << i << "]=" << k << std::endl;
                positions.at(i) = k;

                std::vector<unsigned int> positions_sublist;
                std::vector<unsigned int> counts_sublist;
                for (unsigned int j = 0;j < i + 1 && j < positions.size();j++) {
                    positions_sublist.push_back(positions[j]);
                    counts_sublist.push_back(counts[j]);
                }

                Hash new_hash(N, positions_sublist, counts_sublist);
                Hash mask(N, k + counts[i]);

                std::cout << "mask             : " << mask.to_string() << std::endl;
                std::cout << "broken hash      : " << broken_hash.to_string() << std::endl;
                std::cout << "operational hash : " << broken_hash.to_string() << std::endl;
                std::cout << "new hash         : " << new_hash.to_string() << std::endl;
                std::cin >> test;
                if (((operational_hash & new_hash) & mask).any()) {
                    std::cout << " skip B" << std::endl;
                    continue;
                }

                if (((broken_hash & new_hash.invert()) & mask).any()) {
                    std::cout << " skip A" << std::endl;
                    continue;
                }

                std::cout << " keep" << std::endl;

                if (i == positions.size() - 1) {
                    counter += 1;
                }
                else {
                    counter += try_all(N, positions, counts, i+1);
                }

            }
        }

        return counter;

    }

    unsigned long count_arangements() {
        std::vector<unsigned int> positions;
        unsigned int p = operational_hash.n_bits - std::accumulate(counts.begin(), counts.end(), decltype(counts)::value_type(0)) - counts.size() + 1;
        for (auto c : counts) {
            positions.push_back(p);
            p += c + 1;
        }
        return try_all(broken_hash.n_bits, positions, counts, 0);
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
    while (std::getline(inputFile, line)) {
        Line newLine(line);
        std::cout << newLine.count_arangements() << std::endl;

        // std::pair<std::string, std::vector<int>> parsedLine =
        // parseLine(line); std::string conditions = parsedLine.first;
        // std::vector<int> counts = parsedLine.second;
    }

    inputFile.close();
    return 0;
}
