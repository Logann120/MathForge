# Manual QA and Accessibility Review

This guide covers manual review for the MathForge Streamlit MVP and exported instructional materials. It is intentionally tool-light: use it before major topic, exporter, model, or UI changes without adding browser automation or accessibility tooling.

MathForge is deterministic and instructor-reviewable. Manual QA should confirm both the application workflow and the generated materials remain clear, accurate, readable, and accessible enough for classroom review.

## Current QA Baseline

The current checkpoint covers Markdown, print-friendly standard HTML, ZIP bundles containing Markdown plus standard HTML, Canvas-friendly manual-entry CSV, and separate LibGuides-safe HTML. Automated tests cover exporter structure and deterministic output, but browser print preview, copy/paste behavior, and accessibility review still require manual checks. MathForge does not include a PDF exporter, direct Canvas integration, or direct LibGuides integration.

Status: ready for manual execution. Do not mark this QA pass as passed until a human reviewer completes the scenarios and records results.

## Manual QA Execution Checklist

Use this section for a focused human QA pass. The broader sections below provide additional checks when a release needs deeper review.

### Setup

1. Install dependencies if needed:

   ```bash
   pip install -r requirements.txt
   ```

2. Run the automated suite:

   ```bash
   python -B -m pytest -p no:cacheprovider tests
   ```

3. Launch the Streamlit app:

   ```bash
   streamlit run app/main.py
   ```

4. Keep the `examples/` directory available for static export review. Representative files include:
   - `examples/linear_equations_worksheet.md`
   - `examples/linear_equations_worksheet.html`
   - `examples/linear_equations_resource_pack.md`
   - `examples/linear_equations_resource_pack.html`
   - `examples/linear_equations_worksheet_libguides.html`
   - `examples/linear_equations_resource_pack_libguides.html`

### Representative Scenarios

| Scenario | Inputs | Expected export buttons | Manual checks |
| --- | --- | --- | --- |
| Topic worksheet | Topic mode, `Linear equations`, `Worksheet only`, `Easy`, count `5` | Download Worksheet Markdown, Download Worksheet HTML, Download Worksheet LibGuides-Safe HTML, Download Worksheet Export Bundle, Download Worksheet Canvas Manual-Entry CSV | Worksheet tab shows five problems; solution key tab has matching answers; Markdown is readable when opened as text; standard HTML opens in a browser and includes print-focused CSS; print preview keeps problems and solution key readable; ZIP contains Markdown plus standard HTML only; Canvas CSV has question title, prompt, answer, explanation, topic, difficulty, problem ID, source type, and source ID columns. |
| Topic resource pack | Topic mode, `Quadratic equations by factoring`, `Full Resource Pack`, `Easy`, count `5` | Download Resource Pack Markdown, Download Resource Pack HTML, Download Resource Pack LibGuides-Safe HTML, Download Resource Pack Export Bundle, Download Resource Pack Canvas Manual-Entry Quiz CSV | Resource-pack tabs show worksheet, solution key, study guide, common mistakes, tutor notes, and practice quiz; Markdown and standard HTML include all resource-pack sections; standard HTML print preview keeps major sections readable; ZIP contains Markdown plus standard HTML only; Canvas CSV is labeled manual-entry/import-friendly and represents the practice quiz. |
| Learning Objective worksheet | Learning Objective mode, `College Algebra`, any module/objective, `Worksheet only`, count `3` | Download Worksheet Markdown, Download Worksheet HTML, Download Worksheet LibGuides-Safe HTML, Download Worksheet Export Bundle, Download Worksheet Canvas Manual-Entry CSV | Course, module, objective, mapped topic, and planned output type appear before generation; generated-output summary identifies Learning Objective mode; worksheet export filenames are clear and deterministic; raw export text areas remain readable. |
| Learning Objective resource pack | Learning Objective mode, `College Algebra`, `Systems of Equations`, `Solve systems of linear equations in two variables`, `Full Resource Pack`, count `3` | Download Resource Pack Markdown, Download Resource Pack HTML, Download Resource Pack LibGuides-Safe HTML, Download Resource Pack Export Bundle, Download Resource Pack Canvas Manual-Entry Quiz CSV | Resource pack aligns with the selected objective; study guide, common mistakes, tutor notes, and practice quiz are present; standard HTML browser view and print preview are readable; LibGuides-safe HTML remains a separate scoped fragment and is not included in the ZIP bundle. |

