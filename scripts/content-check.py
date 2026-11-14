#!/usr/bin/env python3
"""Content check for this repository.

Fails if any committed file contains credentials, cloud account identifiers, or
terms the maintainers have marked as not for publication. The marked terms are
stored only as salted SHA-256 digests, so this file does not reveal them.

  python3 scripts/content-check.py           check the repository
  python3 scripts/content-check.py --hash X  print the digest for a new term
"""
import hashlib
import pathlib
import re
import sys

SALT = "atai-cli-skill/content-check/v1:"
SKIP_DIRS = {".git"}
SKIP_FILES = {"content-check.py"}

PATTERNS = {
    "AWS access key id": r"\b(AKIA|ASIA)[0-9A-Z]{16}\b",
    "GitHub token": r"\b(gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{20,})",
    "Slack token": r"\bxox[abpr]-[A-Za-z0-9-]{10,}",
    "Anthropic API key": r"\bsk-ant-[A-Za-z0-9_-]{10,}",
    "private key": r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
    "secret-manager reference": r"op://",
    "12-digit account id": r"(?<![0-9])[0-9]{12}(?![0-9])",
    "AWS ARN": r"\barn:aws[a-z-]*:",
    "UUID": r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b",
    "CGNAT / VPN address": r"\b100\.(6[4-9]|[7-9][0-9]|1[01][0-9]|12[0-7])\.[0-9]+\.[0-9]+\b",
    "employee email": r"[A-Za-z0-9._%+-]+@archetypeai\.[a-z]+",
}

DENY = frozenset("""
11f5579282f9330e54acb0c010661dee41b91efca698ff9926e45d36c50d553f
1755da90fa81422d22215ffac1cc3149b3b566e5dc55e331a59f2c1649b9ca7c
1b14309813f75b379e1f632008cedd07ddad8f72f78e52eac47730c5e6cc8f30
1cb3d76272be62565302ff6a65b357b45c1ba10fc3286c6ff251f01fa5bdff83
1ee7c88655271e295cad0fe9beae93bdbccf3c72a3f15b616bfa822e12445cee
23b47ba710c0e7dc0c3848cdc046f2a2dab71319436fad93e2cd166ba9fda3bf
2526a19b6ff7bb7c815bf8ec981957db4b96794fc3746af31ca1dbcb445dc711
285bf4a5ef412a1047c5b89ff93cf0e2fd3224134305acf62da78660191d79bf
2db53f75b382b12a279d8719e139194ad48fcb4c87cbe4e855731c695a99e98e
351f21564e84482e5d018f5b62a4cb06c3bad0d25580ebf3557dfde1b6d4a7a9
3e0405e4276c51943c9057e3cd0c50f992d01d8dff9037ddbe72ba95d92f1fda
3e90ee510b803c16de6e9c8484492b4f4d3dd189f344de28dff52769afd787b4
4943f5a3094b4e0d25276ab1afd25f36afdee0b25e1648d3e4e08d8be56905e6
4a391a4dbd722e0a232e6ba26dd7b5ffbd3613905341345f60031c7bf4f43005
4bf0e53192a2881d07041a9252a2b265e469435ba091134857f8d32e384d33de
564bbbf5b338e89bfd5fc885d90c9624f553da2e997c2550454e54a78adc878f
58725b5dade3f48ac953fe51ccc76d3356526c98299fa76019a6f2b93435663b
6fd65b66b0edadc3d7b4e906bed1b36927d8b8b5ded94001ee4fd4bccafcdf7f
704d7ed2e6c05e85a31a28a8275375d08af89ea4426c0ce79266f1c78ae12658
7306f429a409b68a9b9d2f7d3eaf1e22725d6c91c5ec18d5107c1bd0f353f549
76ddb8d609764f4eb61d63643ad5cb69e1c920c78580fee9f0b6df9911249b49
796640c65e002a173f89f8c7e2be4bb12c7d2a500fe0bc8a6399215ac83f0cfa
79a828a19e6db351071e25a7479a31625948bc788a0892f0ba607519a69f954a
852c7598bd729d01ead8037270074cf8dbfe1355628949bdc69c2d0ff6eb0a3e
87a6c3bf0cf18148576305e4dae361eab2924f075dc984fd318fadbc1d034065
8a8c434a920ccf0c0fc67dd9c15a7e8042337fc6093a6b383a152610e9350049
8b01153b0623d4866cbdd1f143877e5b0aef7a5162aff74ad94c722724ffaa4e
8f5281d478d1e5694a25fe0b48c9807847f6332264881e26c094361ef9c3157a
91acc79843af417b33513032b56932776611ad873bc93eff41b847ef06c47090
93e38562c999d21543b34ec1b27d5f50c3daf0b14591da3f4b3c6cab256798d6
94af938eab59a27c561192c0f0752ede359023ad31feb4796fc42b53d574215b
96269d995069b951b0e999d83a5576178382835e80dd3ead6431a267a48497bb
970996cabd786528dbc946a0dab94b068725a578c557c8b2b9c177f60b1277a5
99a3c83e489c94cf16a65ea5218d24980cb6c9c28ca2f3188f100713fab3d7f3
a236608b8b3ee7e8412bb59a7dbe1550fc1b060de0f6de03e9eaf06b4c312caf
a5b1b94a75d50afd705e91e188416cfe1b76c15634cdf432e8c48fb05d81c1a1
ac2169cb780fa1522f6dbc2ed7d5ac99b905b3db30a1dd6e76d08abe82ee00fb
b9d2fc2678d56155860a72566249799b3d03f544ac7102f2985dd698b2f0fbe4
bbf00ccef78937e45067482ccc35207e1c6790807c6ef294cd4aa8408b8f55a2
c4165ef4c030d97925718d6d941ee9ea425ffebe3e961bfb0034650164ce8ee6
d598a6b336149eda47e50d20325579701b394564ff9ced570035818da67ecbc6
d598d15ffbefa49a7cf89d7f2ebd4a033a33310fe4f187e677b95bba39d7c68c
d6f3c8244adb30f929e468ee732f674179d510194405a72b3b6876a31af2b7d6
d84af632e83b2895c6b6eacf83ad7ea36954444c0ee6afe2296fb17d2ef6b7a1
dc68c3803ae90072ac05b8525ff681c3aa1af077162ef0a3e10ec412c7a80efc
e02f5115485fd988b7b782c7c5d0aa5d82253bac61a2f5ee0fe5ac4da497efa0
e1da5e0cdcd39f46165960121c980f8061523e850c276d20dfd789348f8ac268
e6124d8f15c242e8e10486bba2dae6a7cd90541a0c067ef1ccd5527aaa8e1dab
f82ce9672fa08c43c6988547d594383c43f66424051ad8c1526a6a4f02358cbc
""".split())

