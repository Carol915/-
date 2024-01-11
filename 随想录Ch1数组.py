#!/usr/bin/env python
# coding: utf-8

# # 代码随想录 Chapter1 数组Array

# # Day1 | 704. Binary Search, 35, 34, 27. Remove Elements  

# ## LC704 Binary Search (easy)

# ![Screenshot 2024-01-10 at 23.54.18.png](<attachment:Screenshot 2024-01-10 at 23.54.18.png>)

# 写在前面：二分法也是一种特殊的双指针，有left, right，还有mid指针。

# ### 写法1: 左闭右闭 [left, right]

# 第一种写法，我们定义 target 是在一个在左闭右闭的区间里，也就是[left, right] （这个很重要）。
# 
# 区间的定义这就决定了二分法的代码应该如何写，因为定义target在[left, right]区间，所以有如下两点：
# 
# - while left <= right: 要使用 **<=** ，因为left == right是有意义的，所以使用 <=
# 
# - if nums[middle] > target: right 要赋值为 **middle - 1**，因为当前这个nums[middle]一定不是target，那么接下来要查找的左区间结束下标位置就是 middle - 1

# In[1]:


class Solution:
    def search(self, nums:list[int], target: int) -> int:
        # method1: [left, right]
        # 如果没找到，res为-1
        res = -1 
        left, right = 0, len(nums) - 1

        while left <= right: 
            mid = (left + right) // 2 # floor division: 向下取整
            # or mid = left + (right - left) // 2

            if nums[mid] > target:
                right = mid - 1  # target在左区间，所以[left, middle - 1]
            elif nums[mid] < target:
                left = mid + 1   # target在右区间，所以[middle + 1, right]
            else:
                # 找到目标，更新res
                res = mid
                break
        
        return res
    
# test
nums = [1, 2, 3, 4, 5, 6, 7, 8]
target = 5
s = Solution()
s.search(nums, target)


# ### 写法2: 左闭右开

# 如果说定义 target 是在一个在左闭右开的区间里，也就是[left, right) ，那么二分法的边界处理方式则截然不同。
# 
# 有如下两点：
# 
# - while (left < right)，这里使用 < ,因为left == right在区间[left, right)是没有意义的
# - if (nums[middle] > target) right 更新为 middle，因为当前nums[middle]不等于target，去左区间继续寻找，而寻找区间是左闭右开区间，所以right更新为middle，即：下一个查询区间不会去比较nums[middle]

# In[8]:


class Solution:
    def search(self, nums: list[int], target: int) -> int:
        # method 2: [left, right)
        # 如果没找到，res为-1
        res = -1 
        left, right = 0, len(nums)

        # 因为left == right的时候，在[left, right)是无效的空间
        while left < right: 
            mid = (left + right) // 2 # floor division: 向下取整
            # or mid = left + (right - left) // 2

            if nums[mid] > target:
                right = mid   # target在左区间，所以[left, middle)
                              # 注意此时mid 一定不是答案
            elif nums[mid] < target:
                left = mid + 1   # target在右区间，所以[middle + 1, right)
            else:
                # 找到目标，更新res
                res = mid
                break
        
        return res

# test
nums = [1, 2, 3, 4, 5, 6, 7, 8]
target = 5
s = Solution()
s.search(nums, target)


# 时间复杂度：O(log N)
# 
# 空间复杂度：O(1)

# ## LC35 Search Insert Position (Easy)

# ![Screenshot 2024-01-11 at 00.21.30.png](<attachment:Screenshot 2024-01-11 at 00.21.30.png>)

# Comment: 
# 
# - 本体也是二分法的变体，就比上一题多一步。
# - 边界处理的时候自己拿草稿纸多演算几步就好。

# ### 写法1: 左闭右闭

# In[10]:


# 自己写的
class Solution:
    def searchInsert(self, nums: list[int], target: int) -> int:
        # 二分法
        # 法1: 左闭右闭
        left, right = 0, len(nums) - 1 
        found = 0
        
        # left == right, 区间有意义
        while left <= right:
            mid = (left + right) // 2

            if nums[mid] > target:
                right = mid - 1  # target在左区间，所以[left, middle - 1]
            elif nums[mid] < target: 
                left = mid + 1  # target在右区间，所以[middle + 1, right]
            else:
                # 找到了
                found = 1
                res = mid
                break
        
        # 如果没找到，那么最后肯定是left == right
        # 然后进到while loop里面，然后left = mid + 1 （不可能是right = mid - 1， 因为如果left永远<= target)
        if found == 0: 
            res = left # left == right + 1
        
        return res

# test
nums = [1,3,5,6]
target = 2
s = Solution()
s.searchInsert(nums, target)


# In[12]:


# 代码随想录优化

