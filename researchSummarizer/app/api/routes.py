from fastapi import APIRouter,HTTPException
from researchSummarizer.app.services.citations import extract_citations, strip_citations

router = APIRouter()
@router.post("/summarize/text")
def summarize_text(
    paperText: str | None = None,
    fileText: str | None = None,
    summaryLength: str = "medium",     # chosen by button, not by typing
    includeCitations: bool = False,
):
    # --- 0) Validate summaryLength comes from 3-button choice --- #
    valid_choices = {"short", "medium", "long"}
    if summaryLength not in valid_choices:
        raise HTTPException(
            status_code=400,
            detail="summaryLength must be one of: short, medium, long"
        )

    # --- 1) Ensure ONLY one input method is used --- #
    if (paperText and paperText.strip()) and (fileText and fileText.strip()):
        raise HTTPException(
            status_code=400,
            detail="Provide either paperText OR fileText, not both."
        )

    if not (paperText and paperText.strip()) and not (fileText and fileText.strip()):
        raise HTTPException(
            status_code=400,
            detail="No input provided. Send paperText (pasted) OR fileText (extracted)."
        )

    # --- 2) Select text source --- #
    text = paperText.strip() if paperText else fileText.strip()

    # --- 3) Placeholder summary --- #
    response_summary = f"[PLACEHOLDER SUMMARY - {summaryLength}]"

    # --- 4) Citations --- #
    if includeCitations:
        citations = extract_citations(text)
        return {
            "summary": response_summary,
            "citations": citations
        }

    return {"summary": response_summary}

from fastapi import File, UploadFile
import tempfile
from researchSummarizer.app.services.extractor import extract_text_from_bytes



@router.post("/summarize/file")
async def summarize_file(
    file: UploadFile = File(...),
    summaryLength: str = "medium",   # passed as query param / button selection
    includeCitations: bool = False,
):
    """
    Accepts a PDF or DOCX upload, extracts text, and delegates to summarize_text.
    """
    # 1) Validate summaryLength early
    if summaryLength not in {"short", "medium", "long"}:
        raise HTTPException(status_code=400, detail="summaryLength must be: short | medium | long")

    # 2) Validate content-type / extension
    filename = file.filename or "uploaded"
    if not (filename.lower().endswith(".pdf") or filename.lower().endswith(".docx")):
        raise HTTPException(status_code=415, detail="Unsupported file type. Use PDF or DOCX.")

    # 3) Read bytes (careful with huge files; you can add size checks here)
    contents = await file.read()

    # 4) Extract text
    extracted = extract_text_from_bytes(filename, contents)
    if not extracted:
        raise HTTPException(status_code=400, detail="Could not extract text from the uploaded file.")

    # 5) Delegate to existing summarize_text function by calling it with fileText
    #    Note: summarize_text is a normal function (not async). We call it directly.
    result = summarize_text(fileText=extracted, summaryLength=summaryLength, includeCitations=includeCitations)

    # 6) Add filename metadata to result so frontend can show what was processed
    result["filename"] = filename
    # Optionally include a short preview
    result["preview"] = extracted[:800] + ("..." if len(extracted) > 800 else "")

    return result
