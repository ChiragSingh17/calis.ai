public class Searching {
    public static void main(String[] args){
        int arr[]={-15,-5,0,15,20};
        int ans = binarySearch(arr,15);
        System.out.println(ans);
    }
    public static int binarySearch(int arr[], int target){
        int start = 0;
        int end = arr.length-1;
        boolean isAsc = arr[start]<arr[end];


        while(start<=end){
            int mid = start +(end-start)/2;
            if(arr[mid]==target){
                return mid;
            }

            if (isAsc){
                if(arr[mid]<target){
                    start = mid+1;
                }else {
                    end=mid-1;
            }
        }else{
            if(arr[mid]>target){
                start = mid+1;
            }else {
                end=mid-1;
        }
        }
        }
        return -1;
    }

}

