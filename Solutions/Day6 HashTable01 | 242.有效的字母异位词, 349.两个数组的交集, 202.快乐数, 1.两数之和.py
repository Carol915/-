#!/usr/bin/env python
# coding: utf-8

# # 代码随想录 Chapter3 Hash Table

# # Day 6 | 242.有效的字母异位词, 349.两个数组的交集, 202.快乐数, 1.两数之和

# **哈希表理论基础**
# 
# 建议：大家要了解哈希表的内部实现原理，哈希函数，哈希碰撞，以及常见哈希表的区别，数组，set 和map。  
# 
# 什么时候想到用哈希法，当我们遇到了要快速判断一个元素是否出现集合里的时候，就要考虑哈希法。  这句话很重要，大家在做哈希表题目都要思考这句话。 
# 
# https://programmercarl.com/哈希表理论基础.html#哈希表

# ## 总结
# 
# 三种哈希结构： array, set, dictionary
# 
# #### 1. Array as Hashtable:
# - **Usage**: Arrays (or lists in Python) can be used as a simple hashtable when you have **a small, fixed range of integer key**s. In this case, the index of the array acts as the key, and the element at that index is the value.
# - **Key**: The array index (an integer).
# - **Value**: The data stored at that index.
# - **When to Use**:
#   - When the keys are **sequential integers**.
#   - When memory is not a constraint (as arrays can waste memory if the range of keys is large but sparsely populated).
#   - When the dataset is small and operations are simple.
#   - e.g. 26个英文字母
# 
# #### 2. Set as Hashtable:
# - **Usage**: A set in Python can act as a hashtable with keys but no associated values. It is ideal for storing unique elements and checking membership efficiently.
# - **Key**: The element itself.
# - **Value**: <span style="color:red">Sets do **not** store values, only keys</span>.
# - **When to Use**:
#   - When you need to keep track of **unique items**.
#   - When the primary operations are **insertion, deletion, and check operations** because they take $O(1)$ time complexity.
#   - When you don't need to store additional data (values) associated with the keys.
#   - e.g. LC349, 128
# 
# #### 3. Dictionary as Hashtable:
# - **Usage**: A dictionary in Python is a direct implementation of a hashtable, where each **key-value pair** is stored.
# - **Key**: The unique identifier used to store and retrieve the value.
# - **Value**: The data associated with a key.
# - **When to Use**:
#   - When you need to associate values with keys (not just check for the presence of a key).
#   - When keys are non-sequential or non-integer.
#   - For more complex data structures where each element needs to store multiple attributes.
#   - <span style="color:red">Keys should be of **immutable** datatype: numbers, string, tuple.</span>
# 

# 我自己的理解是dictionary是最standardize的hashtable，其他两个都是它的简化版本。

# In[2]:


from typing import Optional, List, Dict, Any, Tuple, Union


# ## LC242. Valid Anagram (Easy)

# ![Screenshot 2024-02-05 at 17.22.14.png](<attachment:Screenshot 2024-02-05 at 17.22.14.png>)

# 简单题我就不多做讲解了，本题方法: three structures of hash table, this question we can use **array** or **dictionary**.

# ### method1: array as hashtable

# In[3]:


class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        record = [0] * 26
        for i in s:
            # 并不需要记住字符a的ASCII，只要求出一个相对数值就可以了
            record[ord(i) - ord("a")] += 1      # (1)
        for i in t:
            record[ord(i) - ord("a")] -= 1      # (2)
        for i in range(26):
            if record[i] != 0:
                # record数组如果有的元素不为零0，说明字符串s和t一定是谁多了字符或者谁少了字符。
                return False
        return True

# test 
s = Solution()
s.isAnagram("anagram", "nagaram")


# ![image.png](attachment:image.png)

# ### method2: defaultdict as hashtable

# In[4]:


class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        
        from collections import defaultdict
        
        s_dic = defaultdict(int) # dd with value being integers
        t_dic = defaultdict(int) 

        # key: letter, value: number of occurence 
        for x in s:
            s_dic[x] += 1
        
        for x in t:
            t_dic[x] += 1
            
        return s_dic == t_dic # compare both key and value


