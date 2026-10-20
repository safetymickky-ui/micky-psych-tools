#!/usr/bin/env node
/**
 * Zero-secret launcher for @meshy-ai/meshy-mcp-server.
 * Antigravity's mcp_config.json does not expand ${MESHY_API_KEY} placeholders.
 * This wrapper resolves MESHY_API_KEY from the process environment or Windows
 * User/System registry environment at runtime without ever storing or logging the key.
 */
import { spawn, execFileSync } from 'node:child_process';

function resolveMeshyKey() {
  const existing = process.env.MESHY_API_KEY;
  if (existing && !existing.startsWith('${') && !existing.startsWith('%')) {
    return existing.trim();
  }
  if (process.platform === 'win32') {
    const regPaths = [
      'HKCU\\Environment',
      'HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Environment',
    ];
    for (const regPath of regPaths) {
      try {
        const out = execFileSync('reg.exe', ['query', regPath, '/v', 'MESHY_API_KEY'], {
          encoding: 'utf8',
          stdio: ['ignore', 'pipe', 'ignore'],
        });
        const match = out.match(/MESHY_API_KEY\s+REG_(?:EXPAND_)?SZ\s+(.+)/i);
        if (match && match[1] && match[1].trim()) {
          return match[1].trim();
        }
      } catch {
        // Key not in this registry hive; continue
      }
    }
  }
  return '';
}

const apiKey = resolveMeshyKey();
if (!apiKey) {
  process.stderr.write(
    'Error: MESHY_API_KEY is not set in the environment. Set MESHY_API_KEY in your user environment before using Meshy MCP.\n'
  );
  process.exit(1);
}

const env = { ...process.env, MESHY_API_KEY: apiKey };
const isWin = process.platform === 'win32';
const cmd = isWin ? 'cmd.exe' : 'npx';
const args = isWin
  ? ['/d', '/s', '/c', 'npx -y @meshy-ai/meshy-mcp-server']
  : ['-y', '@meshy-ai/meshy-mcp-server'];

const child = spawn(cmd, args, {
  env,
  stdio: 'inherit',
});

child.on('exit', (code) => {
  process.exit(code ?? 0);
});

child.on('error', (err) => {
  process.stderr.write(`Failed to start @meshy-ai/meshy-mcp-server: ${err.message}\n`);
  process.exit(1);
});
