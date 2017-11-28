module utils
   contains
      function shift_left(grid) result(merged)
         integer, dimension(4,4), intent(in) :: grid
         integer, dimension(4,4) :: merged

         integer :: k,i,j

         do i=1,4
            k = 1
            do j=1,4
               if(grid(j,i) /= 0) then
                  merged(k,i) = grid(j,i)
                  k = k+1
               end if
            end do
            do j=k,4
               merged(j,i) = 0
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
               if(merged(j,i) == merged(j+1,i) .and. merged(j,i) /= 0) then
                  merged(j,i) = 2 * merged(j,i)
                  merged(j+1,i) = 0
               end if
            end do
         end do

         merged = shift_left(merged)

      end function merge_left

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