### Topic-Aware Difficulty UI Checks

Use these checks after any change to topic routing, presets, registry metadata, or Streamlit controls. This section prepares the QA pass only; do not mark it passed until a human reviewer runs the scenarios.

| Scenario | Inputs | Manual checks |
| --- | --- | --- |
| Expanded-difficulty Topic mode worksheet | Topic mode, `Linear equations`, `Quadratic equations by factoring`, and `Systems of linear equations`, `Worksheet only`, each of `Easy`, `Medium`, and `Hard` | Difficulty selector shows exactly `Easy`, `Medium`, and `Hard`; each difficulty generates without a stack trace; worksheet, solution key, exports tab, individual downloads, ZIP bundle, Canvas CSV, and LibGuides-safe HTML controls still appear; generated-output summary shows the selected difficulty. |
| Expanded-difficulty Topic mode resource pack | Topic mode, `Linear equations`, `Quadratic equations by factoring`, and `Systems of linear equations`, `Full Resource Pack`, each of `Easy`, `Medium`, and `Hard` | Difficulty selector shows exactly `Easy`, `Medium`, and `Hard`; each difficulty generates a full resource pack; study guide, common mistakes, tutor notes, practice quiz, export buttons, and generated-output summary remain present; summary reflects the selected difficulty. |
| Easy-only Topic mode coverage | Topic mode, each remaining Easy-only topic, `Worksheet only`, `Easy` | Factoring techniques and functions basics each show only `Easy`; generation still succeeds; export buttons still appear. |
| Expanded-difficulty Learning Objective mode | Learning Objective mode, `College Algebra`, Linear Equations, Quadratic Equations, and Systems of Equations modules, worksheet or resource pack | Difficulty selector shows exactly `Easy`, `Medium`, and `Hard`; generated-output summary identifies Learning Objective mode, mapped topic, and the selected difficulty. |
| Easy-only Learning Objective mode coverage | Learning Objective mode, each remaining Easy-only College Algebra module/objective | Difficulty selector shows only `Easy`; generated output remains aligned to the selected objective; export buttons still appear. |
| Preset defaults | Select each built-in preset before changing topic/objective | Presets still default difficulty to `Easy`; preset-selected values remain editable; selecting a Medium/Hard-capable topic does not change presets into Medium/Hard presets. |

### Cross-Cutting Manual Checks

- Keyboard: tab through controls and export areas; confirm the page can be navigated and scrolled without mouse-only requirements.
- Browser zoom: check generated previews and downloaded HTML at 125% and 200% zoom.
- Copy/paste: copy Markdown, standard HTML text, Canvas CSV text, and LibGuides-safe HTML text into a plain-text editor; confirm content remains readable.
- Standard HTML browser view: confirm headings, lists, worksheet sections, solution keys, and resource-pack sections render without broken markup.
- Standard HTML print preview: confirm `Worksheet`, `Solution Key`, `Study Guide`, `Common Mistakes`, `Tutor Notes`, and `Practice Quiz` sections remain legible; MathForge does not generate PDF files.
- ZIP bundles: confirm bundles contain Markdown plus standard HTML only; Canvas CSV and LibGuides-safe HTML remain separate downloads.
- LibGuides-safe HTML: paste into a LibGuides-style HTML editor or safe HTML sandbox; confirm the `mathforge-libguides-export` wrapper is present and surrounding page styles/headings are not affected.
- Accessibility/readability: confirm meaning does not rely on color alone, heading text is descriptive, lists match the visual grouping, and plain-text math notation remains understandable.
- Error/empty state: confirm count bounds, supported-topic-only selectors, supported difficulty selector, and no stack traces during normal workflows.

