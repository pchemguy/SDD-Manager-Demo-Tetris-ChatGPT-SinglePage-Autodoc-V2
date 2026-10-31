/** Execute the real inline core in an isolated bounded context for pytest. */
import fs from 'node:fs';
import vm from 'node:vm';
const html = fs.readFileSync(new URL('../tetris.html', import.meta.url), 'utf8');
const script = html.match(/<script id="tetris-core">([\s\S]*?)<\/script>/);
if (!script) throw new Error('Inline game core is missing');
const context = vm.createContext({console, Math, Date, JSON, structuredClone});
vm.runInContext(script[1], context, {timeout: 2000});
const value = vm.runInContext(process.argv[2], context, {timeout: 2000});
process.stdout.write(JSON.stringify(value));
