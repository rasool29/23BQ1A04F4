# Stage 1

## Priority Inbox: System Design and Approach

### Objective
The goal is to efficiently filter and display the top 'n' (10) most important unread notifications from a high-volume data stream without relying on database queries. Priority is determined by a combined metric of Notification Type (Weight) and Recency (Timestamp).

### Priority Logic
Weights are statically assigned based on the business requirements:
1.  **Placement** = Weight 3 (Highest)
2.  **Result** = Weight 2
3.  **Event** = Weight 1 (Lowest)

If two notifications have the exact same weight, the timestamp acts as the secondary determining factor, where newer timestamps have higher priority.

### Algorithmic Approach: The Min-Heap
To efficiently maintain the Top 10 notifications as new data streams in, I implemented a **Min-Heap (Priority Queue)** data structure. 

**Why a Min-Heap?**
If we were to sort the entire list of notifications every time a new one arrived, the time complexity would be `O(N log N)`, which is highly inefficient for a massive, continuously growing dataset. 

By using a Min-Heap capped at a size of `K` (where K = 10):
1.  The heap maintains the *smallest* (lowest priority) element of our top 10 at the root node.
2.  As a new notification arrives, its priority is compared to the root node in `O(1)` time.
3.  If the new notification has a higher priority than the root, we perform a `pop-and-push` (heap replace) operation, which takes `O(log K)` time.
4.  If the new notification has a lower priority, it is instantly discarded.

**Efficiency:**
This approach reduces the time complexity from `O(N log N)` to **`O(N log K)`**. Because K (10) is a small constant, `log 10` is essentially a constant time operation. Therefore, the overall time complexity of processing the stream is effectively **`O(N)`**, making it highly scalable and performant for real-time notification streams.
