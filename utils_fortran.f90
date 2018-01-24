module utils
   implicit none

   contains

      subroutine shift_left(grid)
         integer, dimension(4,4) :: grid

         integer :: k,i,j

         do i=1,4
            do j=1,3
               if(grid(i,j) == 0) then
                  do k=j+1,4
                     if(grid(i,k) /= 0) then
                        grid(i,j) = grid(i,k)
                        grid(i,k) = 0
                        exit
                     end if
                  end do
               end if
            end do
         end do

      end subroutine

      subroutine merge_left(grid)
         integer, dimension(4,4) :: grid

         integer :: i, j, k

         do i=1,4
            do j=1,3
               if(grid(i,j) /= 0) then
                  k = j+1
                  do while(grid(i,k) == 0 .and. k < 4)
                     k = k+1
                  end do
                  if(grid(i,k) == grid(i,j)) then
                     grid(i,j) = grid(i,j) + 1
                     grid(i,k) = 0
                  end if
               end if
            end do
         end do

         call shift_left(grid)

      end subroutine

      subroutine reverse_rows(grid)
         integer, dimension(4,4) :: grid
         integer :: i, j, tmp

         do i=1,4
            do j=1,2
               tmp = grid(i,j)
               grid(i,j) = grid(i,5-j)
               grid(i,5-j) = tmp
            end do
         end do

      end subroutine

      subroutine reverse_cols(grid)
         integer, dimension(4,4) :: grid
         integer :: i, j, tmp

         do i=1,2
            do j=1,4
               tmp = grid(i,j)
               grid(i,j) = grid(5-i,j)
               grid(5-i,j) = tmp
            end do
         end do

      end subroutine

      subroutine sub_transpose(grid)
         integer, dimension(4,4) :: grid
         integer :: i, j, tmp

         do i=1,3
            do j=i+1,4
               tmp = grid(i,j)
               grid(i,j) = grid(j,i)
               grid(j,i) = tmp
            end do
         end do

      end subroutine

      subroutine merge_right(grid)
         integer, dimension(4,4) :: grid

         call reverse_rows(grid)
         call merge_left(grid)
         call reverse_rows(grid)

      end subroutine

      subroutine merge_up(grid)
         integer, dimension(4,4) :: grid

         call sub_transpose(grid)
         call merge_left(grid)
         call sub_transpose(grid)

      end subroutine

      subroutine merge_down(grid)
         integer, dimension(4,4) :: grid

         call reverse_cols(grid)
         call merge_up(grid)
         call reverse_cols(grid)

      end subroutine

      function direction(grid, move) result(merged)
         integer, dimension(4,4), intent(in) :: grid
         integer, intent(in) :: move
         integer, dimension(4,4) :: merged

         merged = grid
         select case (move)
            case (1)
               call merge_up(merged)
               return
            case (2)
               call merge_down(merged)
               return
            case (3)
               call merge_right(merged)
               return
            case (4)
               call merge_left(merged)
               return
         end select

      end function

end module utils

