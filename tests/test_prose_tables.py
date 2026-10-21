"""
That a prose table says what the record that owns it says.

**Considered on 2026-08-09 and deliberately not written; written on
2026-10-21.** `IDEAS.md`, *Technical debt*, turned it down for two reasons: a
parser over prose breaks on every rewording, and a test that guards copies
leaves the copies in place. It named what would make it worth writing, figures
creeping back into the navigational documents or a third document that needs
them, and both had happened. And the paragraph that once went stale where no
test could reach it, the scoreboard's ratios (`STATUS.md`, its erratum of
2026-08-29), has been recomputed by hand in every thread since.

So this reads no free prose. It reads tables and citations, which already carry
their anchor, the row's name, and it reads each row in the record that owns it.
A rewording that keeps a table keeps the test. A table whose shape changes
fails loudly instead of passing on nothing, because every check also requires
that it read what it expects to read.

WHAT IS CHECKED HERE, AND WHY.
  * The scoreboard of `STATUS.md`, *The signed rows, and how they came out*:
    each thread's row adds up, the total row is their sum, the heading counts
    the signed rows in words, the named lists hold as many of each thread's
    rows as its row says, and the four ratios under the table are the table's.
  * The same scoreboard against the records. Each row named there carries the
    verdict its own record gives it, the third convention stated above the
    table, and each thread's held, refuted, dead-zone and unadjudicated rows
    are its record's, in both directions.
  * The verdict table of every FINDINGS that has one: each row's verdict and
    thin label are its record's, and where the verdict closes the row, every
    figure in bold before it is printed by the record's row, at the places the
    table gives it.
  * Every verdict cited in parentheses, `(`K-b` refuted)` or `(`J-b` holds,
    thin)`, in the documents that copy verdicts rather than own them.
  * That each check has teeth, on copies of the documents: a total left
    behind, a heading not recounted, a ratio not recomputed, a verdict flipped,
    a thin label added and a figure off by a digit are each caught.

WHAT IS NOT, AND WHY.
  * A figure in free prose. Looked up anywhere in the records it proves
    nothing, because their numeric leaves print every two-place value between
    0 and 1, nearly every three-place one and most four-place ones. Bound to
    the record that owns it, it needs an anchor beside every figure or a list
    kept by hand, which is the parser over prose the item turned down.
  * The pairwise threads, `P` and `B`, have no verdict table: `FINDINGS2.md`
    and `FINDINGS3.md` adjudicate them in prose. Their rows are read on the
    scoreboard and in citations.
  * The signed plans and `PREDICTION.md`. A check that could fail on one of
    them would ask for an edit to a signed file.

A FAILURE IS NOT FIXED BY EDITING THE RECORD, which is what ran. If a table or
a citation disagrees with it, the prose is wrong: a FINDINGS takes a dated
erratum in place, and the copy is corrected in the commit that finds it. A new
thread adds a line to `THREADS`, and one to `TABLES` if its FINDINGS has a
verdict table. The checks below fail until it does.
"""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

STATUS = "STATUS.md"
SCOREBOARD = "The signed rows, and how they came out"

# Where each thread's record keeps its rows: the record, and the keys down to
# the object whose keys are the rows, written `X-y` or `X_y`.
THREADS = {
    "Q": ("results3/order_metrics.json", ("predictions",)),
    "S": ("results3/order_metrics_corpus.json", ("predictions",)),
    "R": ("results3/rank_transfer.json", ("predictions",)),
    "C": ("results3/order_metrics_touched.json", ("predictions",)),
    "D": ("results3/order_metrics_rules.json", ("predictions",)),
    "P": ("results3/declared_order.json", ()),
    "B": ("results3/declared_order_1600.json", ()),
    "A": ("results_sensitivity/sweep.json", ("rows",)),
    "I": ("results_ilp/compare.json", ("rows",)),
    "U": ("results_reuse/score.json", ("verdicts",)),
    "F": ("results_fidelity/score.json", ("verdicts",)),
    "W": ("results_edges/score.json", ("verdicts",)),
    "L": ("results_primacy/score.json", ("verdicts",)),
    "Y": ("results_why/score.json", ("verdicts",)),
    "E": ("results_authorship/score.json", ("verdicts",)),
    "O": ("results_overlap/score.json", ("verdicts",)),
    "K": ("results_blind/score.json", ("verdicts",)),
    "V": ("results_screen/score.json", ("verdicts",)),
    "H": ("results_bound/score.json", ("verdicts",)),
    "M": ("results_ranking/score.json", ("verdicts",)),
    "T": ("results_students/score.json", ("rows",)),
    "J": ("results_escalations/score.json", ("rows",)),
    "N": ("results_spotcheck/score.json", ("rows",)),
    "Z": ("results_unreached/score.json", ("rows",)),
    "G": ("results_manual/score.json", ("verdicts",)),
}

