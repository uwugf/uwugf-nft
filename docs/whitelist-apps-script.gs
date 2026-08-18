/**
 * UwU GF — whitelist form → Google Sheet
 * ---------------------------------------------------------------
 * SETUP (≈5 min):
 * 1. Create a Google Sheet (go to https://sheets.new). Name it "UwU GF Whitelist".
 * 2. Extensions → Apps Script. Delete the default code, paste ALL of this file, Save.
 * 3. Deploy → New deployment → (gear ⚙) Web app.
 *      - Description: uwugf wl
 *      - Execute as: Me
 *      - Who has access: Anyone
 *    → Deploy → Authorize access → allow (it's your own script).
 * 4. Copy the Web app URL (ends in /exec) and paste it back to Claude.
 *
 * ALREADY DEPLOYED? Editing this file is not enough — a web app keeps serving the
 * version you deployed. After pasting: Deploy → Manage deployments → ✏️ edit →
 * Version: "New version" → Deploy. The /exec URL stays the same.
 *
 * Rows: Timestamp | X Handle | Wallet | Referred By | Why | Tasks
 * Visit the /exec URL in a browser anytime to confirm it's live.
 */

var HEADERS = ['Timestamp', 'X Handle', 'Wallet', 'Referred By', 'Why', 'Tasks'];

function doPost(e) {
  var lock = LockService.getScriptLock();
  lock.waitLock(20000); // avoid two submissions clobbering each other
  try {
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheets()[0];
    if (sheet.getLastRow() === 0) {
      sheet.appendRow(HEADERS);
    } else if (sheet.getLastColumn() < HEADERS.length) {
      // Sheet predates the Tasks column: label it instead of writing values under
      // a blank heading. Existing rows keep an empty cell there, which is correct.
      sheet.getRange(1, HEADERS.length).setValue(HEADERS[HEADERS.length - 1]);
    }

    var p = (e && e.parameter) ? e.parameter : {};

    // The form posts a ready-made "tasks" list. Fall back to the individual
    // task_* checkboxes so a submission is still recorded if that field is missing.
    var tasks = p.tasks;
    if (!tasks) {
      tasks = Object.keys(p)
        .filter(function (k) { return k.indexOf('task_') === 0 && p[k]; })
        .map(function (k) { return k.slice(5); })
        .join(',');
    }

    sheet.appendRow([
      new Date(),
      p.twitter || '',
      p.wallet  || '',
      p.ref     || '',
      p.why     || '',
      tasks     || ''
    ]);
    return ContentService
      .createTextOutput(JSON.stringify({ ok: true }))
      .setMimeType(ContentService.MimeType.JSON);
  } catch (err) {
    return ContentService
      .createTextOutput(JSON.stringify({ ok: false, error: String(err) }))
      .setMimeType(ContentService.MimeType.JSON);
  } finally {
    lock.releaseLock();
  }
}

function doGet() {
  return ContentService.createTextOutput('UwU GF whitelist endpoint is live ♥');
}
