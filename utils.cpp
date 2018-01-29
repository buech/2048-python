#include <iostream>
#include <cstdint>
#include <cmath>
#include <algorithm>
#include <unordered_map>

#include "utils.h"

#define INF 1.0e8

static const uint64_t MASK = 0xffff;
static uint16_t merge_left_table[65536];
static uint16_t merge_right_table[65536];
static double score_table[65536];

struct cache_entry_t{
    int depth;
    double score;
};

typedef std::unordered_map<uint64_t, cache_entry_t> cache_t;

static uint64_t transpose(uint64_t x) {
   uint64_t tmp;
   tmp = (x ^ (x >> 12)) & 0x0000f0f00000f0f0ull;
   x ^= tmp ^ (tmp << 12);
   tmp = (x ^ (x >> 24)) & 0x00000000ff00ff00ull;
   x ^= tmp ^ (tmp << 24);

   return x;
}

static inline uint16_t reverse_row(uint16_t row) {
   return (row << 12) | ((row << 4) & 0x0f00) | ((row >> 4) & 0x00f0) | (row >> 12);
}

static int count_free_tiles(uint64_t x) {
   int occupied = 0;
   while(x) {
      if(x & 0xf) occupied++;
      x >>= 4;
   }

   return 16 - occupied;
}

static const double LOST_PENALTY = 200000.0;
static const double EMPTY_WEIGHT = 270.0;
static const double MONO_WEIGHT = 47.0;
static const double MONO_POW = 4.0;
static const double MERGES_WEIGHT = 1400.0;
static const double SUM_WEIGHT = 11.0;
static const double SUM_POW = 3.5;
static const double P_CUTOFF = 0.0025;

static double evaluate_row(uint16_t x) {
   uint16_t mask = 0xf;
   int row[4] = {(x >> 12) & mask,
                 (x >>  8) & mask,
                 (x >>  4) & mask,
                  x        & mask};

   double mono = 0, sum = 0;
   int merges = 0, empty = 0;

   for(int i = 0; i < 4; ++i) {
      if(row[i] != 0) {
         sum += pow(row[i], SUM_POW);
      }
      else empty++;
   }

   double left = 0, right = 0;
   for(int i = 0; i < 3; ++i) {
      if(row[i] > row[i+1]) {
         left += pow(row[i], MONO_POW) - pow(row[i+1], MONO_POW);
      }
      else {
         right += pow(row[i+1], MONO_POW) - pow(row[i], MONO_POW);
      }
      if(row[i] != 0) {
         int k = i+1;
         while(row[k] == 0 && k < 3) k++;
         if(row[k] == row[i]) merges++;
      }
   }

   return LOST_PENALTY
        - MONO_WEIGHT * std::min(left, right)
        + MERGES_WEIGHT * merges
        + EMPTY_WEIGHT * empty
        - SUM_WEIGHT * sum;
}

static inline double _evaluate(uint64_t board) {
   return evaluate_row((board >> 48) & MASK)
        + evaluate_row((board >> 32) & MASK)
        + evaluate_row((board >> 16) & MASK)
        + evaluate_row( board        & MASK);
}

static inline double _evaluate_table(uint64_t board) {
   return score_table[(board >> 48) & MASK]
        + score_table[(board >> 32) & MASK]
        + score_table[(board >> 16) & MASK]
        + score_table[ board        & MASK];
}

static inline double evaluate(uint64_t board) {
   return _evaluate_table(board) + _evaluate_table(transpose(board));
}

void init() {
   for(unsigned x = 0; x < 65536; ++x) {
      uint16_t mask = 0xf;
      unsigned row[4] = {(x >> 12) & mask,
                         (x >>  8) & mask,
                         (x >>  4) & mask,
                          x        & mask};

      for(unsigned i = 0; i < 3; ++i) {
         unsigned j = i+1;
         while(row[j] == 0 && j < 4) j++;
         if(j == 4) break;

         if(row[i] == 0) {
            row[i] = row[j];
            row[j] = 0;
            i--;
         }
         else if(row[i] == row[j]) {
            if(row[i] != 15) row[i]++; // 32k + 32k = 32k
            row[j] = 0;
         }
      }

      uint16_t merged = (row[0] << 12) | (row[1] << 8) | (row[2] << 4) | row[3];
      merge_left_table[x] = merged;

      uint16_t x_rev = reverse_row(x);
      merge_right_table[x_rev] = reverse_row(merged);

      score_table[x] = evaluate_row(x);
   }
}

