import json

json_str = """
{
  "문제": "문제....",
  "문항": "문항....",
  "정답번호": 3,
  "해설": "해설...."
}
"""

print(json.loads(json_str))