# If I print these two defaultdict,  
# 
# ![image.png](attachment:image.png)

# 时间复杂度：$O(M + N)$, where M = len(s), N = len(t)

# ## LC349. Intersection of two arrays (Easy)

# ![Screenshot 2024-02-05 at 17.36.28.png](<attachment:Screenshot 2024-02-05 at 17.36.28.png>)

# 这道题目，主要要学会使用一种哈希数据结构：**unordered_set**，这个数据结构可以解决很多类似的问题。
# 
# 原因是：(1) 输出结果中的每个元素一定是唯一的，也就是说输出的结果的去重的；  
# （2） 同时可以不考虑输出结果的顺序

# In[6]:


class Solution:
    def intersection(self, nums1: List[int], nums2: List[int]) -> List[int]:
        set1 = set(nums1)
        set2 = set(nums2)
        return list((set1 & set2))


# 这道题也可以用array和dict，但是set是最优解。

# ## LC202. Happy Number (Easy)

# ![Screenshot 2024-02-05 at 17.55.55.png](<attachment:Screenshot 2024-02-05 at 17.55.55.png>)

# 这道题目看上去貌似一道数学问题，其实并不是！
# 
# 题目中说了会**无限循环**，那么也就是说求和的过程中，`sum`会重复出现，这对解题很重要！
# 
# 正如之前的理论基础中所说，当我们遇到了要快速判断一个元素是否出现集合里的时候，就要考虑哈希法了。
# 
# 所以这道题目使用哈希法，来**判断这个`sum`是否重复出现**，如果重复了就是`return false`， 否则一直找到`sum`为1为止。
# 
# 判断`sum`是否重复出现就可以使用`unordered_set`。
# 
# 还有一个难点就是求和的过程，如果对取数值各个位上的单数操作不熟悉的话，做这道题也会比较艰难。
# 

# ### method1: set + get_sum

# In[12]:


class Solution:
    def isHappy(self, n: int) -> bool:
        # method1: set as hashtable
        record = set()
        while True:
            # repeatedly get the sum of every digits of n
            n = self.get_sum(n)

            # if n == 1, happy number
            if n == 1:
                return True

            # if n has appeared before, then it means that it loops endlessly in a cycle 
            # which does not include 1.
            elif n in record:
                return False
            else:
                record.add(n)

    def get_sum(self, n: int) -> int:
        '''returns the sum of squares of the original number'''
        new_num = 0
        while n: # n!= 0
            n, r = divmod(n, 10)  # returns (商，余数)， r是n的个位数
            new_num += r**2
        return new_num


# **Remark：关于`get_sum` function**
# 
# - Inside the loop, the `divmod(n, 10)` function is used to divide $n$ by $10$. The result of divmod is a tuple where the first element is the **quotient** ($n$ 的前几位) and the second element is the **remainder** (the last digit of $n$). 这里的目的是**effectively separating the last digit from the rest of the number**. 
# 
# - 然后继续对remainder重复此操作，一位一位的separate，故而要用**while loop**。注意while loop的终止条件是`n = 0`, 说明$n$已经是个位数了，不需要继续separate。（下面的例子可以验证）

# In[10]:


print(divmod(129, 10)) 
print(divmod(12, 10))
print(divmod(1, 10)) # while loop


# ### method2: set + convert to str

# In[15]:


class Solution:
    def isHappy(self, n: int) -> bool:
        # method2: set + convert to str
        record = set()
        record.add(n)
        
        while True:
            # 思路还是去计算new_num, 看有没有重复/死循环
            new_num = 0
            for number in str(n):
                new_num += int(number) ** 2
            n = new_num
            
            # 判断
            if n == 1:
                return True
            if n in record:
                return False
            else: 
                record.add(new_num)


# In[16]:


