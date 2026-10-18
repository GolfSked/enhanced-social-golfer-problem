// Apply URL settings before the shell sends state to its sandboxed frame.
function explorerUrlRoster(state, search, roundCount = 4) {
  const params = new URLSearchParams(search);
  if (!params.has('players') && !params.has('round')) return state;
  const modelContent = { ...state?.modelContent };
  if (params.has('players')) {
    const names = params.get('players').split(':').slice(0, 24)
      .map(name => name.trim().slice(0, 100));
    const count = names.length;
    Object.assign(modelContent, {
      players: count >= 15 && count <= 24 ? count : 16, names,
    });
  }
  if (params.has('round')) {
    const entries = params.getAll('round');
    const settings = [];
    let error = entries.length > roundCount
      ? `This explorer has ${roundCount} rounds; the URL supplies ${entries.length}. Use at most ${roundCount} round parameters.` : '';
    if (!error) entries.forEach((entry, i) => {
      if (error) return;
      const fields = entry.split('|').map(s => s.trim());
      // Some shared links encode an already escaped space (%2520).
      // Repair only spaces in labels, without decoding field separators.
      fields[0] = fields[0].replace(/%20/gi, ' ').trim();
      const [course, start, intervalText] = fields;
      const interval = intervalText === undefined ? 7 : Number(intervalText);
      if (fields.length < 2 || fields.length > 3 || !course || course.length > 100 ||
          !/^([01]\d|2[0-3]):[0-5]\d$/.test(start) ||
          (intervalText !== undefined && !/^\d+$/.test(intervalText)) ||
          !Number.isInteger(interval) || interval < 1 || interval > 60) {
        error = `Round ${i + 1}: use Course|HH:MM or Course|HH:MM|minutes (1–60). Round settings were not applied.`;
      } else settings.push({ course, start, interval });
    });
    modelContent.roundSettings = error ? [] : settings;
    modelContent.roundSettingsError = error;
  }
  return { ...state, modelContent };
}