module eval
   implicit none

   real, parameter :: lost_penalty = 200000.0
   real, parameter :: empty_weight = 270.0
   real, parameter :: mono_weight = 47.0
   real, parameter :: mono_pow = 4.0
   real, parameter :: merges_weight = 1400.0
   real, parameter :: sum_weight = 11.0
   real, parameter :: sum_pow = 3.5

   real, dimension(0:65535) :: score_table

   contains

      function encode_row(row) result(x)
         implicit none
         integer, dimension(4), intent(in) :: row
         integer :: x

         x = 0
         x = ior(x, ishft(row(1), 12))
         x = ior(x, ishft(row(2),  8))
         x = ior(x, ishft(row(3),  4))
         x = ior(x,       row(4)     )

      end function

      function decode_row(x) result(row)
         implicit none
         integer, intent(in) :: x
         integer, dimension(4) :: row

         row(1) = ishft(iand(x, 61440), -12) ! 61440 = z'f000'
         row(2) = ishft(iand(x,  3840),  -8) !  3830 = z'0f00'
         row(3) = ishft(iand(x,   240),  -4) !   240 = z'00f0'
         row(4) =       iand(x,    15)       !    15 = z'000f'

      end function

      subroutine init()
         implicit none
         integer, dimension(4) :: row
         integer :: x

         x = 0
         do while(x < 65536)
            row = decode_row(x)
            score_table(x) = evaluate_row(row)
            x = x+1
         end do

      end subroutine

      function count_free_tiles(grid) result(n)
         integer, dimension(4,4), intent(in) :: grid
         integer :: i, j, n

         n = 0
         do i=1,4
            do j=1,4
               if(grid(i,j) == 0) then
                  n = n + 1
               end if
            end do
         end do

      end function

      function sum_grid(grid) result(s)
         integer, dimension(4,4), intent(in) :: grid
         integer :: i, j
         real :: s

         s = 0
         do i=1,4
            do j=1,4
               s = s + grid(i,j)**sum_pow
            end do
         end do

      end function

      function count_free_row(row) result(n)
         implicit none
         integer, dimension(4), intent(in) :: row
         integer :: i, n

         n = 0
         do i=1,4
            if(row(i) == 0) then
               n = n + 1
            end if
         end do

      end function

      function sum_row(row) result(s)
         implicit none
         integer, dimension(4), intent(in) :: row
         integer :: i
         real :: s

         s = 0
         do i=1,4
            s = s + row(i)**sum_pow
         end do

      end function

      function merges(row) result(m)
         integer, dimension(4), intent(in) :: row
         integer :: m, i, k

         m = 0
         do i=1,3
            if(row(i) /= 0) then
               k = i+1
               do while(row(k) == 0 .and. k < 4)
                  k = k+1
               end do
               if(row(k) == row(i)) then
                  m = m+1
               end if
            end if
         end do

      end function

      function monotonicity(row) result(score)
         integer, dimension(4), intent(in) :: row
         real :: score, left, right
         integer :: i

         left = 0.0
         right = 0.0
         do i=1,3
            if(row(i) > row(i+1)) then
               left = left + (row(i)**mono_pow - row(i+1)**mono_pow)
            else
               right = right + (row(i+1)**mono_pow - row(i)**mono_pow)
            end if
         end do

         score = min(left, right)

      end function

      function evaluate_row(row) result(score)
         implicit none
         integer, dimension(4), intent(in) :: row
         real :: score

         score = lost_penalty &
               + empty_weight * count_free_row(row) &
               - sum_weight * sum_row(row) &
               + merges_weight * merges(row) &
               - mono_weight * monotonicity(row)

      end function

      function evaluate_row_table(row) result(score)
         implicit none
         integer, dimension(4), intent(in) :: row
         real :: score

         score = score_table(encode_row(row))

      end function

      function evaluate(grid) result(score)
         integer, dimension(4,4), intent(in) :: grid
         real :: score
         integer, dimension(4) :: row, col
         integer :: i

         score = 0.0
         do i=1,4
            row = grid(i,:)
            col = grid(:,i)
            score = score &
                  + evaluate_row_table(row) &
                  + evaluate_row_table(col)
         end do

      end function

end module eval

module expecti
   use utils
   use eval

   implicit none

   real, parameter :: inf = huge(1.0)
   integer, dimension(2) :: num = (/1, 2/)
   real, dimension(2) :: p = (/0.9, 0.1/)
   real, parameter :: p_cutoff = 0.0025

   contains

      function search_max(grid, depth, prob) result(max_score)
         integer, dimension(4,4), intent(in) :: grid
         integer, intent(in) :: depth
         real, intent(in) :: prob

         integer, dimension(4,4) :: new_grid
         integer :: move
         real :: score, max_score

         max_score = -inf
         do move=1,4
            new_grid = direction(grid, move)
            if(all(new_grid == grid)) then
               cycle
            end if
            score = search_min(new_grid, depth-1, prob)
            if(score > max_score) then
               max_score = score
            end if
         end do

      end function search_max

      function search_min(grid, depth, prob) result(score)
         integer, dimension(4,4) :: grid
         integer, intent(in) :: depth
         real, intent(in) :: prob
         integer :: n, i, j, free
         real :: score, oofree

         if(depth == 0 .or. prob < p_cutoff) then
            score = evaluate(grid)
            return
         end if

         score = 0
         free = count_free_tiles(grid)
         if(free == 0) then
            score = evaluate(grid)
            return
         end if
         oofree = 1.0 / free
         do n=1,2
            do i=1,4
               do j=1,4
                  if(grid(i,j) == 0) then
                     grid(i,j) = num(n)
                     score = score + p(n) * search_max(grid, depth, p(n)*prob*oofree)
                     grid(i,j) = 0
                  end if
               end do
            end do
         end do

         score = score * oofree

      end function

      function get_next_move(grid, max_depth) result(best_move)
         integer, dimension(4,4), intent(in) :: grid
         integer, intent(in) :: max_depth
         integer, dimension(4,4) :: new_grid
         integer :: move, best_move
         real :: max_score, score

         max_score = -inf
         best_move = 0
         do move = 1,4
            new_grid = direction(grid, move)
            if(all(new_grid == grid)) then
               cycle
            end if
            score = search_min(new_grid, max_depth, 1.0)
            if(score > max_score) then
               max_score = score
               best_move = move
            end if
         end do

      end function