class Solution:
    def isHappy(self, n: int) -> bool:
        # method2: set + convert to str  写法2
        record = set()

        while n not in record:
            record.add(n)
            # 计算new_num
            new_num = 0
            for number in str(n):
                new_num += int(number)**2
            n = new_num

            # 判断
            if new_num == 1:
                return True
            else: # 如果new_num不是1，将n赋值，然后再次进入while loop判断 
                n = new_num  

        # 如果new_num不是1，while loop也进不去，说明n is in record, return False
        return False
            


# In[14]:


# remark: str(n)
n = 129
str(n)
for i in str(n):
    print(i) # print every character in n as a string


# ### method3: array as hashtable
# 
# 写法跟set完全一样

# In[17]:


class Solution:
    def isHappy(self, n: int) -> bool:
        # method3: array as hashtable
        record = list()

        while n not in record:
            record.append(n)   # 唯一不同是set和array添加的语句
            # 计算new_num
            new_num = 0
            for number in str(n):
                new_num += int(number)**2
            n = new_num

            # 判断
            if new_num == 1:
                return True
            else: 
                n = new_num 
                
        return False
            


# ## LC1. Two Sum (Easy)

# ![image.png](attachment:image.png)

# **思路分析**
# 
# **Q1: 为什么要用哈希表？**
# 判断元素是否在集合中出现过，第一反应是哈希法，或者用哈希结构作处理。
# 
# 对于这道题，例如：`nums = [2, 7, 3, 6]`, `target = 9`, 如果我现在遍历到`3`了，我们就想看看 `target - 3` 是不是在之前遍历过的数字中。如果是，那么我们就找到了满足条件的一对数，他们相加等于 `9`。
# 
# **Q2: 哈希表是用来存放什么的？**
# 
# <span style="color:red"><u>**hashtable**</u>来存放<u>**遍历过的元素**</u>。</span>
# 

# **Q2: 用什么结构来存放遍历过的元素？**
# 
# 用<span style="color:red">**Dictionary**</span>。
# 
# **Q3: 为什么让元素当key，让index当value呢？**
# 
# 因为我们想要查找某个**元素**是否出现过。Dictionary就是能在$O(1)$的时间，快速的查找key是否出现过。而且还能找到该数在原来数组中的index，符合题目的要求。下图是一个`nums`的例子。
# 

# ![image.png](attachment:image.png)

# 具体的操作过程举例：

# ![image.png](attachment:image.png)

# In[21]:


class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        # method1: dict as hashtable
        # seen记录已经遍历过的元素及其位置
        seen = dict()

        for index, number in enumerate(nums):
            s = target - number
            # 我们要查找s是否在seen中出现过
            if s in seen.keys():
                return [seen[s], index]
            else:
                # 如果没有找到匹配对，那么就把访问过的元素和下标都加入到seen中
                seen[number] = index


# In[18]:


# remark: enumerate 用法
nums = [2,7,11,15]
for index, value in enumerate(nums):
    print(index, value)


# ### method2: set as hashtable
# 思路跟dict一模一样，就是用了`nums.index(s)`来找某个数`s`对应的下标，相当于讨巧了，所以省略了把原数组下标作为dictionary的value存放的步骤。

# In[ ]:


class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        # method2: set as hashtable
        # seen记录已经遍历过的元素
        seen = set()

        for index, number in enumerate(nums):
            s = target - number
            # 我们要查找s是否在seen中出现过
            if s in seen:
                # s 在nums中的position怎么找？因为现在没有dictionary来存放value了
                # nums.index(s)
                return [nums.index(s), index] 
            else:
                # 如果没有找到匹配对，那么就把访问过的元素都加入到seen中
                seen.add(number)


# In[23]:


# remark
nums = [2,7,11,15]
nums.index(11)


# 时间复杂度：$O(N)$
# (查找元素是否在dict/set中都是$O(1)$)
# 
# 空间复杂度：$O(N)$
# 

# In[ ]:





# In[ ]:


#jupyter nbconvert /Users/xingqitian/Desktop/Python/Leetcode/Ch3_HashTable.ipynb --to html

