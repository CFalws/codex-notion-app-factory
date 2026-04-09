#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]


def read(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


def require(content: str, needle: str, *, label: str) -> None:
    if needle not in content:
        raise AssertionError(f"missing {label}: {needle}")


def main() -> int:
    app_js = read("examples/generated_apps/codex-ops-console/web/app.js")
    api_js = read("examples/generated_apps/codex-ops-console/web/ops-api.js")
    conversations_js = read("examples/generated_apps/codex-ops-console/web/ops-conversations.js")
    jobs_js = read("examples/generated_apps/codex-ops-console/web/ops-jobs.js")
    render_js = read("examples/generated_apps/codex-ops-console/web/ops-render.js")
    store_js = read("examples/generated_apps/codex-ops-console/web/ops-store.js")
    index_html = read("examples/generated_apps/codex-ops-console/web/index.html")
    autonomy_index = index_html.index('id="autonomy-summary"')
    thread_scroller_index = index_html.index('id="thread-scroller"')
    if autonomy_index > thread_scroller_index:
        raise AssertionError("autonomy summary still appears inside the scrollable timeline region")

    require(api_js, "/api/internal/conversations/${conversationId}/append-stream", label="append SSE URL builder")
    require(conversations_js, "new window.EventSource(internalConversationAppendStreamUrl(conversationId))", label="EventSource wiring")
    require(conversations_js, 'addEventListener("conversation.append"', label="append event listener")
    require(conversations_js, "appendEnvelope.conversation_id !== activeConversationId", label="cross-conversation guard")
    require(conversations_js, "appendId <= Number(state.appendStream?.lastAppendId || 0)", label="append_id dedupe")
    require(conversations_js, 'state.appendStream.status = "connecting"', label="connecting state")
    require(conversations_js, 'state.appendStream.status = "live"', label="live state")
    require(conversations_js, 'state.appendStream.status = "reconnecting"', label="reconnecting state")
    require(conversations_js, 'delivery_source: "sse"', label="SSE provenance tagging")
    require(conversations_js, "state.appendStream.transport = \"sse\"", label="SSE transport evidence")
    require(jobs_js, "!isAppendStreamConnected(state, state.currentConversationId)", label="polling refetch skip while connected")
    require(render_js, "LIVE · SSE append #", label="live indicator copy")
    require(render_js, "deriveLiveRunState", label="inline live run state derivation")
    require(render_js, "dataset.liveRunState", label="live run state dataset")
    require(render_js, "dataset.liveRunSource", label="live run source dataset")
    require(render_js, "data-append-source", label="append provenance attribute")
    require(render_js, "dataset.streamState = status", label="stream-state dataset")
    require(render_js, "dataset.renderSource = lastRenderSource", label="render-source dataset")
    require(store_js, "appendStream", label="append stream state")
    require(store_js, "isAppendStreamConnected", label="append stream connection helper")
    require(index_html, 'id="conversation-live-status"', label="live indicator DOM")
    require(index_html, 'id="live-run-row"', label="live run row DOM")
    require(index_html, 'id="append-stream-strip"', label="stream strip DOM")
    require(index_html, 'class="autonomy-rail"', label="header-adjacent autonomy rail DOM")
    require(app_js, "internalConversationAppendStreamUrl", label="controller dependency wiring")
    print("ok: ops append SSE wiring, inline live run row, and autonomy rail are present")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as error:
        print(f"verification failed: {error}", file=sys.stderr)
        raise SystemExit(1)
