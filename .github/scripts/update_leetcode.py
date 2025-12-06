import requests
import os

# fetch
username = "NguyenTien7"
url = "https://leetcode.com/graphql"
query = """
query userStats($username: String!) {
  userContestRanking(username: $username) {
    rating
    globalRanking
    topPercentage
  }
  matchedUser(username: $username) {
    submitStats: submitStatsGlobal {
      acSubmissionNum {
        difficulty
        count
      }
    }
  }
}
"""

try:
    response = requests.post(url, json={"query": query, "variables": {"username": username}})
    response.raise_for_status()
    data = response.json()['data']

    # Extract Contest Data
    contest_data = data.get('userContestRanking')
    if contest_data:
        rating = int(contest_data['rating'])
        ranking = contest_data['globalRanking']
        top_percent = f"{contest_data['topPercentage']}%"
    else:
        rating, ranking, top_percent = "N/A", "N/A", "N/A"

    # Extract Solved Problems Data
    matched_user = data.get('matchedUser')
    total_solved = 0
    easy_solved = 0
    medium_solved = 0
    hard_solved = 0

    if matched_user:
        submission_stats = matched_user['submitStats']['acSubmissionNum']
        for stat in submission_stats:
            if stat['difficulty'] == 'All':
                total_solved = stat['count']
            if stat['difficulty'] == 'Easy':
                easy_solved = stat['count']
            if stat['difficulty'] == 'Medium':
                medium_solved = stat['count']
            if stat['difficulty'] == 'Hard':
                hard_solved = stat['count']

except Exception as e:
    print(f"Error fetching data: {e}")
    rating, ranking, top_percent = 0, 0, 0
    total_solved = 0

# Generate svg (output) - simple template
svg_content = f"""
<svg width="500" height="140" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#2c3e50;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#4ca1af;stop-opacity:1" />
    </linearGradient>
    <style>
      .header {{ font-family: 'Segoe UI', Arial, sans-serif; font-size: 14px; fill: #dfe6e9; font-weight: bold; }}
      .stat-num {{ font-family: 'Segoe UI', Arial, sans-serif; font-size: 32px; fill: #f1c40f; font-weight: bold; }}
      .sub-text {{ font-family: 'Segoe UI', Arial, sans-serif; font-size: 12px; fill: #dfe6e9; }}
      .solved-num {{ font-family: 'Segoe UI', Arial, sans-serif; font-size: 32px; fill: #2ecc71; font-weight: bold; }}
    </style>
  </defs>
  
  <!-- Background -->
  <rect x="5" y="5" width="490" height="130" rx="15" ry="15" fill="url(#grad)" stroke="white" stroke-width="2"/>
  
  <!-- Vertical divider -->
  <line x1="250" y1="20" x2="250" y2="120" stroke="white" stroke-width="1" stroke-opacity="0.3"/>

  <!-- Left col: Rating -->
  <text x="30" y="35" class="header">CONTEST RATING</text>
  <text x="30" y="80" class="stat-num">{rating}</text>
  <text x="30" y="105" class="sub-text">Global Rank: {ranking}</text>
  <text x="30" y="120" class="sub-text">Top {top_percent}</text>

  <!-- Right col: Problems solved -->
  <text x="270" y="35" class="header">PROBLEMS SOLVED</text>
  <text x="270" y="80" class="solved-num">{total_solved}</text>
  
  <!-- Breakdown (Easy/Med/Hard) -->
  <text x="270" y="105" font-family="'Segoe UI', Arial, sans-serif" font-size="12" fill="#dfe6e9">
    <tspan fill="#00b8a3" font-weight="bold">Easy:</tspan> {easy_solved}
    <tspan fill="#ffc01e" font-weight="bold" dx="15">Med:</tspan> {medium_solved}
    <tspan fill="#ef4743" font-weight="bold" dx="15">Hard:</tspan> {hard_solved}
  </text>
</svg>
"""

# save
with open("leetcode_stats.svg", "w") as f:
    f.write(svg_content)