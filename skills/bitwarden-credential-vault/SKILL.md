---
name: bitwarden-credential-vault
description: Use when working with credentials, passwords, usernames, logins, API keys, access tokens, refresh tokens, SSH keys, environment secrets, project secrets, account setup, account lookup, or credential storage and retrieval tasks.
---

# Bitwarden Credential Vault

## When To Use This Skill

Use Bitwarden as the durable source of truth for credentials and secrets. This includes passwords, usernames, login URLs, API keys, access tokens, refresh tokens, SSH keys, service-account details, project secrets, and account setup or lookup work.

Search Bitwarden before asking the user for credentials. Use the available Bitwarden MCP tools exposed by Agent Zero. If MCP tools are unavailable and terminal access is appropriate, use the `bw` CLI without echoing secrets.

## Retrieval Workflow

Identify the service, account, project, client, username, URL, or folder that should contain the credential. If the identity is ambiguous, ask one short targeted question before retrieving or using anything.

Retrieve only the fields needed for the current task. Redact secret values in responses, logs, command output, summaries, and notes. Do not paste raw credentials into chat unless the user explicitly requires it and there is no safer path.

Use Agent Zero project secrets or environment variables only for temporary runtime injection when a tool needs a value. Do not treat project secrets, shell profiles, repository files, or Agent Zero memory as durable secret storage.

## Storage Workflow

Store newly provided or newly generated credentials in Bitwarden unless the user explicitly says not to. Prefer updating an existing matching vault item when there is a clear match instead of creating duplicates.

Preserve useful metadata such as service name, username, login URL, project or client name, folder, and concise operational notes. Do not place secret values in notes unless Bitwarden has no better field for that secret.

## Redaction And Logging

Never store or expose secrets in repository files, chat summaries, logs, shell history, project files, scratch files, or Agent Zero memory. Avoid commands that put secret values directly in shell history or process lists. Prefer stdin, environment injection, or the MCP tool's structured secret field when available.

When showing status, say whether a secret was found, stored, updated, missing, locked, or unavailable. Do not show the secret itself.

## Updating Existing Credentials

Before creating a new item, search for existing records by service name, URL, username, project/client name, and likely folder. Update the existing matching item when the match is clear. If multiple plausible matches exist, ask a short targeted question.

## Failure Handling

If Bitwarden is locked, logged out, missing required environment variables, or the MCP server is unavailable, report the high-level state and the minimum action needed to proceed. Do not ask the user to paste a master password, API client secret, session key, or token into chat unless unavoidable. If interactive credential entry is unavoidable, minimize exposure and never echo values back.
