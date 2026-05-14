#!/usr/bin/env python3
"""
Generate the Agile Network India presentation deck from the AI Coding Playbook.

Talk: "From Typing to Briefing — a practitioner's mental model for agentic coding"
Event: Agile Network India, Bangalore, 18 April 2026
Speaker: Vikas Mishra

Run:  python3 build_deck.py
Out:  AI-Coding-Playbook-AgileNetworkIndia.pptx
"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# ---------------------------------------------------------------- palette ----
INK    = RGBColor(0x20, 0x21, 0x24)   # near-black body text
PAPER  = RGBColor(0xFF, 0xFF, 0xFF)
BLUE   = RGBColor(0x1A, 0x73, 0xE8)   # Google blue — primary accent
DARKBG = RGBColor(0x14, 0x16, 0x22)   # deep slate — title / section / closing
FAINT  = RGBColor(0x2A, 0x2E, 0x42)   # faint number on dark slides
MUTE   = RGBColor(0x5F, 0x63, 0x68)   # secondary grey text
LIGHT  = RGBColor(0xF4, 0xF5, 0xF7)   # panel background
PANELB = RGBColor(0xEC, 0xF1, 0xFB)   # takeaway-panel background (pale blue)
CLOUD  = RGBColor(0xC8, 0xCC, 0xD4)   # light text on dark
GREEN  = RGBColor(0x1E, 0x8E, 0x3E)
RED    = RGBColor(0xD9, 0x3A, 0x2B)
AMBER  = RGBColor(0xE8, 0x8A, 0x00)
CODEBG = RGBColor(0x1B, 0x1D, 0x2A)
CODEFG = RGBColor(0xE6, 0xE8, 0xF0)

BODYFONT = "Arial"
MONOFONT = "Consolas"

SW, SH = 13.333, 7.5
ML     = 0.92                 # left / right margin
CW     = SW - 2 * ML          # content width

prs = Presentation()
prs.slide_width  = Inches(SW)
prs.slide_height = Inches(SH)
BLANK = prs.slide_layouts[6]

EVENT = "Agile Network India  ·  Bangalore  ·  18 April 2026"


# --------------------------------------------------------------- helpers -----
def _box(slide, x, y, w, h, fill=None, line=None):
    shp = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE,
                                 Inches(x), Inches(y), Inches(w), Inches(h))
    if fill is None:
        shp.fill.background()
    else:
        shp.fill.solid()
        shp.fill.fore_color.rgb = fill
    if line is None:
        shp.line.fill.background()
    else:
        shp.line.color.rgb = line
        shp.line.width = Pt(1)
    shp.shadow.inherit = False
    return shp


def _round(slide, x, y, w, h, fill):
    shp = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
                                 Inches(x), Inches(y), Inches(w), Inches(h))
    try:
        shp.adjustments[0] = 0.045
    except Exception:
        pass
    shp.fill.solid()
    shp.fill.fore_color.rgb = fill
    shp.line.fill.background()
    shp.shadow.inherit = False
    return shp


def _tb(slide, x, y, w, h, anchor=MSO_ANCHOR.TOP):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = 0
    tf.margin_top = tf.margin_bottom = 0
    return tf


def _run(p, text, size, color, bold=False, italic=False, name=BODYFONT):
    r = p.add_run()
    r.text = text
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.italic = italic
    r.font.name = name
    r.font.color.rgb = color
    return r


def _kicker(slide, text, color=BLUE):
    tf = _tb(slide, ML, 0.58, CW, 0.34)
    p = tf.paragraphs[0]
    _run(p, text.upper(), 12, color, bold=True)


def _heading(slide, title):
    tf = _tb(slide, ML, 0.92, CW, 1.0)
    p = tf.paragraphs[0]
    p.line_spacing = 1.02
    _run(p, title, 30, INK, bold=True)
    _box(slide, ML, 1.86, 1.55, 0.055, fill=BLUE)


def _footer(slide, n):
    tf = _tb(slide, ML, 7.04, 9.0, 0.34)
    _run(tf.paragraphs[0], EVENT, 9, MUTE)
    tf2 = _tb(slide, SW - ML - 1.5, 7.04, 1.5, 0.34)
    p = tf2.paragraphs[0]
    p.alignment = PP_ALIGN.RIGHT
    _run(p, f"{n:02d}", 9, MUTE, bold=True)


def _topbar(slide):
    _box(slide, 0, 0, SW, 0.075, fill=BLUE)


def _panel(slide, text, y=6.02):
    """Pale-blue key-takeaway strip with a blue left rule."""
    _round(slide, ML, y, CW, 0.78, PANELB)
    _box(slide, ML, y, 0.07, 0.78, fill=BLUE)
    tf = _tb(slide, ML + 0.32, y, CW - 0.6, 0.78, anchor=MSO_ANCHOR.MIDDLE)
    p = tf.paragraphs[0]
    _run(p, "KEY TAKEAWAY   ", 10.5, BLUE, bold=True)
    _run(p, text, 14.5, INK, bold=True)


def _bullets(slide, items, y=2.12, h=3.7, numbered=False):
    tf = _tb(slide, ML, y, CW, h)
    first = True
    n = 0
    for lvl, text in items:
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        if lvl == 0:
            n += 1
            p.space_after = Pt(9)
            p.space_before = Pt(2)
            p.line_spacing = 1.06
            if numbered:
                _run(p, f"{n}   ", 19, BLUE, bold=True)
            else:
                _run(p, "▸   ", 18, BLUE, bold=True)
            _run(p, text, 18.5, INK)
        else:
            p.space_after = Pt(5)
            p.line_spacing = 1.04
            _run(p, "        –   ", 15, MUTE)
            _run(p, text, 15.5, MUTE)
    return tf


# --------------------------------------------------------------- slides ------
def slide_title():
    s = prs.slides.add_slide(BLANK)
    _box(s, 0, 0, SW, SH, fill=DARKBG)
    _box(s, 0, 0, SW, 0.12, fill=BLUE)
    # giant faint mark
    tf = _tb(s, ML, 0.7, CW, 1.1)
    _run(tf.paragraphs[0], "THE AI CODING PLAYBOOK", 14, BLUE, bold=True)

    tf = _tb(s, ML, 2.05, CW, 2.2)
    p = tf.paragraphs[0]
    p.line_spacing = 1.03
    _run(p, "From Typing to Briefing", 52, PAPER, bold=True)
    p2 = tf.add_paragraph()
    p2.line_spacing = 1.03
    p2.space_before = Pt(4)
    _run(p2, "A practitioner's mental model for agentic coding", 26, CLOUD)

    _box(s, ML, 4.5, 1.8, 0.05, fill=BLUE)

    tf = _tb(s, ML, 4.72, CW, 1.15)
    p = tf.paragraphs[0]
    _run(p, "Vikas Mishra", 20, PAPER, bold=True)
    p2 = tf.add_paragraph()
    p2.space_before = Pt(2)
    _run(p2, "Platform & AI Architect, Google", 15, CLOUD)
    p3 = tf.add_paragraph()
    p3.space_before = Pt(2)
    _run(p3, "vikasmishra.ai", 14, BLUE, bold=True)

    tf = _tb(s, ML, 6.62, CW, 0.5)
    _run(tf.paragraphs[0], EVENT, 13, BLUE, bold=True)


def slide_section(num, title, subtitle):
    s = prs.slides.add_slide(BLANK)
    _box(s, 0, 0, SW, SH, fill=DARKBG)
    _box(s, 0, 0, 0.18, SH, fill=BLUE)
    # big faint number
    tf = _tb(s, ML - 0.1, 0.55, 6.0, 3.2)
    _run(tf.paragraphs[0], num, 200, FAINT, bold=True)

    tf = _tb(s, ML, 3.95, CW, 1.4)
    p = tf.paragraphs[0]
    p.line_spacing = 1.03
    _run(p, title, 44, PAPER, bold=True)

    _box(s, ML, 5.32, 1.8, 0.05, fill=BLUE)

    tf = _tb(s, ML, 5.55, CW - 1.0, 1.2)
    p = tf.paragraphs[0]
    p.line_spacing = 1.12
    _run(p, subtitle, 18, CLOUD)


def slide_content(kicker, title, items, panel=None, numbered=False):
    s = prs.slides.add_slide(BLANK)
    _topbar(s)
    _kicker(s, kicker)
    _heading(s, title)
    bh = 3.7 if panel else 4.7
    _bullets(s, items, y=2.12, h=bh, numbered=numbered)
    if panel:
        _panel(s, panel)
    _footer(s, len(prs.slides.slides) if False else _idx())


def slide_mono(kicker, title, code, panel=None):
    s = prs.slides.add_slide(BLANK)
    _topbar(s)
    _kicker(s, kicker)
    _heading(s, title)
    lines = code.split("\n")
    box_h = min(3.55, 0.34 * len(lines) + 0.5)
    _round(s, ML, 2.18, CW, box_h, CODEBG)
    tf = _tb(s, ML + 0.45, 2.18 + 0.22, CW - 0.9, box_h - 0.44)
    first = True
    for ln in lines:
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.line_spacing = 1.18
        color = CODEFG
        bold = False
        if ln.strip().startswith("##"):
            color = BLUE
            bold = True
        elif ln.strip().startswith(("┌", "│", "└", "├")):
            color = RGBColor(0x8A, 0xB4, 0xF8)
        _run(p, ln if ln else " ", 15.5, color, bold=bold, name=MONOFONT)
    if panel:
        _panel(s, panel, y=2.18 + box_h + 0.28)
    _footer(s, _idx())


def slide_context_window(kicker, title, chips, caption, panel=None):
    """Bespoke shape diagram for the context window."""
    s = prs.slides.add_slide(BLANK)
    _topbar(s)
    _kicker(s, kicker)
    _heading(s, title)

    ox, oy, ow, oh = ML, 2.04, CW, 3.74
    _round(s, ox, oy, ow, oh, LIGHT)
    # header strip
    _box(s, ox, oy, ow, 0.52, fill=DARKBG)
    tf = _tb(s, ox, oy, ow, 0.52, anchor=MSO_ANCHOR.MIDDLE)
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    _run(p, "THE CONTEXT WINDOW", 15, PAPER, bold=True)
    # caption strip
    cap_h = 0.5
    _box(s, ox, oy + oh - cap_h, ow, cap_h, fill=BLUE)
    tf = _tb(s, ox, oy + oh - cap_h, ow, cap_h, anchor=MSO_ANCHOR.MIDDLE)
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    _run(p, caption, 14, PAPER, bold=True)
    # 3 x 2 chip grid
    pad, cg, rg = 0.4, 0.3, 0.28
    region_x = ox + pad
    region_y = oy + 0.52 + 0.26
    region_w = ow - 2 * pad
    region_h = oh - 0.52 - cap_h - 0.52
    cw_ = (region_w - 2 * cg) / 3
    ch_ = (region_h - rg) / 2
    for i, txt in enumerate(chips):
        r, c = divmod(i, 3)
        x = region_x + c * (cw_ + cg)
        y = region_y + r * (ch_ + rg)
        _round(s, x, y, cw_, ch_, PAPER)
        _box(s, x, y, 0.06, ch_, fill=BLUE)
        tf = _tb(s, x + 0.22, y, cw_ - 0.36, ch_, anchor=MSO_ANCHOR.MIDDLE)
        p = tf.paragraphs[0]
        p.line_spacing = 1.05
        _run(p, txt, 14.5, INK, bold=True)
    if panel:
        _panel(s, panel, y=oy + oh + 0.26)
    _footer(s, _idx())


def slide_twocol(kicker, title, left, right, panel=None):
    s = prs.slides.add_slide(BLANK)
    _topbar(s)
    _kicker(s, kicker)
    _heading(s, title)
    gap = 0.45
    colw = (CW - gap) / 2
    top = 2.16
    colh = 3.55 if panel else 4.45
    for i, col in enumerate((left, right)):
        x = ML + i * (colw + gap)
        _round(s, x, top, colw, colh, LIGHT)
        _box(s, x, top, colw, 0.52, fill=col["color"])
        tf = _tb(s, x + 0.28, top, colw - 0.5, 0.52, anchor=MSO_ANCHOR.MIDDLE)
        _run(tf.paragraphs[0], col["head"], 15, PAPER, bold=True)
        tf = _tb(s, x + 0.32, top + 0.74, colw - 0.62, colh - 0.95)
        first = True
        for item in col["items"]:
            p = tf.paragraphs[0] if first else tf.add_paragraph()
            first = False
            p.space_after = Pt(8)
            p.line_spacing = 1.07
            _run(p, "▸  ", 14, col["color"], bold=True)
            _run(p, item, 14.5, INK)
    if panel:
        _panel(s, panel)
    _footer(s, _idx())


def slide_closing():
    s = prs.slides.add_slide(BLANK)
    _box(s, 0, 0, SW, SH, fill=DARKBG)
    _box(s, 0, 0, SW, 0.12, fill=BLUE)
    tf = _tb(s, ML, 2.35, CW, 1.6, anchor=MSO_ANCHOR.MIDDLE)
    _run(tf.paragraphs[0], "Go ship something.", 56, PAPER, bold=True)

    _box(s, ML, 4.05, 1.8, 0.05, fill=BLUE)

    tf = _tb(s, ML, 4.35, CW, 1.0)
    p = tf.paragraphs[0]
    p.line_spacing = 1.15
    _run(p, "The AI Coding Playbook — 21 chapters, concept-first, ", 18, CLOUD)
    _run(p, "every example runnable.", 18, CLOUD, bold=True)
    p2 = tf.add_paragraph()
    p2.space_before = Pt(6)
    _run(p2, "Concepts stay. Realizations change. Build the habits — "
             "the next tool is just a new surface.", 16, MUTE)

    tf = _tb(s, ML, 6.35, CW, 0.7)
    p = tf.paragraphs[0]
    _run(p, "Thank you.   ", 18, PAPER, bold=True)
    _run(p, "Vikas Mishra  ·  vikasmishra.ai  ·  " + EVENT, 13, BLUE, bold=True)


# footer index — true slide position (the slide was just added)
def _idx():
    return len(prs.slides)


# ----------------------------------------------------------------- build -----
slide_title()

slide_content(
    "Introduction",
    "Why this talk exists",
    [
        (0, "Most writing about “AI coding” is one of three things — and none survive a real codebase:"),
        (1, "A marketing page for a tool you already know exists"),
        (1, "A three-minute demo that falls apart on a real repo"),
        (1, "A tutorial from six months ago — ancient, in this space"),
        (0, "This talk is the reference I wished existed: concepts first, tool recipes second."),
        (0, "Drawn from actually running agents against real codebases — not transcripts of someone else’s tutorial."),
    ],
    panel="Concepts stay. Realizations get updated when the tools change.",
)

slide_content(
    "Foundations · Ch.1",
    "What is actually new",
    [
        (0, "Every prior tool — the IDE, the debugger, the LSP, autocomplete — sat next to your code. You held the pen."),
        (0, "Agentic coding is categorically different: the agent reads, plans, edits files, runs commands, observes output, iterates."),
        (0, "You are no longer typing. You are briefing."),
        (0, "The skill shifts — from “how do I write the code” to “how do I describe the outcome, scope the work, and verify the result.”"),
    ],
    panel="This is not a productivity multiplier on the old skill. It is a different skill.",
)

slide_content(
    "Foundations · Ch.1",
    "The 10x is not faster typing",
    [
        (0, "People who are 10x faster with an agent are not typing faster. They are:"),
        (1, "Briefing better"),
        (1, "Scoping tighter"),
        (1, "Catching the agent’s failure modes earlier"),
        (0, "People who are underwhelmed usually have not shifted modes — still typing, with the agent as a fancy autocomplete."),
        (0, "The rest of this talk is about making that shift."),
    ],
)

slide_section("01", "The Mental Model",
              "One window. Everything the model sees. Every technique in this talk is a consequence of it.")

slide_context_window(
    "The one diagram everything depends on",
    "The context window",
    [
        "System prompt",
        "Your brief",
        "Files the agent read",
        "Tool results",
        "The agent's own plans and notes",
        "Intermediate outputs + your follow-ups",
    ],
    "Everything the model sees",
    panel="The agent has exactly one input: this window.",
)

slide_content(
    "The Mental Model",
    "One input, no memory",
    [
        (0, "The model has no memory of prior sessions — unless you give it one (memory systems, later in this talk)."),
        (0, "It cannot “just know” anything about your codebase that is not either:"),
        (1, "In the window, or"),
        (1, "Fetchable by a tool"),
        (0, "Most “the agent is confused” complaints reduce to: the relevant thing is not in the window — or the window is so full it got crowded out."),
    ],
)

slide_content(
    "The Mental Model",
    "This explains everything that goes wrong",
    [
        (0, "“It forgot what we decided.”  →  The decision was not in the window, or got crowded out by later content."),
        (0, "“It keeps making the same mistake.”  →  The correction is there, but buried under 40k tokens of file reads."),
        (0, "“It invented a function that doesn’t exist.”  →  The real function is in a file it never read. Inventing was the only option."),
    ],
    panel="Every technique is about controlling what is in the window — for how long, at what position.",
)

slide_content(
    "The Mental Model",
    "What “agentic” actually means",
    [
        (0, "An agent is an LLM in a loop. Each turn:"),
        (1, "1  ·  It sees the current context window"),
        (1, "2  ·  It decides: respond with text, call a tool, or stop"),
        (1, "3  ·  If it called a tool, the result is appended to the window"),
        (1, "4  ·  Go to 1"),
        (0, "“Tools” here means file reads, file edits, shell commands, web search, MCP calls, subagent spawns — anything the runtime exposes."),
    ],
)

slide_content(
    "The Mental Model",
    "The runtime matters as much as the model",
    [
        (0, "When people say an agent is “smart” or “dumb,” they are describing how well that loop converges on a useful outcome."),
        (0, "Raw model capability matters — but so does the runtime: tool selection, permissions, context discipline, memory, hooks."),
        (0, "A strong model with a weak runtime underperforms a weak model with a strong runtime — on almost any real task."),
    ],
    panel="Intelligence is not the bottleneck. Context is.",
)

slide_section("02", "The Google-First Stack",
              "Gemini CLI as the default. Google Antigravity when parallelism is the point. The concepts carry across both.")

slide_content(
    "Landscape · Ch.2",
    "The landscape, without the matrix",
    [
        (0, "Forget feature-by-feature comparison matrices — they go stale in weeks. Four axes actually matter:"),
        (1, "Surface area — terminal CLI, IDE, or web"),
        (1, "Control granularity — confirm-each-call vs autonomous bursts"),
        (1, "Ecosystem fit — what does it compose with: your cloud, your stack, your tools"),
        (1, "Model strategy — single-vendor, multi-model, or bring-your-own"),
        (0, "Every product choice reduces to those four. The rest is UX polish."),
    ],
)

slide_content(
    "Landscape · Ch.2",
    "Gemini CLI — the default if you are in or near Google",
    [
        (0, "Surface: terminal. Control: per-call by default, plus Plan Mode for review-then-execute."),
        (0, "Ecosystem: native to Google Cloud — Vertex AI, BigQuery, Cloud Functions, Cloud Workstations, Firebase Studio."),
        (0, "Model: Gemini 3 Pro / Flash by default; Vertex Model Garden unlocks Gemma, Qwen, DeepSeek, Llama."),
        (0, "Best at: anything that composes with Google Cloud, shell-heavy workflows, free-tier exploration."),
    ],
    panel="Install in one line:   npm install -g @google/gemini-cli   →   gemini",
)

slide_content(
    "Antigravity · Ch.19",
    "Google Antigravity — the agentic IDE",
    [
        (0, "Announced 18 Nov 2025 alongside Gemini 3. Not a CLI, not a traditional IDE — an agent-first environment on a VS Code fork."),
        (0, "Two views you live in:"),
        (1, "Editor — familiar VS Code-style editing, for inspecting and refining code"),
        (1, "Manager (“Mission Control”) — spawn and monitor multiple autonomous agents, each in its own workspace"),
        (0, "Default model is Gemini 3; Claude and GPT-OSS are also selectable per task."),
    ],
)

slide_content(
    "Antigravity · Ch.19",
    "The mental-model shift with Antigravity",
    [
        (0, "With a CLI you run a session: prompt, the agent works, you review, you prompt again."),
        (0, "With Antigravity you run a queue of agents: describe work, an agent spawns in its own workspace, you review artifacts — while briefing the next task."),
        (0, "The analogy that helps: Antigravity is to agentic coding what CI is to local testing. The work happens elsewhere; you watch outcomes, not keystrokes."),
    ],
    panel="Parallelism is the default, not the exception — up to 5 agents at once in Mission Control.",
)

slide_content(
    "Antigravity · Ch.19",
    "You review artifacts, not transcripts",
    [
        (0, "The agent’s work surfaces as named, reviewable outputs — they replace the CLI’s transcript:"),
        (1, "Task List  ·  Implementation Plan  ·  Code Diffs"),
        (1, "Screenshots  ·  Browser Recordings  ·  Walkthroughs"),
        (0, "Browser subagent — drives Chrome to verify a UI renders, investigate web-app bugs, and record reproductions."),
        (0, "Customization layer: Rules (policy), Workflows (reusable procedures), Skills (named capabilities), Allowlists."),
    ],
)

slide_twocol(
    "Antigravity vs Gemini CLI",
    "When to reach for which",
    {"head": "Reach for Antigravity", "color": AMBER, "items": [
        "Parallel, independent tasks you want to fan out",
        "GUI-friendly onboarding for a less terminal-heavy teammate",
        "You want to watch the agent drive a browser",
        "Gemini 3 specifically matters for the task",
    ]},
    {"head": "Reach for Gemini CLI", "color": BLUE, "items": [
        "A tight, iterative loop on a single problem",
        "CI-like automation and scripting",
        "Heavy MCP ecosystem usage",
        "Free-tier exploration and shell-heavy work",
    ]},
    panel="Both, for most serious users. The durable concepts carry across either surface.",
)

slide_section("03", "Briefing, Not Prompting",
              "The skill shift that explains most of the variance between “the agent is magic” and “the agent is useless.”")

slide_content(
    "Prompting · Ch.3",
    "From prompt to brief",
    [
        (0, "Prompting a chat model is a single-turn transaction: you ask, it answers, you judge."),
        (0, "Briefing an agent is a multi-turn commitment: you describe an outcome; it reads, plans, edits, runs, iterates; you supervise and redirect."),
        (0, "The input is not a prompt — it is a working agreement the agent returns to across dozens of turns. Two consequences:"),
        (1, "Clarity compounds — a vague brief drifts exponentially across every tool call"),
        (1, "What you leave out matters as much as what you put in"),
    ],
)

slide_mono(
    "Prompting · Ch.3",
    "The four parts of a good brief",
    "## Outcome\n"
    "   What \"done\" looks like — concretely, verifiably.\n"
    "\n"
    "## Scope\n"
    "   What to touch — and, more importantly, what NOT to.\n"
    "\n"
    "## Constraints\n"
    "   Non-goals. Conventions. Things the agent can't derive.\n"
    "\n"
    "## Verification\n"
    "   How you'll both know it is actually done.",
    panel="All four parts is usually 4–8 sentences. That is the right size.",
)

slide_twocol(
    "Prompting · Ch.3",
    "Same task. Radically different trajectory.",
    {"head": "Bad brief", "color": RED, "items": [
        "“The API is too slow on the users endpoint, make it faster.”",
        "One sentence, no structure.",
        "Nothing concrete to verify against.",
        "The agent fills the blanks with its prior — usually wrong.",
    ]},
    {"head": "Good brief", "color": GREEN, "items": [
        "Outcome: GET /users/:id p95 latency under 100ms in staging.",
        "Scope: two named files; new tests allowed.",
        "Constraints: no caching yet; don’t change the response shape.",
        "Verification: run the bench, show p50 / p95 / p99.",
    ]},
    panel="The difference between a 30-minute focused session and a 3-hour drift.",
)

slide_content(
    "Prompting · Ch.3",
    "The spec-first habit",
    [
        (0, "For anything bigger than “rename this variable,” write the brief in a file before you paste it."),
        (0, "It forces you to think through outcome / scope / non-goals / acceptance criteria — before you are watching the agent move and tolerating ambiguity."),
        (0, "Keep specs under version control in specs/. A few paragraphs — it is not a design doc, do not over-engineer it."),
        (0, "Teams that do this ship with markedly lower rollback rates than teams that freestyle every session."),
    ],
    panel="Spec-first is the single most impactful habit you can adopt.",
)

slide_content(
    "Prompting · Ch.3",
    "Durable patterns — they hold across tools and model generations",
    [
        (0, "Plan before edit — “tell me the plan, do not edit anything yet.” It is cheaper to fix a plan than a diff.  (gemini --plan)"),
        (0, "Explore first, read narrowly — “find the 3 files most relevant to X, then read only those.”"),
        (0, "Use structure — pick Markdown headings or XML tags and be consistent. It is how the model finds each part 30 turns later."),
        (0, "Name the unit of work — every session is about one thing. Say what it is, at the top."),
        (0, "Refer to things by their real names — file paths, function names, line numbers. The agent can grep."),
    ],
)

slide_twocol(
    "Prompting · Ch.3",
    "Anti-patterns you will do — everyone does",
    {"head": "Stop", "color": RED, "items": [
        "“Please could you kindly, when you get a chance…” — polite padding burns tokens and reads as noise",
        "Stacked asks — “fix the bug, add retries, clean up logging, update the README” is four tasks",
        "“Do whatever you think is best” — delegating judgment to something without your context",
    ]},
    {"head": "Do instead", "color": GREEN, "items": [
        "Be direct. The model is not offended.",
        "Split into four sessions — each is faster and better than the combined attempt",
        "Scope the latitude: “I don’t care about X, pick anything reasonable”",
    ]},
    panel="When the agent goes wrong, do not pile on corrections. Fix the brief. Start fresh.",
)

slide_section("04", "Memory & Context Economics",
              "Durable context in, noise out — and a clear-eyed look at where the money actually goes.")

slide_content(
    "Memory · Ch.4",
    "Memory — durable context without re-briefing",
    [
        (0, "The model has no persistent state. Every new session starts with an empty window."),
        (0, "Memory in an agentic CLI is just files the tool reads into context automatically. No vector store, no embedding search, no magic."),
        (0, "Three-tier hierarchy — the same concept in every tool; GEMINI.md is one realization:"),
        (1, "User / global — your personal preferences, on every project"),
        (1, "Project / shared — build & test commands, architecture facts, conventions — committed to git"),
        (1, "Nested / path-scoped — rules for one directory, loaded on demand when the agent touches it"),
    ],
    panel="The highest-leverage thing you can do after learning to brief well.",
)

slide_twocol(
    "Memory · Ch.4",
    "What goes in a memory file — and what does not",
    {"head": "Put in", "color": GREEN, "items": [
        "Build / test / run commands, with their real names",
        "Architecture one-liners — three sentences save fifty tool calls of exploration",
        "Conventions the agent will not infer",
        "Non-goals — “do not add dependencies without asking”",
    ]},
    {"head": "Keep out", "color": RED, "items": [
        "Secrets, API keys, tokens — memory files get committed and logged",
        "Bulk documentation — link to it, do not inline it",
        "Transient state — “working on X, due Friday” goes stale, and stale context actively misleads",
    ]},
    panel="Think onboarding doc for a senior engineer: specific, terse, load-bearing. Not a novel. Under 200 lines.",
)

slide_content(
    "Context Rot · Ch.9",
    "Context rot — why long sessions get dumber",
    [
        (0, "The model did not get dumber. Your context got dirtier."),
        (0, "The window is finite; every tool call, file read, and aborted “let me try” stays in it. The symptoms look like forgetfulness; the cause is attention dilution."),
        (0, "The four symptoms — if you see two in one session, stop. Do not push through:"),
        (1, "Repetition — re-suggests a change it already made"),
        (1, "Confident invention — a function name that does not exist"),
        (1, "Drift — a one-thing fix now touches seven files"),
        (1, "Hedging — “this should work,” “usually this pattern…”"),
    ],
)

slide_content(
    "Context Rot · Ch.9",
    "Signal vs noise — the habits that push rot out 10x",
    [
        (0, "End sessions at task boundaries — a fresh context is a feature, not a cost. Default to fresh."),
        (0, "Compact aggressively — not when you are out of space, but when signal-to-noise drops. Compact with a hint."),
        (0, "Checkpoint decisions into durable files — specs/, docs/decisions/, memory — so nothing load-bearing is lost."),
        (0, "Read narrowly — every unnecessary full-file read is a context tax."),
        (0, "Delegate exploration to subagents — they burn their own context; yours stays clean."),
        (0, "One concern at a time — scope creep is a context killer."),
    ],
)

slide_content(
    "Saving Tokens · Ch.10",
    "Where the tokens actually go",
    [
        (0, "File reads dominate — a 1,000-line file is 3–8k tokens; do that twenty times and you are past 100k."),
        (0, "Tool descriptions — every MCP server, skill, and command sits in the header of every single turn."),
        (0, "Intermediate reasoning, verbose tool output, memory files — all compound across the session."),
        (0, "Notice what is NOT on the list: the actual code changes. Writing a file is cheap."),
    ],
    panel="Reading files is expensive. Writing them is cheap. That asymmetry is the core economic insight.",
)

slide_content(
    "Subagents · Ch.11",
    "Subagents — the heaviest single lever",
    [
        (0, "A subagent is a second agent instance — its own context window, its own narrow task. It returns a summary."),
        (0, "Two things make them powerful:"),
        (1, "Context isolation — heavy reads happen elsewhere; your session stays sharp"),
        (1, "Parallelism — several can work independent pieces at once"),
        (0, "Two things make them dangerous:"),
        (1, "They still cost tokens — you moved the cost off your screen, not away"),
        (1, "Parallelism magnifies mistakes — a misbriefed subagent burns tokens fast, four at a time"),
    ],
    panel="Brief a subagent like a contractor: outcome, scope, constraints, verification — and what NOT to return.",
)

slide_section("05", "Putting It Together",
              "The workflows are applications of everything so far — not new techniques.")

slide_content(
    "Workflows · Ch.21",
    "A long-horizon workflow that does not rot",
    [
        (0, "Start — memory loaded, narrow goal, minimal brief"),
        (0, "Explore — subagent-delegated; you get back a summary, not 40 file reads"),
        (0, "Plan — the agent produces a plan in plan mode; you review; checkpoint it to a file"),
        (0, "Implement one phase — one logical chunk, run the tests, commit"),
        (0, "Compact or restart — with a hint: “keep the plan and the commit summary; drop the tool output”"),
        (0, "Repeat — for phase 2, phase 3…"),
    ],
    panel="A 4-hour task never becomes a 4-hour session — it becomes 3–5 short, clean sessions chained through files.",
    numbered=True,
)

slide_content(
    "Workflows · Ch.21",
    "Six playbooks — what they all share",
    [
        (0, "Bug triage · multi-file migration · spec-to-shipped · on-call triage · research-driven decision · PR review at scale"),
        (0, "Read the briefs and notice what repeats:"),
        (1, "Four-part structure — outcome, scope, constraints, deliver"),
        (1, "Plan-first and approval checkpoints almost everywhere"),
        (1, "An explicit “do not do X” where X is the obvious-but-wrong move"),
        (1, "A named, committable artifact at the end"),
    ],
    panel="The workflows are applications of everything so far. Writing one from scratch every session means the habits are not built yet.",
)

slide_content(
    "Testing · Ch.16",
    "One trap worth naming: tests",
    [
        (0, "The failure mode of AI-assisted testing: tests that compile, run, pass — and tell you nothing about whether the feature works."),
        (0, "Two patterns to brief against:"),
        (1, "Test-the-implementation — asserts the branches it just saw; coupled to the code, not the contract"),
        (1, "Test-the-happy-path-only — real bugs hide at boundaries: empty, max length, unicode, null, timeout"),
        (0, "Brief for it: test from the contract, plan before code, match the existing style, run the tests — and if they fail, stop. Do not soften the test to pass."),
    ],
    panel="Tests are only useful if they can fail when the code is wrong.",
)

slide_content(
    "Recap",
    "The whole thing, in one slide",
    [
        (0, "The agent has one input: the context window. Everything else is a consequence."),
        (0, "Stop typing, start briefing — outcome, scope, constraints, verification. Spec-first for anything non-trivial."),
        (0, "Move durable context into memory files. Keep them terse and load-bearing."),
        (0, "Protect signal-to-noise: end at task boundaries, read narrowly, delegate, compact."),
        (0, "Pick the surface for the task — Gemini CLI for the tight loop, Antigravity when parallelism pays."),
    ],
    panel="Concepts stay. Realizations change. Build the habits — the next tool is just a new surface.",
)

slide_closing()

OUT = "AI-Coding-Playbook-AgileNetworkIndia.pptx"
prs.save(OUT)
print(f"wrote {OUT} — {len(prs.slides)} slides")
