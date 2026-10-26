# -*- coding: utf-8 -*-
"""Turn off Vercel Deployment Protection for the higher-heights project so the site is public."""
import json, os, urllib.request, urllib.error

AUTH = os.path.expanduser(os.path.join(os.environ["APPDATA"], "com.vercel.cli", "Data", "auth.json"))
TOKEN = json.load(open(AUTH))["token"]
PROJ = "prj_th5hWVuZTeIhNtqVB46Wg7GE3RVw"
TEAM = "team_FFzZ7j2gPKEvVuXnCHzj7eW1"
BASE = "https://api.vercel.com"


def call(method, path, body=None):
    url = f"{BASE}{path}"
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", f"Bearer {TOKEN}")
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.status, json.loads(r.read().decode() or "{}")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:400]


st, proj = call("GET", f"/v9/projects/{PROJ}?teamId={TEAM}")
print("GET project:", st)
for k in ("name", "ssoProtection", "passwordProtection", "publicSource", "targets"):
    print(f"   {k}: {proj.get(k) if isinstance(proj, dict) else proj}")

st, res = call("PATCH", f"/v9/projects/{PROJ}?teamId={TEAM}",
               {"ssoProtection": None, "passwordProtection": None})
print("PATCH protection off:", st)
if st != 200:
    print("   ", res)
else:
    print("   ssoProtection now:", res.get("ssoProtection"))
    print("   passwordProtection now:", res.get("passwordProtection"))