class Solution:
    def searchInsert(self, nums: list[int], target: int) -> int:
        # 二分法
        # 法1: 左闭右闭
        left, right = 0, len(nums) - 1 
        
        while left <= right:
            mid = (left + right) // 2
            if nums[mid] > target:
                right = mid - 1     # target在左区间，所以[left, middle - 1]
            elif nums[mid] < target: 
                left = mid + 1      # target在右区间，所以[middle + 1, right]
            else:
                return mid          # return 直接 end function
        
        return left                 # left == right + 1 跟随想录一样


# ### 写法2: 左闭右开

# In[13]:


# 自己写，随想录没有
class Solution:
    def searchInsert(self, nums: list[int], target: int) -> int:
        # 二分法
        # 法2: 左闭右开
        left, right = 0, len(nums) 
        
        while left < right:
            mid = (left + right) // 2
            if nums[mid] > target:
                right = mid         # target在左区间，所以[left, middle）
            elif nums[mid] < target: 
                left = mid + 1      # target在右区间，所以[middle + 1, right)
            else:
                return mid          # return 直接 end function
        
        # 如果没找到，最后是left == right 出的while loop
        return left                


# ## LC27 Remove Element

# ![Screenshot 2024-01-11 at 00.52.38.png](<attachment:Screenshot 2024-01-11 at 00.52.38.png>)

# ![Screenshot 2024-01-11 at 00.52.58.png](<attachment:Screenshot 2024-01-11 at 00.52.58.png>)

# ### 法1: 暴力解法

# In[16]:


class Solution:
    def removeElement(self, nums: list[int], val: int) -> int:
        k = len(nums)
        for i in range(len(nums)):
            while(nums[i] == val):
                nums[i] = 200
                k -= 1
        nums.sort()
        return k 


# 时间复杂度: O($N^2$)  
# 空间复杂度：O(1)

# 注：
# 
# - 其实也可以用del nums[i] 的方法写暴力，但是比较麻烦。原因是delete 某个元素过后，nums的长度会发生改变，很影响你for loop 的遍历（比如下面这个错误的代码）。所以我们只是巧妙地运用了0 <= nums[i] <= 50 这个限制条件，把和val相等的数字都改成200，这样数组长度不变。
# 
# - 另外这里目的是让我们学会del库函数的实现，carl说可以用库函数做的就别用库函数。

# In[15]:


nums = [1,3,5,6]
del nums[0]
nums


# In[19]:


class Solution:
    def removeElement(self, nums: list[int], val: int) -> int:
        # n 为最初的len(nums)
        n = len(nums)
        k = len(nums)
        for i in range(n):
            while nums[i] == val:
                del nums[i]
                k -= 1
        
        # 补齐nums的长度
        underscores = ['_' for _ in range(n - k)]

        nums.extend(underscores)
        return k 
    
# test
nums = [1,3,5,6]
val = 3
s = Solution()
s.removeElement(nums, val)


# ### 法2: 双指针 fast, slow

# 双指针有left right, fast slow, 后面有专门的章节讲。

# **双指针法（快慢指针法）**： 通过一个快指针和慢指针在一个for循环下完成两个for循环的工作。
# 
# 定义快慢指针
# 
# **快指针**：fast always move to the right every time!
# 
# **慢指针**：slow 的移动是有条件的。  
# 在本题中，只有当nums[fast] != val的时候slow才会往右移动一格。换句话说，**如果nums[fast] == val，那么slow就不动，默默等待被替换**。

# In[20]:


# 写法1: use while loop

class Solution:
    def removeElement(self, nums: list[int], val: int) -> int:

        slow, fast = 0, 0
        
        while fast < len(nums):
            if nums[fast] != val:
                nums[slow] = nums[fast]
                # 如果nums[fast] == val，那么slow就不动，默默等待被替换
                slow += 1
            # fast moves to the right every time
            fast += 1
        
        # slow指针相当于在计数有多少个number != val
        return slow

# test
nums = [1,3,5,6]
val = 3
s = Solution()
s.removeElement(nums, val)


# 再次强调快慢指针的精妙之处：
# - fast index相当于在遍历数组，  
# - slow index在nums[fast] == val的时候不动，默默等待被替换。另外，slow指针相当于在计数有多少个number != val。

# In[21]:


# 写法2: use for loop 

class Solution:
    def removeElement(self, nums: list[int], val: int) -> int:
      
        slow, fast = 0, 0

        # fast 遍历数组的功能在这里体现，然后不需要 fast += 1 了
        for fast in range(len(nums)):
            if nums[fast] != val:
                nums[slow] = nums[fast]
                # 如果nums[fast] == val，那么slow就不动，默默等待被替换
                slow += 1
        
        # slow指针相当于在计数有多少个number != val
        return slow


# 重点：fast 指针遍历数组的功能在这里体现，然后不需要 fast += 1 了

# 时间复杂度: O($N$)  
# 空间复杂度：O(1)

# In[4]:


pip install nbconvert


# In[2]:


# run in terminal
jupyter nbconvert /Users/xingqitian/Desktop/Python/Leetcode/随想录Ch1数组.ipynb --to python


# In[ ]:




