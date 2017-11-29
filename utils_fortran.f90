module utils
   contains
      function shift_left(grid) result(merged)
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
         integer, dimension(4,4), intent(in) :: grid
         integer, dimension(4,4) :: merged

         merged = merge_left(grid(:,4:1:-1))
         merged = merged(:,4:1:-1)

      end function merge_right

      function merge_up(grid) result(merged)
         integer, dimension(4,4), intent(in) :: grid
         integer, dimension(4,4) :: merged

         merged = transpose(merge_left(transpose(grid)))

      end function merge_up

      function merge_down(grid) result(merged)
         integer, dimension(4,4), intent(in) :: grid
         integer, dimension(4,4) :: merged

         merged = merge_up(grid(4:1:-1,:))
         merged = merged(4:1:-1,:)

      end function merge_down

end module utils

program test
   use utils

   integer, dimension(4,4) :: grid, merged
   integer :: i,j

   grid(1,1) = 0
   grid(1,2) = 0
   grid(1,3) = 2
   grid(1,4) = 2

   grid(2,1) = 0
   grid(2,2) = 2
   grid(2,3) = 0
   grid(2,4) = 4

   grid(3,1) = 4
   grid(3,2) = 4
   grid(3,3) = 8
   grid(3,4) = 8

   grid(4,1) = 4
   grid(4,2) = 8
   grid(4,3) = 16
   grid(4,4) = 0

   do i=1,4
      print *, grid(i,1), grid(i,2), grid(i,3), grid(i,4)
   end do
   print *

   merged = merge_left(grid)

   do i=1,4
      print *, merged(i,1), merged(i,2), merged(i,3), merged(i,4)
   end do

end program test
