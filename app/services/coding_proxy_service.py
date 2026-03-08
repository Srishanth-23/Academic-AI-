import httpx
from fastapi import HTTPException
from collections import defaultdict

async def fetch_leetcode_stats(username: str):
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            # Try the unofficial REST API first
            profile_response = await client.get(
                f"https://alfa-leetcode-api.onrender.com/{username}", timeout=25.0
            )
            calendar_response = await client.get(
                f"https://alfa-leetcode-api.onrender.com/{username}/calendar", timeout=25.0
            )

            if profile_response.status_code == 200 and "errors" not in profile_response.json():
                profile_data = profile_response.json()
                calendar_data = calendar_response.json() if calendar_response.status_code == 200 else {}

                heatmap = calendar_data.get("submissionCalendar", "{}")
                import json
                if isinstance(heatmap, str):
                    try:
                        heatmap = json.loads(heatmap)
                    except:
                        heatmap = {}

                def safe_int(val, default=0) -> int:
                    try: return int(val)
                    except: return default

                return {
                    "platform": "leetcode",
                    "username": username,
                    "ranking": safe_int(profile_data.get("ranking", 0)),
                    "rating": safe_int(profile_data.get("contributionPoint", 0)),
                    "reputation": safe_int(profile_data.get("reputation", 0)),
                    "totalSolved": safe_int(profile_data.get("totalSolved", 0)),
                    "easySolved": safe_int(profile_data.get("easySolved", 0)),
                    "mediumSolved": safe_int(profile_data.get("mediumSolved", 0)),
                    "hardSolved": safe_int(profile_data.get("hardSolved", 0)),
                    "totalQuestions": safe_int(profile_data.get("totalQuestions", 3000)),
                    "heatmap": heatmap
                }

            # === Fallback: direct LeetCode GraphQL API ===
            gql_query = """
            {
              matchedUser(username: "%s") {
                username
                submitStats: submitStatsGlobal {
                  acSubmissionNum {
                    difficulty
                    count
                  }
                }
                profile { ranking reputation }
              }
            }
            """ % username
            gql_resp = await client.post(
                "https://leetcode.com/graphql",
                json={"query": gql_query},
                headers={"Content-Type": "application/json", "Referer": "https://leetcode.com"},
                timeout=25.0
            )
            if gql_resp.status_code == 200:
                gql_data = gql_resp.json()
                matched = gql_data.get("data", {}).get("matchedUser")
                if matched:
                    sub_stats = matched.get("submitStats", {}).get("acSubmissionNum", [])
                    total = easy = medium = hard = 0
                    for s in sub_stats:
                        d, c = s.get("difficulty",""), int(s.get("count",0))
                        if d == "All": total = c
                        elif d == "Easy": easy = c
                        elif d == "Medium": medium = c
                        elif d == "Hard": hard = c
                    profile = matched.get("profile", {})
                    return {
                        "platform": "leetcode",
                        "username": username,
                        "ranking": int(profile.get("ranking", 0) or 0),
                        "rating": int(profile.get("reputation", 0) or 0),
                        "reputation": int(profile.get("reputation", 0) or 0),
                        "totalSolved": total, "easySolved": easy,
                        "mediumSolved": medium, "hardSolved": hard,
                        "totalQuestions": 3000, "heatmap": {}
                    }

            raise HTTPException(status_code=404, detail="LeetCode user not found or APIs unavailable. Try again later.")
        except httpx.RequestError as e:
            raise HTTPException(status_code=503, detail=f"Failed to reach LeetCode APIs: {str(e)}")


async def fetch_codechef_stats(username: str):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"https://codechef-api.vercel.app/handle/{username}", timeout=10.0)
            if response.status_code != 200:
                 raise HTTPException(status_code=404, detail="CodeChef user not found")
                 
            data = response.json()
            if not data.get("success", False):
                 raise HTTPException(status_code=404, detail="CodeChef user not found")
                 
            # Convert heatmap array into a dictionary of timestamp mappings to counts
            heatmap = {}
            if "heatMap" in data:
                # CodeChef API usually returns an array of {date: "YYYY-MM-DD", value: count}
                import datetime
                for item in data["heatMap"]:
                    try:
                        date_obj = datetime.datetime.strptime(item["date"], "%Y-%m-%d")
                        timestamp = str(int(date_obj.timestamp()))
                        # Ensure item["value"] is cast to an integer safely
                        val = item.get("value")
                        heatmap[timestamp] = int(val) if val is not None else 0
                    except:
                        pass
            
            # Safely cast stats that might be strings
            def safe_int(val, default=0) -> int:
                try:
                    return int(val)
                except (ValueError, TypeError):
                    return default
                    
            return {
                "platform": "codechef",
                "username": username,
                "ranking": safe_int(data.get("globalRank", 0)),
                "rating": safe_int(data.get("currentRating", 0)),
                "stars": str(data.get("stars", "1★")),
                "totalSolved": safe_int(data.get("fullySolved", {}).get("count", 0)),
                "partiallySolved": safe_int(data.get("partiallySolved", {}).get("count", 0)),
                "heatmap": heatmap
            }
        except httpx.RequestError as e:
            raise HTTPException(status_code=503, detail=f"Failed to communicate with CodeChef API: {str(e)}")


async def fetch_codeforces_stats(username: str):
    async with httpx.AsyncClient() as client:
        try:
            info_response = await client.get(f"https://codeforces.com/api/user.info?handles={username}", timeout=10.0)
            if info_response.status_code != 200 or info_response.json().get("status") != "OK":
                raise HTTPException(status_code=404, detail="CodeForces user not found")
                
            user_info = info_response.json()["result"][0]
            
            status_response = await client.get(f"https://codeforces.com/api/user.status?handle={username}", timeout=15.0)
            submissions = status_response.json().get("result", []) if status_response.status_code == 200 else []
            
            solved_problems = set()
            heatmap: dict[str, int] = {}
            easy = 0
            medium = 0
            hard = 0
            
            import datetime
            for sub in submissions:
                if sub.get("verdict") == "OK":
                    prob = sub.get("problem", {})
                    prob_id = f"{prob.get('contestId')}-{prob.get('index')}"
                    
                    # Track heatmap by day timestamp
                    created = sub.get("creationTimeSeconds")
                    if created:
                        dt = datetime.datetime.fromtimestamp(created)
                        day_ts = str(int(datetime.datetime(dt.year, dt.month, dt.day).timestamp()))
                        heatmap[day_ts] = heatmap.get(day_ts, 0) + 1
                        
                    if prob_id not in solved_problems:
                        solved_problems.add(prob_id)
                        rating = prob.get("rating", 0)
                        if rating == 0:
                            easy = easy + 1  # type: ignore
                        elif rating < 1200:
                            easy = easy + 1  # type: ignore
                        elif rating < 1900:
                            medium = medium + 1  # type: ignore
                        else:
                            hard = hard + 1  # type: ignore

            return {
                 "platform": "codeforces",
                 "username": username,
                 "ranking": user_info.get("maxRating", 0),
                 "rating": user_info.get("rating", 0),
                 "rankName": user_info.get("rank", "unrated"),
                 "maxRankName": user_info.get("maxRank", "unrated"),
                 "totalSolved": len(solved_problems),
                 "easySolved": easy,
                 "mediumSolved": medium,
                 "hardSolved": hard,
                 "heatmap": heatmap
            }
        except httpx.RequestError as e:
             raise HTTPException(status_code=503, detail=f"Failed to communicate with CodeForces API: {str(e)}")