### QA Results Template

Use this template when the human review is complete:

```text
Date:
Reviewer:
Environment/browser:
Automated test command/result:
Scenarios tested:
Pass/fail summary:
Issues found:
Follow-up actions:
Notes on standard HTML print preview:
Notes on LibGuides-safe copy/paste:
Notes on Canvas CSV manual-entry usability:
Notes on topic-aware difficulty UI:
```

## Launch

Install dependencies if needed:

```bash
pip install -r requirements.txt
```

Run the Streamlit app:

```bash
streamlit run app/main.py
```

Run the test suite before manual review:

```bash
python -B -m pytest -p no:cacheprovider tests
```

## Streamlit App Workflow

Review both generation modes and both output types.

### Presets

- Confirm the built-in presets appear: `Quick Worksheet`, `Standard Practice Set`, and `Full Tutor Resource Pack`.
- Select each preset and confirm it updates the starting defaults for output type and problem count.
- Confirm preset-selected values can still be manually changed before clicking `Generate`.
- Confirm presets do not add saved custom presets, accounts, persistence, or file-based configuration.

### Topic Mode

- Select `Topic mode`.
- Confirm only currently supported topics appear.
- Generate a worksheet for each supported topic at the default difficulty.
- Confirm the generated worksheet title matches the selected topic.
- Confirm the problem count matches the requested count.
- Confirm the advanced `Problem ID prefix` default is topic-specific.
- Confirm changing the problem count updates the generated output after clicking `Generate`.
- Confirm Linear equations, Quadratic equations by factoring, and Systems of linear equations expose `Easy`, `Medium`, and `Hard`.
- Confirm all remaining supported topics expose only `Easy`.
- Generate Linear equations, Quadratic equations by factoring, and Systems of linear equations worksheets and resource packs at `Easy`, `Medium`, and `Hard`.
- Confirm generated-output summaries show the selected difficulty.

### Learning Objective Mode

- Select `Learning Objective mode`.
- Confirm the selection flow is readable: Course, Module, Learning Objective.
- Confirm `College Algebra` appears as the current course.
- Select each module and confirm its learning objective is readable.
- Confirm the selected learning objective caption appears before generation.
- Confirm the Learning Objective Context summary appears before generation.
- Confirm the context summary includes course, module, selected objective, mapped topic, and planned output type.
- Generate output from at least one objective and confirm it matches the selected topic.
- Confirm the generated-output summary identifies `Learning Objective mode` and includes course, module, objective, and mapped topic.
- Confirm Linear Equations, Quadratic Equations, and Systems of Equations objectives expose `Easy`, `Medium`, and `Hard`.
- Confirm remaining objectives expose only `Easy`.
- Confirm generated-output summaries show the selected difficulty.

### Worksheet Only

- Select `Worksheet only`.
- Generate output in Topic mode and Learning Objective mode.
- Confirm the tabs are limited to worksheet, solution key, and exports.
- Confirm the worksheet preview lists numbered problems.
- Confirm the solution key preview includes answers and solution steps.
- Confirm the generated-output summary appears in the exports area before download buttons and raw export text.
- Confirm the summary includes output type, context, difficulty, problem count, problem ID prefix, export filenames, and available download types.
- Confirm Markdown, HTML, and LibGuides-safe HTML download buttons are present.
- Confirm the worksheet export bundle download is present and does not replace the individual downloads.
- Confirm the Canvas manual-entry CSV download is present as a separate optional export.
- Expand raw Markdown, HTML, and LibGuides-safe HTML export text areas and confirm they are readable.
- Expand the raw Canvas CSV text area and confirm it is readable as CSV.

### Full Resource Pack

