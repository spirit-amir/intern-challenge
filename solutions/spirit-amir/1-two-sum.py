def find_two_sum(nums, target):
    num_dict = {}
    for index, num in enumerate(nums):
        complement = target - num
        if complement in num_dict:
            return [num_dict[complement], index]
        num_dict[num] = index
    return []

# Example usage:

target = int(input().strip())
nums = list(map(int, input().strip().split()))

result = find_two_sum(nums, target)
print(result[0], result[1])



