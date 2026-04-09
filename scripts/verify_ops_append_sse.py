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


def require_absent(content: str, needle: str, *, label: str) -> None:
    if needle in content:
        raise AssertionError(f"unexpected {label}: {needle}")


def main() -> int:
    app_js = read("examples/generated_apps/codex-ops-console/web/app.js")
    api_js = read("examples/generated_apps/codex-ops-console/web/ops-api.js")
    conversations_js = read("examples/generated_apps/codex-ops-console/web/ops-conversations.js")
    jobs_js = read("examples/generated_apps/codex-ops-console/web/ops-jobs.js")
    render_js = read("examples/generated_apps/codex-ops-console/web/ops-render.js")
    store_js = read("examples/generated_apps/codex-ops-console/web/ops-store.js")
    styles_css = read("examples/generated_apps/codex-ops-console/web/styles.css")
    index_html = read("examples/generated_apps/codex-ops-console/web/index.html")
    autonomy_detail_index = index_html.index('id="autonomy-detail"')
    thread_scroller_index = index_html.index('id="thread-scroller"')
    footer_dock_index = index_html.index('id="conversation-footer-dock"')
    composer_shell_index = index_html.index('class="composer-shell"')
    session_strip_index = index_html.index('id="session-strip"')
    draft_status_index = index_html.index('id="draft-status"')
    composer_footer_index = index_html.index('class="composer-footer"')
    sidebar_index = index_html.index('<aside class="sidebar panel">')
    main_stage_index = index_html.index('<section class="main-stage panel">')
    secondary_panel_index = index_html.index('id="secondary-panel"')
    if not (secondary_panel_index < autonomy_detail_index):
        raise AssertionError("detailed autonomy summary is no longer reachable through the secondary panel")
    if not (thread_scroller_index < footer_dock_index < composer_shell_index):
        raise AssertionError("footer dock does not wrap the session strip and composer after the thread scroller")
    if not (composer_shell_index < session_strip_index < draft_status_index < composer_footer_index):
        raise AssertionError("composer-adjacent activity bar no longer sits inside the composer shell ahead of footer actions")
    if not (sidebar_index < main_stage_index < secondary_panel_index):
        raise AssertionError("desktop workspace no longer uses sidebar, main stage, then secondary panel order")

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
    require(conversations_js, "syncConversationCardState", label="conversation card state sync helper")
    require(conversations_js, "showPendingOutgoing", label="pending outgoing render helper")
    require(conversations_js, "clearPendingOutgoing", label="pending outgoing clear helper")
    require(conversations_js, "showPendingAssistant", label="pending assistant handoff helper")
    require(conversations_js, "shouldClearPendingOutgoing", label="pending handoff clear predicate")
    require(conversations_js, "data-conversation-live-state", label="conversation card live state marker")
    require(conversations_js, "dom.threadScroller?.dataset.sessionPresentation", label="left rail uses session presentation state")
    require(jobs_js, "!isAppendStreamConnected(state, state.currentConversationId)", label="polling refetch skip while connected")
    require(render_js, "deriveLiveRunState", label="inline live run state derivation")
    require(render_js, "dom.heroConversationState", label="hero conversation state null-safe wiring")
    require(render_js, "dom.heroJobState", label="hero job state null-safe wiring")
    require(render_js, 'state: "sending"', label="local pending sending state")
    require(render_js, 'state: "generating"', label="assistant placeholder generating state")
    require(render_js, "renderSessionStrip", label="unified session strip renderer")
    require(render_js, 'presentation === "sending"', label="sending presentation state")
    require(render_js, "LOCAL HANDOFF", label="local handoff activity label")
    require(render_js, 'data-pending-local="true"', label="pending local timeline marker")
    require(render_js, 'data-pending-assistant="true"', label="pending assistant timeline marker")
    require(render_js, "local-pending", label="pending local render source")
    require(render_js, "local-assistant-placeholder", label="assistant placeholder render source")
    require(render_js, "autonomyContextStrip.hidden = true", label="compact autonomy context clear state")
    require(render_js, "autonomyContextStrip.hidden = false", label="compact autonomy context active state")
    require(render_js, "autonomyDetailMeta", label="secondary panel autonomy detail meta wiring")
    require(render_js, "autonomy-context-line", label="compact autonomy context markup")
    require(render_js, "autonomy-context-iteration", label="compact autonomy iteration markup")
    require(render_js, "dataset.sessionPresentation", label="session strip presentation dataset")
    require(render_js, "dataset.sessionTerminal", label="session strip terminal dataset")
    require(render_js, 'presentation === "idle" || presentation === "terminal"', label="idle or terminal collapse rule")
    require(render_js, "dataset.liveRunState", label="live run state dataset")
    require(render_js, "dataset.liveRunSource", label="live run source dataset")
    require(render_js, "data-append-source", label="append provenance attribute")
    require(render_js, "dataset.streamState = status", label="stream-state dataset")
    require(render_js, "dataset.renderSource = lastRenderSource", label="render-source dataset")
    require(conversations_js, 'dom.threadScroller.dataset.pendingConversationId = conversationId', label="thread switch pending marker")
    require(conversations_js, "state.currentConversationId && state.currentConversationId !== conversationId", label="thread switch clear guard")
    require(store_js, "appendStream", label="append stream state")
    require(store_js, "pendingOutgoing", label="pending outgoing state")
    require(store_js, "assistantCreatedAt", label="assistant placeholder pending timestamp state")
    require(store_js, "baselineAppendId", label="pending handoff baseline append id state")
    require(store_js, "isAppendStreamConnected", label="append stream connection helper")
    require(index_html, 'id="session-strip"', label="session strip DOM")
    require(index_html, 'id="session-strip-state"', label="session strip state DOM")
    require(index_html, 'id="session-strip-meta"', label="session strip meta DOM")
    require(index_html, 'id="session-strip-detail"', label="session strip detail DOM")
    require(index_html, 'data-activity-bar="composer-adjacent"', label="composer-adjacent activity bar DOM")
    require(index_html, 'id="conversation-footer-dock"', label="conversation footer dock DOM")
    require(index_html, 'data-footer-dock="session-composer"', label="footer dock mode DOM")
    require(index_html, 'id="autonomy-detail"', label="secondary panel autonomy detail DOM")
    require(index_html, 'id="autonomy-detail-meta"', label="secondary panel autonomy detail meta DOM")
    require(index_html, 'id="secondary-panel"', label="secondary panel DOM")
    require(index_html, 'id="secondary-panel-toggle"', label="secondary panel toggle DOM")
    require(index_html, 'id="secondary-panel-close"', label="secondary panel close DOM")
    require(index_html, 'id="nav-sheet-toggle"', label="mobile nav toggle DOM")
    require(index_html, 'id="nav-sheet-close"', label="mobile nav close DOM")
    require(index_html, 'id="nav-sheet-scrim"', label="mobile nav scrim DOM")
    require(app_js, "internalConversationAppendStreamUrl", label="controller dependency wiring")
    require(app_js, "showPendingOutgoing", label="pending outgoing submit wiring")
    require(app_js, "showPendingAssistant", label="pending assistant submit wiring")
    require(app_js, "clearPendingOutgoing", label="pending outgoing clear wiring")
    require(app_js, "setNavigationOpen", label="mobile nav state helper")
    require(app_js, "setSecondaryPanelOpen", label="secondary panel state helper")
    require(app_js, 'window.innerWidth > 860', label="mobile nav resize reset")
    require(styles_css, 'body[data-nav-open="true"] .sidebar', label="mobile nav drawer CSS")
    require(styles_css, 'body[data-secondary-panel-open="true"] .desktop-shell', label="desktop secondary panel layout CSS")
    require(styles_css, ".autonomy-detail-card", label="secondary panel autonomy detail card CSS")
    require(styles_css, ".secondary-panel", label="secondary panel CSS")
    require(styles_css, ".thread-sidecar", label="thread sidecar CSS")
    require(styles_css, ".conversation-card-live", label="conversation card live badge CSS")
    require(styles_css, ".conversation-card-marker", label="conversation card selected badge CSS")
    require(styles_css, ".timeline-item.message.user.pending-local", label="pending local message CSS")
    require(styles_css, ".timeline-item.message.assistant.pending-assistant", label="pending assistant message CSS")
    require(styles_css, ".session-strip", label="session strip CSS")
    require(styles_css, ".session-activity-bar", label="composer activity bar CSS")
    require(styles_css, ".session-strip-main", label="composer activity main CSS")
    require(styles_css, ".session-strip-side", label="composer activity side CSS")
    require(styles_css, ".session-strip-draft", label="composer activity draft CSS")
    require(styles_css, "position: sticky;", label="sticky footer CSS")
    require(styles_css, "env(safe-area-inset-bottom)", label="safe-area footer padding CSS")
    require(styles_css, ".mobile-nav-toggle", label="mobile nav button CSS")
    require_absent(index_html, 'id="conversation-live-status"', label="legacy live badge DOM")
    require_absent(index_html, 'id="live-run-row"', label="legacy live run row DOM")
    require_absent(index_html, 'id="append-stream-strip"', label="legacy append stream DOM")
    require_absent(index_html, 'id="autonomy-context-strip"', label="header autonomy strip DOM")
    require_absent(index_html, 'id="hero-conversation-state"', label="header conversation status DOM")
    require_absent(index_html, 'id="hero-job-state"', label="header job status DOM")
    require_absent(index_html, "sidebar-inspector", label="legacy sidebar inspector")
    require_absent(index_html, "sidebar-footer", label="legacy sidebar footer")
    require_absent(index_html, 'class="autonomy-rail"', label="legacy standalone autonomy rail DOM")
    print("ok: ops desktop secondary panel, footer dock, session strip, compact autonomy context strip, append SSE wiring, and mobile nav drawer are present")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as error:
        print(f"verification failed: {error}", file=sys.stderr)
        raise SystemExit(1)