# Rows a thread's record keeps somewhere else. `P-c`'s record states its verdict
# only in words, in the kill switch Stage C read before Stage D could run.
# `B-d` is read on both surfaces and holds on both; `FINDINGS3.md` §11
# adjudicates it on the space.
ELSEWHERE = {
    "P-c": ("results2/pair_judgement_hidden.json", ("kill_switch",)),
    "B-a": ("results3/edge_direction_1600.json", ("B_a",)),
    "B-d": ("results3/edge_direction_1600.json",
            ("B_d_direction_by_queue_ranking_side", "space")),
}

# The FINDINGS that carry a verdict table, and the threads whose rows it holds.
# By file and not by name, because a name is not unique across the records:
# `FINDINGS_AUDIT.md`'s own predictions are also called `P-a` to `P-g`.
TABLES = {
    "results3/FINDINGS_ORDERS.md": "QSRCD",
    "results_sensitivity/FINDINGS_SENSITIVITY.md": "A",
    "results_ilp/FINDINGS_ILP.md": "I",
    "results_reuse/FINDINGS_REUSE.md": "U",
    "results_fidelity/FINDINGS_FIDELITY.md": "F",
    "results_edges/FINDINGS_EDGES.md": "W",
    "results_primacy/FINDINGS_PRIMACY.md": "L",
    "results_why/FINDINGS_WHY.md": "Y",
    "results_authorship/FINDINGS_AUTHORSHIP.md": "E",
    "results_overlap/FINDINGS_OVERLAP.md": "O",
    "results_blind/FINDINGS_BLIND.md": "K",
    "results_screen/FINDINGS_SCREEN.md": "V",
    "results_bound/FINDINGS_BOUND.md": "H",
    "results_ranking/FINDINGS_RANKING.md": "M",
    "results_students/FINDINGS_STUDENTS.md": "T",
    "results_escalations/FINDINGS_ESCALATIONS.md": "J",
    "results_spotcheck/FINDINGS_SPOTCHECK.md": "N",
    "results_unreached/FINDINGS_UNREACHED.md": "Z",
    "results_manual/FINDINGS_MANUAL.md": "G",
}
PROSE_ONLY = {"P": "results2/FINDINGS2.md", "B": "results3/FINDINGS3.md"}
NOT_TABLES = {
    "results3/FINDINGS_AUDIT.md":
        "its P-a to P-g are the audit's own predictions, not the pairwise thread's",
}

# The documents that copy verdicts rather than own them. The FINDINGS are read
# by their tables instead: a citation there may name a row of another file.
COPIES = ("STATUS.md", "IDEAS.md", "README.md", "CLAUDE.md", "PAIRWISE_WRITEUP.md",
          "ARBITRATION_REPORT.md", "CHAT_SUMMARY.md", "EXTERNAL_REVIEW.md")

# The adjudicated rows whose bands were set on a development set, so that the
# scoreboard's last two ratios leave them out. Transcribed from the paragraph
# under the table, and checked against the marks in the table's thread column.
DEVELOPMENT_SET = frozenset({"Y-a", "Y-b", "Y-c", "Y-d", "V-b", "V-c", "V-d"})

HOLDS, REFUTED, DEAD, NONE, REPORTED = (
    "holds", "refuted", "dead zone", "not adjudicated", "reported")

ROW = re.compile(r"[A-Z]-[a-z]")
WORD = re.compile(r"^[*_`\s]*(holds|hold|held|refuted|neither|no verdict|"
                  r"unadjudicable|reported|not refuted)\b", re.I)
SAID = {"holds": HOLDS, "hold": HOLDS, "held": HOLDS, "refuted": REFUTED,
        "neither": DEAD, "no verdict": NONE, "unadjudicable": NONE,
        "reported": REPORTED, "not refuted": None}
