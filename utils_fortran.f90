module utils
   contains

      subroutine shift_left(grid)
         implicit none
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
         implicit none
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
                     grid(i,j) = 2*grid(i,j)
                     grid(i,k) = 0
                  end if
               end if
            end do
         end do

         call shift_left(grid)

      end subroutine

      subroutine reverse_rows(grid)
         implicit none
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
         implicit none
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
         implicit none
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
         implicit none
         integer, dimension(4,4) :: grid

         call reverse_rows(grid)
         call merge_left(grid)
         call reverse_rows(grid)

      end subroutine

      subroutine merge_up(grid)
         implicit none
         integer, dimension(4,4) :: grid

         call sub_transpose(grid)
         call merge_left(grid)
         call sub_transpose(grid)

      end subroutine

      subroutine merge_down(grid)
         implicit none
         integer, dimension(4,4) :: grid

         call reverse_cols(grid)
         call merge_up(grid)
         call reverse_cols(grid)

      end subroutine

      function direction(grid, move) result(merged)
         implicit none
         integer, dimension(4,4), intent(in) :: grid
         integer, intent(in) :: move
         integer, dimension(4,4) :: merged

         merged = grid
         select case (move)
            case (1)
               call merge_up(merged)
            case (2)
               call merge_down(merged)
            case (3)
               call merge_right(merged)
            case (4)
               call merge_left(merged)
         end select

      end function

end module utils

module eval
   contains

      function count_free_tiles(grid) result(n)
         implicit none
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

      function smoothness(grid) result(score)
         implicit none
         integer, dimension(4,4), intent(in) :: grid
         integer :: score, i, j, s

         score = 0
         do i=1,4
            do j=1,4
               s = 1E08
               if(i > 1) then
                  s = min(s, abs(grid(i,j) - grid(i-1,j)))
               end if
               if(j > 1) then
                  s = min(s, abs(grid(i,j) - grid(i,j-1)))
               end if
               if(i < 4) then
                  s = min(s, abs(grid(i,j) - grid(i+1,j)))
               end if
               if(j < 4) then
                  s = min(s, abs(grid(i,j) - grid(i,j+1)))
               end if
               score = score - s
            end do
         end do

      end function

      function monotonicity(grid) result(score)
         implicit none
         integer, dimension(4,4), intent(in) :: grid
         integer :: i, j, m
         real :: l, r, u, d, lr, ud, score
         l = 0
         r = 0
         u = 0
         d = 0
         lr = 0
         ud = 0

         do i=1,4
            m = 0
            do j=1,3
               if(grid(i,j) >= grid(i,j+1)) then
                  m = m + 1
                  l = l + 4*m**2
               else
                  l = l - abs(grid(i,j) - grid(i,j+1)) * 1.5
                  m = 0
               end if
            end do
            m = 0
            do j=1,3
               if(grid(i,j) <= grid(i,j+1)) then
                  m = m + 1
                  r = r + 4*m**2
               else
                  r = r - abs(grid(i,j) - grid(i,j+1)) * 1.5
                  m = 0
               end if
            end do
         end do

         lr = lr + max(l, r)

         do j=1,4
            m = 0
            do i=1,3
               if(grid(i,j) >= grid(i+1,j)) then
                  m = m + 1
                  u = u + 4*m**2
               else
                  u = u - abs(grid(i,j) - grid(i+1,j)) * 1.5
                  m = 0
               end if
            end do
            m = 0
            do i=1,3
               if(grid(i,j) <= grid(i+1,j)) then
                  m = m + 1
                  d = d + 4*m**2
               else
                  d = d - abs(grid(i,j) - grid(i+1,j)) * 1.5
                  m = 0
               end if
            end do
         end do

         ud = ud + max(u, d)

         score = lr + ud

      end function

      function evaluate(grid) result(score)
         implicit none
         integer, dimension(4,4), intent(in) :: grid
         real :: score

         score = monotonicity(grid) + smoothness(grid) - (16 - count_free_tiles(grid))**2

      end function

end module eval

module expecti
   use utils
   use eval

   real, parameter :: inf = 1E08
   integer, dimension(2) :: num = (/2, 4/)
   real, dimension(2) :: p = (/0.9, 0.1/)

   contains

      function search_max(grid, depth) result(max_score)
         implicit none
         integer, dimension(4,4), intent(in) :: grid
         integer, intent(in) :: depth

         integer, dimension(4,4) :: new_grid
         integer :: move
         real :: score, max_score

         max_score = -inf
         do move=1,4
            new_grid = direction(grid, move)
            if(all(new_grid == grid)) then
               cycle
            end if
            score = search_min(new_grid, depth-1)
            if(score > max_score) then
               max_score = score
            end if
         end do

      end function search_max

      function search_min(grid, depth) result(score)
         implicit none
         integer, dimension(4,4) :: grid
         integer, intent(in) :: depth
         integer :: n, i, j, free
         real :: score

         if(depth == 0) then
            score = evaluate(grid)
            return
         end if

         score = 0
         free = 0
         do n=1,2
            do i=1,4
               do j=1,4
                  if(grid(i,j) == 0) then
                     grid(i,j) = num(n)
                     free = free + 1
                     score = score + p(n) * search_max(grid, depth)
                     grid(i,j) = 0
                  end if
               end do
            end do
            if(free == 0) then
               score = evaluate(grid)
               return
            end if
         end do

         score = 2 * score / free

      end function

      function get_next_move(grid, max_depth) result(best_move)
         implicit none
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
            score = search_min(new_grid, max_depth)
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

   real, parameter :: inf = 1E08
   integer, dimension(2) :: num = (/2, 4/)

   contains

      function search_max(grid, depth, alpha, beta) result(max_score)
         implicit none
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
         implicit none
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
         implicit none
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
   use expecti

   implicit none

   integer, dimension(4,4) :: grid, merged

   grid = reshape((/0, 0, 2, 2,&
                    0, 2, 0, 4,&
                    4, 4, 8, 8,&
                    4, 8,16, 0/), (/4, 4/))

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

end program test
