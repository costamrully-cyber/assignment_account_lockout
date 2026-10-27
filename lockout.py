# Augustine
# Assignment 5 Account lockout

LOCK_LIMIT = 3

events = [
    ("08:00", "amina", "FAIL"),
    ("08:01", "amina", "OK"),
    ("08:02", "brian", "FAIL"),
    ("08:03", "brian", "FAIL"),
    ("08:04", "amina", "FAIL"),
    ("08:05", "brian", "FAIL"),
    ("08:06", "brian", "OK"),
    ("08:07", "cynthia", "FAIL"),
    ("08:08", "cynthia", "FAIL"),
    ("08:09", "cynthia", "OK"),
    ("08:10", "cynthia", "FAIL"),
    ("08:11", "dan", "FAIL"),
    ("08:12", "amina", "FAIL"),
    ("08:13", "cynthia", "FAIL"),
    ("08:14", "dan", "FAIL"),
    ("08:15", "amina", "OK"),
    ("08:16", "dan", "FAIL"),
    ("08:17", "cynthia", "FAIL"),
    ("08:18", "dan", "OK"),
    ("08:19", "esther", "OK"),
    ]

def get_users(events):
    users = []
    for t, u, s in events:
        if u not in users:
            users.append(u)
    return users

def check_user(user, events, limit=LOCK_LIMIT):
    total = 0
    run = 0
    locked = False
    lock_time = "-"
    blocked = 0
    for t, u, s in events:
        if u == user:
            if locked == True:
                blocked += 1
            elif s == "FAIL":
                total += 1
                run += 1
                if run >= limit:
                    locked = True
                    lock_time = t
            else:
                run = 0
    return (user, total, locked, lock_time, blocked)

def check_all(events, limit=LOCK_LIMIT):
    results = []
    for u in get_users(events):
        results.append(check_user(u, events, limit))
    return results

# main part
print("==Per user==")
results = check_all(events)
for user, total, locked, lock_time, blocked in results:
    if locked == True:
        print(user, ":", total, "fails, LOCKED at", lock_time, "blocked:", blocked)
    else:
        print(user, ":", total, "fails, OK")

print("==Locked users==")
locked_users = [(user, lock_time) for user, total, locked, lock_time, blocked in results if locked == True]
print(locked_users)

print("==Total blocked==")
total_blocked = 0
for user, total, locked, lock_time, blocked in results:
    total_blocked += blocked
print(total_blocked)

print("==Most fails==")
rank = []
for user, total, locked, lock_time, blocked in results:
    rank.append((total, user))
rank.sort(reverse=True)
print(rank[0][1], "with", rank[0][0])

print("==Limit 2==")
for user, total, locked, lock_time, blocked in check_all(events, 2):
    if locked == True:
        print(user, "LOCKED at", lock_time)

print("==Limit 4==")
found = False
for user, total, locked, lock_time, blocked in check_all(events, 4):
    if locked == True:
        print(user, "LOCKED at", lock_time)
        found = True
if found == False:
    print("no account locked")