BOLD = re.compile(r"\*\*(.+?)\*\*")
FIGURE = re.compile(r"(?<![\w.`])[+\-−]?\d[\d,]*(?:\.\d+)?")
THIN = re.compile(r"\bthin(?:ly)?\b", re.I)
CITATION = re.compile(
    r"\((?P<rows>`[A-Z]-[a-z]`(?:(?:,| and|, and) `[A-Z]-[a-z]`)*) "
    r"(?P<word>holds|hold|held|refuted)\b(?P<rest>[^)]*)\)")

UNITS = ("zero one two three four five six seven eight nine ten eleven twelve "
         "thirteen fourteen fifteen sixteen seventeen eighteen nineteen").split()
TENS = "- - twenty thirty forty fifty sixty seventy eighty ninety".split()


# ---------------------------------------------------------------- the records

_JSON: dict[str, object] = {}


def record(path: str) -> object:
    if path not in _JSON:
        _JSON[path] = json.loads((REPO / path).read_text())
    return _JSON[path]


def descend(obj: object, keys: tuple[str, ...]) -> object:
    for key in keys:
        obj = obj[key]  # type: ignore[index]
    return obj


def verdict(row: object) -> str | None:
    """The verdict a record's row gives, in the words of the scoreboard.

    Records write it four ways: a `verdict` string, a `holds` or `band_holds`
    flag, `unadjudicable` or `adjudicates: false`, and, for `P-c` alone, a
    sentence that names the row."""
    if not isinstance(row, dict):
        return None
    said = row.get("verdict")
    if isinstance(said, str):
        said = said.lower()
        for start, word in (("holds", HOLDS), ("refuted", REFUTED),
                            ("neither", DEAD)):
            if said.startswith(start):
                return word
        if "not a verdict" in said:
            return NONE
    for flag in ("holds", "band_holds"):
        if isinstance(row.get(flag), bool):
            return HOLDS if row[flag] else REFUTED
    if row.get("unadjudicable") is True:
        return NONE
    if row.get("adjudicates") is False:
        return REPORTED
    band = row.get("band")
    if isinstance(band, str):
        named = re.match(r"[A-Z]-[a-z] (HOLDS|REFUTED)\b", band)
        if named:
            return HOLDS if named.group(1) == "HOLDS" else REFUTED
    return None


def rows_of(thread: str) -> dict[str, object]:
    """Every row the thread's record keeps, by name."""
    path, keys = THREADS[thread]
    place = descend(record(path), keys)
    rows = {key.replace("_", "-"): value for key, value in place.items()
            if re.fullmatch(rf"{thread}[-_][a-z]", key)}
    for name, (path, keys) in ELSEWHERE.items():
        if name[0] == thread:
            rows[name] = descend(record(path), keys)
    return rows


def row_of(name: str) -> object:
    if name[0] not in THREADS:
        return None
    return rows_of(name[0]).get(name)


def thin_of(row: object) -> bool | None:
    """Whether the record calls the row thin, or None where it keeps no label.
    A label kept as null is one the plan does not define for that row."""
    if isinstance(row, dict) and "thin" in row:
        return bool(row["thin"])
    return None


def leaves(obj: object):
    if isinstance(obj, bool):
        return
    if isinstance(obj, (int, float)):
        yield obj
    elif isinstance(obj, dict):
        for value in obj.values():
            yield from leaves(value)
    elif isinstance(obj, list):
        for value in obj:
            yield from leaves(value)


def printed(figure: str, row: object) -> bool:
    """Whether a leaf of the row prints as the figure, at its places, as a
    fraction or as a percentage. Signs and thousands are read as written."""
    text = figure.replace("−", "-").replace(",", "")
    places = len(text.split(".")[1]) if "." in text else 0

    def shown(value: float) -> str:
        out = f"{value:.{places}f}"
        return out[1:] if out.startswith("-") and float(out) == 0 else out

    want = shown(float(text))
    return any(want in (shown(v), shown(100 * v)) for v in leaves(row))


# ---------------------------------------------------------- reading the prose

def section(text: str, heading: str) -> str:
    start = text.index(f"\n## {heading}\n")
    end = text.find("\n## ", start + 1)
    return text[start:] if end == -1 else text[start:end]


