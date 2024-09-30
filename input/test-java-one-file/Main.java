import java.util.Arrays;

public class Main {

    // Function to implement Bubble Sort
    public static void bubbleSort(int[] array) {
        int n = array.length;
        boolean swapped;
        
        // Traverse through all elements in the array
        for (int i = 0; i < n - 1; i++) {
            swapped = false;

            // Compare each element with the next and swap if necessary
            for (int j = 0; j < n - i - 1; j++) {
                if (array[j] > array[j + 1]) {
                    // Swap array[j] and array[j+1]
                    int temp = array[j];
                    array[j] = array[j + 1];
                    array[j + 1] = temp;
                    swapped = true;
                }
            }

            // If no elements were swapped in the inner loop, array is sorted
            if (!swapped) {
                break;
            }
        }
    }

    public static void main(String[] args) {
        // Example array to sort
        int[] array = {64, 34, 25, 12, 22, 11, 90};

        System.out.println("Unsorted array: " + Arrays.toString(array));

        // Apply bubble sort
        bubbleSort(array);

        System.out.println("Sorted array: " + Arrays.toString(array));
    }
}
