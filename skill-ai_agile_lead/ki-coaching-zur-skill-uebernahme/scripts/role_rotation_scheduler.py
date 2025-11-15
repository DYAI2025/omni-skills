#!/usr/bin/env python3
# Role Rotation Scheduler for Agile Teams
import sys
import argparse
import itertools

ROLES = ["Architect", "Craftsman", "Critic"]


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--team", required=True, help="Kommagetrennte Liste von Namen")
    p.add_argument("--sprints", type=int, required=True)
    p.add_argument("--start", type=int, default=0, help="Startindex im Team für Architect")
    args = p.parse_args()

    team = [t.strip() for t in args.team.split(",") if t.strip()]
    if len(team) < len(ROLES):
        print("[Rotate] Mind. 3 Teammitglieder benötigt.", file=sys.stderr)
        sys.exit(1)

    print("sprint,Architect,Craftsman,Critic")
    idx = args.start % len(team)
    ring = itertools.cycle(range(len(team)))
    for _ in range(idx):
        next(ring)

    for s in range(1, args.sprints + 1):
        order = [None] * 3
        for i in range(3):
            order[i] = team[next(ring)]
        print(f"{s},{order[0]},{order[1]},{order[2]}")


if __name__ == "__main__":
    main()
