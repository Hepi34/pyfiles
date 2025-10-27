import random
import time
import os
import threading
import argparse

# © Noah, 21.10.2025

# Default values in case no arguments are provided
# List parameters
HOW_MANY_NUMBERS = 10000
LOWEST_RANDOM = 1
HIGHEST_RANDOM = 100000

# How many loops to run (every loop has a different list)
NUM_LOOPS = 3

# Compare 2 elements and switch if left one is bigger 
def bubbleSort(list):
    while True:
        numberOfChanges = 0
        for i in range(len(list) - 1):
            if (list[i]) > (list[i+1]):
                temp1 = list[i]
                list[i] = list[i+1]
                list[i+1] = temp1
                numberOfChanges += 1
        
        if numberOfChanges == 0:
            break      

    return list         

# Compare 2 numbers, move the right one to the left until the one on the left is smaller or equal              
def insertionSort(list):
    for i in range(1, len(list)):
        num = list[i]
        j = i - 1

        while j >= 0 and list[j] > num:
            list[j + 1] = list[j]
            j -= 1
        list[j+1] = num
    
    return list

# Split lists in half until there is 1 element, then add them back togehter by order
def mergeSort(list):
    if len(list) > 1:

        mid = len(list) // 2
        left = list[:mid]
        right = list[mid:]

        mergeSort(left) # 5
        mergeSort(right) # 8

        i_l = 0
        i_r = 0
        i = 0

        while i_l < len(left) and i_r < len(right):
            if right[i_r] < left[i_l]:
                list[i] = right[i_r]
                i_r += 1
                i += 1
            else:
                list[i] = left[i_l]
                i_l += 1
                i += 1
        
        while i_l < len(left):
            list[i] = left[i_l]
            i_l += 1
            i += 1


        while i_r < len(right):
            list[i] = right[i_r]
            i_r += 1
            i += 1

    return list

# Set a pivot and sort elements to the left and right of the chosen pivot. Repeat until only one remains, then add back together
def quickSort(list):
    if len(list) <= 1:
        return list

    pivot = list[0]

    smaller = []
    larger = []    

    for i in range(1, len(list)):
        if list[i] >= pivot:
            larger.append(list[i])
        else:
            smaller.append(list[i])

    sorted_smaller = quickSort(smaller)
    sorted_larger = quickSort(larger)

    return sorted_smaller + [pivot] + sorted_larger

# Generates a list using the parameters at the start of the file
def makeList():
    numberlist = []

    for i in range(HOW_MANY_NUMBERS):
        numberlist.append(random.randint(LOWEST_RANDOM, HIGHEST_RANDOM))

    return numberlist

# Tests all four algorhithms with the same list and returns the time taken to sort 
def testAll(list):
    list1 = list.copy()
    s1 = time.time()
    bubbleSort(list1)
    e1 = time.time()
    bubbleTime = e1 - s1

    list2 = list.copy()
    s2 = time.time()
    insertionSort(list2)
    e2 = time.time()
    insertionTime = e2 - s2

    list3 = list.copy()
    s3 = time.time()
    mergeSort(list3)
    e3 = time.time()
    mergeTime = e3 - s3

    list4 = list.copy()
    s4 = time.time()
    quickSort(list4)
    e4 = time.time()
    quickTime = e4 - s4

    return bubbleTime, insertionTime, mergeTime, quickTime

# Unnecessary loading spinner to indicate activity :)
def loadingAnimation(stop_event: threading.Event):
    spinner = ["|", "/", "-", "\\"]
    idx = 0
    while not stop_event.is_set():
        # Overwrite the current line's start with a spinner char
        print('\r' + spinner[idx], end='', flush=True)
        idx = (idx + 1) % len(spinner)
        time.sleep(0.1)

# Test all four algorhithms numLoop times and return a list with the times taken
def testLoop(numLoop):
    bubbleTimes = []
    insertionTimes = []
    mergeTimes = []
    quickTimes = []

    for i in range(numLoop):

        # Clear the terminal on all OSes
        os.system('cls' if os.name == 'nt' else 'clear')

        print("(DEBUG) Iteration " + str(i+1))
        # For the loading animnation
        print(" ", end='', flush=True)

        stop_event = threading.Event()
        spinner_thread = threading.Thread(target=loadingAnimation, args=(stop_event,), daemon=True)
        spinner_thread.start()

        list = makeList()
        bubbleTime, insertionTime, mergeTime, quickTime = testAll(list)

        stop_event.set()
        spinner_thread.join()

        os.system('cls' if os.name == 'nt' else 'clear')


        bubbleTimes.append(bubbleTime)
        insertionTimes.append(insertionTime)
        mergeTimes.append(mergeTime)
        quickTimes.append(quickTime)
    
        
    return bubbleTimes, insertionTimes, mergeTimes, quickTimes

# Get the avg of a list (simple)
def getAvg(list):
    return sum(list) / len(list)

# Main testing loop
def main(numLoop):

    bubbleTimes, insertionTimes, mergeTimes, quickTimes = testLoop(numLoop)

    bubbleAvg = getAvg(bubbleTimes)
    insertionAvg = getAvg(insertionTimes)
    mergeAvg = getAvg(mergeTimes)
    quickAvg = getAvg(quickTimes)

    print("Bubble Sort Average Time: " + str(bubbleAvg))
    print("Insertion Sort Average Time: " + str(insertionAvg))
    print("Merge Sort Average Time: " + str(mergeAvg))
    print("Quick Sort Average Time: " + str(quickAvg))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Script that compares Bubble, Insertion, Merge and Quick sorting algorhithms"
    )
    parser.add_argument("--listnum", required=False, type=int, default=10000, help="The amount of numbers in the list to sort. Default 10000")
    parser.add_argument("--lowestrand", required=False, type=int, default=1, help="The lowest possible random number. Default 1")
    parser.add_argument("--highestrand", required=False, type=int, default=100000, help="The highest possible random number. Default 100000")
    parser.add_argument("--iterations", required=False, type=int, default=3, help="The numer of iterations to test the algorhithms with different lists. Default 3")

    args = parser.parse_args()


    HOW_MANY_NUMBERS = args.listnum
    LOWEST_RANDOM = args.lowestrand
    HIGHEST_RANDOM = args.highestrand
    NUM_LOOPS = args.iterations

    main(NUM_LOOPS)
