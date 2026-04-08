# 🕷️ Smart Web Research Agent

An agentic web scraper built with **LangGraph** + **Playwright** that autonomously researches a question by crawling the web and producing a structured report.

## How it works

```
planner → scraper → evaluator ──(sufficient)──→ summarizer → END
              ↑           │
              └──(not yet)─┘
```

| Node | Role |
|---|---|
| `planner` | LLM decides which URLs to research |
| `scraper` | Playwright fetches & extracts page content |
| `evaluator` | LLM judges if enough info was gathered |
| `summarizer` | LLM writes a clean structured report |

## Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
playwright install chromium
```

### 2. Configure API key
```bash
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

### 3. Run
```bash
python main.py
```

## Project Structure

```
smart-research-agent/
├── main.py            # Entry point
├── graph.py           # LangGraph wiring
├── state.py           # ResearchState definition
├── requirements.txt
├── .env.example
├── nodes/
│   ├── planner.py     # Decides URLs to scrape
│   ├── scraper.py     # Calls Playwright tool
│   ├── evaluator.py   # Checks if data is sufficient
│   └── summarizer.py  # Writes final report
└── tools/
    └── scraper.py     # Playwright + BeautifulSoup scraper
```

## Customization

- **Change the question**: Edit the `question` variable in `main.py`
- **Adjust max loops**: Change `MAX_LOOPS` in `nodes/evaluator.py` (default: 3)
- **Change content length**: Edit the `[:3000]` slice in `tools/scraper.py`
- **Switch LLM**: Replace `ChatAnthropic` with `ChatOpenAI` in any node file