end module expecti

module alpha_beta
   use utils
   use eval

   implicit none

   real, parameter :: inf = huge(1.0)
   integer, dimension(2) :: num = (/1, 2/)

   contains

      function search_max(grid, depth, alpha, beta) result(max_score)
         integer, dimension(4,4), intent(in) :: grid
         integer, intent(in) :: depth
         real, intent(in) :: alpha, beta

         integer, dimension(4,4) :: new_grid
         integer :: move
         real :: score, max_score

         max_score = alpha
         do move=1,4
            new_grid = direction(grid, move)
            if(all(new_grid == grid)) then
               cycle
            end if
            score = search_min(new_grid, depth-1, max_score, beta)
            if(score > max_score) then
               max_score = score
               if(max_score >= beta) then
                  exit
               end if
            end if
         end do

      end function

      function search_min(grid, depth, alpha, beta) result(min_score)
         integer, dimension(4,4) :: grid
         integer, intent(in) :: depth
         real, intent(in) :: alpha, beta
         integer :: n, i, j, free
         real :: min_score, score

         if(depth == 0) then
            min_score = evaluate(grid)
            return
         end if

         min_score = beta
         free = 0
         do n=1,2
            do i=1,4
               do j=1,4
                  if(grid(i,j) == 0) then
                     grid(i,j) = num(n)
                     free = free + 1
                     score = search_max(grid, depth, alpha, min_score)
                     grid(i,j) = 0
                     if(score < min_score) then
                        min_score = score
                        if(min_score <= alpha) then
                           return
                        end if
                     end if
                  end if
               end do
            end do
            if(free == 0) then
               min_score = evaluate(grid)
               return
            end if
         end do

      end function

      function get_next_move(grid, max_depth) result(best_move)
         integer, dimension(4,4), intent(in) :: grid
         integer, intent(in) :: max_depth
         integer, dimension(4,4) :: new_grid
         integer :: move, best_move
         real :: max_score, score

         max_score = -inf
         best_move = 0
         do move = 1,4
            new_grid = direction(grid, move)
            if(all(new_grid == grid)) then
               cycle
            end if
            score = search_min(new_grid, max_depth, max_score, inf)
            if(score > max_score) then
               max_score = score
               best_move = move
            end if
         end do

      end function

end module

program test
   use utils
   use eval
   use expecti

   implicit none

   integer, dimension(4,4) :: grid, merged
   integer :: x = 65535 ! 0xffff

   grid = reshape((/0, 0, 1, 1,&
                    0, 1, 0, 2,&
                    2, 2, 3, 3,&
                    2, 3, 4, 0/), (/4, 4/))

   print *, 'Original'
   print '(4 i3)', grid(:,:)
   print *

   merged = direction(grid, 4)

   print *, '<'
   print '(4 i3)', merged(:,:)
   print *

   merged = direction(merged, 3)

   print *, '>'
   print '(4 i3)', merged(:,:)
   print *

   merged = direction(merged, 1)

   print *, '^'
   print '(4 i3)', merged(:,:)
   print *

   merged = direction(merged, 2)

   print *, 'v'
   print '(4 i3)', merged(:,:)
   print *

   print *, get_next_move(grid, 1)
   print *

   print '(4 z4)', encode_row( (/15,15,15,15/) )
   print '(4 i3)', decode_row(x)
   print *

   print *, "Initializing table..."
   call init()
   print *, "Done!"
   print *, evaluate_row( (/15,15,15,15/) )
   print *, evaluate_row_table( (/15,15,15,15/) )

end program test
