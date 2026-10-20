
Osvaldo and his friend Rogelio are looking to buy some paints to add some color to his house. He knows each color he uses to paint his house will add a beauty x (not necessarily positive) to the house. The store is having a special offer; the paints are placed in a square matrix, and if you buy a set of paints such that you can draw a spiral in the matrix beginning in one of the corners and filling the whole matrix, where the set is contiguous in the spiral, the paint is free! Since Rogelio is in a hurry to start training for ICPC, they have asked you to help them find the best sum of beauty one can add to the house if the paint is free, notice you can decide to buy no paints.
Input

On the first line a number N (1≤N≤1000), the length of the matrix. In the next N lines, N numbers ai,j (−107≤ai,j≤107) indicating the beauty that color will add to the house if bought.
Output

Just a number X the best sum of beauty you can get added to the house such that the paints are free.

Examples
Input
2
-1 3
2 -5

Output
4

Input
3
1 -2 4
3 8 -6
5 1 -10

Output
20

Note
A spiral is a traversal of the matrix that is a reflection or rotation of one similar to this:

1	12	11	10
2	13	16	9
3	14	15	8
4	5	6	7

This is the specific case for n=4