def cells(line: str) -> list[str]:
    """A table row's cells, an escaped pipe kept inside its cell."""
    parts = [part.strip() for part in re.split(r"(?<!\\)\|", line.strip())]
    return parts[1:-1] if line.rstrip().endswith("|") else parts[1:]


def number(words: str) -> int:
    total = 0
    for word in re.split(r"[\s-]+", words.lower()):
        if word == "and":
            continue
        if word in UNITS:
            total += UNITS.index(word)
        elif word in TENS:
            total += 10 * TENS.index(word)
        elif word == "hundred":
            total *= 100
        else:
            raise ValueError(f"not a number word: {word}")
    return total


def scoreboard(text: str) -> dict:
    """The scoreboard as `STATUS.md` writes it."""
    body = section(text, SCOREBOARD)
    lines = body.splitlines()
    head = next(i for i, line in enumerate(lines) if line.startswith("| thread |"))
    columns = cells(lines[head])[1:]
    threads, total, marks = {}, None, {}
    for line in lines[head + 2:]:
        if not line.startswith("|"):
            break
        row = cells(line)
        counts = dict(zip(columns, (int(c.strip("* ")) for c in row[1:])))
        if row[0] == "**total**":
            total = counts
            continue
        letter = re.match(r"\*\*([A-Z])\*\* ·", row[0]).group(1)
        threads[letter] = counts
        mark = re.search(r"\*(?:(\w+) )?bands? set on a development set\*", row[0])
        if mark:
            marks[letter] = mark.group(1)
    named = {}
    for label in ("Refuted", "Hold", "Reported"):
        found = re.findall(rf"\b{label}:((?:\s*`[A-Z]-[a-z]`,?)+)\.", body)
        if len(found) != 1:
            raise ValueError(f"the named list {label!r} is not there once")
        named[label] = ROW.findall(found[0])
    heading = re.search(r"\*\*([A-Z][a-z]+(?:[ -][a-z]+)*) rows have been signed",
                        body)
    ratios = [(int(a), int(b), c) for a, b, c in
              re.findall(r"(\d+)\s+of\s+(\d+)\s+=\s+\*\*(\d+\.\d)%\*\*", body)]
    return {"threads": threads, "total": total, "marks": marks, "named": named,
            "heading": heading.group(1) if heading else None, "ratios": ratios}


def verdict_rows(text: str, threads: str):
    """Each row of a verdict table whose name belongs to `threads`, with the
    cell that states its verdict: the first one that opens with a verdict."""
    for number_, line in enumerate(text.splitlines(), 1):
        if not line.startswith("|"):
            continue
        row = cells(line)
        named = row and re.match(r"^[*`\s]*([A-Z]-[a-z])[*`]*(?:\s|·|$)", row[0])
        if not named or named.group(1)[0] not in threads:
            continue
        for at, cell in enumerate(row[1:], 1):
            word = WORD.match(cell)
            if word:
                yield number_, named.group(1), row, at, SAID[word.group(1).lower()]
                break


def citations(text: str):
    """Each verdict cited in parentheses: the line, the rows, the verdict, and
    the rows the citation calls thin."""
    for number_, line in enumerate(text.splitlines(), 1):
        for cited in CITATION.finditer(line):
            rows = ROW.findall(cited.group("rows"))
            rest = cited.group("rest")
            thin = set(re.findall(r"`([A-Z]-[a-z])` thin(?:ly)?\b", rest))
            if not thin and re.match(r",\s*thin(?:ly)?\b", rest):
                thin = set(rows)
            yield number_, rows, SAID[cited.group("word")], thin


# --------------------------------------------------------------- the problems

