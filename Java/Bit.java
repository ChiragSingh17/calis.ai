import java.util.*;

public class Bit {
    public static void main(String[] args) {
        Scanner in = new Scanner(System.in);
        int oper = in.nextInt();
        int n=5 , pos = 1, BitMask = 1<<pos;
        if(oper==1){
         int newNumber = BitMask|n;
         System.out.println(newNumber);
        }else{
            //clear
            int newBitMask = ~(BitMask);
            int newNumber = newBitMask & n;
            System.out.println(newNumber);
        }

    }

    }

