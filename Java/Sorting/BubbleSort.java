package Sorting;

import java.util.Arrays;

public class BubbleSort {
    public class Sorting {
    public static void printarray(int arr[]){
     System.out.print(Arrays.toString(arr)+" ");
    }
    public static void main(String args[]){
        int arr [] = {7,8,3,1,2};
    //time complexity = O(n^2)
    //Bubble sort
    for(int i=0; i < arr.length-1; i++){
        for(int j=0;j < arr.length-i-1 ;j++){
            if(arr[j]>arr[j+1]){
                //swap
                int temp = arr[j];
                arr[j] = arr[j+1];
                arr[j+1] = temp;
            }
        }
    }
    printarray(arr);
    }

}
}