TOKEN = re.compile(r"[a-z0-9][a-z0-9._-]*")
SEP = re.compile(r"([._-])")


def digest(term: str) -> str:
    return hashlib.sha256((SALT + term.lower()).encode()).hexdigest()


def candidates(token: str):
    """Every run of 1-4 consecutive parts of a token, rejoined with its separators."""
    token = token.strip("._-")
    parts = SEP.split(token)
    words = parts[0::2]
    seps = parts[1::2]
    for i in range(len(words)):
        for j in range(i, min(i + 4, len(words))):
            out = words[i]
            for k in range(i, j):
                out += seps[k] + words[k + 1]
            yield out


def check(root: pathlib.Path) -> int:
    problems = 0
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.name in SKIP_FILES:
            continue
        if SKIP_DIRS.intersection(path.relative_to(root).parts):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        rel = path.relative_to(root)
        for n, line in enumerate(text.splitlines(), 1):
            for label, pat in PATTERNS.items():
                if re.search(pat, line):
                    print(f"::error file={rel},line={n}::content check: {label}")
                    problems += 1
            for token in TOKEN.findall(line.lower()):
                if any(digest(c) in DENY for c in candidates(token)):
                    print(f"::error file={rel},line={n}::content check: term not for publication")
                    problems += 1
                    break
    if problems == 0:
        print(f"content check: clean ({len(PATTERNS)} patterns, {len(DENY)} marked terms)")
    return 1 if problems else 0


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--hash":
        print(digest(sys.argv[2]))
        sys.exit(0)
    sys.exit(check(pathlib.Path(__file__).resolve().parent.parent))