def scoreboard_problems(text: str) -> list[str]:
    """What in the scoreboard does not add up, or is not its records'."""
    try:
        board = scoreboard(text)
    except (ValueError, AttributeError, StopIteration) as exc:
        return [f"{STATUS}: the scoreboard cannot be read ({exc})"]
    out = []
    threads, total, named = board["threads"], board["total"], board["named"]
    for letter, n in threads.items():
        if n["adjudicated"] != n["refuted"] + n["dead zone"] + n["hold"]:
            out.append(f"{letter}: adjudicated is not refuted + dead zone + hold")
        if n["signed"] < n["adjudicated"] + n["reported"]:
            out.append(f"{letter}: more rows adjudicated and reported than signed")
    if total is None:
        out.append("the total row is missing")
    else:
        for column, value in total.items():
            summed = sum(n[column] for n in threads.values())
            if value != summed:
                out.append(f"total {column} is {value}, its rows sum to {summed}")
    if board["heading"] is None:
        out.append("the heading's count of signed rows is missing")
    elif total:
        try:
            counted = number(board["heading"])
        except ValueError as exc:
            counted = None
            out.append(f"the heading's count cannot be read ({exc})")
        if counted is not None and counted != total["signed"]:
            out.append(f"the heading says {board['heading']!r} rows, "
                       f"the table {total['signed']}")
    seen: dict[str, str] = {}
    for label, rows in named.items():
        for name in rows:
            if name in seen:
                out.append(f"{name} is named both {seen[name]} and {label}")
            seen[name] = label
    columns = {"Refuted": "refuted", "Hold": "hold", "Reported": "reported"}
    for label, column in columns.items():
        for letter in sorted({r[0] for r in named[label]} | set(threads)):
            listed = sum(1 for r in named[label] if r[0] == letter)
            if letter not in threads:
                out.append(f"{label} names {letter} rows, the table has no {letter}")
            elif listed != threads[letter][column]:
                out.append(f"{letter}: {threads[letter][column]} {column} in the "
                           f"table, {listed} named under {label}")

    # Against the records, in both directions.
    if set(threads) != set(THREADS):
        out.append(f"the table's threads {sorted(threads)} are not THREADS' "
                   f"{sorted(THREADS)}")
    for letter in sorted(set(threads) & set(THREADS)):
        kept = {name: verdict(row) for name, row in rows_of(letter).items()}
        for label, word in (("Refuted", REFUTED), ("Hold", HOLDS)):
            listed = {r for r in named[label] if r[0] == letter}
            gives = {name for name, said in kept.items() if said == word}
            for name in sorted(listed - gives):
                out.append(f"{name} is named {label}; its record gives "
                           f"{kept.get(name, 'no row')}")
            for name in sorted(gives - listed):
                out.append(f"{name}: its record gives {word}, and it is not "
                           f"named {label}")
        for name in (r for r in named["Reported"] if r[0] == letter):
            if kept.get(name) in (HOLDS, REFUTED, DEAD, NONE):
                out.append(f"{name} is named Reported; its record gives {kept[name]}")
        n = threads[letter]
        for word, expected in ((DEAD, n["dead zone"]),
                               (NONE, n["signed"] - n["adjudicated"] - n["reported"])):
            found = sorted(name for name, said in kept.items() if said == word)
            if len(found) != expected:
                out.append(f"{letter}: {expected} rows {word} by the table, "
                           f"its record gives {found}")

    # The ratios: refuted over adjudicated, with and without `Q` and the rows
    # whose bands were set on a development set. A row in the dead zone is
    # adjudicated and named in no list, so its record names it here.
    dead = {name for letter in set(threads) & set(THREADS)
            for name, row in rows_of(letter).items() if verdict(row) == DEAD}
    adjudicated = set(named["Refuted"]) | set(named["Hold"]) | dead
    for letter in threads:
        mark = board["marks"].get(letter, False)
        dev = {r for r in DEVELOPMENT_SET if r[0] == letter}
        if mark is False:
            expected = 0
        elif mark is None:
            expected = len({r for r in adjudicated if r[0] == letter})
        else:
            try:
                expected = number(mark)
            except ValueError as exc:
                out.append(f"{letter}: the development-set mark cannot be read ({exc})")
                continue
        if len(dev) != expected:
            out.append(f"{letter}: the table marks {expected} rows set on a "
                       f"development set, DEVELOPMENT_SET holds {sorted(dev)}")
    out += [f"{r} is in DEVELOPMENT_SET and not adjudicated"
            for r in sorted(DEVELOPMENT_SET - adjudicated)]
    refuted = set(named["Refuted"])
    expected_ratios = set()
    for drop_q in (False, True):
        for drop_dev in (False, True):
            kept_rows = {r for r in adjudicated
                         if not (drop_q and r[0] == "Q")
                         and not (drop_dev and r in DEVELOPMENT_SET)}
            expected_ratios.add((len(kept_rows & refuted), len(kept_rows)))
    written = board["ratios"]
    for a, b, shown in written:
        if f"{100 * a / b:.1f}" != shown:
            out.append(f"{a} of {b} is not {shown}%")
    if {(a, b) for a, b, _ in written} != expected_ratios or len(written) != 4:
        out.append(f"the ratios read {[(a, b) for a, b, _ in written]}, the "
                   f"table and the named lists give {sorted(expected_ratios)}")
    return out


