import Data.Set (Set)
import qualified Data.Set as Set

-- for each element in the list, removes it from the set if it exists
setminus :: Set Int -> [Int] -> Set Int
setminus s [] = s
setminus s (h:t) = setminus (Set.delete h s) t

-- return column as list
get_col :: [[Int]] -> Int -> [Int]
get_col grid c = [grid!!r!!c | r <- [0..8]]

-- return list of numbers in a sub block containing r,c
get_block :: [[Int]] -> Int -> Int -> [Int]
get_block grid r c = let rmin = 3*(r`div`3) in let cmin = 3*(c`div`3) in
                  [grid!!rr!!cc | rr <- [rmin..rmin+2], cc <- [cmin..cmin+2]]

-- adds n to the grid at r,c
insert :: [[Int]] -> Int -> Int -> Int -> [[Int]]
insert grid n r c = [ [ if rr == r && cc == c then n else grid!!rr!!cc
                        | cc <- [0..8]]
                      | rr <- [0..8]]

solve :: [[Int]] -> Int -> [[Int]]
solve grid 81 = grid -- solved
solve grid p = let r = p `div` 9 in let c = p `mod` 9 in
            if (grid!!r!!c) /= 0 then solve grid (p+1)
            else
                -- numbers that can go in current cell
                let valid = Set.toList ( setminus (Set.fromList [1..9])
                                (grid!!r ++ (get_col grid c)
                                 ++ (get_block grid r c)) ) in
                -- get first solution from recursion if solution can be found
                let sols = dropWhile (\x -> x == [])
                           [solve (insert grid n r c) (p+1) | n <- valid] in
                -- return solution grid, otherwise [] if no solution
                if sols == [] then [] else head sols

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

main = do
    print sample
    print (solve sample 0)
