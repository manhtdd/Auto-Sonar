# Function to implement Bubble Sort
def bubble_sort(arr):
    n = len(arr)
    # Traverse through all elements in the array
    for i in range(n):
        swapped = False
        # Traverse the array from 0 to n-i-1
        # The last i elements are already sorted
        for j in range(0, n - i - 1):
            # Swap if the element found is greater
            # than the next element
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        # If no two elements were swapped in the inner loop, then break
        if not swapped:
            break

# Main execution
if __name__ == "__main__":
    # Example array
    arr = [64, 34, 25, 100, 22, 11, 90]
    
    print("Unsorted array:", arr)
    
    # Call bubble sort function
    bubble_sort(arr)
    
    print("Sorted array:", arr)
