"""Browser capture schema records without live browser scraping."""

from __future__ import annotations

import hashlib
from dataclasses import asdict, dataclass
from typing import Literal
from urllib.parse import urlparse

CaptureProvider = Literal["manual", "browser_export", "recorded_fixture"]
CaptureStatus = Literal["captured", "partial", "failed"]
CaptureArtifactType = Literal["html", "screenshot", "markdown", "accessibility_tree", "network_summary"]


class BrowserCaptureError(ValueError):
    pass


@dataclass(frozen=True)
class BrowserViewport:
    width: int
    height: int
    device_scale_factor: float = 1.0

    def __post_init__(self) -> None:
        if self.width <= 0 or self.height <= 0:
            raise BrowserCaptureError("Viewport width and height must be positive.")
        if self.device_scale_factor <= 0:
            raise BrowserCaptureError("Viewport device scale factor must be positive.")

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(frozen=True)
class BrowserCaptureArtifact:
    artifact_id: str
    artifact_type: CaptureArtifactType
    media_type: str
    sha256: str
    size_bytes: int
    redacted: bool = True

    def __post_init__(self) -> None:
        if not self.artifact_id.strip():
            raise BrowserCaptureError("Artifact id is required.")
        if len(self.sha256) != 64:
            raise BrowserCaptureError("Artifact sha256 must be a hex digest.")
        if self.size_bytes < 0:
            raise BrowserCaptureError("Artifact size must be non-negative.")

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(frozen=True)
class BrowserCaptureRecord:
    capture_id: str
    url: str
    provider: CaptureProvider
    status: CaptureStatus
    captured_at: str
    viewport: BrowserViewport
    artifacts: tuple[BrowserCaptureArtifact, ...]
    notes: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.capture_id.strip():
            raise BrowserCaptureError("Capture id is required.")
        parsed = urlparse(self.url)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise BrowserCaptureError(f"Invalid capture URL: {self.url}")
        if not self.captured_at.strip():
            raise BrowserCaptureError("captured_at is required.")
        if self.status == "captured" and not self.artifacts:
            raise BrowserCaptureError("Captured records must include at least one artifact.")

    def to_dict(self) -> dict[str, object]:
        return {
            "capture_id": self.capture_id,
            "url": self.url,
            "provider": self.provider,
            "status": self.status,
            "captured_at": self.captured_at,
            "viewport": self.viewport.to_dict(),
            "artifacts": [artifact.to_dict() for artifact in self.artifacts],
            "notes": list(self.notes),
        }


def artifact_digest(content: str | bytes) -> str:
    data = content.encode("utf-8") if isinstance(content, str) else content
    return hashlib.sha256(data).hexdigest()


def make_capture_artifact(artifact_id: str, artifact_type: CaptureArtifactType, media_type: str, content: str | bytes, *, redacted: bool = True) -> BrowserCaptureArtifact:
    data = content.encode("utf-8") if isinstance(content, str) else content
    return BrowserCaptureArtifact(artifact_id, artifact_type, media_type, artifact_digest(data), len(data), redacted)
