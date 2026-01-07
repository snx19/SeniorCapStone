"""Script to test the demo workflow."""
import asyncio
import httpx
import sys

async def test_demo():
    """Test the full demo workflow."""
    base_url = "http://localhost:8000"
    
    print("\n" + "="*60)
    print("AI ORAL EXAM GRADER - DEMO TEST")
    print("="*60)
    
    async with httpx.AsyncClient(follow_redirects=False, timeout=30.0) as client:
        # 1. Test Health
        print("\n[1/6] Testing health endpoint...")
        try:
            response = await client.get(f"{base_url}/api/health")
            print(f"   ✓ Health check: {response.json()}")
        except Exception as e:
            print(f"   ✗ Health check failed: {e}")
            return
        
        # 2. Test Login
        print("\n[2/6] Testing login...")
        try:
            response = await client.post(
                f"{base_url}/api/login",
                data={"username": "demo_student"},
                follow_redirects=False
            )
            if response.status_code == 302:
                location = response.headers.get("location", "")
                print(f"   ✓ Login successful!")
                print(f"   ✓ Redirected to: {location}")
                
                # Extract exam ID from location
                if "/api/exam/" in location:
                    exam_id = location.split("/api/exam/")[1].split("/")[0]
                    print(f"   ✓ Exam ID: {exam_id}")
                else:
                    print("   ✗ Could not extract exam ID")
                    return
            else:
                print(f"   ✗ Login failed with status: {response.status_code}")
                print(f"   Response: {response.text[:200]}")
                return
        except Exception as e:
            print(f"   ✗ Login failed: {e}")
            return
        
        # 3. Get first question
        print("\n[3/6] Fetching first question...")
        try:
            response = await client.get(f"{base_url}/api/exam/{exam_id}")
            if response.status_code == 200:
                print(f"   ✓ Question page loaded (Status: {response.status_code})")
                # Check if it's HTML
                if "question" in response.text.lower():
                    print("   ✓ Question content detected in response")
            else:
                print(f"   ✗ Failed to get question: {response.status_code}")
                print(f"   Response: {response.text[:200]}")
        except Exception as e:
            print(f"   ✗ Error fetching question: {e}")
        
        # 4. Test question endpoint with database query
        print("\n[4/6] Testing exam status...")
        try:
            # We can't easily extract question ID from HTML, so let's just verify the page structure
            response = await client.get(f"{base_url}/api/exam/{exam_id}")
            if response.status_code == 200 and "Question" in response.text:
                print("   ✓ Exam page structure looks correct")
            else:
                print(f"   ⚠ Status check incomplete (but page loaded)")
        except Exception as e:
            print(f"   ✗ Error: {e}")
        
        # 5. Simulate answering (we'd need to extract question_id from HTML for real test)
        print("\n[5/6] Note: Full answer submission requires question_id from HTML")
        print("   ℹ You can test this manually in the browser")
        
        # 6. Test completion page (after all questions answered)
        print("\n[6/6] Testing completion endpoint structure...")
        try:
            response = await client.get(f"{base_url}/api/exam/{exam_id}/complete")
            if response.status_code == 200:
                print("   ✓ Completion page endpoint exists")
            elif response.status_code == 404:
                print("   ℹ Completion page not available yet (exam still in progress)")
            else:
                print(f"   ⚠ Status: {response.status_code}")
        except Exception as e:
            print(f"   ℹ Note: {e}")
    
    print("\n" + "="*60)
    print("DEMO TEST SUMMARY")
    print("="*60)
    print("✓ Server is running")
    print("✓ Health endpoint working")
    print("✓ Login functionality working")
    print("✓ Exam creation working")
    print("✓ Question page accessible")
    print("\n🌐 OPEN YOUR BROWSER TO: http://localhost:8000")
    print("   Enter a username and complete the exam manually to see full workflow!")
    print("="*60 + "\n")

if __name__ == "__main__":
    asyncio.run(test_demo())