static inline uint64_t merge_left(uint64_t board) {
   return ((uint64_t)merge_left_table[(board >> 48) & MASK] << 48) |
          ((uint64_t)merge_left_table[(board >> 32) & MASK] << 32) |
          ((uint64_t)merge_left_table[(board >> 16) & MASK] << 16) |
           (uint64_t)merge_left_table[ board        & MASK];
}

static inline uint64_t merge_right(uint64_t board) {
   return ((uint64_t)merge_right_table[(board >> 48) & MASK] << 48) |
          ((uint64_t)merge_right_table[(board >> 32) & MASK] << 32) |
          ((uint64_t)merge_right_table[(board >> 16) & MASK] << 16) |
           (uint64_t)merge_right_table[ board        & MASK];
}

static inline uint64_t merge_up(uint64_t board) {
   return transpose(merge_left(transpose(board)));
}

static inline uint64_t merge_down(uint64_t board) {
   return transpose(merge_right(transpose(board)));
}

static uint64_t direction(uint64_t board, int move) {
   switch(move) {
      case 4: return merge_left(board);
      case 3: return merge_right(board);
      case 2: return merge_down(board);
      case 1: return merge_up(board);
      default: return board;
   }
}

static double search_min(uint64_t board, int max_depth, int depth, double p, cache_t &cache);

static double search_max(uint64_t board, int max_depth, int depth, double p, cache_t &cache) {
   double max_score = -INF;

   for(int move = 4; move > 0; --move) {
      uint64_t new_board = direction(board, move);
      if(new_board == board) continue;
      double score = search_min(new_board, max_depth-1, depth+1, p, cache);
      if(score > max_score) max_score = score;
   }

   return max_score;
}

static double search_min(uint64_t board, int max_depth, int depth, double p, cache_t &cache) {
   if(max_depth == 0 || p < P_CUTOFF) return evaluate(board);

   const cache_t::iterator &i = cache.find(board);
   if(i != cache.end()) {
      cache_entry_t entry = i->second;
      if(entry.depth >= depth) return entry.score;
   }

   int free = count_free_tiles(board);
   if(free == 0) return evaluate(board);
   double oofree = 1.0 / free;
   p *= oofree;
   uint64_t num = 0x1000000000000000;
   uint64_t mask = 0xf000000000000000;
   double score = 0;
   while(mask) {
      if((board & mask) == 0) {
         score += 0.9 * search_max(board | num, max_depth, depth, 0.9 * p, cache);
         score += 0.1 * search_max(board | (num << 1), max_depth, depth, 0.1 * p, cache);
      }
      mask >>= 4;
      num >>= 4;
   }

   score *= oofree;

   cache_entry_t entry = {depth, score};
   cache[board] = entry;

   return score;
}

int get_next_move(uint64_t board, int max_depth) {
   cache_t cache;

   double max_score = -INF;
   int best_move = 0;

   for(int move = 4; move > 0; --move) {
      uint64_t new_board = direction(board, move);
      if(new_board == board) continue;
      double score = search_min(new_board, max_depth, 1, 1.0, cache);
      if(score > max_score) {
         max_score = score;
         best_move = move;
      }
   }

   return best_move;
}

int main() {

   std::cout << "Initializing tables..." << std::endl;
   init();
   std::cout << "Done!" << std::endl;

   uint64_t board = 0x0011010222332340ull;

   for(int i = 0; i < 10; ++i) {
      int best_move = get_next_move(board << 4*i, 10);
      std::cout << best_move << std::endl;
   }
   return 0;
}

