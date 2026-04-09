import { normalizeBaseUrl } from "./ops-store.js";

export function requestHeaders(extraHeaders = {}) {
  return {
    "Content-Type": "application/json",
    ...extraHeaders,
  };
}

export async function fetchJson(_dom, url, options = {}) {
  const response = await fetch(url, {
    headers: requestHeaders(options.headers || {}),
    ...options,
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || `HTTP ${response.status}`);
  }

  return response.json();
}

export function selectedAppData(dom) {
  const option = dom.appSelect.selectedOptions[0];
  if (!option) {
    return null;
  }

  return {
    appId: option.value,
    title: option.dataset.title || option.value,
    deploymentUrl: option.dataset.deploymentUrl || "",
  };
}

export function appsUrl() {
  return `${normalizeBaseUrl()}/api/apps`;
}

export function appConversationsUrl(appId) {
  return `${normalizeBaseUrl()}/api/apps/${appId}/conversations`;
}

export function appGoalsUrl(appId) {
  return `${normalizeBaseUrl()}/api/apps/${appId}/goals`;
}

export function conversationUrl(conversationId) {
  return `${normalizeBaseUrl()}/api/conversations/${conversationId}`;
}

export function conversationMessagesUrl(conversationId) {
  return `${conversationUrl(conversationId)}/messages`;
}

export function internalConversationAppendStreamUrl(conversationId) {
  return `${normalizeBaseUrl()}/api/internal/conversations/${conversationId}/append-stream`;
}

export function proposalsApplyUrl(jobId) {
  return `${normalizeBaseUrl()}/api/proposals/${jobId}/apply`;
}

export function jobUrl(jobId) {
  return `${normalizeBaseUrl()}/api/jobs/${jobId}`;
}
