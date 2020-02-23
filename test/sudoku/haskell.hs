import Data.Set (Set)
import qualified Data.Set as Set

-- for each element in the list, removes it from the set if it exists
setminus :: Set Int -> [Int] -> [Int]
setminus s [] = Set.toList s
setminus s (h:t) = setminus (Set.delete h s) t

-- return column as list
get_col :: [[Int]] -> Int -> [Int]
get_col grid c = [grid!!r!!c | r <- [0..8]]

-- return list of numbers in a sub block containing r,c
get_block3x3 :: [[Int]] -> Int -> Int -> [Int]
get_block3x3 grid r c = let rmin = 3*(r`div`3) in let cmin = 3*(c`div`3) in
                  [grid!!rr!!cc | rr <- [rmin..rmin+2], cc <- [cmin..cmin+2]]

-- generalized to boards of other sizes
get_block :: [[Int]] -> Int -> Int -> Int -> Int -> [Int]
get_block grid r c br bc = let rmin = br*(r`div`br) in
                           let cmin = bc*(c`div`bc) in
    [grid!!rr!!cc | rr <- [rmin..rmin+br-1], cc <- [cmin..cmin+bc-1]]

-- adds n to the grid at r,c
insert :: [[Int]] -> Int -> Int -> Int -> [[Int]]
insert grid n r c = [ [ if rr == r && cc == c then n else grid!!rr!!cc
                        | cc <- [0..8]]
                      | rr <- [0..8]]

solve3x3 :: [[Int]] -> Int -> [[Int]]
solve3x3 grid 81 = grid -- solved
solve3x3 grid p = let r = p `div` 9 in let c = p `mod` 9 in
            if (grid!!r!!c) /= 0 then solve3x3 grid (p+1)
            else
                -- numbers that can go in current cell
                let valid = setminus (Set.fromList [1..9])
                                (grid!!r ++ (get_col grid c)
                                 ++ (get_block3x3 grid r c)) in
                -- get first solution from recursion if solution can be found
                let sols = dropWhile (\x -> x == [])
                           [solve3x3 (insert grid n r c) (p+1) | n <- valid] in
                -- return solution grid, otherwise [] if no solution
                if sols == [] then [] else head sols

verify3x3 :: [[Int]] -> Bool
verify3x3 grid = let numsset = Set.fromList [1..9] in
    and [ and [(Set.fromList (grid!!r)) == numsset | r <- [0..8]],
          and [(Set.fromList (get_col grid c)) == numsset | c <- [0..8]],
          and [(Set.fromList (get_block3x3 grid (3*r) (3*c))) == numsset
               | r <- [0..2], c <- [0..2]] ]

-- generalized to other sizes
solve :: [[Int]] -> Int -> Int -> Int -> [[Int]]
solve grid p br bc = if p == (br*br*bc*bc) then grid -- solved
                     else let r = p `div` (br*bc) in let c = p `mod` (br*bc) in
    if (grid!!r!!c) /= 0 then solve grid (p+1) br bc
    else let valid = setminus (Set.fromList [1..br*bc])
                     (grid!!r ++ (get_col grid c) ++ (get_block grid r c br bc))
      in let sols = dropWhile (\x -> x == [])
                    [solve (insert grid n r c) (p+1) br bc | n <- valid] in
         if sols == [] then [] else head sols

verify :: [[Int]] -> Int -> Int -> Bool
verify grid br bc = let numsset = Set.fromList [1..br*bc] in
    and [ and [(Set.fromList (grid!!r)) == numsset | r <- [0..br*bc-1]],
          and [(Set.fromList (get_col grid c)) == numsset | c <- [0..br*bc-1]],
          and [(Set.fromList (get_block grid (br*r) (bc*c) br bc)) == numsset
               | r <- [0..br-1], c <- [0..bc-1]] ]

sample :: [[Int]]
sample = [[1,0,0,0,2,0,0,3,7],
          [0,6,0,0,0,5,1,4,0],
          [0,5,0,0,0,0,0,2,9],
          [0,0,0,9,0,0,4,0,0],
          [0,0,4,1,0,3,7,0,0],
          [0,0,1,0,0,4,0,0,0],
          [4,3,0,0,0,0,0,1,0],
          [0,1,7,5,0,0,0,8,0],
          [2,8,0,0,4,0,0,0,6]]

main =
    let sample_solved = solve sample 0 3 3 in do
    print sample
    print sample_solved
    print (verify sample_solved 3 3)
