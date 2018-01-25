#include <iostream>
#include <cstdint>
#include <cmath>
#include <algorithm>
#include <unordered_map>

#include "utils.h"

#define INF 1.0e8

static const uint64_t MASK = 0xffff;
static uint16_t merge_left_table[0xffff];
static uint16_t merge_right_table[0xffff];
static double score_table[0xffff];

struct map_entry_t{
    int depth;
    double score;
};

typedef std::unordered_map<uint64_t, map_entry_t> map_t;

static uint64_t transpose(uint64_t x) {
   uint64_t t;
   t = (x ^ (x >> 12)) & 0x0000f0f00000f0f0ull;
   x ^= t ^ (t << 12);
   t = (x ^ (x >> 24)) & 0x00000000ff00ff00ull;
   x ^= t ^ (t << 24);

   return x;
}

static uint16_t reverse_row(uint16_t row) {
   return (row << 12) | ((row << 4) & 0x0f00) | ((row >> 4) & 0x00f0) | (row >> 12);
}

static const double LOST_PENALTY = 200000.0;
static const double EMPTY_WEIGHT = 270.0;
static const double MONO_WEIGHT = 47.0;
static const double MONO_POW = 4.0;
static const double MERGES_WEIGHT = 2000.0;
static const double SUM_WEIGHT = 11.0;
static const double SUM_POW = 3.5;
static const double P_CUTOFF = 0.005;

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
         while(row[k] == 0 && k < 4) k++;
         if(row[k] == row[i]) merges++;
      }
   }

   return -SUM_WEIGHT * sum + MERGES_WEIGHT * merges - MONO_WEIGHT * std::min(left, right) + EMPTY_WEIGHT * empty + LOST_PENALTY;
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
   for(uint16_t x = 0; x < 0xffff; ++x) {
      uint16_t mask = 0xf;
      int row[4] = {(x >> 12) & mask,
                    (x >>  8) & mask,
                    (x >>  4) & mask,
                     x        & mask};

      for(int i = 0; i < 3; ++i) {
         int j;
         for(j = i+1; j < 4; ++j) {
            if(row[j] != 0) break;
         }
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
      case 1: return merge_up(board);
      case 2: return merge_down(board);
      case 3: return merge_right(board);
      case 4: return merge_left(board);
      default: return board;
   }
}

static int count_free_tiles(const uint64_t &x) {
   int empty = 0;
   for(int i = 0; i < 64; i += 4) {
      empty += (((x >> i) & 0xf) == 0);
   }

   return empty;
}

static double search_min(uint64_t board, int depth, int curdepth, double p, map_t &table);

static double search_max(uint64_t board, int depth, int curdepth, double p, map_t &table) {
   double max_score = -INF;

   for(int move = 4; move > 0; --move) {
      uint64_t new_board = direction(board, move);
      if(new_board == board) continue;
      double score = search_min(new_board, depth-1, curdepth+1, p, table);
      if(score > max_score) max_score = score;
   }

   return max_score;
}

static double search_min(uint64_t board, int depth, int curdepth, double p, map_t &table) {
   if(depth == 0 || p < P_CUTOFF) return evaluate(board);

   const map_t::iterator &i = table.find(board);
   if(i != table.end()) {
      map_entry_t entry = i->second;
      if(entry.depth >= curdepth) return entry.score;
   }

   int free = count_free_tiles(board);
   if(free == 0) return evaluate(board);
   double oofree = 1.0 / free;
   p *= oofree;
   uint64_t num = 0x1;
   uint64_t tmp = board;
   double score = 0;
   while(num) {
      if((tmp & 0xf) == 0) {
         score += 0.9 * search_max(board | num, depth, curdepth, 0.9 * p, table);
         score += 0.1 * search_max(board | (num << 1), depth, curdepth, 0.1 * p, table);
      }
      tmp >>= 4;
      num <<= 4;
   }

   score *= oofree;

   map_entry_t entry = {curdepth, score};
   table[board] = entry;

   return score;
}

int get_next_move(uint64_t board, int depth) {
   map_t table;

   double max_score = -INF;
   int best_move = 0;

   for(int move = 4; move > 0; --move) {
      uint64_t new_board = direction(board, move);
      if(new_board == board) continue;
      double score = search_min(new_board, depth, 1, 1.0, table);
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

