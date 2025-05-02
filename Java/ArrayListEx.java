import java.util.ArrayList;
import java.util.*;
public class ArrayListEx {
    public static void main(String[] args) {
        int[] arr={1, 55, 78, 94, 45};
        // swap(arr, 0, 3);
        System.out.println("Before Reversing" +" "+ Arrays.toString(arr));
        reverse(arr);
        System.out.println("After reversing" +" "+ Arrays.toString(arr));
        // System.out.println(max(arr));
        

















       ArrayList<Integer> list = new ArrayList<>(1);
       Scanner sc = new Scanner(System.in);
        // list.add(69);
        // list.add(54);
        // list.add(78787);
        // list.add(53);
        // System.out.println(list);
        // list.set(1,78);
        // System.out.println(list);

        // for (int i = 0; i < 5; i++) {
        //    list.add(sc.nextInt());
        // }
        // System.out.println(list);

        
        // ArrayList<ArrayList<Integer>> l = new ArrayList<>();
        // for (int i = 0; i < 3; i++) {
        //    l.add(new ArrayList<>());
        // }
        // for (int i = 0; i < 3; i++) {
        //     for (int j = 0; j < 3; j++) {
        //         l.get(i).add(sc.nextInt());
        //     }
        // }
        // System.out.println(l);
    }
    static void reverse(int[] arr){
        int start =0;
        int end=arr.length-1;
        while(start<end){
            swap(arr, start, end);
            start++;
            end--;
        }
    }
    static void swap(int[] arr, int index1, int index2){
        int temp = arr[index1];
        arr[index1]=arr[index2];
        arr[index2] =temp;
    // }
    // public static int max(int[] arr){
    //     int max = arr[0];
    //     for (int i = 1; i < arr.length; i++) {
    //         if(arr[i]>max){
    //             max = arr[i];
                
    //         }
    //     }
    //     return max;
    }
}
