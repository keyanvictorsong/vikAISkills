# Code & Workspace Organization Principles

## Purpose
This document outlines principles for maintaining organized, scalable, and traceable code workspaces. Following these guidelines ensures clarity, reduces confusion, and makes collaboration easier.

---

## Core Principles

### 1. Goal-Based Top-Level Organization
- **Top-level folders should represent the primary goal or domain**
- All related subfolders, configurations, and resources live inside this goal folder
- Makes the workspace self-documenting at a glance
- Easy to share, archive, or move entire functional areas
- Structure example:
  ```
  AI-Agent-PowerGiver/
  ├── copilot-ai-agent/
  ├── claude-ai-agent/
  └── README.md
  ```
- **Benefits:**
  - Clear domain boundaries
  - Everything related to one goal is grouped together
  - Easier to find and maintain related components
  - Scales well as projects grow

### 2. One Folder Per Conversation/Task
- Each new conversation or task should be created within its own dedicated folder
- This maintains clear separation between different work streams
- Makes it easy to archive, share, or delete completed work
- Example: `task_20251228_table_extraction_improvement/`

### 3. Task-Specific Data and Output
- Non-recurring data and output results should live inside each task's folder
- Keeps all related artifacts together for easy reference
- When a task is complete, everything needed to understand it is in one place
- Structure example:
  ```
  task_folder/
  ├── input_data/
  ├── output_results/
  └── scripts/
  ```

### 4. Recurring Data in Separate Folder
- Shared or recurring datasets should be stored in a dedicated common folder
- Prevents duplication across multiple task folders
- Use symlinks or path references when tasks need access
- Example: `shared_datasets/`, `common_resources/`

### 5. Descriptive Folder Names (Long is OK)
- Folder names should be specific and self-documenting
- Include key identifiers: date, purpose, model version, etc.
- Avoid generic names like `test/`, `output/`, `data/`
- Good examples:
  - `pixel_grid_2.2_basic_output/`
  - `step3_format_conversion_json_to_csv/`
  - `benchmark_gp22_vs_tsr21_20251228/`

### 6. Step-Based Folder Structure
- Complex tasks with multiple steps should divide each step into its own folder
- Each step folder contains its code and corresponding test code
- Makes debugging and iteration on specific steps easier
- Structure example:
  ```
  task_folder/
  ├── step1_data_extraction/
  │   ├── extract.py
  │   └── test_extract.py
  ├── step2_transformation/
  │   ├── transform.py
  │   └── test_transform.py
  └── step3_output_generation/
      ├── generate.py
      └── test_generate.py
  ```

### 7. Purpose-Named Tests
- Test files should clearly indicate what they're testing
- Include the functionality or scenario being tested in the name
- Examples:
  - `test_table_cell_boundary_detection.py`
  - `test_empty_table_handling.py`
  - `test_merged_cell_extraction.py`

---

## Folder Naming Conventions

### Top-Level Folders (Goal-Based)
```
[Primary-Goal-Or-Domain]
```
**Examples:**
- `AI-Agent-PowerGiver/` - Contains all AI agent configuration tools
- `Browser-Automation-Suite/` - Browser automation tools and scripts
- `Data-Pipeline-Orchestration/` - ETL and data processing workflows
- `API-Integration-Framework/` - API clients and integration utilities

### Mid-Level Folders (Category/Component)
```
[category]_[description]_[version/date]_[output_type]
```

**Examples:**
| Purpose | Folder Name |
|---------|-------------|
| Model testing output | `pixel_grid_2.2_output/` |
| Step in pipeline | `step1_oneocr_generation/` |
| Comparison results | `comparison_adi_vs_tsr21_output/` |
| Benchmark data | `benchmark_2000_samples_20251228/` |

---

## Quick Checklist

Before starting a new task, ask:
- [ ] Is there a top-level goal folder for this domain, or do I need to create one?
- [ ] Did I create a new folder for this task inside the appropriate goal folder?
- [ ] Is the folder name specific and descriptive?
- [ ] Are my steps separated into subfolders?
- [ ] Are test files named after their purpose?
- [ ] Is shared data referenced from a common location?
- [ ] Will someone else understand this structure in 6 months?

---

## Anti-Patterns to Avoid

❌ Generic folder names: `test/`, `output/`, `new/`, `temp/`  
❌ Mixing multiple tasks in one folder  
❌ Duplicating shared datasets across tasks  
❌ Test files named `test1.py`, `test2.py`  
❌ Deeply nested structures without clear purpose  
❌ Leaving intermediate/debug files scattered around  

---

*Last Updated: January 1, 2026*
