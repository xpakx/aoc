from utils.loader import get_file
from utils.runner import AdventDay


def load(filename):
    return get_file(filename, as_int=True)


def step(nums):
    moved = False
    for i in range(len(nums)-1):
        if nums[i] > nums[i+1]:
            nums[i] -= 1
            nums[i+1] += 1
            moved = True
    return moved


def step_second_phase(nums):
    moved = False
    for i in range(len(nums)-1):
        if nums[i] < nums[i+1]:
            nums[i+1] -= 1
            nums[i] += 1
            moved = True
    return moved


def checksum(nums):
    return sum([x*(i+1) for i, x in enumerate(nums)])


def part1(nums):
    print("0:", nums)
    phase = 1
    for i in range(10):
        if phase == 1:
            moved = step(nums)
        if not moved:
            phase = 2
        if phase == 2:
            moved = step_second_phase(nums)
        if not moved:
            break
        print(f"{i+1}: {nums}")

    print(nums)
    return checksum(nums)


def part2(nums):
    phase = 1
    i = 0
    while True:
        if phase == 1:
            moved = step(nums)
        if not moved:
            break
        i += 1

    verify(nums)
    mean = sum(nums) // len(nums)
    i += sum(mean - num for num in nums if num < mean)
    return i


def verify(nums):
    assert all(
        nums[i] <= nums[i+1] for i in range(len(nums)-1)
    ), "Input should be monotonically ascending"


def part3(nums):
    verify(nums)
    # Now, since the input is sorted, we have
    # left side with deficits and right side of surpluses
    # so, there is such k, that for indices i in [0, k]
    # all nums[i] < mean, and for all i in [k+1, n]
    # all nums[i] >= mean
    # the task is equivalent to moving mass
    # from surplus part to deficit part

    # let's consider a cycle (equivalent to step_second_phase()
    # method

    # now let's suppose that at the beginning of step j,
    # there is a k that fullfill such conditions,
    # then at i==k, nums[k]_current <= nums[k]_start
    # (bc one duck could be moved "back"),
    # and i+1 wasn't moved yet;
    # and bc k was boundary between deficits and surpluses,
    # it is guaranteed that there is exactly one swap
    # from surpluses to deficits, because:
    # nums[k]_current < nums[k+1]_start

    # then either
    # nums[k+1]_current == mean - 1,
    # or nums[k+1]_current >= mean otherwise
    # in the former case, deficit we got would be
    # filled from nums[k+1], which is >= mean, and so on.
    # because there is still surplus on the right side,
    # then there is an element at j>k, that nums[j]>=mean+1
    # so even when it will move one duck left, it would be
    # at least == mean
    # so k cannot move right

    # what's more:
    # and for each i<k nums[i]_start < mean,
    # and num[i] could grow only if num[i+1]_start>num[i]_current,
    # because of that num[i] could at most grow to
    # mean-1 if num[i]_current == mean-2 and num[i+1]_start == mean-1

    # so the only place when nums[i] can grow to mean is k
    # so (1) there are no "heaps" before k-1, and (2) k either
    # moves 1 place left or stays at the same place

    # so we know that in each cycle there is one duck
    # moved from [k+1, n-1] to [0, k] and
    # that the balancing ends when k == 0
    # (because all [0, n-1] are >= mean, so
    # if at least one is > mean by c, then sum is
    # n*mean + c, which is a contradiction,
    # bc intial input is balanceable, and by
    # properties of mean), and that at the beginning
    # of each cycle there is a k with such properties

    # because of that the total amount of cycles
    # is equal to total surplus

    mean = sum(nums) // len(nums)
    return sum(mean - num for num in nums if num < mean)


app = AdventDay()
app.run()
