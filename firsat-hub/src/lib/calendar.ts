import type { EventRow } from "./types";

const TZ = "Europe/Istanbul";

/** Verilen anın İstanbul'daki takvim gününü YYYY-MM-DD olarak döner. */
function istanbulDate(d: Date): string {
  return new Intl.DateTimeFormat("en-CA", { timeZone: TZ, year: "numeric", month: "2-digit", day: "2-digit" }).format(d);
}
const compact = (iso: string) => iso.replace(/-/g, "");
function nextDay(iso: string): string {
  const d = new Date(iso + "T00:00:00Z");
  d.setUTCDate(d.getUTCDate() + 1);
  return d.toISOString().slice(0, 10);
}

export function daysLeft(deadline: string | null): number | null {
  if (!deadline) return null;
  const a = new Date(istanbulDate(new Date()) + "T00:00:00Z").getTime();
  const b = new Date(istanbulDate(new Date(deadline)) + "T00:00:00Z").getTime();
  return Math.round((b - a) / 86400000);
}

function details(e: EventRow) {
  return `Son başvuru: ${e.title}\nBaşvuru linki: ${e.application_url}`;
}

export function googleCalendarUrl(e: EventRow): string | null {
  if (!e.deadline) return null;
  const day = istanbulDate(new Date(e.deadline));
  const p = new URLSearchParams({
    action: "TEMPLATE",
    text: `Son başvuru: ${e.title}`,
    dates: `${compact(day)}/${compact(nextDay(day))}`,
    details: details(e),
    location: e.application_url,
  });
  return `https://calendar.google.com/calendar/render?${p.toString()}`;
}

const esc = (s: string) => s.replace(/\\/g, "\\\\").replace(/;/g, "\\;").replace(/,/g, "\\,").replace(/\n/g, "\\n");

export function buildIcs(e: EventRow): string | null {
  if (!e.deadline) return null;
  const day = istanbulDate(new Date(e.deadline));
  const stamp = new Date().toISOString().replace(/[-:]/g, "").replace(/\.\d{3}/, "");
  return [
    "BEGIN:VCALENDAR",
    "VERSION:2.0",
    "PRODID:-//Firsat Hub//TR",
    "CALSCALE:GREGORIAN",
    "BEGIN:VEVENT",
    `UID:${e.id}@firsat-hub`,
    `DTSTAMP:${stamp}`,
    `DTSTART;VALUE=DATE:${compact(day)}`,
    `DTEND;VALUE=DATE:${compact(nextDay(day))}`,
    `SUMMARY:${esc(`Son başvuru: ${e.title}`)}`,
    `DESCRIPTION:${esc(details(e))}`,
    `URL:${e.application_url}`,
    "BEGIN:VALARM",
    "ACTION:DISPLAY",
    `DESCRIPTION:${esc(`Yarın son gün: ${e.title}`)}`,
    "TRIGGER:-P1D",
    "END:VALARM",
    "END:VEVENT",
    "END:VCALENDAR",
  ].join("\r\n");
}

export function formatDate(deadline: string | null): string {
  if (!deadline) return "Sürekli başvuru";
  return new Intl.DateTimeFormat("tr-TR", { timeZone: TZ, day: "numeric", month: "long", year: "numeric" }).format(new Date(deadline));
}
