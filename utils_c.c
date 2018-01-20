#include <stdio.h>
#include <stdint.h>
#include <math.h>

#define INF 1.0e8

uint16_t merge_left_table[0xffff];
uint16_t merge_right_table[0xffff];

uint64_t transpose(uint64_t x) {
   uint64_t t;
   t = (x ^ (x >> 12)) & 0x0000f0f00000f0f0ULL;
   x ^= t ^ (t << 12);
   t = (x ^ (x >> 24)) & 0x00000000ff00ff00ULL;
   x ^= t ^ (t << 24);

   return x;
}

uint16_t reverse_row(uint16_t row) {
   return (row << 12) | ((row << 4) & 0x0f00) | ((row >> 4) & 0x00f0) | (row >> 12);
}

void init() {
   for(unsigned x = 0; x < 0xffff; ++x) {
      unsigned row[4] = {(x & 0xf000) >> 12, (x & 0x0f00) >> 8, (x & 0x00f0) >> 4, x & 0x000f};

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
            if(row[i] != 0xf) row[i]++;
            row[j] = 0;
         }
      }

      uint16_t merged = (row[0] << 12) | (row[1] << 8) | (row[2] << 4) | row[3];
      unsigned x_rev = reverse_row(x);

      merge_left_table[x] = merged;
      merge_right_table[x_rev] = reverse_row(merged);
   }
}

uint64_t merge_left(uint64_t board) {
   return ((uint64_t)merge_left_table[(board & 0xffff000000000000ULL) >> 48] << 48) |
          ((uint64_t)merge_left_table[(board & 0x0000ffff00000000ULL) >> 32] << 32) |
          ((uint64_t)merge_left_table[(board & 0x00000000ffff0000ULL) >> 16] << 16) |
           (uint64_t)merge_left_table[ board & 0x000000000000ffffULL];
}

uint64_t merge_right(uint64_t board) {
   return ((uint64_t)merge_right_table[(board & 0xffff000000000000ULL) >> 48] << 48) |
          ((uint64_t)merge_right_table[(board & 0x0000ffff00000000ULL) >> 32] << 32) |
          ((uint64_t)merge_right_table[(board & 0x00000000ffff0000ULL) >> 16] << 16) |
           (uint64_t)merge_right_table[ board & 0x000000000000ffffULL];
}

uint64_t merge_up(uint64_t board) {
   return transpose(merge_left(transpose(board)));
}

uint64_t merge_down(uint64_t board) {
   return transpose(merge_right(transpose(board)));
}

uint64_t direction(uint64_t board, int move) {
   switch(move) {
      case 1: return merge_up(board);
      case 2: return merge_down(board);
      case 3: return merge_right(board);
      case 4: return merge_left(board);
      default: return ~0ULL;
   }
}

int count_free_tiles(uint64_t x) {
   x |= (x >> 2) & 0x3333333333333333ULL;
   x |= (x >> 1);
   x = ~x & 0x1111111111111111ULL;

   x += x >> 32;
   x += x >> 16;
   x += x >> 8;
   x += x >> 4;

   return x & 0xf;
}

const float MONO_WEIGHT = 47.0;
const float MONO_POW = 4.0;
const float MERGES_WEIGHT = 2000.0;

float min(float a, float b) {
   return a < b ? a:b;
}

float evaluate_row(uint16_t x) {
   unsigned row[4] = {(x & 0xf000) >> 12, (x & 0x0f00) >> 8, (x & 0x00f0) >> 4, x & 0x000f};

   float mono = 0;
   int merges = 0;

   float left = 0, right = 0;
   for(int i = 0; i < 3; ++i) {
      if(row[i] > row[i+1]) {
         left += pow(row[i], MONO_POW) - pow(row[i+1], MONO_POW);
      }
      else {
         left += pow(row[i+1], MONO_POW) - pow(row[i], MONO_POW);
      }
      if(row[i] != 0) {
         int k = i+1;
         while(row[k] == 0 && k < 4) k++;
         if(row[k] == row[i]) merges++;
      }
   }

   return MERGES_WEIGHT * merges - MONO_WEIGHT * min(left, right);
}

float evaluate(uint64_t board) {
   uint16_t rows[4] = {(board & 0xffff000000000000ULL) >> 48,
                       (board & 0x0000ffff00000000ULL) >> 32,
                       (board & 0x00000000ffff0000ULL) >> 16,
                        board & 0x000000000000ffffULL};

   float score = 0;
   for(int i = 0; i < 4; ++i) {
      score += evaluate_row(rows[i]);
   }

   return score;
}

float search_min(uint64_t board, int depth, float p);
float search_max(uint64_t board, int depth, float p) {
   float max_score = -INF;

   for(unsigned move = 1; move < 5; ++move) {
      uint64_t new_board = direction(board, move);
      if(new_board == board) continue;
      float score = search_min(new_board, depth-1, p);
      if(score > max_score) max_score = score;
   }

   return max_score;
}

float search_min(uint64_t board, int depth, float p) {
   if(depth == 0 || p < 0.0001) return evaluate(board);

   float score = 0;
   int free = count_free_tiles(board);
   if(free == 0) return evaluate(board);
   float oofree = 1.0 / free;
   p *= oofree;
   uint64_t num = 0x1;
   uint64_t tmp = board;
   while(num) {
      if((tmp & 0xf) == 0) {
         score += 0.9f * search_max(board | num, depth, 0.9f * p);
         score += 0.1f * search_max(board | (num << 1), depth, 0.1f * p);
      }
      tmp >>= 4;
      num <<= 4;
   }

   return score * oofree;
}

int get_next_move(uint64_t board, int depth) {
   float max_score = -INF;
   unsigned best_move = 0;

   for(unsigned move = 1; move < 5; ++move) {
      uint64_t new_board = direction(board, move);
      if(new_board == board) continue;
      float score = search_min(new_board, depth, 1.0);
      if(score > max_score) {
         max_score = score;
         best_move = move;
      }
   }

   return best_move;
}