def table_problems(name: str, text: str, threads: str) -> list[str]:
    """What in a FINDINGS' verdict table is not its record's."""
    out, tabled = [], set()
    for line, row_name, row, at, said in verdict_rows(text, threads):
        where = f"{name}:{line} {row_name}"
        kept = row_of(row_name)
        if kept is None:
            out.append(f"{where}: no row in its record")
            continue
        gives = verdict(kept)
        tabled.add(row_name)
        if said is None:
            out.append(f"{where}: a verdict this test cannot read, {row[at]!r}")
        elif said in (HOLDS, REFUTED, DEAD, NONE) and said != gives:
            out.append(f"{where}: the table says {said}, its record {gives}")
        elif said == REPORTED and gives not in (None, REPORTED):
            out.append(f"{where}: the table says reported, its record {gives}")
        thin = thin_of(kept)
        if thin is not None and thin != bool(THIN.search(row[at])):
            out.append(f"{where}: thin is {thin} in its record, the table says "
                       f"{row[at]!r}")
        if at == len(row) - 1:
            for cell in row[1:at]:
                for bold in BOLD.findall(cell):
                    for figure in FIGURE.findall(bold):
                        if not printed(figure, kept):
                            out.append(f"{where}: {figure} in bold is not "
                                       f"printed by its record's row")
    for letter in threads:
        wanted = {r for r, row in rows_of(letter).items()
                  if verdict(row) in (HOLDS, REFUTED, DEAD, NONE)}
        for missing in sorted(wanted - tabled):
            out.append(f"{name}: no verdict row read for {missing}")
    return out


def citation_problems(name: str, text: str) -> list[str]:
    """What a verdict cited in parentheses says that its record does not."""
    out = []
    for line, rows, said, thin in citations(text):
        for row_name in rows:
            where = f"{name}:{line} ({row_name})"
            kept = row_of(row_name)
            if kept is None:
                out.append(f"{where}: no row in its record")
                continue
            if verdict(kept) != said:
                out.append(f"{where}: cited {said}, its record {verdict(kept)}")
            if row_name in thin and thin_of(kept) is False:
                out.append(f"{where}: cited thin, its record says it is not")
    return out


# ----------------------------------------------------------------- the checks

def read(path: str) -> str:
    return (REPO / path).read_text()


class TestTheScoreboardAddsUp(unittest.TestCase):
    """`STATUS.md`'s scoreboard, against itself and against its records."""

    def test_it_agrees_with_itself_and_its_records(self):
        self.assertEqual(scoreboard_problems(read(STATUS)), [])

    def test_it_was_read_whole(self):
        board = scoreboard(read(STATUS))
        self.assertEqual(set(board["threads"]), set(THREADS))
        self.assertEqual(len(board["ratios"]), 4)
        self.assertTrue(all(board["named"].values()))


class TestTheVerdictTables(unittest.TestCase):
    """Each FINDINGS' verdict table against the record that owns its rows."""

    def test_every_table_agrees_with_its_records(self):
        problems = []
        for name, threads in TABLES.items():
            problems += table_problems(name, read(name), threads)
        self.assertEqual(problems, [])

    def test_every_thread_has_a_table_or_a_reason(self):
        tabled = set("".join(TABLES.values()))
        self.assertEqual(set(THREADS) - tabled, set(PROSE_ONLY))
        self.assertFalse(tabled & set(PROSE_ONLY))

    def test_no_findings_with_a_verdict_table_is_left_out(self):
        """A new FINDINGS whose table names a thread's rows is mapped, or its
        reason for not being one is stated in NOT_TABLES."""
        for path in sorted(REPO.glob("results*/FINDINGS*.md")):
            name = str(path.relative_to(REPO))
            if name in TABLES or name in NOT_TABLES:
                continue
            found = [r for _, r, *_ in verdict_rows(path.read_text(), "".join(THREADS))]
            self.assertEqual(found, [], f"{name} has verdict rows and is not in TABLES")


