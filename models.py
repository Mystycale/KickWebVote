import time
import uuid
from collections import Counter, defaultdict
from typing import Dict, List, Optional
from datetime import datetime


class Votation:
    def __init__(
        self,
        poll_id: str,
        question: str,
        options: List[str],
        max_votes_per_user: int,
        channel: str,
        initiated_by: str = "web",
    ):
        self.poll_id = poll_id
        self.question = question
        self.options = list(options)
        self.max_votes_per_user = max(1, int(max_votes_per_user))
        self.channel = channel
        self.initiated_by = initiated_by
        self.started_at = time.time()
        self.started_at_iso = datetime.now().isoformat()
        self.ended_at_iso: Optional[str] = None
        self.active = True
        # nick -> list of option indices (1-based)
        self.votes_by_kick: Dict[str, List[int]] = {}
        self.counts: Counter = Counter()
        # ordered list of recent voters for live display
        self.voter_order: List[str] = []

    # ------------------------------------------------------------------
    def try_vote(self, kick_nick: str, option_index: int) -> bool:
        if not self.active:
            return False
        if not (1 <= option_index <= len(self.options)):
            return False
        user_votes = self.votes_by_kick.get(kick_nick, [])
        if len(user_votes) >= self.max_votes_per_user:
            return False
        if option_index in user_votes:
            return False
        user_votes.append(option_index)
        self.votes_by_kick[kick_nick] = user_votes
        self.counts[option_index] += 1
        if kick_nick not in self.voter_order:
            self.voter_order.append(kick_nick)
        return True

    def finalize(self):
        self.active = False
        self.ended_at_iso = datetime.now().isoformat()

    # ------------------------------------------------------------------
    def counts_dict(self) -> Dict[int, int]:
        return {i + 1: self.counts.get(i + 1, 0) for i in range(len(self.options))}

    def voters_by_option(self) -> Dict[int, List[str]]:
        byopt: Dict[int, List[str]] = defaultdict(list)
        for nick, opts in self.votes_by_kick.items():
            for opt in opts:
                byopt[opt].append(nick)
        return dict(byopt)

    def total_votes(self) -> int:
        return sum(self.counts.values())

    def recent_voters(self, n: int = 5) -> List[dict]:
        latest = self.voter_order[-n:][::-1]
        return [{"username": v} for v in latest]

    # ------------------------------------------------------------------
    def to_ws_payload(self) -> dict:
        return {
            "type": "vote_update",
            "poll_id": self.poll_id,
            "question": self.question,
            "options": self.options,
            "counts": self.counts_dict(),
            "total_votes": self.total_votes(),
            "active": self.active,
            "channel": self.channel,
            "max_votes_per_user": self.max_votes_per_user,
        }

    def to_history_dict(self) -> dict:
        voters_by_opt = self.voters_by_option()
        counts = self.counts_dict()
        total = self.total_votes()
        options_summary = []
        for i, opt in enumerate(self.options):
            idx = i + 1
            cnt = counts.get(idx, 0)
            pct = round((cnt / total * 100) if total else 0, 1)
            options_summary.append(
                {
                    "index": idx,
                    "label": opt,
                    "votes": cnt,
                    "percent": pct,
                    "voters": voters_by_opt.get(idx, []),
                }
            )
        return {
            "poll_id": self.poll_id,
            "question": self.question,
            "options": self.options,
            "channel": self.channel,
            "max_votes_per_user": self.max_votes_per_user,
            "started_at": self.started_at_iso,
            "ended_at": self.ended_at_iso,
            "total_votes": total,
            "counts": counts,
            "options_summary": options_summary,
            "voters_by_option": {
                str(k): v for k, v in voters_by_opt.items()
            },
        }
