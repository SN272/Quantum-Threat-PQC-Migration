import time
import statistics

measurements = []

for _ in range(10):
    start = time.perf_counter()

    total = 0                       
    for i in range(1_000_000):
        total += i

    end = time.perf_counter()

    measurements.append(end - start)

print("Measurements: ", measurements)
print("Mean: ", statistics.mean(measurements))
print("Median: ", statistics.median(measurements))
print("Minimum", min(measurements))
print("Standard Deviation: ", statistics.stdev(measurements))