- Select `Full Resource Pack`.
- Generate output in Topic mode and Learning Objective mode.
- Confirm the tabs include worksheet, solution key, study guide, common mistakes, tutor notes, practice quiz, and exports.
- Confirm study guide content has an overview, key ideas, and worked-example guidance.
- Confirm common mistakes include mistakes and corrections.
- Confirm tutor notes include notes and discussion prompts.
- Confirm the practice quiz includes questions and an answer key.
- Confirm the generated-output summary appears in the exports area before download buttons and raw export text.
- Confirm the summary identifies `Full Resource Pack` and includes resource-pack export filenames.
- Confirm Resource Pack Markdown, HTML, and LibGuides-safe HTML download buttons are present.
- Confirm the resource-pack export bundle download is present and does not replace the individual downloads.
- Confirm the Resource Pack Canvas manual-entry quiz CSV download is present when a practice quiz exists.
- Expand raw export text areas and confirm the content includes all resource-pack sections.

### Downloads

- Download worksheet Markdown and HTML.
- Download worksheet LibGuides-safe HTML.
- Download resource-pack Markdown and HTML.
- Download resource-pack LibGuides-safe HTML.
- Download worksheet and resource-pack Canvas manual-entry CSV files.
- Download worksheet and resource-pack ZIP bundles.
- Confirm filenames are clear and deterministic.
- Confirm filenames identify MathForge, the topic or learning-objective context, the output type, the problem ID prefix, and the file format.
- Confirm custom problem ID prefixes with spaces, punctuation, or path-like characters are sanitized in filenames.
- Confirm ZIP bundles contain the same Markdown and HTML files offered by the individual buttons.
- Confirm ZIP bundles still contain Markdown and standard HTML only; LibGuides-safe HTML remains a separate download.
- Confirm Canvas CSV files include question title, prompt, answer, explanation, topic, difficulty, problem ID, source type, and source ID columns.
- Confirm Canvas CSV files are labeled as manual-entry/import-friendly exports, not direct Canvas publishing.
- Open downloaded HTML in a browser and confirm it renders without obvious broken markup.
- Open standard HTML in browser print preview and confirm worksheet, solution key, and resource-pack sections remain readable.
- Paste LibGuides-safe HTML into a test LibGuides-style content area or HTML sandbox and confirm it does not alter page/global headings or surrounding content.
- Open downloaded Markdown in a text editor and confirm it is readable as plain text.

### Error and Empty-State Behavior

The current UI constrains most inputs to valid values. For manual review:

- Confirm count cannot be set below 1 or above 25.
- Confirm unsupported topics are not exposed in the Topic mode selector.
- Confirm unsupported difficulty levels are not exposed for the selected topic.
- Confirm the app does not show stack traces during normal generation.
- If a generation failure is intentionally triggered during development, confirm the user-facing error is understandable and does not expose internal stack traces.

## Exported HTML Accessibility Review

Use a browser and basic keyboard navigation. When practical, also inspect the HTML source or browser developer tools.

### Structure

- Confirm exported HTML starts at `h2` or lower, not `h1`, so it can be embedded in Canvas or LibGuides.
- Confirm headings follow a sensible order.
- Confirm worksheet, instructions, problems, solution key, study guide, common mistakes, tutor notes, and practice quiz appear in semantic sections.
- Confirm ordered lists are used for problems, solution steps, and quiz questions.
- Confirm unordered lists are used for guidance, mistakes, corrections, tutor notes, and answer keys where appropriate.
- Confirm no layout tables are introduced.

### Readability

- Confirm math expressions are readable as plain text.
- Confirm line breaks in systems of equations remain understandable.
- Confirm solution steps are visually grouped with the correct answer.
- Confirm resource-pack sections are easy to scan.
- Confirm content remains readable at browser zoom levels such as 125% and 200%.

### Keyboard and Browser Usability

- Confirm downloaded HTML opens in a standard browser.
- Confirm the page can be navigated with keyboard scrolling.
- Confirm text can be selected and copied.
- Confirm links or buttons are not required inside exported content.
- Confirm browser print preview is readable and does not hide important sections.

### Standard HTML Print Review

- Confirm standard HTML, not LibGuides-safe HTML, contains print-focused CSS.
- Confirm browser print preview keeps headings with the content that follows where practical.
- Confirm individual problems, solution entries, and quiz questions do not split awkwardly across pages where practical.
- Confirm solution keys and major resource-pack sections start and flow legibly in print preview.
- Confirm print behavior uses ordinary browser HTML/CSS only; MathForge does not generate PDF files.

