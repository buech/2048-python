module utils
   contains

      function shift_left(grid) result(merged)
         implicit none
         integer, dimension(4,4), intent(in) :: grid
         integer, dimension(4,4) :: merged

         integer :: k,i,j

         merged(:,:) = 0
         do i=1,4
            k = 1
            do j=1,4
               if(grid(i,j) /= 0) then
                  merged(i,k) = grid(i,j)
                  k = k+1
               end if
            end do
         end do

      end function shift_left

      function merge_left(grid) result(merged)
         implicit none
         integer, dimension(4,4), intent(in) :: grid
         integer, dimension(4,4) :: merged

         integer :: i,j

         merged = shift_left(grid)

         do i=1,4
            do j=1,3
               if(merged(i,j) == merged(i,j+1) .and. merged(i,j) /= 0) then
                  merged(i,j) = 2 * merged(i,j)
                  merged(i,j+1) = 0
               end if
            end do
         end do

         merged = shift_left(merged)

      end function merge_left

      function merge_right(grid) result(merged)
         implicit none
         integer, dimension(4,4), intent(in) :: grid
         integer, dimension(4,4) :: merged

         merged = merge_left(grid(:,4:1:-1))
         merged = merged(:,4:1:-1)

      end function merge_right

      function merge_up(grid) result(merged)
         implicit none
         integer, dimension(4,4), intent(in) :: grid
         integer, dimension(4,4) :: merged

         merged = transpose(merge_left(transpose(grid)))

      end function merge_up

      function merge_down(grid) result(merged)
         implicit none
         integer, dimension(4,4), intent(in) :: grid
         integer, dimension(4,4) :: merged

         merged = merge_up(grid(4:1:-1,:))
         merged = merged(4:1:-1,:)

      end function merge_down

      function direction(grid, move) result(merged)
         implicit none
         integer, dimension(4,4), intent(in) :: grid
         integer, intent(in) :: move
         integer, dimension(4,4) :: merged
         integer :: moved

         select case (move)
            case (1)
               merged = merge_up(grid)
            case (2)
               merged = merge_down(grid)
            case (3)
               merged = merge_right(grid)
            case (4)
               merged = merge_left(grid)
         end select

      end function direction

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

      function evaluate(grid) result(score)
         implicit none
         integer, dimension(4,4), intent(in) :: grid
         integer :: score

         score = count_free_tiles(grid)

      end function

end module eval

module expecti
   use utils
   use eval

   integer, parameter :: inf = 1E08
   integer, dimension(2) :: num = (/2, 4/)
   real, dimension(2) :: p = (/0.9, 0.1/)

   contains

      function search_max(grid, depth) result(max_score)
         implicit none
         integer, dimension(4,4), intent(in) :: grid
         integer, intent(in) :: depth

         integer, dimension(4,4) :: new_grid
         integer :: move, score, max_score

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
         integer :: n, i, j, free, score

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
         integer :: max_score = -inf
         integer :: score, move, best_move

         best_move = 1
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
