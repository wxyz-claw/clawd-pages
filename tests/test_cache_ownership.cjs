const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

async function activated(file, keys) {
  const handlers = {}, deleted = [], pending = [];
  const context = {
    self: {addEventListener: (name, fn) => handlers[name] = fn,
      clients: {claim: () => Promise.resolve()}, skipWaiting: () => {}},
    caches: {keys: async () => keys, delete: async key => {deleted.push(key); return true;}}
  };
  vm.runInNewContext(fs.readFileSync(path.join(__dirname, '..', file), 'utf8'), context);
  handlers.activate({waitUntil: promise => pending.push(promise)});
  await Promise.all(pending);
  return deleted.sort();
}

(async () => {
  const keys = ['clawd-shell-v1', 'clawd-shell-v10', 'clawd-runtime-v2', 'clawd-fonts-v10',
    'eye-rest-timer-v1', 'eye-rest-timer-v5', 'other-application'];
  assert.deepEqual(await activated('sw.js', keys), ['clawd-runtime-v2', 'clawd-shell-v1']);
  assert.deepEqual(await activated('eye-rest/sw.js', keys), ['eye-rest-timer-v1']);
  console.log('PASS: workers delete only their own obsolete caches');
})().catch(error => {console.error(error); process.exitCode = 1;});
