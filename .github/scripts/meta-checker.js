const fs = require('fs');
const path = require('path');

function isLeafDir(dirPath) {
  const entries = fs.readdirSync(dirPath, { withFileTypes: true });
  return !entries.some(e => e.isDirectory());
}

function processLeafDir(dirPath) {
  const metaPath = path.join(dirPath, '.meta.json');
  if (fs.existsSync(metaPath)) return; // Already has .meta.json, skip.

  const files = fs.readdirSync(dirPath).filter(f => fs.statSync(path.join(dirPath, f)).isFile());

  let valid = true;
  const episodes = {};

  for (const file of files) {
    const match = file.match(/^Episode(\d{1,2})-s([12])\.json$/);
    if (!match) {
      valid = false;
      break;
    }
    const [ , ep, sector ] = match;
    episodes[ep] = {
      Sectors: Math.max(episodes[ep]?.Sectors || 1, parseInt(sector, 10))
    };
  }

  if (!valid || Object.keys(episodes).length === 0) return;

  // Write .meta.json
  fs.writeFileSync(metaPath, JSON.stringify(episodes, null, 2));
  console.log(`Created ${metaPath}`);
}

function walk(dirPath) {
  const entries = fs.readdirSync(dirPath, { withFileTypes: true });

  // Ignore .git and node_modules
  if (dirPath.includes('.git') || dirPath.includes('node_modules')) return;

  if (isLeafDir(dirPath)) {
    processLeafDir(dirPath);
  } else {
    for (const entry of entries) {
      if (entry.isDirectory()) {
        walk(path.join(dirPath, entry.name));
      }
    }
  }
}

// Start from repo root
walk(process.cwd());