### Accessibility Considerations

- Confirm meaning does not rely on color alone.
- Confirm heading text is descriptive.
- Confirm list structure matches the visual grouping.
- Confirm exported fragments are portable enough to paste into an LMS content editor.
- Note any limitations caused by plain-text math notation so they can be addressed in future accessibility work.

## LibGuides-Safe HTML Review

- Confirm the export is wrapped in `mathforge-libguides-export`.
- Confirm embedded headings start at `h3` or lower.
- Confirm no `h1` or `h2` headings appear in the exported fragment.
- Confirm CSS selectors are scoped to the MathForge wrapper and do not target global page elements.
- Confirm no scripts, external fonts, or external stylesheets are included.
- Confirm the fragment can be copied into a LibGuides-style HTML editor without changing surrounding page styles.
- Note that this check verifies paste-friendly behavior only; it does not certify compatibility with every institutional LibGuides configuration.

## Exported Markdown Review

- Confirm the worksheet title is a top-level heading.
- Confirm instructions, problems, solution key, and resource-pack sections use consistent headings.
- Confirm problem numbering is stable and readable.
- Confirm solution steps are nested or grouped under the correct answer.
- Confirm study guide, common mistakes, tutor notes, and practice quiz sections appear in full resource-pack exports.
- Confirm Markdown-sensitive math text remains readable after escaping.
- Confirm content is usable when copied into a plain-text editor, Markdown editor, or LMS rich-text field.

## Pre-Release Manual QA Checklist

- [ ] Full automated test suite passes locally.
- [ ] Streamlit app launches with `streamlit run app/main.py`.
- [ ] Built-in presets provide editable defaults for common workflows.
- [ ] Topic mode generates worksheet-only output for every supported topic.
- [ ] Topic mode generates full resource packs for every supported topic.
- [ ] Topic mode exposes Medium and Hard only for Linear equations, Quadratic equations by factoring, and Systems of linear equations.
- [ ] Linear equations, Quadratic equations by factoring, and Systems of linear equations generate worksheet-only and full resource-pack output at Easy, Medium, and Hard.
- [ ] Learning Objective mode exposes College Algebra modules and objectives.
- [ ] Learning Objective mode derives difficulty options from the mapped topic.
- [ ] Learning Objective mode shows course/module/objective context and mapped topic before generation.
- [ ] Learning Objective mode generates at least one worksheet and one full resource pack.
- [ ] Worksheet previews show problems and solution steps.
- [ ] Resource-pack previews show study guide, common mistakes, tutor notes, and practice quiz.
- [ ] Generated-output summaries appear before export downloads and include filename/download context.
- [ ] Markdown export text areas and downloads work for worksheet-only and resource-pack output.
- [ ] HTML export text areas and downloads work for worksheet-only and resource-pack output.
- [ ] LibGuides-safe HTML export text areas and downloads work for worksheet-only and resource-pack output.
- [ ] Canvas manual-entry CSV text areas and downloads work for worksheet-only and resource-pack output.
- [ ] ZIP export bundles download for worksheet-only and resource-pack output.
- [ ] Downloaded HTML opens in a browser and has sensible semantic structure.
- [ ] Standard HTML print preview keeps worksheet and resource-pack sections readable.
- [ ] Downloaded Markdown is readable when opened as plain text.
- [ ] Browser zoom and print preview remain readable.
- [ ] No normal workflow exposes a stack trace to the user.
- [ ] Any observed accessibility or usability limitation is documented before release.

## Known Manual QA Gaps

- There is no automated browser regression suite yet.
- There is no automated accessibility scanner configured.
- There is no screen-reader-specific test script yet.
- Plain-text math notation is readable but not equivalent to MathML or fully accessible equation rendering.
- Streamlit component accessibility depends partly on Streamlit itself.
- Canvas CSV compatibility may vary by institution and may require manual cleanup before import or quiz creation.
