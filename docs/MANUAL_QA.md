# Manual QA and Accessibility Review

This guide covers manual review for the MathForge Streamlit MVP and exported instructional materials. It is intentionally tool-light: use it before major topic, exporter, model, or UI changes without adding browser automation or accessibility tooling.

MathForge is deterministic and instructor-reviewable. Manual QA should confirm both the application workflow and the generated materials remain clear, accurate, readable, and accessible enough for classroom review.

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

### Learning Objective Mode

- Select `Learning Objective mode`.
- Confirm the selection flow is readable: Course, Module, Learning Objective.
- Confirm `College Algebra` appears as the current course.
- Select each module and confirm its learning objective is readable.
- Confirm the selected learning objective caption appears before generation.
- Generate output from at least one objective and confirm it matches the selected topic.

### Worksheet Only

- Select `Worksheet only`.
- Generate output in Topic mode and Learning Objective mode.
- Confirm the tabs are limited to worksheet, solution key, and exports.
- Confirm the worksheet preview lists numbered problems.
- Confirm the solution key preview includes answers and solution steps.
- Confirm Markdown and HTML download buttons are present.
- Confirm the worksheet export bundle download is present and does not replace the individual downloads.
- Expand raw Markdown and HTML export text areas and confirm they are readable.

### Full Resource Pack

- Select `Full Resource Pack`.
- Generate output in Topic mode and Learning Objective mode.
- Confirm the tabs include worksheet, solution key, study guide, common mistakes, tutor notes, practice quiz, and exports.
- Confirm study guide content has an overview, key ideas, and worked-example guidance.
- Confirm common mistakes include mistakes and corrections.
- Confirm tutor notes include notes and discussion prompts.
- Confirm the practice quiz includes questions and an answer key.
- Confirm Resource Pack Markdown and HTML download buttons are present.
- Confirm the resource-pack export bundle download is present and does not replace the individual downloads.
- Expand raw export text areas and confirm the content includes all resource-pack sections.

### Downloads

- Download worksheet Markdown and HTML.
- Download resource-pack Markdown and HTML.
- Download worksheet and resource-pack ZIP bundles.
- Confirm filenames are clear and deterministic.
- Confirm filenames identify MathForge, the topic or learning-objective context, the output type, the problem ID prefix, and the file format.
- Confirm custom problem ID prefixes with spaces, punctuation, or path-like characters are sanitized in filenames.
- Confirm ZIP bundles contain the same Markdown and HTML files offered by the individual buttons.
- Open downloaded HTML in a browser and confirm it renders without obvious broken markup.
- Open downloaded Markdown in a text editor and confirm it is readable as plain text.

### Error and Empty-State Behavior

The current UI constrains most inputs to valid values. For manual review:

- Confirm count cannot be set below 1 or above 25.
- Confirm unsupported topics are not exposed in the Topic mode selector.
- Confirm unsupported difficulty levels are not exposed.
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

### Accessibility Considerations

- Confirm meaning does not rely on color alone.
- Confirm heading text is descriptive.
- Confirm list structure matches the visual grouping.
- Confirm exported fragments are portable enough to paste into an LMS content editor.
- Note any limitations caused by plain-text math notation so they can be addressed in future accessibility work.

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
- [ ] Learning Objective mode exposes College Algebra modules and objectives.
- [ ] Learning Objective mode generates at least one worksheet and one full resource pack.
- [ ] Worksheet previews show problems and solution steps.
- [ ] Resource-pack previews show study guide, common mistakes, tutor notes, and practice quiz.
- [ ] Markdown export text areas and downloads work for worksheet-only and resource-pack output.
- [ ] HTML export text areas and downloads work for worksheet-only and resource-pack output.
- [ ] ZIP export bundles download for worksheet-only and resource-pack output.
- [ ] Downloaded HTML opens in a browser and has sensible semantic structure.
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
