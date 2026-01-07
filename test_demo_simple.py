"""Simple demo test script."""
import asyncio
import httpx

async def quick_test():
    """Quick test of the fixed demo."""
    print("\n" + "="*60)
    print("TESTING FIXED DEMO")
    print("="*60)
    
    async with httpx.AsyncClient(follow_redirects=False, timeout=30.0) as client:
        # Test login
        print("\n[1] Testing login...")
        try:
            response = await client.post(
                "http://localhost:8000/api/login",
                data={"username": "test_user"},
                follow_redirects=False
            )
            if response.status_code == 302:
                location = response.headers.get("location", "")
                exam_id = location.split("/api/exam/")[1].split("/")[0] if "/api/exam/" in location else None
                print(f"   [OK] Login successful! Exam ID: {exam_id}")
                
                # Test getting questions
                print("\n[2] Testing question page...")
                q_response = await client.get(f"http://localhost:8000/api/exam/{exam_id}")
                if q_response.status_code == 200:
                    content = q_response.text
                    # Check for different question types
                    has_data_structures = "data structures" in content.lower() or "arrays" in content.lower()
                    has_big_o = "big o" in content.lower() or "complexity" in content.lower()
                    has_recursion = "recursion" in content.lower()
                    
                    print(f"   [OK] Question page loaded")
                    print(f"   - Contains data structures content: {has_data_structures}")
                    print(f"   - Contains Big O content: {has_big_o}")
                    print(f"   - Contains recursion content: {has_recursion}")
                    
                    # Check question number
                    if "Question 1" in content:
                        print(f"   [OK] Question 1 detected")
                    elif "Question 2" in content:
                        print(f"   [OK] Question 2 detected")
                    elif "Question 3" in content:
                        print(f"   [OK] Question 3 detected")
                else:
                    print(f"   [ERROR] Failed to load question page: {q_response.status_code}")
            else:
                print(f"   [ERROR] Login failed: {response.status_code}")
        except Exception as e:
            print(f"   [ERROR] Test failed: {e}")
    
    print("\n" + "="*60)
    print("DEMO TEST COMPLETE")
    print("="*60)
    print("\nOpen http://localhost:8000 in your browser to try the full demo!")
    print("You should now see:")
    print("  - 3 DIFFERENT questions (one at a time)")
    print("  - No API key errors")
    print("  - Working grading without errors\n")

if __name__ == "__main__":
    asyncio.run(quick_test())