class TestTheCitations(unittest.TestCase):
    """Verdicts cited in parentheses by the documents that copy them."""

    def test_every_citation_agrees_with_its_record(self):
        problems = []
        for name in COPIES:
            problems += citation_problems(name, read(name))
        self.assertEqual(problems, [])

    def test_the_index_cites_verdicts(self):
        """If `STATUS.md` stopped citing in this form, the check above would
        pass on nothing."""
        self.assertGreater(len(list(citations(read(STATUS)))), 0)


class TestTheTeeth(unittest.TestCase):
    """Each check catches what it exists for, on a copy of the documents."""

    @classmethod
    def setUpClass(cls):
        cls.status = read(STATUS)

    def replaced(self, text: str, old: str, new: str) -> str:
        self.assertEqual(text.count(old), 1, f"{old!r} is not there once")
        return text.replace(old, new)

    def test_a_total_left_behind(self):
        board = section(self.status, SCOREBOARD)
        total = next(line for line in board.splitlines()
                     if line.startswith("| **total** |"))
        signed = cells(total)[1]
        status = self.replaced(self.status, total,
                               total.replace(signed, "**1000**", 1))
        self.assertTrue(any(p.startswith("total signed")
                            for p in scoreboard_problems(status)))

    def test_a_heading_not_recounted(self):
        heading = scoreboard(self.status)["heading"]
        status = self.replaced(self.status, f"**{heading} rows",
                               "**Two rows")
        self.assertTrue(any("the heading says" in p
                            for p in scoreboard_problems(status)))

    def test_a_ratio_not_recomputed(self):
        a, b, shown = scoreboard(self.status)["ratios"][0]
        status = self.replaced(self.status, f"{a} of {b} = **{shown}%**",
                               f"{a + 1} of {b} = **{shown}%**")
        problems = scoreboard_problems(status)
        self.assertTrue(any(f"{a + 1} of {b} is not" in p for p in problems))
        self.assertTrue(any(p.startswith("the ratios read") for p in problems))

    def test_a_row_named_under_the_wrong_verdict(self):
        moved = scoreboard(self.status)["named"]["Refuted"][-1]
        status = self.replaced(self.status, "\nHold: `", f"\nHold: `{moved}`, `")
        problems = scoreboard_problems(status)
        self.assertIn(f"{moved} is named both Refuted and Hold", problems)
        self.assertIn(f"{moved} is named Hold; its record gives refuted", problems)

    def test_a_verdict_flipped_in_a_table(self):
        name = "results_reuse/FINDINGS_REUSE.md"
        text = read(name)
        line = next(l for l in text.splitlines() if l.startswith("| `U-d` |"))
        flipped = self.replaced(text, line, line.replace("**refuted**", "**holds**"))
        self.assertIn("table says holds, its record refuted",
                      " ".join(table_problems(name, flipped, "U")))

    def test_a_thin_label_added_in_a_table(self):
        name = "results_edges/FINDINGS_EDGES.md"
        text = read(name)
        line = next(l for l in text.splitlines() if l.startswith("| `W-a` |"))
        thin = self.replaced(text, line, line.replace("**holds**", "**holds, thin**"))
        self.assertIn("thin is False in its record",
                      " ".join(table_problems(name, thin, "W")))

    def test_a_thin_label_cited_where_the_record_keeps_none(self):
        """Null is a label the plan does not define for that row: `Z-c`'s."""
        self.assertIn("cited thin, its record says it is not",
                      " ".join(citation_problems("x", "(`Z-c` holds, thin)")))

    def test_a_figure_off_by_a_digit(self):
        name = "results_reuse/FINDINGS_REUSE.md"
        text = read(name)
        line = next(l for l in text.splitlines() if l.startswith("| `U-a` |"))
        bold = BOLD.findall(line)[0]
        off = bold[:-1] + str((int(bold[-1]) + 1) % 10)
        changed = self.replaced(text, line, line.replace(f"**{bold}**", f"**{off}**"))
        self.assertIn(f"{off} in bold is not printed",
                      " ".join(table_problems(name, changed, "U")))

    def test_a_row_lost_from_a_table(self):
        name = "results_reuse/FINDINGS_REUSE.md"
        text = read(name)
        line = next(l for l in text.splitlines() if l.startswith("| `U-c` |"))
        lost = self.replaced(text, line + "\n", "")
        self.assertIn("no verdict row read for U-c",
                      " ".join(table_problems(name, lost, "U")))

    def test_a_citation_flipped(self):
        cited = re.search(r"\(`([A-Z]-[a-z])` (holds|refuted)\b", self.status)
        said = SAID[cited.group(2)]
        other = HOLDS if said == REFUTED else REFUTED
        status = (self.status[:cited.start()] + f"(`{cited.group(1)}` {other}"
                  + self.status[cited.end():])
        self.assertIn(f"cited {other}, its record {said}",
                      " ".join(citation_problems(STATUS, status)))


