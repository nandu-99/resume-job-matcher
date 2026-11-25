# Interface refinement

## Direction and audit

The interface supports recruiter review of a resume against a job description. Its character is composed, precise, and considered. The visual reference is a hiring desk: white paper, graphite type, clear document labels. The two document panels and fit label carry the hierarchy. Numbered document headings provide a small, consistent signature.

The original palette was already restrained. The audit found repeated guidance, excess vertical spacing, similar visual weight for secondary and primary actions, unclear document context above the input selectors, and a PDF flow that grew substantially after extraction. The user requested a broader UX refinement, including desktop first-fold fit and explicit loading feedback, while retaining the white theme.

## Changes by pass

| Pass | Implementation |
|---|---|
| Spacing | Compact page heading, 8/12/16/24/32-pixel spacing, shorter text editors, and tighter result content |
| Color | White page and document surfaces; one graphite text ramp and a dark primary action |
| Icons | Numbered document labels; no decorative emoji or additional icon library |
| Copy | Short document-specific prompts, concise readiness guidance, and privacy detail in an expander |
| Type | System interface text with Georgia for the product heading and fit result; tabular character counts |
| Layout | Paired document panels, header-level example/Clear actions, then analysis and result in the existing section order |
| Details | Document readiness labels, consistently rounded controls, focus rings, a shared-height source row, and PDF/OCR controls in a popover |
| Visuals | The actual document workspace and result provide the visual focus; no generated image or decorative chart |
| Motion | Short color/border transitions and native progress indicators only while work is running; reduced-motion support |

## Interaction states

An action callback records a pending operation before the next render. That render disables editing, input switching, upload controls, example/Clear, and repeat analysis before performing the operation. The result area shows a native running status with a description of the real work. It does not display a fabricated percentage or staged progress timer.

A placeholder clears previous result content before showing the running state. On completion or a handled failure, pending state is cleared and the page reruns with controls available. Error references and entered text follow the existing safe-error policy. Changing a document or OCR setting still invalidates extracted text and old results. Reviewed text remains editable.

PDF source controls open in a popover so the extracted text and analysis action remain aligned. The user can reopen PDF source to replace the file or enable OCR on every page. An unread PDF shows a disabled preview with an instruction to read it first. Text and PDF modes reserve the same source-row height so editor tops and panel bottoms align, including mixed input modes. Extracted text is applied before widgets are rendered on the next run. Example and Clear retain their existing behaviour.

## Verification

The local test suite covers the existing inference and PDF/OCR flows, error recovery, and clearing. Browser checks use the actual saved CPU checkpoint, synthetic PDFs, desktop and mobile viewports, and the running PDF state. All 38 tests passed, including the 30 saved prediction checks. Browser measurements at 1440 pixels verify equal panel heights, editor tops at the same measured position, and an 8-pixel gap from the result heading to its description for empty, prediction, mixed-input, and two-PDF states. At 1366 by 768 pixels, the result ends at approximately 708 pixels with two PDFs ready for review. White mobile layouts at 390 and 320 pixels stack the document panels without horizontal overflow and keep the header buttons on one row. The browser also verifies real model prediction and reopening the PDF source. Measurements are recorded in [ui_verification.json](ui_verification.json).

First-fold fit targets ordinary desktop viewports. Mobile keeps document inputs at readable sizes and stacks them in order; scrolling is expected. Document text can scroll within its editor. Accessibility includes meaningful native input labels, visible focus styles, white backgrounds with a dark system preference, and reduced-motion support.

The matching model, input limit, dataset, training, and saved evaluation are unchanged. The hosted text-service benchmark remains separate evidence and does not establish PDF/OCR latency or hosted verification of this UI update.

## Design reference

Refinement used [unslop](https://heydamir.design/unslop) by [Damir Sokolovsky (@heydamir)](https://x.com/heydamir), licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Its audit and craft guidance informed this adaptation; no generated image or image prompt was used.

## Layout safeguards

Streamlit 1.67 applies a negative bottom margin to its markdown wrapper. The interface removes that wrapper compensation when applying its own paragraph and heading spacing, preventing text from extending into the following row. Border styling targets the actual panel and textarea root rather than all panel children, preserving complete step-marker and input borders. Browser geometry checks measure rendered text boxes and panel edges instead of using first-fold fit alone as a layout check.
