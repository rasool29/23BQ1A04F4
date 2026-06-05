import requests
import heapq
from datetime import datetime

# Define the weights based on the problem statement
WEIGHTS = {
    "Placement": 3,
    "Result": 2,
    "Event": 1
}

def fetch_notifications(api_url, token):
    """Fetches notifications from the protected API."""
    # Note: Replace 'Bearer' with the correct auth scheme if they gave you an API Key instead
    headers = {"Authorization": f"Bearer {token}"} 
    
    try:
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            return response.json().get("notifications", [])
        else:
            print(f"Failed to fetch data. Status Code: {response.status_code}")
            return []
    except Exception as e:
        print(f"Error connecting to API: {e}")
        return []

def get_top_n_notifications(notifications, n=10):
    """
    Uses a Min-Heap to efficiently find the top N notifications.
    We keep the heap size at exactly N. 
    """
    min_heap = []
    counter = 0  # Tie-breaker for heap to prevent dictionary comparison errors

    for notif in notifications:
        notif_type = notif.get("Type")
        weight = WEIGHTS.get(notif_type, 0) # Default weight 0 for unknown types
        
        # Parse the timestamp string into a datetime object for comparison
        time_str = notif.get("Timestamp")
        try:
            dt = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            continue # Skip corrupted dates

        # Tuple structure: (weight, datetime, counter, notification_dictionary)
        # Python's heap compares the first element (weight), then second (datetime)
        heap_item = (weight, dt, counter, notif)
        counter += 1

        if len(min_heap) < n:
            # If heap has less than N items, just push
            heapq.heappush(min_heap, heap_item)
        else:
            # If heap is full, compare new item with the smallest item in the heap (min_heap[0])
            # min_heap[0][:2] extracts just the (weight, datetime) of the smallest item
            if heap_item[:2] > min_heap[0][:2]:
                # If new item is strictly greater, pop the smallest and push the new one
                heapq.heapreplace(min_heap, heap_item)

    # Extract the actual notification dictionaries from the heap
    top_notifications = [item[3] for item in min_heap]
    
    # The heap gives us the top 10, but they aren't perfectly sorted descending yet.
    # Sort them one final time for display (Highest weight and newest date first)
    top_notifications.sort(
        key=lambda x: (WEIGHTS.get(x["Type"], 0), datetime.strptime(x["Timestamp"], "%Y-%m-%d %H:%M:%S")), 
        reverse=True
    )
    
    return top_notifications

if __name__ == "__main__":
    # --- CONFIGURATION ---
    API_URL = "http://4.224.186.213/evaluation-service/notifications"
    
    # IMPORTANT: Put the token or API key they provided you here!
    YOUR_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJNYXBDbGFpbXMiOnsiYXVkIjoiaHR0cDovLzIwLjI0NC41Ni4xNDQvZXZhbHVhdGlvbi1zZXJ2aWNlIiwiZW1haWwiOiJzaGFpa3Jhc29vbDI5MTBAZ21haWwuY29tIiwiZXhwIjoxNzgwNjQxNTMwLCJpYXQiOjE3ODA2NDA2MzAsImlzcyI6IkFmZm9yZCBNZWRpY2FsIFRlY2hub2xvZ2llcyBQcml2YXRlIExpbWl0ZWQiLCJqdGkiOiI4NjA4NGI3YS01ODM4LTQ3NGUtYWE0MS0wNWM1ZGExYjVlOTYiLCJsb2NhbGUiOiJlbi1JTiIsIm5hbWUiOiJzaGFpayByYXNvb2wiLCJzdWIiOiJjZjg2NmM1OC00NDFjLTRjZTAtOWIyNC1lNjdkNDc4NmJjOWEifSwiZW1haWwiOiJzaGFpa3Jhc29vbDI5MTBAZ21haWwuY29tIiwibmFtZSI6InNoYWlrIHJhc29vbCIsInJvbGxObyI6IjIzYnExYTA0ZjQiLCJhY2Nlc3NDb2RlIjoiUVFkRVl5IiwiY2xpZW50SUQiOiJjZjg2NmM1OC00NDFjLTRjZTAtOWIyNC1lNjdkNDc4NmJjOWEiLCJjbGllbnRTZWNyZXQiOiJxZHRuWFprV3JIRkRYbWZuIn0.F28pjMQkQZ0TN0K8w4OEHnzO64sP2-5wp9yOhNNl6CU" 
    
    print("Fetching notifications from API...")
    raw_notifications = fetch_notifications(API_URL, YOUR_TOKEN)
    
    if raw_notifications:
        print(f"Successfully fetched {len(raw_notifications)} notifications.")
        top_10 = get_top_n_notifications(raw_notifications, n=10)
        
        print("\n" + "="*50)
        print(" TOP 10 PRIORITY INBOX ".center(50, "="))
        print("="*50)
        
        for i, n in enumerate(top_10, 1):
            print(f"{i:2}. [{n['Type'].upper()}] - {n['Message']}")
            print(f"    Time: {n['Timestamp']} | ID: {n['ID']}\n")
    else:
        print("No notifications processed.")
