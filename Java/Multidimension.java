import java.util.Arrays;
import java.util.Scanner;

public class Multidimension {
    public static void main(String[] args) {
        Scanner in = new Scanner(System.in);
    //   int[][] arr =new int[3][];  
    // int[][] arr2D = {
    //     {1, 2, 3},
    //     {4, 5, 6},
    //     {7, 8, 9}
    // };
    // System.out.print(Arrays.toString(arr2D));
        int arr[][] = {
            {1, 2, 5, 7},
            {8, 6, 4},
            {9, 0}
        };
    // for (int row = 0; row < arr.length; row++) {
    //     for (int col = 0; col < arr[row].length; col++) {
    //         arr[row][col]=in.nextInt();
    //     }
    // }
    // for (int[] a:arr ) {
    //     System.out.println(Arrays.toString(a));
    // }
  for (int row = 0; row < arr.length; row++) {
    for(int col=0;col<arr[row].length;col++){
        System.out.print(arr[row][col]+" ");
    }System.out.println();
  }
}

}

