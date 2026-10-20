const { mkdir, readFile, writeFile } = require('node:fs/promises');
const path = require('node:path');

function escapeMarkdown(value) {
  return String(value ?? '')
    .replace(/[&<>|`*_[\]\\]/g, (character) => `&#${character.codePointAt(0)};`)
    .replace(/\r\n|\r|\n/g, '<br>');
}

function formatCodeSpan(value) {
  const text = String(value ?? '')
    .replace(/\r\n|\r|\n/g, ' ')
    .replace(/\|/g, '\\|');
  if (!text) return '';

  const runs = text.match(/`+/g) ?? [];
  const delimiter = '`'.repeat(runs.reduce((length, run) => Math.max(length, run.length), 0) + 1);
  const padding = /^`|`$|^ .* $/.test(text) ? ' ' : '';
  return `${delimiter}${padding}${text}${padding}${delimiter}`;
}

async function main() {
  const args = process.argv.slice(2);
  if (args.length !== 3 || args.some((argument) => !argument.trim())) {
    throw new Error('Usage: node generate-app-list.js <input.json> <output.md> <latest_release>');
  }

  const [inputPath, outputPath, latestRelease] = args;
  const applications = JSON.parse(await readFile(inputPath, 'utf8'));

  if (!Array.isArray(applications)) {
    throw new Error('The JSON file must contain an array.');
  }

  const header = (await readFile(path.join(__dirname, 'appList.header'), 'utf8'))
    .replaceAll('{application_count}', String(applications.length))
    .replaceAll('{{ abcdesktop.latest_release }}', () => latestRelease);

  const labelColumns = [
    'oc.acl',
    'oc.cat',
    'oc.containerengine',
    'oc.desktopfile',
    'oc.displayname',
    'oc.icon',
    'oc.rules',
    'oc.showinview',
    'oc.template',
  ];
  const columns = [
    'Icon',
    'Name',
    'Dockerfile',
    'Json',
    'Repository Tags',
    'Access Control',
    'Category',
    'Container Engine',
    'Desktop File',
    'Display Name',
    'Icon File',
    'Rules',
    'View Visibility',
    'Template',
  ];
  const lines = [
    `| ${columns.join(' | ')} |`,
    `| ${columns.map(() => '---').join(' | ')} |`,
  ];
  const iconsPath = path.join(path.dirname(outputPath), 'icons');
  await mkdir(iconsPath, { recursive: true });

  for (const application of applications) {
    const applicationLabels = application.Config?.Labels ?? {};
    let iconImage = '';

    if (applicationLabels['oc.icondata']) {
      const iconName = applicationLabels['oc.icon'];
      if (typeof iconName !== 'string' || !iconName.toLowerCase().endsWith('.svg')
        || /[\\/]/.test(iconName)) {
        throw new Error('The oc.icon label must contain an SVG filename without a path.');
      }

      await writeFile(
        path.join(iconsPath, iconName),
        Buffer.from(applicationLabels['oc.icondata'], 'base64'),
      );
      iconImage = `<img src="../icons/${encodeURIComponent(iconName)}" alt="Icon" width="48">`;
    }

    const tags = (application.RepoTags ?? [])
      .map((tag) => `<code>${escapeMarkdown(tag)}</code>`)
      .join('<br>');
    const name = applicationLabels['oc.name'];
    const dockerfile = name
      ? `[Dockerfile](<https://github.com/abcdesktopio/images/tree/main/artifact/${encodeURIComponent(latestRelease)}/${encodeURIComponent(name).toLowerCase()}.d>)`
      : '';
    const json = name
      ? `[Json](<https://github.com/abcdesktopio/images/tree/main/artifact/${encodeURIComponent(latestRelease)}/${encodeURIComponent(name).toLowerCase()}.d.${encodeURIComponent(latestRelease)}.json>)`
      : '';

    const cells = [
      iconImage,
      escapeMarkdown(name),
      dockerfile,
      json,
      tags,
      ...labelColumns.map((key) => key === 'oc.acl' || key === 'oc.rules'
        ? formatCodeSpan(applicationLabels[key])
        : escapeMarkdown(applicationLabels[key])),
    ];

    lines.push(`| ${cells.join(' | ')} |`);
  }

  await writeFile(outputPath, `${header}\n\n${lines.join('\n')}\n`, 'utf8');
  console.log(`${applications.length} entries exported to ${outputPath}`);
}

main().catch((error) => {
  console.error(`Error: ${error.message}`);
  process.exitCode = 1;
});