class TestTheReaders(unittest.TestCase):
    """The readers on inputs worked by hand."""

    def test_number_words(self):
        self.assertEqual(number("One hundred and nineteen"), 119)
        self.assertEqual(number("Ninety-nine"), 99)
        self.assertEqual(number("Two hundred and forty-one"), 241)
        with self.assertRaises(ValueError):
            number("a dozen")

    def test_cells_keep_an_escaped_pipe(self):
        self.assertEqual(cells(r"| `Y-d` | \|·\| < 0.06 | **holds** |"),
                         ["`Y-d`", r"\|·\| < 0.06", "**holds**"])

    def test_printed_reads_signs_places_and_percentages(self):
        row = {"median": 0.0207, "gap": -0.17594, "n": 5900, "share": 0.216}
        for figure in ("+0.0207", "−0.1759", "5,900", "21.6", "0.22"):
            self.assertTrue(printed(figure, row), figure)
        for figure in ("0.0208", "0.1759", "5,901"):
            self.assertFalse(printed(figure, row), figure)

    def test_printed_does_not_read_flags(self):
        self.assertFalse(printed("1", {"holds": True}))

    def test_the_four_ways_a_record_gives_a_verdict(self):
        self.assertEqual(verdict({"verdict": "REFUTED"}), REFUTED)
        self.assertEqual(verdict({"verdict": "holds"}), HOLDS)
        self.assertEqual(verdict({"verdict": "NEITHER"}), DEAD)
        self.assertEqual(verdict({"verdict": "UNSTABLE ACROSS BEAMS — not a verdict"}),
                         NONE)
        self.assertEqual(verdict({"holds": False, "thin": True}), REFUTED)
        self.assertEqual(verdict({"band_holds": True}), HOLDS)
        self.assertEqual(verdict({"holds": None, "unadjudicable": True}), NONE)
        self.assertEqual(verdict({"adjudicates": False}), REPORTED)
        self.assertEqual(verdict({"band": "P-c HOLDS and Stage D may run"}), HOLDS)
        self.assertIsNone(verdict({"band": "> 0.4824"}))

    def test_citations_read_lists_and_thin_labels(self):
        text = ("a (`J-a` and `J-b` hold, `J-b` thinly) b (`Z-a`, `Z-b` refuted)\n"
                "c (`V-a` refuted, thinly, at −0.0126) d (`H-a`, `H-b`)\n")
        self.assertEqual(list(citations(text)), [
            (1, ["J-a", "J-b"], HOLDS, {"J-b"}),
            (1, ["Z-a", "Z-b"], REFUTED, set()),
            (2, ["V-a"], REFUTED, {"V-a"}),
        ])

    def test_verdict_rows_find_the_cell_that_states_it(self):
        text = ("| **Q-a** | **HOLDS** | prose with **0.5** |\n"
                "| **R-b** | a claim | **NEITHER**: 45 of 208 |\n"
                "| `I-b` · covers | above both | **no verdict** |\n"
                "| `X-a` | not a thread here | **holds** |\n")
        found = [(r, at, said) for _, r, _, at, said in verdict_rows(text, "QRI")]
        self.assertEqual(found, [("Q-a", 1, HOLDS), ("R-b", 2, DEAD),
                                 ("I-b", 2, NONE)])


if __name__ == "__main__":
    unittest.main()
